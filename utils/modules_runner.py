import re
import json
import copy
import random
import telebot
import asyncio
import traceback

from dev_settings import Settings
from modules import Logger
from aiohttp import ClientSession
from utils.networks import EthereumRPC
from web3 import AsyncWeb3, AsyncHTTPProvider
from functions import get_rpc_by_chain_name
from modules.interfaces import SoftwareException, CriticalException
from config.constants import ACCOUNT_NAMES, EVM_PRIVATE_KEYS, PROXIES, SOLANA_PRIVATE_KEYS, MNEMONICS
from utils.route_generator import AVAILABLE_MODULES_INFO, get_func_by_name
from utils.tools import clean_gwei_file, clean_bridge_progress_file, network_handler, retry_on_error
from general_settings import (
    USE_PROXY, SLEEP_MODE, SLEEP_TIME_MODULES, TG_ID, TG_TOKEN, MOBILE_PROXY, MOBILE_PROXY_URL_CHANGER,
    WALLETS_TO_WORK, TELEGRAM_NOTIFICATIONS, SAVE_PROGRESS, SLEEP_TIME_ACCOUNTS, BREAK_ROUTE,
    SOFTWARE_MODE, ACCOUNTS_IN_STREAM, WALLETS_TO_EXCLUDE, STOP_SOFTWARE
)


class Runner(Logger):

    @staticmethod
    def get_wallets():
        account_names = []

        if WALLETS_TO_WORK == 0:
            account_names = copy.deepcopy(ACCOUNT_NAMES)
        elif isinstance(WALLETS_TO_WORK, int):
            account_names = copy.deepcopy([ACCOUNT_NAMES[WALLETS_TO_WORK - 1]])
        elif isinstance(WALLETS_TO_WORK, tuple):
            account_names = copy.deepcopy(
                [ACCOUNT_NAMES[i - 1] for i in WALLETS_TO_WORK if 0 < i <= len(ACCOUNT_NAMES)]
            )
        elif isinstance(WALLETS_TO_WORK, list):
            for item in WALLETS_TO_WORK:
                if isinstance(item, int):
                    if 0 < item <= len(ACCOUNT_NAMES):
                        account_names.append(ACCOUNT_NAMES[item - 1])
                elif isinstance(item, list) and len(item) == 2:
                    start, end = item
                    if 0 < start <= end <= len(ACCOUNT_NAMES):
                        account_names.extend([ACCOUNT_NAMES[i - 1] for i in range(start, end + 1)])
        else:
            account_names = []

        if WALLETS_TO_EXCLUDE == 0:
            pass
        elif isinstance(WALLETS_TO_EXCLUDE, int):
            if WALLETS_TO_EXCLUDE <= len(account_names):
                account_names = [account for account in account_names if
                                 account != ACCOUNT_NAMES[WALLETS_TO_EXCLUDE - 1]]
        elif isinstance(WALLETS_TO_EXCLUDE, tuple):
            indices_to_remove = sorted(WALLETS_TO_EXCLUDE, reverse=True)
            for index in indices_to_remove:
                if 0 < index <= len(ACCOUNT_NAMES):
                    account_names = [account for account in account_names if account != ACCOUNT_NAMES[index - 1]]
        elif isinstance(WALLETS_TO_EXCLUDE, list):
            for item in WALLETS_TO_EXCLUDE:
                if isinstance(item, int):
                    if 0 < item <= len(ACCOUNT_NAMES):
                        account_names = [account for account in account_names if account != ACCOUNT_NAMES[item - 1]]
                elif isinstance(item, list) and len(item) == 2:
                    start, end = item
                    if 0 < start <= end <= len(ACCOUNT_NAMES):
                        for i in range(start, end + 1):
                            account_names = [account for account in account_names if account != ACCOUNT_NAMES[i - 1]]
        else:
            account_names = []

        with open(Settings.PROGRESS_FILE_PATH, 'r') as file:
            wallets_progress_json = json.load(file)
        order = list(wallets_progress_json.keys())

        account_names_with_order = [account_name for account_name in order if account_name in account_names]

        return account_names_with_order

    @staticmethod
    def get_ready_wallets():
        ready_wallets_list = []

        with open(Settings.PROGRESS_FILE_PATH, 'r') as file:
            wallets_progress_json = json.load(file)

        for account_name in wallets_progress_json.keys():
            if wallets_progress_json[account_name]['current_step'] == len(wallets_progress_json[account_name]['route']):
                ready_wallets_list.append(account_name)

        return ready_wallets_list

    @staticmethod
    async def make_request(method: str = 'GET', url: str = None, headers: dict = None):

        async with ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers) as response:
                if response.status == 200:
                    return True
                return False

    async def send_tg_message(self, account_name, message_to_send, result_list, modules_len):
        try:
            message_to_send.insert(
                0,
                f'💵 Annihilator | Account name: "{account_name}"\n \n{modules_len} module(s) in route\n'
            )

            success_count = len([1 for i in result_list if i[0]])
            errors_count = len(result_list) - success_count

            if errors_count > 0:
                disable_notification = False
            else:
                disable_notification = True

            message_to_send.append(f'Total result:    ✅   —   {success_count}    |    ❌   —   {errors_count}')

            str_send = '*' + '\n'.join([re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', message)
                                        for message in message_to_send]) + '*'
            bot = telebot.TeleBot(TG_TOKEN)
            bot.send_message(TG_ID, str_send, parse_mode='MarkdownV2', disable_notification=disable_notification)
            print()
            self.logger_msg(account_name, None, msg=f"Telegram message sent", type_msg='success')
        except Exception as error:
            self.logger_msg(account_name, None, msg=f"Telegram | API Error: {error}", type_msg='error')

    @staticmethod
    def load_routes():
        with open(Settings.PROGRESS_FILE_PATH, 'r') as f:
            return json.load(f)

    async def smart_sleep(self, account_name, account_number=1, accounts_delay=False):
        if SLEEP_MODE and account_number:
            if accounts_delay:
                duration = random.randint(*tuple(x * account_number for x in SLEEP_TIME_ACCOUNTS))
            else:
                duration = random.randint(*SLEEP_TIME_MODULES)
            self.logger_msg(account_name, None, msg=f"💤 Sleeping for {duration} seconds\n")
            await asyncio.sleep(duration)

    def update_step(self, account_name, step):
        wallets = self.load_routes()
        wallets[str(account_name)]["current_step"] = step
        with open(Settings.PROGRESS_FILE_PATH, 'w') as f:
            json.dump(wallets, f, indent=4)

    @staticmethod
    def collect_bad_wallets(account_name, module_name):
        try:
            with open('./data/bad_wallets.json', 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data.setdefault(str(account_name), []).append(module_name)

        with open('./data/bad_wallets.json', 'w') as file:
            json.dump(data, file, indent=4)

    async def change_ip_proxy(self):
        for index, proxy_url in enumerate(MOBILE_PROXY_URL_CHANGER, 1):
            while True:
                try:
                    self.logger_msg(None, None, msg=f'Trying to change IP №{index} address\n')

                    await self.make_request(url=proxy_url)

                    self.logger_msg(None, None, msg=f'IP №{index} address changed!\n', type_msg='success')
                    await asyncio.sleep(5)
                    break

                except Exception as error:
                    self.logger_msg(None, None, msg=f'Bad URL for change IP №{index}. Error: {error}', type_msg='error')
                    await asyncio.sleep(15)

    async def check_proxies_status(self):
        tasks = []
        for proxy in PROXIES:
            tasks.append(self.check_proxy_status(None, proxy=proxy))
        await asyncio.gather(*tasks)

    async def check_proxy_status(self, account_name: str = None, proxy: str = None, silence: bool = False):
        try:
            w3 = AsyncWeb3(
                AsyncHTTPProvider(random.choice(EthereumRPC.rpc), request_kwargs={"proxy": f"http://{proxy}"})
            )
            if await w3.is_connected():
                if not silence:
                    info = f'Proxy {proxy[proxy.find("@"):]} successfully connected to Ethereum RPC'
                    self.logger_msg(account_name, None, msg=info, type_msg='success')
                return True
            self.logger_msg(account_name, None, msg=f"Proxy: {proxy} can`t connect to Ethereum RPC", type_msg='error')
            return False
        except Exception as error:
            self.logger_msg(account_name, None, msg=f"Bad proxy: {proxy} | Error: {error}", type_msg='error')
            return False

    @staticmethod
    def get_proxy_for_account(account_name):
        if USE_PROXY:
            try:
                account_number = ACCOUNT_NAMES.index(account_name)
                num_proxies = len(PROXIES)
                return PROXIES[account_number % num_proxies]
            except Exception as error:
                raise SoftwareException(f"Bad data in proxy: {error}")

    @staticmethod
    def get_mnemonic_for_account(account_name):
        try:
            account_number = ACCOUNT_NAMES.index(account_name)
            num_proxies = len(MNEMONICS)
            return MNEMONICS[account_number % num_proxies]
        except Exception as error:
            raise SoftwareException(f"Bad data in Cosmos mnemonic: {error}")

    @staticmethod
    def get_solana_private_key_for_account(account_name):
        try:
            account_number = ACCOUNT_NAMES.index(account_name)
            num_private_keys = len(SOLANA_PRIVATE_KEYS)
            return SOLANA_PRIVATE_KEYS[account_number % num_private_keys]
        except Exception as error:
            raise SoftwareException(f"Bad data in Solana private key: {error}")

    @staticmethod
    def get_evm_private_key_for_account(account_name):
        try:
            account_number = ACCOUNT_NAMES.index(account_name)
            num_private_keys = len(EVM_PRIVATE_KEYS)
            return EVM_PRIVATE_KEYS[account_number % num_private_keys]
        except Exception as error:
            raise SoftwareException(f"Bad data in EVM private key: {error}")

    def get_current_progress_for_account(self, account_name):
        route_data = self.load_routes().get(str(account_name), {}).get('route', [])
        if SAVE_PROGRESS:
            return self.load_routes()[str(account_name)]["current_step"], route_data
        return 0, route_data

    @network_handler
    @retry_on_error
    async def start_module(self, module_func, module_input_data):
        return await module_func(module_input_data)

    async def run_account_modules(self, account_name: str, index: int = 1, parallel_mode: bool = False):
        message_list, result_list, module_counter = [], [], 0
        try:
            clean_bridge_progress_file(account_name)
            evm_private_key = self.get_evm_private_key_for_account(account_name)
            solana_private_key = self.get_solana_private_key_for_account(account_name)
            cosmos_mnemonic = self.get_mnemonic_for_account(account_name)
            proxy = self.get_proxy_for_account(account_name)
            current_step, route_data = self.get_current_progress_for_account(account_name)
            route_list_info = [[*i.split(':::')] for i in route_data]

            if current_step >= len(route_list_info):
                self.logger_msg(
                    account_name, None, msg=f"All modules were completed", type_msg='warning')
                return False

            while current_step < len(route_list_info):
                module_counter += 1
                module_func_name, rpc_name = route_list_info[current_step][0], route_list_info[current_step][1]
                module_func = get_func_by_name(module_func_name)
                module_log_name = AVAILABLE_MODULES_INFO[module_func][2]
                network = get_rpc_by_chain_name(rpc_name)

                if parallel_mode and module_counter == 1:
                    await self.smart_sleep(account_name, index, accounts_delay=True)

                self.logger_msg(account_name, None, msg=f"🚀 Launch module: {module_log_name}\n")

                module_input_data = {
                    "account_name": account_name,
                    "evm_private_key": evm_private_key,
                    "cosmos_mnemonic": cosmos_mnemonic,
                    "solana_private_key": solana_private_key,
                    "network": network,
                    "proxy": proxy
                }

                result = await self.start_module(module_func, module_input_data)

                if result:
                    self.update_step(account_name, current_step + 1)
                    if not (current_step + 2) > len(route_list_info):
                        await self.smart_sleep(account_name)
                else:
                    self.collect_bad_wallets(account_name, module_func_name)
                    if BREAK_ROUTE:
                        message_list.extend([f'❌   {module_log_name}\n', f'💀   The route was stopped!\n'])
                        account_progress = (False, module_func_name, account_name)
                        result_list.append(account_progress)
                        break

                current_step += 1
                message_list.append(f'{"✅" if result else "❌"}   {module_log_name}\n')
                account_progress = (result, module_func_name, account_name)
                result_list.append(account_progress)

            if TELEGRAM_NOTIFICATIONS:
                await self.send_tg_message(
                    account_name, message_to_send=message_list, result_list=result_list,
                    modules_len=len(route_list_info)
                )
                if any(['💀   The route was stopped!' in msg for msg in message_list]) and  STOP_SOFTWARE:
                    raise CriticalException('Can not continue wallets, cuz STOP_SOFTWARE = True')

            if not SOFTWARE_MODE:
                self.logger_msg(None, None, msg=f"Start running next wallet!\n")
            else:
                self.logger_msg(account_name, None, msg=f"Wait for other wallets in stream!\n")

            return True
        except CriticalException as error:
            raise error
        except Exception as error:
            self.logger_msg(account_name, None, msg=f"Error during the route! Error: {error}\n", type_msg='error')
            traceback.print_exc()

    async def run_consistently(self):

        account_names = self.get_wallets()

        for account_name in account_names:

            result = await self.run_account_modules(account_name)

            if len(account_names) > 1 and result:
                await self.smart_sleep(account_name, accounts_delay=True)

            if MOBILE_PROXY:
                await self.change_ip_proxy()

    async def run_parallel(self):
        all_wallets = list(self.get_wallets())

        ready_wallets = self.get_ready_wallets()

        selected_wallets = [wallet for wallet in all_wallets if wallet not in ready_wallets]

        num_accounts = len(selected_wallets)
        accounts_per_stream = ACCOUNTS_IN_STREAM
        num_streams, remainder = divmod(num_accounts, accounts_per_stream)

        for stream_index in range(num_streams + (remainder > 0)):
            start_index = stream_index * accounts_per_stream
            end_index = (stream_index + 1) * accounts_per_stream if stream_index < num_streams else num_accounts

            account_names = selected_wallets[start_index:end_index]

            tasks = []

            for index, account_name in enumerate(account_names):
                tasks.append(asyncio.create_task(self.run_account_modules(account_name, index, parallel_mode=True)))

            result_list = await asyncio.gather(*tasks, return_exceptions=True)

            for result in result_list:
                if isinstance(result, Exception):
                    raise result

            if MOBILE_PROXY:
                await self.change_ip_proxy()

            self.logger_msg(
                None, None,
                msg=f"Wallets in stream completed their tasks, launching next stream\n", type_msg='success'
            )

    async def run_accounts(self):
        clean_gwei_file()

        try:
            if SOFTWARE_MODE:
                await self.run_parallel()
            else:
                await self.run_consistently()

            self.logger_msg(None, None, msg=f"All accounts completed their tasks!\n", type_msg='success')
        except Exception as error:
            self.logger_msg(None, None, msg=error, type_msg='error')
            if not isinstance(error, CriticalException):
                traceback.print_exc()
