import copy
import json

from utils.tools import clean_progress_file
from functions import *
from web3 import AsyncWeb3
from config.constants import ACCOUNT_NAMES
from modules import Logger
from modules.interfaces import SoftwareException
from general_settings import SHUFFLE_ROUTE, SHUFFLE_WALLETS, WALLETS_TO_WORK, WALLETS_TO_EXCLUDE
from dev_settings import Settings

AVAILABLE_MODULES_INFO = {
    # module_name                       : (module name, priority, tg info, can be help module, supported network)
    fee_support_withdraw: (fee_support_withdraw, -3, 'Fee support withdraw', 0, []),
    fee_support_withdraw_for_arb: (fee_support_withdraw_for_arb, -3, 'Fee support withdraw for Arbitrum', 0, []),
    fee_support_withdraw_for_base: (fee_support_withdraw_for_base, -3, 'Fee support withdraw for Base', 0, []),
    okx_withdraw: (okx_withdraw, -3, 'OKX withdraw', 0, []),
    bingx_withdraw: (bingx_withdraw, -3, 'BingX withdraw', 0, []),
    binance_withdraw: (binance_withdraw, -3, 'Binance withdraw', 0, []),
    bitget_withdraw: (bitget_withdraw, -3, 'Bitget withdraw', 0, []),
    okx_custom_withdraw_1: (okx_custom_withdraw_1, -3, 'OKX custom withdraw #1', 0, []),
    okx_custom_withdraw_2: (okx_custom_withdraw_2, -3, 'OKX custom withdraw #2', 0, []),
    okx_custom_withdraw_3: (okx_custom_withdraw_3, -3, 'OKX custom withdraw #3', 0, []),
    okx_custom_withdraw_4: (okx_custom_withdraw_4, -3, 'OKX custom withdraw #4', 0, []),
    bitget_custom_withdraw_1: (bitget_custom_withdraw_1, -3, 'Bitget custom withdraw #1', 0, []),
    bitget_custom_withdraw_2: (bitget_custom_withdraw_2, -3, 'Bitget custom withdraw #2', 0, []),
    bitget_custom_withdraw_3: (bitget_custom_withdraw_3, -3, 'Bitget custom withdraw #3', 0, []),
    bitget_custom_withdraw_4: (bitget_custom_withdraw_4, -3, 'Bitget custom withdraw #4', 0, []),
    binance_custom_withdraw_1: (binance_custom_withdraw_1, -3, 'Binance custom withdraw #1', 0, []),
    binance_custom_withdraw_2: (binance_custom_withdraw_2, -3, 'Binance custom withdraw #2', 0, []),
    binance_custom_withdraw_3: (binance_custom_withdraw_3, -3, 'Binance custom withdraw #3', 0, []),
    binance_custom_withdraw_4: (binance_custom_withdraw_4, -3, 'Binance custom withdraw #4', 0, []),
    make_balance_to_average: (make_balance_to_average, -2, 'Check and make wanted balance', 0, []),
    bridge_rhino: (bridge_rhino, 1, 'Rhino bridge', 0, [2, 3, 4, 8, 9, 11, 12]),
    bridge_layerswap: (bridge_layerswap, 1, 'LayerSwap bridge', 0, [2, 3, 4, 8, 9, 11, 12]),
    bridge_orbiter: (bridge_orbiter, 1, 'Orbiter bridge', 0, [2, 3, 4, 8, 9, 11, 12]),
    bridge_across: (bridge_across, 1, 'Across bridge', 0, [2, 3, 11, 12]),
    bridge_bungee: (bridge_bungee, 1, 'Bungee bridge', 0, [2, 3, 11, 12]),
    bridge_owlto: (bridge_owlto, 1, 'Owlto bridge', 0, [2, 3, 11, 12]),
    bridge_relay: (bridge_relay, 1, 'Relay bridge', 0, [2, 3, 11, 12]),
    bridge_nitro: (bridge_nitro, 1, 'Nitro bridge', 0, [2, 3, 11, 12]),
    bridge_usenexus: (bridge_usenexus, 2, 'UseNexus bridge', 0, [0]),
    bridge_inevm: (bridge_inevm, 2, 'inEVM bridge', 0, [0]),
    bridge_nautilus: (bridge_nautilus, 2, 'Nautilus bridge', 0, [0]),
    bridge_stargate: (bridge_stargate, 2, 'Stargate bridge', 0, [0]),
    bridge_jumper: (bridge_jumper, 2, 'Jumper bridge', 0, [0]),
    bridge_debridge: (bridge_debridge, 2, 'deBridge bridge', 0, [0]),
    bridge_squidrouter: (bridge_squidrouter, 2, 'SquidRouter bridge', 0, [0]),
    bridge_rango: (bridge_rango, 2, 'Rango bridge', 0, [0]),
    bridge_renzo: (bridge_renzo, 2, 'Renzo bridge', 0, [0]),
    bridge_rango_simple: (bridge_rango_simple, 2, 'Rango simple bridge', 0, [0]),
    bridge_xyfinance: (bridge_xyfinance, 2, 'XYFinance bridge', 0, [0]),
    bridge_superform: (bridge_superform, 2, 'Superform bridge', 0, [0]),
    withdraw_superform: (withdraw_superform, 2, 'Superform withdraw', 0, [0]),
    deposit_aave_simple: (deposit_aave_simple, 2, 'Deposit AAVE', 0, [0]),
    withdraw_aave_simple: (withdraw_aave_simple, 2, 'Withdraw AAVE', 0, [0]),
    deposit_basilisk_simple: (deposit_basilisk_simple, 2, 'Deposit Basilisk', 0, [0]),
    withdraw_basilisk_simple: (withdraw_basilisk_simple, 2, 'Withdraw Basilisk', 0, [0]),
    deposit_eralend_simple: (deposit_eralend_simple, 2, 'Deposit EraLend', 0, [0]),
    withdraw_eralend_simple: (withdraw_eralend_simple, 2, 'Withdraw EraLend', 0, [0]),
    deposit_keom_simple: (deposit_keom_simple, 2, 'Deposit Keom', 0, [0]),
    withdraw_keom_simple: (withdraw_keom_simple, 2, 'Withdraw Keom', 0, [0]),
    deposit_layerbank_simple: (deposit_layerbank_simple, 2, 'Deposit LayerBank', 0, [0]),
    withdraw_layerbank_simple: (withdraw_layerbank_simple, 2, 'Withdraw LayerBank', 0, [0]),
    deposit_moonwell_simple: (deposit_moonwell_simple, 2, 'Deposit Moonwell', 0, [0]),
    withdraw_moonwell_simple: (withdraw_moonwell_simple, 2, 'Withdraw Moonwell', 0, [0]),
    deposit_seamless_simple: (deposit_seamless_simple, 2, 'Deposit Seamless', 0, [0]),
    withdraw_seamless_simple: (withdraw_seamless_simple, 2, 'Withdraw Seamless', 0, [0]),
    deposit_zerolend_simple: (deposit_zerolend_simple, 2, 'Deposit Zerolend', 0, [0]),
    withdraw_zerolend_simple: (withdraw_zerolend_simple, 2, 'Withdraw Zerolend', 0, [0]),
    deposit_elixir: (deposit_elixir, 2, 'Deposit ETH on Elixir', 0, [0]),
    deposit_usdc_elixir: (deposit_usdc_elixir, 2, 'Deposit USDC on Elixir', 0, [0]),
    withdraw_usdc_elixir: (withdraw_usdc_elixir, 2, 'Withdraw USDC on Elixir', 0, [0]),
    custom_swap: (custom_swap, 2, 'Custom Swap', 0, [0]),
    swap_jumper: (swap_jumper, 2, 'Jumper swap', 0, [0]),
    swap_debridge: (swap_debridge, 2, 'deBridge swap', 0, [0]),
    swap_squidrouter: (swap_squidrouter, 2, 'SquidRouter swap', 0, [0]),
    refuel_nautilus: (refuel_nautilus, 2, 'Refuel Nautilus from BNB Chain', 0, [0]),
    double_swap_bebop: (double_swap_bebop, 2, 'Double Bebop swap', 0, [0]),
    bridge_hyperlane_merkly: (bridge_hyperlane_merkly, 2, 'Merkly Hyperlane token bridge', 0, [0]),
    swap_izumi: (swap_izumi, 2, 'iZumi swap', 1, [3, 4, 8, 11]),
    swap_eth_to_ezeth: (swap_eth_to_ezeth, 2, 'Swap ETH -> ezETH', 1, [3, 4, 8, 11]),
    swap_ezeth_to_eth: (swap_ezeth_to_eth, 2, 'Swap ezETH -> ETH', 1, [3, 4, 8, 11]),
    swap_eth_to_tia_arb: (swap_eth_to_tia_arb, 2, 'Swap ETH -> TIA.n on Arbitrum', 1, [3, 4, 8, 11]),
    swap_tia_to_eth_arb: (swap_tia_to_eth_arb, 2, 'Swap TIA.n -> ETH on Arbitrum', 1, [3, 4, 8, 11]),
    swap_eth_to_tia_manta: (swap_eth_to_tia_manta, 2, 'Swap ETH -> TIA.n on Manta', 1, [3, 4, 8, 11]),
    swap_tia_to_eth_manta: (swap_tia_to_eth_manta, 2, 'Swap TIA.n -> ETH on Manta', 1, [3, 4, 8, 11]),
    swap_bnb_to_zbc_bsc: (swap_bnb_to_zbc_bsc, 2, 'Swap BNB -> ZBC on BNB Chain', 1, [3, 4, 8, 11]),
    swap_zbc_to_bnb_bsc: (swap_zbc_to_bnb_bsc, 2, 'Swap ZBC -> BNB on BNB Chain', 1, [3, 4, 8, 11]),
    smart_swap_in_for_bridging: (smart_swap_in_for_bridging, 2, 'Smart swap native for bridging tokens', 1, [3, 4, 8, 11]),
    smart_swap_out_for_bridging: (smart_swap_out_for_bridging, 2, 'Smart swap bridging tokens for native', 1, [3, 4, 8, 11]),
    smart_wrap_eth: (smart_wrap_eth, 2, 'Smart wrap native token', 0, []),
    smart_unwrap_eth: (smart_unwrap_eth, 2, 'Smart unwrap native token', 0, []),
    smart_rubyscore: (smart_rubyscore, 2, 'Smart Vote on RubyScore', 0, []),
    smart_check_in: (smart_check_in, 2, 'Smart CheckIn on Owlto', 0, []),
    smart_mintfun: (smart_mintfun, 2, 'Smart mint on MintFun', 0, []),
    mint_dbk: (mint_dbk, 2, 'DBK Genesis NFT mint', 0, []),
    add_liquidity_ambient: (add_liquidity_ambient, 2, 'Add liquidity wrsETH/ETH on Ambient', 0, []),
    remove_liquidity_ambient: (remove_liquidity_ambient, 2, 'Remove liquidity wrsETH/ETH on Ambient', 0, []),
    mint_squid_scholar_nft: (mint_squid_scholar_nft, 2, 'Squid Scholar NFT mint', 0, []),
    mint_stix_pass: (mint_stix_pass, 2, 'STIX Launch Tournament Pass Mint', 0, []),
    smart_dmail: (smart_dmail, 2, 'Smart send Dmail', 0, []),
    bridge_hyperlane_nft: (bridge_hyperlane_nft, 3, 'Merkly Hyperlane NFT bridge', 0, []),
    bridge_hyperlane_token: (bridge_hyperlane_token, 3, 'Merkly Hyperlane Tokens bridge', 0, []),
    claim_rewards_bungee: (claim_rewards_bungee, 2, 'Claim Socket rewards', 0, [11]),
    claim_op_across: (claim_op_across, 2, 'Claim OP on Across', 0, [11]),
    rhino_recovery_funds: (rhino_recovery_funds, 2, 'Rhino refund', 0, [11]),
    bridge_zerius: (bridge_zerius, 3, 'Zerius bridge NFT', 0, []),
    bridge_merkly: (bridge_merkly, 3, 'Merkly bridge NFT', 0, []),
    bridge_l2pass: (bridge_l2pass, 3, 'L2Pass bridge NFT', 0, []),
    bridge_nogem: (bridge_nogem, 3, 'nogem.app bridge NFT', 0, []),
    bridge_nogem_hnft: (bridge_nogem_hnft, 3, 'nogem.app bridge Hyperlane NFT', 0, []),
    bridge_nogem_htoken: (bridge_nogem_htoken, 3, 'nogem.app bridge Hyperlane token', 0, []),
    bridge_whale: (bridge_whale, 3, 'Whale bridge NFT', 0, []),
    bridge_getmint: (bridge_getmint, 3, 'GetMint Hyperlane bridge NFT', 0, []),
    bridge_womex: (bridge_womex, 3, 'Womex Hyperlane bridge NFT', 0, []),
    custom_sleep1: (custom_sleep1, 3, 'Custom Sleep #1', 0, []),
    custom_sleep2: (custom_sleep2, 3, 'Custom Sleep #2', 0, []),
    custom_sleep3: (custom_sleep3, 3, 'Custom Sleep #3', 0, []),
    refuel_bungee: (refuel_bungee, 3, 'Bungee refuel', 0, []),
    refuel_merkly: (refuel_merkly, 3, 'Merkly refuel', 0, []),
    refuel_l2pass: (refuel_l2pass, 3, 'L2Pass refuel', 0, []),
    refuel_nogem: (refuel_nogem, 3, 'nogem.app refuel', 0, []),
    refuel_zerius: (refuel_zerius, 3, 'Zerius refuel', 0, []),
    custom_random_approve: (custom_random_approve, 3, 'Custom Random Approve', 0, []),
    custom_rubyscore: (custom_rubyscore, 3, 'Custom RubyScore', 0, []),
    custom_check_in: (custom_check_in, 3, 'Custom CheckIn Owlto', 0, []),
    custom_mintfun: (custom_mintfun, 3, 'Custom Mintfun', 0, []),
    custom_dmail: (custom_dmail, 3, 'Custom Dmail', 0, []),
    custom_transfer_eth: (custom_transfer_eth, 3, 'Custom transfer ETH', 0, []),
    custom_transfer_eth_to_myself: (custom_transfer_eth_to_myself, 3, 'Custom transfer ETH to myself', 0, []),
    custom_wrap_eth: (custom_wrap_eth, 3, 'Custom wrap ETH', 0, []),
    custom_unwrap_eth: (custom_unwrap_eth, 3, 'Custom unwrap ETH', 0, []),
    refuel_whale: (refuel_whale, 3, 'Whale refuel', 0, []),
    smart_random_approve: (smart_random_approve, 2, 'Smart random approve', 0, [0]),
    smart_organic_swaps: (smart_organic_swaps, 2, 'Smart organic swap', 0, [0]),
    smart_organic_landings: (smart_organic_landings, 2, 'Smart organic landings', 0, [0]),
    bingx_transfer: (bingx_transfer, 2, 'BingX transfer', 0, []),
    smart_stake_tia: (smart_stake_tia, 2, 'Smart stake TIA in Celestia', 0, []),
    smart_transfer_eth: (smart_transfer_eth, 2, 'Smart transfer native token', 0, []),
    smart_transfer_cosmos: (smart_transfer_cosmos, 2, 'Smart transfer native token', 0, []),
    smart_transfer_eth_to_myself: (smart_transfer_eth_to_myself, 2, ' Smart transfer native token to myself', 0, []),
    smart_transfer_cosmos_to_cex: (smart_transfer_cosmos_to_cex, 2, ' Smart transfer native token to CEX', 0, []),
    okx_deposit: (okx_deposit, 5, 'OKX deposit', 0, []),
    bingx_deposit: (bingx_deposit, 5, 'Bingx deposit', 0, []),
    binance_deposit: (binance_deposit, 5, 'Binance deposit', 0, []),
    bitget_deposit: (bitget_deposit, 5, 'BitGet deposit', 0, []),
    okx_custom_deposit_1: (okx_custom_deposit_1, 5, 'OKX custom deposit #1', 0, []),
    mint_jumper: (mint_jumper, 2, 'Mint NFT on Mercle', 0, []),
    claim_task1_jumper: (claim_task1_jumper, 2, 'Claim task 1 on Mercle', 0, []),
    claim_task2_jumper: (claim_task2_jumper, 2, 'Claim task 2 on Mercle', 0, []),
    full_custom_swap1: (full_custom_swap1, 2, 'Custom swap #1', 0, [3, 4, 8, 11]),
    full_custom_swap2: (full_custom_swap2, 2, 'Custom swap #2', 0, [3, 4, 8, 11]),
    full_custom_swap3: (full_custom_swap3, 2, 'Custom swap #3', 0, [3, 4, 8, 11]),
    wrap_abuser: (wrap_abuser, 2, 'Wrap Abuse =)', 0, []),
    collector_eth: (collector_eth, 4, 'Collect ETH from tokens in all Netowrks', 0, []),
}


def get_func_by_name(module_name, help_message: bool = False):
    for k, v in AVAILABLE_MODULES_INFO.items():
        if k.__name__ == module_name:
            if help_message:
                return v[2]
            return v[0]


class RouteGenerator(Logger):
    def __init__(self):
        Logger.__init__(self)
        self.modules_names_const = [module.__name__ for module in list(AVAILABLE_MODULES_INFO.keys())]
        self.w3 = AsyncWeb3()

    @staticmethod
    def classic_generate_route():
        route = []
        copy_full_route = copy.deepcopy(Settings.CLASSIC_ROUTES_MODULES_USING)
        rpc = 'Arbitrum'
        flag = any(isinstance(sub_route, tuple) for sub_route in copy_full_route)

        if flag:
            blocks = []
            individual_modules_positions = []

            for i, item in enumerate(copy_full_route):
                if isinstance(item, tuple):
                    blocks.append(tuple(item))
                else:
                    individual_modules_positions.append((i, item))

            random.shuffle(blocks)
            blocks_count = random.randint(*copy.deepcopy(Settings.CLASSIC_ROUTES_BLOCKS_COUNT))
            total_blocks = blocks[:blocks_count]

            new_full_route_flat = []
            for block in total_blocks:
                new_full_route_flat.append(block)

            for position, modules in individual_modules_positions:
                new_full_route_flat.insert(position, modules)

            if Settings.ADD_FEE_SUPPORT_FOR_TXS:
                new_full_route_flat.insert(0, ['fee_support_withdraw'])
        else:
            new_full_route_flat = Settings.CLASSIC_ROUTES_MODULES_USING

        for i in new_full_route_flat:
            if isinstance(i, list):
                module_name = random.choice(i)
                if module_name is None:
                    continue
                if ':' in module_name:
                    module_name, rpc = module_name.split(':')

                module = get_func_by_name(module_name)
                if module:
                    module = get_func_by_name(module_name)
                    route.append(f"{module.__name__}:::{rpc}")
                else:
                    raise SoftwareException(f'Нет модуля с именем "{module_name}" в софте.')
            else:
                for sub_module in i:
                    module_name = random.choice(sub_module)
                    if module_name is None:
                        continue
                    if ':' in module_name:
                        module_name, rpc = module_name.split(':')

                    module = get_func_by_name(module_name)
                    if module:
                        route.append(f"{module.__name__}:::{rpc}")
                    else:
                        raise SoftwareException(f'Нет модуля с именем "{module_name}" в софте.')
            rpc = "Arbitrum"

        return route

    @staticmethod
    def sort_classic_route(route):
        modules_dependents = {
            'okx_withdraw': 0,
            'bingx_withdraw': 0,
            'binance_withdraw': 0,
            'make_balance_to_average': 1,
            'bridge_rhino': 1,
            'bridge_layerswap': 1,
            'bridge_nitro': 1,
            'bridge_orbiter': 1,
            'bridge_across': 1,
            'bridge_owlto': 1,
            'bridge_relay': 1,
            'bridge_native': 1,
            'bridge_zora': 1,
            'collector_eth': 3,
            'okx_deposit': 4,
            'bingx_deposit': 4,
            'binance_deposit': 4,
            'okx_deposit_l0': 4,
        }

        new_route = []
        classic_route = []
        for module_name in route:
            if module_name in modules_dependents:
                classic_route.append((module_name, modules_dependents[module_name]))
            else:
                new_route.append((module_name, 2))

        random.shuffle(new_route)
        classic_route.extend(new_route)
        route_with_priority = [module[0] for module in sorted(classic_route, key=lambda x: x[1])]

        return route_with_priority

    def classic_routes_json_save(self):
        clean_progress_file()

        with open(Settings.PROGRESS_FILE_PATH, 'w') as file:
            accounts_data = {}
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
                                account_names = [account for account in account_names if
                                                 account != ACCOUNT_NAMES[i - 1]]
            else:
                account_names = []

            if SHUFFLE_WALLETS:
                random.shuffle(account_names)

            for account_name in account_names:
                if isinstance(account_name, (str, int)):
                    classic_route = self.classic_generate_route()
                    if SHUFFLE_ROUTE:
                        classic_route = self.sort_classic_route(route=classic_route)
                    account_data = {
                        "current_step": 0,
                        "route": classic_route
                    }
                    accounts_data[str(account_name)] = account_data
            json.dump(accounts_data, file, indent=4)
        self.logger_msg(
            None, None,
            msg=f'Successfully generated {len(accounts_data)} classic routes in {Settings.PROGRESS_FILE_PATH}\n',
            type_msg='success'
        )

    def smart_routes_json_save(self, account_name: str, route: list):
        progress_file_path = './data/services/wallets_progress.json'

        try:
            with open(progress_file_path, 'r+') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = {}

        data[account_name] = {
            "current_step": 0,
            "route": ([" ".join(item) for item in route] if isinstance(route[0], tuple) else route) if route else []
        }

        with open(progress_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        self.logger_msg(
            None, None,
            msg=f'Successfully generated smart routes for {account_name}',
            type_msg='success'
        )

    # def get_full_smart_route(self):
    #     clean_progress_file()
    #     self.logger_msg(
    #         None, None,
    #         f'Start generate full smart routes for each account...\n'
    #     )
    #     time.sleep(2)
    #
    #     HYPERLANE_VOLUME
    #     HYPERLANE_TXS
    #     HYPERLANE_BRIDGE_MODULES
    #     HYPERLANE_RANDOM_MODULES
    #     HYPERLANE_LZ_MODULES
    #
    #     with open('./data/services/wallets_progress.json', 'w') as file:
    #         accounts_data = {}
    #         for account_name in ACCOUNT_NAMES:
    #             if isinstance(account_name, (str, int)):
    #
    #
    #                 account_data = {
    #                     "current_step": 0,
    #                     "route": classic_route
    #                 }
    #
    #                 accounts_data[str(account_name)] = account_data
    #         json.dump(accounts_data, file, indent=4)
    #     self.logger_msg(
    #         None, None,
    #         f'Successfully generated {len(accounts_data)} classic routes in data/services/wallets_progress.json\n',
    #         'success'
    #     )
