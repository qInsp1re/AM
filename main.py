import asyncio
import sys

from config.constants import TITLE
from termcolor import cprint
from modules import balance_checker
from questionary import Choice, select

from dev_settings import Settings
from modules.interfaces import SoftwareException
from utils.modules_runner import Runner
from utils.route_generator import RouteGenerator
from utils.tools import progress_file_is_not_empty, get_addresses_for_cex, create_cex_withdrawal_list
from version import VERSION
from pathlib import Path


def are_you_sure(module=None, gen_route: bool = False):
    if gen_route or not progress_file_is_not_empty():
        answer = select(
            '\n ⚠️⚠️⚠️ THIS ACTION WILL DELETE ALL PREVIOUS PROGRESS FOR ROUTES, continue? ⚠️⚠️⚠️ \n',
            choices=[
                Choice("❌  NO", 'main'),
                Choice("✅  YES", 'module'),
            ],
            qmark='☢️',
            pointer='👉'
        ).ask()
        print()
        if answer == 'main':
            main()
        else:
            if module:
                module()


def choose_run_option(route: str):
    if progress_file_is_not_empty():
        answer = select(
            f'\n ⚠️⚠️⚠️ Detected progress for {route}, what do you want to do? ⚠️⚠️⚠️ \n',
            choices=[
                Choice(f"✅  Save progress and run {route} without route generation", 'run_accounts'),
                Choice(f"⚠️ Clear progress and run {route} with route generation", 'gen_route'),
            ],
            qmark='☢️',
            pointer='👉'
        ).ask()
        print()
        if answer == 'gen_route':
            generator = RouteGenerator()
            generator.classic_routes_json_save()
        elif answer == 'run_accounts':
            pass
        else:
            raise KeyboardInterrupt
    else:
        generator = RouteGenerator()
        generator.classic_routes_json_save()


def choose_preset_to_run():
    saved_presets_settings = Settings.get_presets_settings()
    saved_routes = list(saved_presets_settings.keys())
    choices = [
        Choice(f"↩️ Go back", 'go_back')
    ]
    for saved_route in saved_routes:
        choices.append(
            Choice(f"🟢 {saved_route}", saved_route)
        )
    answer = select(
        'Choose saved route to run for each wallet',
        choices=choices,
        qmark='🛠️',
        pointer='👉'
    ).ask()
    if answer in saved_routes:
        Settings.prepare_settings(route=answer)
        runner = Runner()
        choose_run_option(route=answer)
        create_cex_withdrawal_list()
        asyncio.run(runner.run_accounts())
    elif answer == 'go_back':
        main()
    else:
        raise KeyboardInterrupt


def main():
    cprint(TITLE, 'red')
    cprint(f'⚙️ v{VERSION}\n', attrs=["bold"])
    cprint(f'❤️ My channel for latest updates: https://t.me/askaer\n', 'light_cyan', attrs=["blink"])
    try:
        while True:
            answer = select(
                'What do you want to do?',
                choices=[
                    Choice("🚀 Start running route for each wallet", 'routes_run'),
                    Choice("📄 Generate route for each wallet", 'routes_gen'),
                    Choice("📂 Go to saved routes", 'get_presets'),
                    Choice("✅ Check the connection of each proxy", 'check_proxy'),
                    Choice("🗃️ Get wallet addresses for each account", 'get_addresses_for_cex'),
                    Choice("📊 Get Cosmos + Solana balances for all wallets", 'wallet_balances'),
                    Choice('❌ Exit', "exit")
                ],
                qmark='🛠️',
                pointer='👉'
            ).ask()

            match answer:
                case 'check_proxy':
                    print()
                    runner = Runner()
                    asyncio.run(runner.check_proxies_status())
                    print()
                case 'routes_run':
                    print()
                    Settings.prepare_settings()
                    runner = Runner()
                    create_cex_withdrawal_list()
                    asyncio.run(runner.run_accounts())
                    print()
                case 'get_addresses_for_cex':
                    print()
                    get_addresses_for_cex()
                    print()
                case 'wallet_balances':
                    print()
                    asyncio.run(balance_checker.main())
                    print()
                case 'routes_gen':
                    Settings.prepare_settings()
                    generator = RouteGenerator()
                    are_you_sure(generator.classic_routes_json_save, gen_route=True)
                case 'get_presets':
                    print()
                    choose_preset_to_run()
                case 'exit':
                    sys.exit()
                case _:
                    raise KeyboardInterrupt

    except KeyboardInterrupt:
        cprint(f'\nQuick software shutdown by <ctrl + C>', color='light_yellow')
        sys.exit()

    except SoftwareException as error:
        cprint(f'\n{error}', color='light_red')
        sys.exit()


if __name__ == "__main__":
    main()
