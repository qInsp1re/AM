import random

from modules import *
from utils.networks import *
from dev_settings import Settings


def get_client(module_input_data) -> Client | CosmosClient | SolanaClient:
    if module_input_data["network"].name in ['Celestia', 'Injective', 'Neutron']:
        return CosmosClient(module_input_data)
    elif module_input_data["network"].name == 'Solana':
        return SolanaClient(module_input_data)
    return Client(module_input_data)


def get_rpc_by_chain_name(chain_id):
    return {
        0: ArbitrumRPC,
        "Arbitrum": ArbitrumRPC,
        "Arbitrum Nova": Arbitrum_novaRPC,
        "Base": BaseRPC,
        "Linea": LineaRPC,
        "Manta": MantaRPC,
        "Polygon": PolygonRPC,
        "Optimism": OptimismRPC,
        "Scroll": ScrollRPC,
        # 9: StarknetRPC,
        "Polygon zkEVM": Polygon_ZKEVM_RPC,
        "zkSync": zkSyncEraRPC,
        "Zora": ZoraRPC,
        "Ethereum": EthereumRPC,
        "Avalanche": AvalancheRPC,
        "BNB Chain": BSC_RPC,
        "Moonbeam": MoonbeamRPC,
        "Harmony": HarmonyRPC,
        "Telos": TelosRPC,
        "Celo": CeloRPC,
        "Gnosis": GnosisRPC,
        "Core": CoreRPC,
        "TomoChain": TomoChainRPC,
        "Conflux": ConfluxRPC,
        "Orderly": OrderlyRPC,
        "Horizen": HorizenRPC,
        "Metis": MetisRPC,
        "Astar": AstarRPC,
        "OpBNB": OpBNB_RPC,
        "Mantle": MantleRPC,
        "Moonriver": MoonriverRPC,
        "Klaytn": KlaytnRPC,
        "Kava": KavaRPC,
        "Fantom": FantomRPC,
        "Aurora": AuroraRPC,
        "Canto": CantoRPC,
        "DFK": DFK_RPC,
        "Fuse": FuseRPC,
        "Goerli": GoerliRPC,
        "Meter": MeterRPC,
        "OKX Chain": OKX_RPC,
        "Shimmer": ShimmerRPC,
        "Tenet": TenetRPC,
        "XPLA": XPLA_RPC,
        "LootChain": LootChainRPC,
        "ZKFair": ZKFairRPC,
        "Beam": BeamRPC,
        "InEVM": InEVM_RPC,
        "Rarible": RaribleRPC,
        "Blast": BlastRPC,
        "Mode": ModeRPC,
        "Celestia": CelestiaRPC,
        "Neutron": NeutronRPC,
        "Injective": INJ_RPC,
        "Nautilus": NautilusRPC,
        "Solana": SolanaRPC,
        "xLayer": xLayerRPC,
        "Taiko": TaikoRPC,
        "DBK": DbkRPC,
        "Gravity": GravityRPC,
    }[chain_id]


async def cex_deposit_util(current_client, dapp_id: int, deposit_data: tuple):
    class_name = {
        1: OKX,
        2: BingX,
        3: Binance,
        4: Bitget
    }[dapp_id]

    return await class_name(current_client).deposit(deposit_data=deposit_data)


async def okx_deposit(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_cex_deposit(dapp_id=1)


async def bingx_deposit(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_cex_deposit(dapp_id=2)


async def binance_deposit(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_cex_deposit(dapp_id=3)


async def bitget_deposit(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_cex_deposit(dapp_id=4)


async def okx_custom_deposit_1(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_cex_deposit(dapp_id=5)


async def bridge_utils(current_client, dapp_id, bridge_data, need_fee=False):
    class_bridge = {
        1: Across,
        2: Bungee,
        3: LayerSwap,
        4: Nitro,
        5: Orbiter,
        6: Owlto,
        7: Relay,
        8: Rhino,
        10: Rango,
        11: XYfinance,
    }[dapp_id]

    return await class_bridge(current_client).bridge(bridge_data, need_check=need_fee)


async def bridge_across(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge(dapp_id=1)


async def bridge_bungee(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge(dapp_id=2)


async def bridge_layerswap(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge(dapp_id=3)


async def bridge_nitro(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge(dapp_id=4)


async def bridge_orbiter(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge(dapp_id=5)


async def bridge_owlto(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge(dapp_id=6)


async def bridge_relay(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge(dapp_id=7)


async def bridge_rhino(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge(dapp_id=8)


async def bridge_rango_simple(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge(dapp_id=10)


async def bridge_xyfinance(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge(dapp_id=11)


async def omnichain_util(
        module_input_data, chain_from_name: str, dapp_id: int = 0, dapp_mode: int | str = 0,
        input_data: dict | int = None, need_check: bool = False,
):
    class_name, src_chain_name = {
        1: (L2Pass, Settings.SRC_CHAIN_L2PASS),
        2: (Nogem, Settings.SRC_CHAIN_NOGEM),
        3: (Merkly, Settings.SRC_CHAIN_MERKLY),
        4: (Whale, Settings.SRC_CHAIN_WHALE),
        5: (Zerius, Settings.SRC_CHAIN_ZERIUS),
        6: (GetMint, Settings.SRC_CHAIN_GETMINT_HYPERLANE),
        7: (Womex, Settings.SRC_CHAIN_GETMINT_HYPERLANE),
        8: (Bungee, Settings.SRC_CHAIN_BUNGEE),
    }[dapp_id]

    source_chain_name = random.choice(src_chain_name) if not chain_from_name else chain_from_name
    module_input_data["network"] = get_rpc_by_chain_name(source_chain_name)
    worker = class_name(get_client(module_input_data))

    if dapp_mode in [1, 2]:
        func = {
            1: worker.refuel,
            2: worker.bridge,
        }[dapp_mode]
    else:
        func = {
            'bridge NFT Wormhole': worker.wnft_bridge,
            'bridge Token Wormhole': worker.wt_bridge,
            'bridge NFT Hyperlane': worker.hnft_bridge,
            'bridge Token Hyperlane': worker.ht_bridge,
        }[dapp_mode]

    return await func(input_data, need_check=need_check)


async def bridge_l2pass(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_layerzero_util(dapp_id=1, dapp_mode=2)


async def bridge_nogem(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_layerzero_util(dapp_id=2, dapp_mode=2)


async def bridge_merkly(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_layerzero_util(dapp_id=3, dapp_mode=2)


async def bridge_whale(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_layerzero_util(dapp_id=4, dapp_mode=2)


async def bridge_zerius(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_layerzero_util(dapp_id=5, dapp_mode=2)


async def refuel_l2pass(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_layerzero_util(dapp_id=1, dapp_mode=1)


async def refuel_nogem(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_layerzero_util(dapp_id=2, dapp_mode=1)


async def refuel_merkly(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_layerzero_util(dapp_id=3, dapp_mode=1)


async def refuel_whale(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_layerzero_util(dapp_id=4, dapp_mode=1)


async def refuel_zerius(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_layerzero_util(dapp_id=5, dapp_mode=1)


async def refuel_bungee(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_layerzero_util(dapp_id=8, dapp_mode=1)


async def vote_rubyscore(current_client):
    worker = RubyScore(current_client)
    return await worker.vote()


async def check_in_owlto(current_client):
    worker = Owlto(current_client)
    return await worker.check_in()


async def mint_mintfun(current_client):
    worker = MintFun(current_client)
    return await worker.mint()


async def bridge_hyperlane_nft(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.merkly_omnichain_util(dapp_id=3, dapp_function=2)


async def bridge_hyperlane_token(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.merkly_omnichain_util(dapp_id=3, dapp_function=3)


async def bridge_getmint(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.merkly_omnichain_util(dapp_id=2, dapp_function=2)


async def bridge_womex(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.merkly_omnichain_util(dapp_id=1, dapp_function=2)


async def bridge_nogem_hnft(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.merkly_omnichain_util(dapp_id=4, dapp_function=2)


async def bridge_nogem_htoken(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.merkly_omnichain_util(dapp_id=4, dapp_function=3)


async def okx_withdraw(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_cex_withdraw(dapp_id=1)


async def fee_support_withdraw(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.get_fee_support_for_txs()


async def fee_support_withdraw_for_arb(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.get_fee_support_for_arb()


async def fee_support_withdraw_for_base(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.get_fee_support_for_base()


async def okx_custom_withdraw_1(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.okx_custom_withdraw_1()


async def okx_custom_withdraw_2(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.okx_custom_withdraw_2()


async def okx_custom_withdraw_3(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.okx_custom_withdraw_3()


async def okx_custom_withdraw_4(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.okx_custom_withdraw_4()


async def bitget_custom_withdraw_1(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.bitget_custom_withdraw_1()


async def bitget_custom_withdraw_2(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.bitget_custom_withdraw_2()


async def bitget_custom_withdraw_3(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.bitget_custom_withdraw_3()


async def bitget_custom_withdraw_4(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.bitget_custom_withdraw_4()


async def binance_custom_withdraw_1(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.binance_custom_withdraw_1()


async def binance_custom_withdraw_2(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.binance_custom_withdraw_2()


async def binance_custom_withdraw_3(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.binance_custom_withdraw_3()


async def binance_custom_withdraw_4(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.binance_custom_withdraw_4()


async def bingx_withdraw(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_cex_withdraw(dapp_id=2)


async def binance_withdraw(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_cex_withdraw(dapp_id=3)


async def bitget_withdraw(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_cex_withdraw(dapp_id=4)


async def smart_random_approve(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_random_approve()


async def custom_random_approve(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_random_approve(custom_rpc=True)


async def send_message_dmail(current_client):
    worker = Dmail(current_client)
    return await worker.send_message()


async def smart_wrap_eth(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_wrap()


async def smart_unwrap_eth(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_unwrap()


async def smart_stake_tia(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.stake_celestia()


async def smart_rubyscore(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_rubyscore()


async def smart_check_in(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_check_in()


async def smart_mintfun(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_mintfun()


async def smart_dmail(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_dmail()


async def smart_transfer_eth(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_transfer(random_address=True)


async def smart_transfer_eth_to_myself(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_transfer()


async def smart_transfer_cosmos(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_transfer_cosmos(random_address=True)


async def smart_transfer_cosmos_to_cex(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_transfer_cosmos()


async def transfer_eth(current_client, **kwargs):
    worker = SimpleEVM(current_client)
    return await worker.transfer_eth(**kwargs)


async def transfer_eth_to_myself(current_client, **kwargs):
    worker = SimpleEVM(current_client)
    return await worker.transfer_eth_to_myself(**kwargs)


async def transfer_cosmos(current_client, **kwargs):
    worker = SimpleCosmos(current_client)
    return await worker.transfer_native(**kwargs)


async def transfer_cosmos_to_cex(current_client, **kwargs):
    worker = SimpleCosmos(current_client)
    return await worker.transfer_native_to_cex(**kwargs)


async def wrap_eth(current_client, **kwargs):
    worker = SimpleEVM(current_client)
    return await worker.wrap_eth(**kwargs)


async def unwrap_eth(current_client, **kwargs):
    worker = SimpleEVM(current_client)
    return await worker.unwrap_eth(**kwargs)


async def custom_rubyscore(module_input_data):
    worker = RubyScore(get_client(module_input_data))
    return await worker.vote()


async def custom_check_in(module_input_data):
    worker = Owlto(get_client(module_input_data))
    return await worker.check_in()


async def custom_mintfun(module_input_data):
    worker = MintFun(get_client(module_input_data))
    return await worker.mint()


async def custom_dmail(module_input_data):
    worker = Dmail(get_client(module_input_data))
    return await worker.send_message()


async def custom_transfer_eth(module_input_data):
    worker = SimpleEVM(get_client(module_input_data))
    return await worker.transfer_eth()


async def custom_transfer_eth_to_myself(module_input_data):
    worker = SimpleEVM(get_client(module_input_data))
    return await worker.transfer_eth_to_myself()


async def custom_wrap_eth(module_input_data):
    worker = SimpleEVM(get_client(module_input_data))
    return await worker.wrap_eth()


async def custom_unwrap_eth(module_input_data):
    worker = SimpleEVM(get_client(module_input_data))
    return await worker.unwrap_eth()


async def deposit_aave(current_client, **kwargs):
    worker = Aave(current_client)
    return await worker.deposit(**kwargs)


async def withdraw_aave(current_client, **kwargs):
    worker = Aave(current_client)
    return await worker.deposit(**kwargs)


async def deposit_basilisk(current_client, **kwargs):
    worker = Basilisk(current_client)
    return await worker.deposit(**kwargs)


async def withdraw_basilisk(current_client, **kwargs):
    worker = Basilisk(current_client)
    return await worker.deposit(**kwargs)


async def deposit_eralend(current_client, **kwargs):
    worker = EraLend(current_client)
    return await worker.deposit(**kwargs)


async def withdraw_eralend(current_client, **kwargs):
    worker = EraLend(current_client)
    return await worker.deposit(**kwargs)


async def deposit_keom(current_client, **kwargs):
    worker = Keom(current_client)
    return await worker.deposit(**kwargs)


async def withdraw_keom(current_client, **kwargs):
    worker = Keom(current_client)
    return await worker.deposit(**kwargs)


async def deposit_layerbank(current_client, **kwargs):
    worker = LayerBank(current_client)
    return await worker.deposit(**kwargs)


async def withdraw_layerbank(current_client, **kwargs):
    worker = LayerBank(current_client)
    return await worker.deposit(**kwargs)


async def deposit_moonwell(current_client, **kwargs):
    worker = Moonwell(current_client)
    return await worker.deposit(**kwargs)


async def withdraw_moonwell(current_client, **kwargs):
    worker = Moonwell(current_client)
    return await worker.deposit(**kwargs)


async def deposit_seamless(current_client, **kwargs):
    worker = Seamless(current_client)
    return await worker.deposit(**kwargs)


async def withdraw_seamless(current_client, **kwargs):
    worker = Seamless(current_client)
    return await worker.deposit(**kwargs)


async def deposit_zerolend(current_client, **kwargs):
    worker = ZeroLend(current_client)
    return await worker.deposit(**kwargs)


async def withdraw_zerolend(current_client, **kwargs):
    worker = ZeroLend(current_client)
    return await worker.deposit(**kwargs)


async def deposit_aave_simple(module_input_data, **kwargs):
    worker = Aave(get_client(module_input_data))
    return await worker.deposit(**kwargs)


async def withdraw_aave_simple(module_input_data, **kwargs):
    worker = Aave(get_client(module_input_data))
    return await worker.withdraw(**kwargs)


async def deposit_basilisk_simple(module_input_data, **kwargs):
    worker = Basilisk(get_client(module_input_data))
    return await worker.deposit(**kwargs)


async def withdraw_basilisk_simple(module_input_data, **kwargs):
    worker = Basilisk(get_client(module_input_data))
    return await worker.withdraw(**kwargs)


async def deposit_eralend_simple(module_input_data, **kwargs):
    worker = EraLend(get_client(module_input_data))
    return await worker.deposit(**kwargs)


async def withdraw_eralend_simple(module_input_data, **kwargs):
    worker = EraLend(get_client(module_input_data))
    return await worker.withdraw(**kwargs)


async def deposit_keom_simple(module_input_data, **kwargs):
    worker = Keom(get_client(module_input_data))
    return await worker.deposit(**kwargs)


async def withdraw_keom_simple(module_input_data, **kwargs):
    worker = Keom(get_client(module_input_data))
    return await worker.withdraw(**kwargs)


async def deposit_layerbank_simple(module_input_data, **kwargs):
    worker = LayerBank(get_client(module_input_data))
    return await worker.deposit(**kwargs)


async def withdraw_layerbank_simple(module_input_data, **kwargs):
    worker = LayerBank(get_client(module_input_data))
    return await worker.withdraw(**kwargs)


async def deposit_moonwell_simple(module_input_data, **kwargs):
    worker = Moonwell(get_client(module_input_data))
    return await worker.deposit(**kwargs)


async def withdraw_moonwell_simple(module_input_data, **kwargs):
    worker = Moonwell(get_client(module_input_data))
    return await worker.withdraw(**kwargs)


async def deposit_seamless_simple(module_input_data, **kwargs):
    worker = Seamless(get_client(module_input_data))
    return await worker.deposit(**kwargs)


async def withdraw_seamless_simple(module_input_data, **kwargs):
    worker = Seamless(get_client(module_input_data))
    return await worker.withdraw(**kwargs)


async def deposit_zerolend_simple(module_input_data, **kwargs):
    worker = ZeroLend(get_client(module_input_data))
    return await worker.deposit(**kwargs)


async def withdraw_zerolend_simple(module_input_data, **kwargs):
    worker = ZeroLend(get_client(module_input_data))
    return await worker.withdraw(**kwargs)


async def deposit_elixir(module_input_data):
    module_input_data["network"] = EthereumRPC
    worker = Elixir(get_client(module_input_data))
    return await worker.deposit()


async def deposit_usdc_elixir(module_input_data):
    module_input_data["network"] = ArbitrumRPC
    worker = Elixir(get_client(module_input_data))
    return await worker.deposit_usdc()


async def withdraw_usdc_elixir(module_input_data):
    module_input_data["network"] = ArbitrumRPC
    worker = Elixir(get_client(module_input_data))
    return await worker.withdraw_usdc()


async def swap_izumi(current_client, **kwargs):
    worker = Izumi(current_client)
    return await worker.swap(**kwargs)


async def swap_bebop(current_client, **kwargs):
    worker = Bebop(current_client)
    return await worker.swap(**kwargs)


async def double_swap_bebop(module_input_data, **kwargs):
    worker = Bebop(get_client(module_input_data))
    return await worker.double_swap(**kwargs)


async def swap_dackieswap(current_client, **kwargs):
    worker = DackieSwap(current_client)
    return await worker.swap(**kwargs)


async def swap_odos(current_client, **kwargs):
    worker = ODOS(current_client)
    return await worker.swap(**kwargs)


async def swap_xyfinance(current_client, **kwargs):
    worker = XYfinance(current_client)
    return await worker.bridge(**kwargs)


async def swap_syncswap(current_client, **kwargs):
    worker = SyncSwap(current_client)
    return await worker.swap(**kwargs)


async def swap_openocean(current_client, **kwargs):
    worker = OpenOcean(current_client)
    return await worker.swap(**kwargs)


async def swap_1inch(current_client, **kwargs):
    worker = OneInch(current_client)
    return await worker.swap(**kwargs)


async def swap_jupiter(current_client, **kwargs):
    worker = Jupiter(current_client)
    return await worker.swap(**kwargs)


async def swap_pancake(current_client, **kwargs):
    worker = PancakeSwap(current_client)
    return await worker.swap(**kwargs)


async def swap_sushiswap(current_client, **kwargs):
    worker = SushiSwap(current_client)
    return await worker.swap(**kwargs)


async def swap_ambient(current_client, **kwargs):
    worker = Ambient(current_client)
    return await worker.swap(**kwargs)


async def swap_woofi(current_client, **kwargs):
    worker = WooFi(current_client)
    return await worker.swap(**kwargs)


async def swap_spacefi(current_client, **kwargs):
    worker = SpaceFi(current_client)
    return await worker.swap(**kwargs)


async def swap_maverick(current_client, **kwargs):
    worker = Maverick(current_client)
    return await worker.swap(**kwargs)


async def swap_velocore(current_client, **kwargs):
    worker = Velocore(current_client)
    return await worker.swap(**kwargs)


async def swap_uniswap(current_client, **kwargs):
    worker = Uniswap(current_client)
    return await worker.swap(**kwargs)


async def swap_thruster(current_client, **kwargs):
    worker = Thruster(current_client)
    return await worker.swap(**kwargs)


async def swap_quickswap(current_client, **kwargs):
    worker = QuickSwap(current_client)
    return await worker.swap(**kwargs)


async def custom_swap(module_input_data, **kwargs):
    worker = Custom(get_client(module_input_data))
    return await worker.custom_swaps(**kwargs)


async def collect_eth_util(module_input_data, **kwargs):
    worker = Custom(get_client(module_input_data))
    return await worker.collect_eth_util(**kwargs)


async def smart_organic_swaps(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_organic_swaps()


async def smart_organic_landings(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_organic_landings()


async def swap_eth_to_tia_arb(module_input_data, **kwargs):
    module_input_data["network"] = get_rpc_by_chain_name("Arbitrum")

    worker = Custom(get_client(module_input_data))
    return await worker.swap_tia_arb(**kwargs)


async def swap_tia_to_eth_arb(module_input_data, **kwargs):
    module_input_data["network"] = get_rpc_by_chain_name("Arbitrum")

    worker = Custom(get_client(module_input_data))
    return await worker.swap_tia_arb(reverse=True, **kwargs)


async def swap_eth_to_ezeth(module_input_data, **kwargs):
    worker = Custom(get_client(module_input_data))
    return await worker.swap_ezeth(**kwargs)


async def swap_ezeth_to_eth(module_input_data, **kwargs):
    worker = Custom(get_client(module_input_data))
    return await worker.swap_ezeth(reverse=True, **kwargs)


async def add_liquidity_ambient(module_input_data):
    module_input_data["network"] = ScrollRPC
    worker = Custom(get_client(module_input_data))
    return await worker.ambient_wrseth_scroll()


async def remove_liquidity_ambient(module_input_data):
    module_input_data["network"] = ScrollRPC
    worker = Custom(get_client(module_input_data))
    return await worker.ambient_wrseth_scroll(reverse=True)


async def swap_bnb_to_zbc_bsc(module_input_data, **kwargs):
    module_input_data["network"] = get_rpc_by_chain_name('BNB Chain')

    worker = Custom(get_client(module_input_data))
    return await worker.swap_zbc_bsc(**kwargs)


async def swap_zbc_to_bnb_bsc(module_input_data, **kwargs):
    module_input_data["network"] = get_rpc_by_chain_name('BNB Chain')

    worker = Custom(get_client(module_input_data))
    return await worker.swap_zbc_bsc(reverse=True, **kwargs)


async def swap_eth_to_tia_manta(module_input_data, **kwargs):
    module_input_data["network"] = get_rpc_by_chain_name('Manta')

    worker = Custom(get_client(module_input_data))
    return await worker.swap_tia_manta(**kwargs)


async def swap_tia_to_eth_manta(module_input_data, **kwargs):
    module_input_data["network"] = get_rpc_by_chain_name('Manta')

    worker = Custom(get_client(module_input_data))
    return await worker.swap_tia_manta(reverse=True, **kwargs)


async def smart_swap_in_for_bridging(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_swap_for_bridging()


async def smart_swap_out_for_bridging(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_swap_for_bridging(reverse=True)


async def full_custom_swap1(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.custom_swap(custom_type=1)


async def full_custom_swap2(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.custom_swap(custom_type=2)


async def full_custom_swap3(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.custom_swap(custom_type=3)


async def wrap_abuser(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.wraps_abuser()


async def collector_eth(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.collector_eth()


async def refuel_nautilus(module_input_data):
    module_input_data["network"] = get_rpc_by_chain_name('BNB Chain')

    worker = Custom(get_client(module_input_data))
    return await worker.refuel_nautilus()


async def swap_traderjoe(current_client, **kwargs):
    worker = TraderJoeXyz(current_client)
    return await worker.swap(**kwargs)


async def make_balance_to_average(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.balance_average()


async def bridge_usenexus(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge_omnichain(dapp_id=1)


async def bridge_hyperlane_merkly(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge_omnichain(dapp_id=2)


async def bridge_inevm(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge_omnichain(dapp_id=3)


async def bridge_nautilus(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge_omnichain(dapp_id=4)


async def bridge_stargate(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge_omnichain(dapp_id=5)


async def bridge_debridge(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge_omnichain(dapp_id=6)


async def bridge_jumper(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge_omnichain(dapp_id=7)


async def bridge_squidrouter(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge_omnichain(dapp_id=8)


async def bridge_rango(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge_omnichain(dapp_id=9)


async def bridge_renzo(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge_omnichain(dapp_id=10)


async def bridge_superform(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_bridge_superform()


async def withdraw_superform(module_input_data):
    worker = Superform(get_client(module_input_data))
    return await worker.withdraw()


async def swap_jumper(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_swaps(dapp_id=1)


async def swap_debridge(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_swaps(dapp_id=2)


async def swap_squidrouter(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.smart_swaps(dapp_id=3)


async def swap_jumper_custom(current_client, **kwargs):
    worker = Jumper(current_client)
    return await worker.bridge(**kwargs)


async def okx_withdraw_util(current_client, **kwargs):
    worker = OKX(current_client)
    return await worker.withdraw(**kwargs)


async def bingx_withdraw_util(current_client, **kwargs):
    worker = BingX(current_client)
    return await worker.withdraw(**kwargs)


async def binance_withdraw_util(current_client, **kwargs):
    worker = Binance(current_client)
    return await worker.withdraw(**kwargs)


async def bitget_withdraw_util(current_client, **kwargs):
    worker = Bitget(current_client)
    return await worker.withdraw(**kwargs)


async def bingx_transfer(module_input_data):
    worker = BingX(get_client(module_input_data))
    return await worker.withdraw(transfer_mode=True)


async def claim_rewards_bungee(module_input_data):
    module_input_data["network"] = get_rpc_by_chain_name('Arbitrum')
    worker = Bungee(get_client(module_input_data))
    return await worker.claim_rewards()


async def claim_op_across(module_input_data):
    module_input_data["network"] = get_rpc_by_chain_name('Optimism')
    worker = Across(get_client(module_input_data))
    return await worker.claim_rewards()


async def rhino_recovery_funds(module_input_data):
    worker = Rhino(get_client(module_input_data))
    return await worker.recovery_funds()


async def mint_jumper(module_input_data):
    module_input_data["network"] = BaseRPC
    worker = Jumper(get_client(module_input_data))
    return await worker.mint_jumper()


async def claim_task1_jumper(module_input_data):
    module_input_data["network"] = BaseRPC
    worker = Jumper(get_client(module_input_data))
    return await worker.claim_task_1()


async def claim_task2_jumper(module_input_data):
    module_input_data["network"] = BaseRPC
    worker = Jumper(get_client(module_input_data))
    return await worker.claim_task_2()


async def custom_sleep1(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.custom_sleep(sleep_type=1)


async def custom_sleep2(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.custom_sleep(sleep_type=2)


async def custom_sleep3(module_input_data):
    worker = Custom(get_client(module_input_data))
    return await worker.custom_sleep(sleep_type=3)


async def mint_dbk(module_input_data):
    module_input_data["network"] = DbkRPC
    worker = DBK(get_client(module_input_data))
    return await worker.mint()


async def mint_squid_scholar_nft(module_input_data):
    module_input_data["network"] = ArbitrumRPC
    worker = SquidRouter(get_client(module_input_data))
    return await worker.mint()


async def mint_stix_pass(module_input_data):
    module_input_data["network"] = BaseRPC
    worker = Stix(get_client(module_input_data))
    return await worker.mint_pass()
