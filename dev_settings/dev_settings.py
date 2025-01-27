import importlib.util
import os


class Settings:
    PROGRESS_FILE_PATH = None

    @staticmethod
    def load_settings(settings: dict):
        for key, value in settings.items():
            if hasattr(Settings, key):
                setattr(Settings, key, value)

    @staticmethod
    def get_presets_settings(with_custom: bool = False):
        base_dir = os.path.dirname(os.path.dirname(__file__))

        def load_settings_from_file(f_path):
            spec = importlib.util.spec_from_file_location(os.path.basename(f_path), f_path)
            settings_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(settings_module)
            settings = {
                attr: value for attr, value in vars(settings_module).items() if not attr.startswith("__")
            }
            return settings

        presets_dir = os.path.join(base_dir, 'presets')
        all_settings = {}

        for filename in os.listdir(presets_dir):
            if filename.endswith('.py'):
                setting_name = filename[:-3]
                file_path = os.path.join(presets_dir, filename)
                all_settings[setting_name] = load_settings_from_file(file_path)

        if with_custom:
            custom_settings_file = os.path.join(base_dir, 'settings.py')
            custom_settings = load_settings_from_file(custom_settings_file)
            all_settings['custom'] = custom_settings

        return all_settings

    @staticmethod
    def prepare_settings(route: str = 'custom'):
        all_settings = Settings.get_presets_settings(with_custom=True)

        if route != 'custom':
            Settings.load_settings(all_settings['custom'])
            Settings.PROGRESS_FILE_PATH = f'./data/services/{route}_wallets_progress.json'
        else:
            Settings.PROGRESS_FILE_PATH = f'./data/services/wallets_progress.json'

        settings = all_settings[route]
        Settings.load_settings(settings)

    GLOBAL_LIMITER = None
    MINIMUM_ORGANIC_SWAP_AMOUNT = None
    SWAP_AMOUNT = None
    DACKIESWAP_AMOUNT = None
    LANDINGS_AMOUNT = None
    TRANSFER_AMOUNT = None
    WRAPS_AMOUNT = None
    STAKE_AMOUNT = None
    DBK_BRIDGE_AMOUNT = None
    RENZO_EZETH_SWAP_AMOUNT = None
    ARBITRUM_TIA_SWAP_AMOUNT = None
    MANTA_TIA_SWAP_AMOUNT = None
    ONEINCH_SWAP_AMOUNT = None
    REFUEL_NAUTILUS_AMOUNT = None
    AMBIENT_WRSETH_AMOUNT = None
    ELIXIR_AMOUNT = None
    ELIXIR_USDC_AMOUNT = None
    WAIT_FOR_RECEIPT_CEX = None
    COLLECT_FROM_SUB_CEX = None
    FEE_SUPPORT_DATA = None
    FEE_SUPPORT_MIN_WITHDRAW = None
    FEE_SUPPORT_CEXS = None
    TRANSFER_COSMOS_CEXS = None
    OKX_WITHDRAW_DATA = None
    OKX_DEPOSIT_DATA = None
    OKX_CUSTOM_DEPOSIT_1 = None
    BINGX_WITHDRAW_DATA = None
    BINGX_DEPOSIT_DATA = None
    BINANCE_WITHDRAW_DATA = None
    BINANCE_DEPOSIT_DATA = None
    BITGET_WITHDRAW_DATA = None
    BITGET_DEPOSIT_DATA = None
    OKX_CUSTOM_WITHDRAW_1 = None
    OKX_CUSTOM_WITHDRAW_2 = None
    OKX_CUSTOM_WITHDRAW_3 = None
    OKX_CUSTOM_WITHDRAW_4 = None
    BITGET_CUSTOM_WITHDRAW_1 = None
    BITGET_CUSTOM_WITHDRAW_2 = None
    BITGET_CUSTOM_WITHDRAW_3 = None
    BITGET_CUSTOM_WITHDRAW_4 = None
    BINANCE_CUSTOM_WITHDRAW_1 = None
    BINANCE_CUSTOM_WITHDRAW_2 = None
    BINANCE_CUSTOM_WITHDRAW_3 = None
    BINANCE_CUSTOM_WITHDRAW_4 = None
    CEX_BALANCER_CONFIG = None
    WAIT_FOR_RECEIPT_BRIDGE = None
    NATIVE_CHAIN_FROM_NAMES = None
    NATIVE_CHAIN_TO_NAMES = None
    NATIVE_BRIDGE_AMOUNT = None
    NATIVE_TOKEN_NAME = None
    NATIVE_AMOUNT_LIMITER = None
    ACROSS_CHAIN_FROM_NAMES = None
    ACROSS_CHAIN_TO_NAMES = None
    ACROSS_BRIDGE_AMOUNT = None
    ACROSS_TOKEN_NAME = None
    ACROSS_AMOUNT_LIMITER = None
    BUNGEE_CHAIN_FROM_NAMES = None
    BUNGEE_CHAIN_TO_NAMES = None
    BUNGEE_BRIDGE_AMOUNT = None
    BUNGEE_TOKEN_NAME = None
    BUNGEE_ROUTE_TYPE = None
    BUNGEE_AMOUNT_LIMITER = None
    LAYERSWAP_CHAIN_FROM_NAMES = None
    LAYERSWAP_CHAIN_TO_NAMES = None
    LAYERSWAP_BRIDGE_AMOUNT = None
    LAYERSWAP_TOKEN_NAME = None
    LAYERSWAP_AMOUNT_LIMITER = None
    NITRO_CHAIN_FROM_NAMES = None
    NITRO_CHAIN_TO_NAMES = None
    NITRO_BRIDGE_AMOUNT = None
    NITRO_TOKEN_NAME = None
    NITRO_AMOUNT_LIMITER = None
    ORBITER_CHAIN_FROM_NAMES = None
    ORBITER_CHAIN_TO_NAMES = None
    ORBITER_BRIDGE_AMOUNT = None
    ORBITER_TOKEN_NAME = None
    ORBITER_AMOUNT_LIMITER = None
    OWLTO_CHAIN_FROM_NAMES = None
    OWLTO_CHAIN_TO_NAMES = None
    OWLTO_BRIDGE_AMOUNT = None
    OWLTO_TOKEN_NAME = None
    OWLTO_AMOUNT_LIMITER = None
    RELAY_CHAIN_FROM_NAMES = None
    RELAY_CHAIN_TO_NAMES = None
    RELAY_BRIDGE_AMOUNT = None
    RELAY_TOKEN_NAME = None
    RELAY_AMOUNT_LIMITER = None
    RHINO_CHAIN_FROM_NAMES = None
    RHINO_CHAIN_TO_NAMES = None
    RHINO_BRIDGE_AMOUNT = None
    RHINO_TOKEN_NAME = None
    RHINO_AMOUNT_LIMITER = None
    RANGO_CHAIN_FROM_NAMES = None
    RANGO_CHAIN_TO_NAMES = None
    RANGO_BRIDGE_AMOUNT = None
    RANGO_TOKEN_NAME = None
    RANGO_AMOUNT_LIMITER = None
    XYFINANCE_CHAIN_FROM_NAMES = None
    XYFINANCE_CHAIN_TO_NAMES = None
    XYFINANCE_BRIDGE_AMOUNT = None
    XYFINANCE_TOKEN_NAME = None
    XYFINANCE_AMOUNT_LIMITER = None
    BRIDGE_SWITCH_CONTROL = None
    WAIT_FOR_RECEIPT = None
    WAIT_FOR_RECEIPT_L0 = None
    ALL_DST_CHAINS = None
    SEARCH_CHAINS = None
    POSSIBLE_TOKENS = None
    SUPERFORM_CHAIN_FROM = None
    SUPERFORM_CHAIN_WITHDRAW = None
    SUPERFORM_VAULTS_TO = None
    SUPERFORM_TOKEN_NAME = None
    SUPERFORM_AMOUNT = None
    SUPERFROM_EXCLUDE_ROUTE = None
    SUPERFORM_BRIDGE_MODE = None
    USENEXUS_CHAINS = None
    USENEXUS_TOKENS = None
    USENEXUS_AMOUNT = None
    USENEXUS_BRIDGE_COUNT = None
    USENEXUS_RUN_TIMES = None
    USENEXUS_AMOUNT_LIMITER = None
    MERKLY_CHAINS = None
    MERKLY_TOKENS = None
    MERKLY_AMOUNT = None
    MERKLY_BRIDGE_COUNT = None
    MERKLY_RUN_TIMES = None
    MERKLY_AMOUNT_LIMITER = None
    INEVM_CHAINS = None
    INEVM_TOKENS = None
    INEVM_AMOUNT = None
    INEVM_BRIDGE_COUNT = None
    INEVM_RUN_TIMES = None
    INEVM_AMOUNT_LIMITER = None
    RENZO_CHAINS = None
    RENZO_TOKENS = None
    RENZO_AMOUNT = None
    RENZO_BRIDGE_COUNT = None
    RENZO_RUN_TIMES = None
    RENZO_AMOUNT_LIMITER = None
    NAUTILUS_CHAINS = None
    NAUTILUS_TOKENS = None
    NAUTILUS_AMOUNT = None
    NAUTILUS_BRIDGE_COUNT = None
    NAUTILUS_RUN_TIMES = None
    NAUTILUS_AMOUNT_LIMITER = None
    STARGATE_CHAINS = None
    STARGATE_TOKENS = None
    STARGATE_AMOUNT = None
    STARGATE_BRIDGE_COUNT = None
    STARGATE_RUN_TIMES = None
    STARGATE_AMOUNT_LIMITER = None
    SQUIDROUTER_CHAINS = None
    SQUIDROUTER_TOKENS = None
    SQUIDROUTER_AMOUNT = None
    SQUIDROUTER_BRIDGE_COUNT = None
    SQUIDROUTER_RUN_TIMES = None
    SQUIDROUTER_AMOUNT_LIMITER = None
    SQUIDROUTER_SWAP_TOKENS = None
    DEBRIDGE_CHAINS = None
    DEBRIDGE_TOKENS = None
    DEBRIDGE_AMOUNT = None
    DEBRIDGE_BRIDGE_COUNT = None
    DEBRIDGE_RUN_TIMES = None
    DEBRIDGE_AMOUNT_LIMITER = None
    DEBRIDGE_SWAP_TOKENS = None
    RANGO_CHAINS = None
    RANGO_TOKENS = None
    RANGO_AMOUNT = None
    RANGO_BRIDGE_COUNT = None
    RANGO_RUN_TIMES = None
    RANGO_AMOUNT_LIMITER2 = None
    RANGO_SWAP_TOKENS = None
    JUMPER_CHAINS = None
    JUMPER_TOKENS = None
    JUMPER_AMOUNT = None
    JUMPER_BRIDGE_COUNT = None
    JUMPER_RUN_TIMES = None
    JUMPER_ROUTE_TYPE = None
    JUMPER_AMOUNT_LIMITER = None
    JUMPER_SWAP_TOKENS = None
    SRC_CHAIN_L2PASS = None
    DST_CHAIN_L2PASS_NFT = None
    DST_CHAIN_L2PASS_REFUEL = None
    SRC_CHAIN_NOGEM = None
    DST_CHAIN_NOGEM_NFT = None
    DST_CHAIN_NOGEM_REFUEL = None
    SRC_CHAIN_MERKLY = None
    DST_CHAIN_MERKLY_NFT = None
    DST_CHAIN_MERKLY_REFUEL = None
    SRC_CHAIN_WHALE = None
    DST_CHAIN_WHALE_NFT = None
    DST_CHAIN_WHALE_REFUEL = None
    SRC_CHAIN_ZERIUS = None
    DST_CHAIN_ZERIUS_NFT = None
    DST_CHAIN_ZERIUS_REFUEL = None
    SRC_CHAIN_BUNGEE = None
    DST_CHAIN_BUNGEE_REFUEL = None
    SRC_CHAIN_MERKLY_HYPERLANE = None
    DST_CHAIN_MERKLY_HYPERLANE = None
    MERKLY_HYP_TOKENS_AMOUNTS = None
    SRC_CHAIN_NOGEM_HYPERLANE = None
    DST_CHAIN_NOGEM_HYPERLANE = None
    NOGEM_HYP_TOKENS_AMOUNTS = None
    SRC_CHAIN_GETMINT_HYPERLANE = None
    DST_CHAIN_GETMINT_HYPERLANE = None
    SRC_CHAIN_WOMEX_HYPERLANE = None
    DST_CHAIN_WOMEX_HYPERLANE = None
    CUSTOM_SWAP_DATA = None
    COLLECTOR_MIN_AMOUNTS = None
    COLLECTOR_DATA = None
    AMBIENT_PERCENT_RANGE = None
    MINTFUN_CONTRACTS = None
    MINTFUN_MINT_COUNT = None
    CUSTOM_SLEEP_1 = None
    CUSTOM_SLEEP_2 = None
    CUSTOM_SLEEP_3 = None
    FULL_CUSTOM_SWAP_DATA1 = None
    FULL_CUSTOM_SWAP_DATA2 = None
    FULL_CUSTOM_SWAP_DATA3 = None
    CLASSIC_ROUTES_BLOCKS_COUNT = None
    ADD_FEE_SUPPORT_FOR_TXS = None
    CLASSIC_ROUTES_MODULES_USING = None
    BEBOP_DOUBLESWAP_FROM_TOKEN_NAMES = None
    BEBOP_DOUBLESWAP_AMOUNTS = None
    BEBOP_DOUBLESWAP_TO_TOKEN_NAME = None
