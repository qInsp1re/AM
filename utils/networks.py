class NetworkRPC:
    def __init__(
            self,
            name: str,
            rpc: list,
            chain_id: int | str,
            eip1559_support: bool,
            token: str,
            explorer: str,
            decimals: int = 18
    ):
        self.name = name
        self.rpc = rpc
        self.chain_id = chain_id
        self.eip1559_support = eip1559_support
        self.token = token
        self.explorer = explorer
        self.decimals = decimals

    def __repr__(self):
        return f'{self.name}'


CosmosRPC = NetworkRPC(
    name='Cosmos',
    rpc=[
        'https://cosmos-grpc.publicnode.com:443',
    ],
    chain_id='cosmoshub-4',
    eip1559_support=True,
    token='uatom',
    explorer='https://era.zksync.network/',
)

SolanaRPC = NetworkRPC(
    name='Solana',
    rpc=[
        'https://mainnet.helius-rpc.com/?api-key=6ef7a874-4198-4317-b1c6-22f875ec7efc',
    ],
    chain_id=7565164,
    eip1559_support=False,
    token='SOL',
    explorer='https://solscan.io/',
)

NautilusRPC = NetworkRPC(
    name='Nautilus',
    rpc=[
        'https://22222.rpc.thirdweb.com',
    ],
    chain_id=22222,
    eip1559_support=False,
    token='ZBC',
    explorer='https://nautscan.com/',
)

OsmosisRPC = NetworkRPC(
    name='Osmo',
    rpc=[
        'https://osmosis-grpc.publicnode.com:443',
    ],
    chain_id="osmosis-1",
    eip1559_support=False,
    token='uosmo',
    explorer='https://www.mintscan.io/osmosis/',
)

CelestiaRPC = NetworkRPC(
    name='Celestia',
    rpc=[
        #'https://grpc.celestia.nodestake.top',
        #'https://celestia-grpc.chainode.tech:443',
        'https://celestia.grpc.kjnodes.com:443',
        #'https://grpc.lunaroasis.net:443',
    ],
    chain_id='celestia',
    eip1559_support=True,
    token='utia',
    explorer='https://celenium.io/',
)

NeutronRPC = NetworkRPC(
    name='Neutron',
    rpc=[
        'https://neutron-grpc.publicnode.com:443',
        #'https://neutron-grpc.lavenderfive.com:443',
    ],
    chain_id='neutron-1',
    eip1559_support=True,
    token='untrn',
    explorer='https://neutron.celat.one/neutron-1/',
)

INJ_RPC = NetworkRPC(
    name='Injective',
    rpc=[
        'https://sentry.chain.grpc.injective.network:443',
    ],
    chain_id='injective-1',
    eip1559_support=True,
    token='inj',
    explorer='https://explorer.injective.network/',
)

zkSyncEraRPC = NetworkRPC(
    name='zkSync',
    rpc=[
        'https://mainnet.era.zksync.io',
    ],
    chain_id=324,
    eip1559_support=False,
    token='ETH',
    explorer='https://era.zksync.network/',
)

ScrollRPC = NetworkRPC(
    name='Scroll',
    rpc=[
        'https://rpc.scroll.io',
        'https://scroll-mainnet.public.blastapi.io',
        # 'https://rpc.ankr.com/scroll',
    ],
    chain_id=534352,
    eip1559_support=True,
    token='ETH',
    explorer='https://scrollscan.com/'
)

ArbitrumRPC = NetworkRPC(
    name='Arbitrum',
    rpc=[
        'https://arbitrum.llamarpc.com',
    ],
    chain_id=42161,
    eip1559_support=False,
    token='ETH',
    explorer='https://arbiscan.io/',
)


OptimismRPC = NetworkRPC(
    name='Optimism',
    rpc=[
        'https://optimism.llamarpc.com',
        #'https://optimism.drpc.org',
    ],
    chain_id=10,
    eip1559_support=False,
    token='ETH',
    explorer='https://optimistic.etherscan.io/',
)


PolygonRPC = NetworkRPC(
    name='Polygon',
    rpc=[
        'https://polygon-rpc.com',
    ],
    chain_id=137,
    eip1559_support=False,
    token='POL',
    explorer='https://polygonscan.com/',
)


AvalancheRPC = NetworkRPC(
    name='Avalanche',
    rpc=[
        'https://avalanche.drpc.org'
    ],
    chain_id=43114,
    eip1559_support=False,
    token='AVAX',
    explorer='https://snowtrace.io/',
)


EthereumRPC = NetworkRPC(
    name='Ethereum',
    rpc=[
        'https://rpc.ankr.com/eth',
        'https://eth.drpc.org'
    ],
    chain_id=1,
    eip1559_support=False,
    token='ETH',
    explorer='https://etherscan.io/'
)

Arbitrum_novaRPC = NetworkRPC(
    name='Arbitrum Nova',
    rpc=[
        'https://rpc.ankr.com/arbitrumnova',
        'https://arbitrum-nova.publicnode.com',
        'https://arbitrum-nova.drpc.org',
        'https://nova.arbitrum.io/rpc'
    ],
    chain_id=42170,
    eip1559_support=False,
    token='ETH',
    explorer='https://nova.arbiscan.io/'
)

BaseRPC = NetworkRPC(
    name='Base',
    rpc=[
        'https://mainnet.base.org',
    ],
    chain_id=8453,
    eip1559_support=False,
    token='ETH',
    explorer='https://basescan.org/'
)

LineaRPC = NetworkRPC(
    name='Linea',
    rpc=[
        # 'https://linea.drpc.org',
        'https://rpc.linea.build'
    ],
    chain_id=59144,
    eip1559_support=False,
    token='ETH',
    explorer='https://lineascan.build/'
)

ZoraRPC = NetworkRPC(
    name='Zora',
    rpc=[
        'https://rpc.zora.energy'
    ],
    chain_id=7777777,
    eip1559_support=False,
    token='ETH',
    explorer='https://zora.superscan.network/'
)

Polygon_ZKEVM_RPC = NetworkRPC(
    name='Polygon zkEVM',
    rpc=[
        'https://1rpc.io/polygon/zkevm',
        'https://zkevm-rpc.com',
        'https://rpc.ankr.com/polygon_zkevm'
    ],
    chain_id=1101,
    eip1559_support=False,
    token='ETH',
    explorer='https://zkevm.polygonscan.com/'
)

BSC_RPC = NetworkRPC(
    name='BNB Chain',
    rpc=[
        'https://rpc.ankr.com/bsc',
        'https://binance.llamarpc.com',
    ],
    chain_id=56,
    eip1559_support=False,
    token='BNB',
    explorer='https://bscscan.com/'
)

MantaRPC = NetworkRPC(
    name='Manta',
    rpc=[
        'https://pacific-rpc.manta.network/http'
        'https://1rpc.io/manta'
    ],
    chain_id=169,
    eip1559_support=False,
    token='ETH',
    explorer='https://pacific-explorer.manta.network/'
)

MantleRPC = NetworkRPC(
    name='Mantle',
    rpc=[
        'https://mantle.publicnode.com',
        'https://mantle-mainnet.public.blastapi.io',
        'https://mantle.drpc.org',
        'https://rpc.ankr.com/mantle',
    ],
    chain_id=5000,
    eip1559_support=False,
    token='MNT',
    explorer='https://explorer.mantle.xyz/'
)

OpBNB_RPC = NetworkRPC(
    name='OpBNB',
    rpc=[
        'https://opbnb.publicnode.com',
        'https://opbnb-mainnet-rpc.bnbchain.org',
        'https://opbnb-mainnet.nodereal.io/v1/e9a36765eb8a40b9bd12e680a1fd2bc5',
    ],
    chain_id=204,
    eip1559_support=False,
    token='BNB',
    explorer='https://opbnbscan.com/'
)

MoonbeamRPC = NetworkRPC(
    name='Moonbeam',
    rpc=[
        'https://rpc.ankr.com/moonbeam',
        'https://rpc.api.moonbeam.network',
    ],
    chain_id=1284,
    eip1559_support=False,
    token='GLMR',
    explorer='https://moonscan.io/'
)

MoonriverRPC = NetworkRPC(
    name='Moonriver',
    rpc=[
        'https://moonriver.public.blastapi.io',
        'https://moonriver.publicnode.com',
    ],
    chain_id=1285,
    eip1559_support=False,
    token='MOVR',
    explorer='https://moonriver.moonscan.io/'
)


HarmonyRPC = NetworkRPC(
    name='Harmony One',
    rpc=[
        'https://api.harmony.one',
        'https://a.api.s0.t.hmny.io',
        'https://endpoints.omniatech.io/v1/harmony/mainnet-0/public',
        'https://1rpc.io/one',
    ],
    chain_id=1666600000,
    eip1559_support=False,
    token='ONE',
    explorer='https://explorer.harmony.one/'
)

TelosRPC = NetworkRPC(
    name='Telos',
    rpc=[
        'https://mainnet.telos.net/evm',
        'https://rpc1.eu.telos.net/evm',
        'https://rpc1.us.telos.net/evm',
        'https://api.kainosbp.com/evm',
    ],
    chain_id=40,
    eip1559_support=False,
    token='TLOS',
    explorer='https://explorer.telos.net/'
)

CeloRPC = NetworkRPC(
    name='Celo',
    rpc=[
        'https://forno.celo.org',
        'https://rpc.ankr.com/celo',
        'https://1rpc.io/celo',
    ],
    chain_id=42220,
    eip1559_support=False,
    token='CELO',
    explorer='https://explorer.celo.org/mainnet/'
)

GnosisRPC = NetworkRPC(
    name='Gnosis',
    rpc=[
        'https://gnosis.drpc.org',
        'https://1rpc.io/gnosis',
    ],
    chain_id=100,
    eip1559_support=False,
    token='XDAI',
    explorer='https://gnosisscan.io/'
)

CoreRPC = NetworkRPC(
    name='CoreDAO',
    rpc=[
        'https://rpc.ankr.com/core',
        'https://1rpc.io/core',
        'https://rpc.coredao.org',
    ],
    chain_id=1116,
    eip1559_support=False,
    token='CORE',
    explorer='https://scan.coredao.org/'
)

TomoChainRPC = NetworkRPC(
    name='TomoChain',
    rpc=[
        'https://rpc.tomochain.com',
        'https://tomo.blockpi.network/v1/rpc/public',
        'https://viction.blockpi.network/v1/rpc/public',
    ],
    chain_id=88,
    eip1559_support=False,
    token='TOMO',
    explorer='https://tomoscan.io/'
)

ConfluxRPC = NetworkRPC(
    name='Conflux',
    rpc=[
        'https://evm.confluxrpc.com',
    ],
    chain_id=1030,
    eip1559_support=False,
    token='CFX',
    explorer='https://evm.confluxscan.io/'
)

OrderlyRPC = NetworkRPC(
    name='Orderly',
    rpc=[
        'https://l2-orderly-mainnet-0.t.conduit.xyz',
        'https://rpc.orderly.network',
    ],
    chain_id=291,
    eip1559_support=False,
    token='ETH',
    explorer='https://explorer.orderly.network/'
)

HorizenRPC = NetworkRPC(
    name='Horizen EON',
    rpc=[
        'https://rpc.ankr.com/horizen_eon',
        'https://eon-rpc.horizenlabs.io/ethv1',
    ],
    chain_id=7332,
    eip1559_support=False,
    token='ZEN',
    explorer='https://explorer.horizen.io/'
)

MetisRPC = NetworkRPC(
    name='Metis',
    rpc=[
        'https://metis-mainnet.public.blastapi.io',
        'https://metis-pokt.nodies.app',
        'https://andromeda.metis.io/?owner=1088'
    ],
    chain_id=1088,
    eip1559_support=False,
    token='METIS',
    explorer='https://explorer.metis.io/'
)

AstarRPC = NetworkRPC(
    name='Astar',
    rpc=[
        'https://evm.astar.network',
        'https://astar.public.blastapi.io',
        'https://1rpc.io/astr',
        'https://astar-rpc.dwellir.com'
    ],
    chain_id=592,
    eip1559_support=False,
    token='ASTR',
    explorer='https://astar.blockscout.com/'
)

KavaRPC = NetworkRPC(
    name='Kava',
    rpc=[
        #'https://kava-pokt.nodies.app',
        'https://evm.kava.io',
    ],
    chain_id=2222,
    eip1559_support=False,
    token='KAVA',
    explorer='https://kavascan.com/'
)

KlaytnRPC = NetworkRPC(
    name='Klaytn',
    rpc=[
        'https://rpc.ankr.com/klaytn',
        'https://klaytn.drpc.org',
    ],
    chain_id=8217,
    eip1559_support=False,
    token='KLAY',
    explorer='https://klaytnscope.com/'
)

FantomRPC = NetworkRPC(
    name='Fantom',
    rpc=[
        'https://rpc.ankr.com/fantom',
    ],
    chain_id=250,
    eip1559_support=False,
    token='FTM',
    explorer='https://ftmscan.com/'
)

AuroraRPC = NetworkRPC(
    name='Aurora',
    rpc=[
        'https://mainnet.aurora.dev',
        'https://endpoints.omniatech.io/v1/aurora/mainnet/public',
        'https://1rpc.io/aurora',
        'https://aurora.drpc.org'
    ],
    chain_id=1313161554,
    eip1559_support=False,
    token='ETH',
    explorer='https://explorer.aurora.dev/'
)

CantoRPC = NetworkRPC(
    name='Canto',
    rpc=[
        'https://canto.gravitychain.io',
        'https://jsonrpc.canto.nodestake.top',
        'https://mainnode.plexnode.org:8545',
        'https://canto.slingshot.finance'
    ],
    chain_id=7700,
    eip1559_support=False,
    token='CANTO',
    explorer='https://cantoscan.com/'
)

DFK_RPC = NetworkRPC(
    name='DFK',
    rpc=[
        'https://avax-pokt.nodies.app/ext/bc/q2aTwKuyzgs8pynF7UXBZCU7DejbZbZ6EUyHr3JQzYgwNPUPi/rpc',
        'https://dfkchain.api.onfinality.io/public',
        'https://mainnode.plexnode.org:8545',
        'https://subnets.avax.network/defi-kingdoms/dfk-chain/rpc'
    ],
    chain_id=53935,
    eip1559_support=False,
    token='JEWEL',
    explorer='https://avascan.info/blockchain/dfk'
)

FuseRPC = NetworkRPC(
    name='Fuse',
    rpc=[
        'https://rpc.fuse.io',
        'https://fuse-pokt.nodies.app',
        'https://fuse.liquify.com',
        'https://fuse.api.onfinality.io/public'
    ],
    chain_id=122,
    eip1559_support=False,
    token='FUSE',
    explorer='https://cantoscan.com/'
)

GoerliRPC = NetworkRPC(
    name='Goerli',
    rpc=[
        'https://endpoints.omniatech.io/v1/eth/goerli/public',
        'https://rpc.ankr.com/eth_goerli',
        'https://eth-goerli.public.blastapi.io',
        'https://goerli.blockpi.network/v1/rpc/public'
    ],
    chain_id=5,
    eip1559_support=False,
    token='ETH',
    explorer='https://goerli.etherscan.io/'
)

MeterRPC = NetworkRPC(
    name='Meter',
    rpc=[
        'https://rpc.meter.io',
        'https://rpc-meter.jellypool.xyz',
        'https://meter.blockpi.network/v1/rpc/public',
    ],
    chain_id=82,
    eip1559_support=False,
    token='MTR',
    explorer='https://scan.meter.io/'
)

OKX_RPC = NetworkRPC(
    name='OKX Chain',
    rpc=[
        'https://exchainrpc.okex.org',
        'https://oktc-mainnet.public.blastapi.io',
        'https://1rpc.io/oktc',
        'https://okt-chain.api.onfinality.io/public'
    ],
    chain_id=66,
    eip1559_support=False,
    token='OKT',
    explorer='https://www.oklink.com/ru/oktc'
)

ShimmerRPC = NetworkRPC(
    name='Shimmer',
    rpc=[
        'https://json-rpc.evm.shimmer.network',
    ],
    chain_id=148,
    eip1559_support=False,
    token='SMR',
    explorer='https://explorer.shimmer.network/'
)

TenetRPC = NetworkRPC(
    name='Tenet',
    rpc=[
        'https://rpc.tenet.org',
        'https://tenet-evm.publicnode.com',
    ],
    chain_id=1559,
    eip1559_support=False,
    token='TENET',
    explorer='https://tenetscan.io/'
)

XPLA_RPC = NetworkRPC(
    name='XPLA',
    rpc=[
        'https://dimension-evm-rpc.xpla.dev	',
    ],
    chain_id=37,
    eip1559_support=False,
    token='XPLA',
    explorer='https://explorer.xpla.io/'
)

LootChainRPC = NetworkRPC(
    name='LootChain',
    rpc=[
        'https://rpc.lootchain.com/http',
    ],
    chain_id=5151706,
    eip1559_support=False,
    token='AGLD',
    explorer='https://explorer.lootchain.com/'
)

ZKFairRPC = NetworkRPC(
    name='ZKFair',
    rpc=[
        'https://rpc.zkfair.io',
        'https://zkfair.rpc.thirdweb.com',
    ],
    chain_id=42766,
    eip1559_support=False,
    token='USDC',
    explorer='https://scan.zkfair.io/'
)

BeamRPC = NetworkRPC(
    name='Beam',
    rpc=[
        'https://subnets.avax.network/beam/mainnet/rpc'
    ],
    chain_id=4337,
    eip1559_support=False,
    token='Beam',
    explorer='https://4337.snowtrace.io/'
)

InEVM_RPC = NetworkRPC(
    name='InEVM',
    rpc=[
        'https://inevm.calderachain.xyz/http'
    ],
    chain_id=2525,
    eip1559_support=False,
    token='INJ',
    explorer='https://inevm.calderaexplorer.xyz/'
)

BlastRPC = NetworkRPC(
    name='Blast',
    rpc=[
        'https://rpc.blast.io',
        'https://rpc.ankr.com/blast'
    ],
    chain_id=81457,
    eip1559_support=False,
    token='ETH',
    explorer='https://blastscan.io/'
)

ModeRPC = NetworkRPC(
    name='Mode',
    rpc=[
        'https://1rpc.io/mode',
    ],
    chain_id=34443,
    eip1559_support=False,
    token='ETH',
    explorer='https://explorer.mode.network/'
)


RaribleRPC = NetworkRPC(
    name='Rarible',
    rpc=[
        ''
    ],
    chain_id=0,
    eip1559_support=False,
    token='',
    explorer=''
)

xLayerRPC = NetworkRPC(
    name='xLayer',
    rpc=[
        'https://rpc.xlayer.tech'
    ],
    chain_id=196,
    eip1559_support=False,
    token='OKB',
    explorer='https://www.oklink.com/ru/xlayer/'
)

TaikoRPC = NetworkRPC(
    name='Taiko',
    rpc=[
        'https://rpc.taiko.xyz'
    ],
    chain_id=167000,
    eip1559_support=False,
    token='ETH',
    explorer='https://taikoscan.io/'
)

DbkRPC = NetworkRPC(
    name='DBK Chain',
    rpc=[
        'https://rpc.mainnet.dbkchain.io'
    ],
    chain_id=20240603,
    eip1559_support=False,
    token='ETH',
    explorer='https://scan.dbkchain.io/'
)

GravityRPC = NetworkRPC(
    name='Gravity',
    rpc=[
        'https://rpc.gravity.xyz'
    ],
    chain_id=1625,
    eip1559_support=False,
    token='G',
    explorer='https://explorer.gravity.xyz/'
)

# zkSyncLite = Network(
#     name='zksync_lite',
#     rpc=[],
#     chain_id=0,
#     eip1559_support=True,
#     token='ETH',
#     explorer='https://zkscan.io/'
# )
