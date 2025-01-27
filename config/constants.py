from utils.tools import get_accounts_data

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

ETH_MASK = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

NATIVE_CONTRACTS_PER_CHAIN = {
    'zkSync': {
        'deposit'           : '0x32400084C286CF3E17e7B677ea9583e60a000324',
        'withdraw'          : '0x000000000000000000000000000000000000800A',
        'contact_deployer'  : '0x0000000000000000000000000000000000008006'
    },
    'Starknet': {
        "evm_contract"       : "0xae0Ee0A63A2cE6BaeEFFE56e7714FB4EFE48D419",
        "stark_contract"     :  0x073314940630fd6dcda0d772d4c972c4e0a9946bef9dabf4ef84eda8ef542b82,
    },
    'Scroll':{
        "deposit"            : "0xF8B1378579659D8F7EE5f3C929c2f3E332E41Fd6",
        "withdraw"           : "0x4C0926FF5252A435FD19e10ED15e5a249Ba19d79",
        "oracle"             : "0x987e300fDfb06093859358522a79098848C33852"
    },
    'Base':{
        "deposit"            : "0x49048044D57e1C92A77f79988d21Fa8fAF74E97e",
        "withdraw"           : "0x4200000000000000000000000000000000000016"
    },
    'Linea':{
        "deposit"            : "0xd19d4B5d358258f05D7B411E21A1460D11B0876F",
        "withdraw"           : "0x508Ca82Df566dCD1B0DE8296e70a96332cD644ec"
    },
    'Arbitrum Nova':{
        "deposit"            : "0x",
        "withdraw"           : "0x"
    },
    'Zora':{
        "deposit"            : "0x",
        "withdraw"           : "0x"
    }
}


ACROSS_CLAIM_CONTRACTS = {
    'Optimism': '0xc8b31410340d57417be62672f6b53dfb9de30ac2'
}

ACROSS_CONTRACT = {
    'Arbitrum'              : '0x269727F088F16E1Aea52Cf5a97B1CD41DAA3f02D',
    'Optimism'              : '0x269727F088F16E1Aea52Cf5a97B1CD41DAA3f02D',
    'Base'                  : '0x269727F088F16E1Aea52Cf5a97B1CD41DAA3f02D',
    'Etherium'              : '0x269727F088F16E1Aea52Cf5a97B1CD41DAA3f02D',
    'Polygon'               : '0x9295ee1d8C5b022Be115A2AD3c30C72E34e7F096',
}

APERTURE_CONTRACTS = {
    'Manta': {
        'router': '0x3488d5A2D0281f546e43435715C436b46Ec1C678',
        'quoter': '0x000000000d44011EACAB39AB7965687d0bc2B16A'
    }
}

MAVERICK_CONTRACTS = {
    'zkSync':{
        "router"                : '0x39E098A153Ad69834a9Dac32f0FCa92066aD03f4',
        "pool_information"      : '0x57D47F505EdaA8Ae1eFD807A860A79A28bE06449',
        "position"              : '0xFd54762D435A490405DDa0fBc92b7168934e8525',
        "position_inspector"    : '0x852639EE9dd090d30271832332501e87D287106C',
        "ETH-USDC"              : '0x41C8cf74c27554A8972d3bf3D2BD4a14D8B604AB',
        "BUSD-USDC"             : '0x45E24D7B0C780cc78b42A1D1750E70e0f6d8Bb2d',
        "BUSD-ETH"              : '0x3Ae63FB198652E294B8DE4C2EF659D95D5ff28BE',
        "ETH-MAV"               : '0x4D47167e66e86d1a1083f52136832d4f1eF5809A',
        "USDC-MAV"              : '0xBf90Be5BBc07fbf548D3bCeED34F1D471c018f34',
        "BUSD-MAV"              : '0x9f4A993b3120e52044810F1c91088a5630a8bF63',
    },
    'Base':{
        "router"                : '0x32AED3Bce901DA12ca8489788F3A99fCe1056e14',
        "pool_information"      : '0x6E230D0e457Ea2398FB3A22FB7f9B7F68F06a14d',
        "position"              : '0x0d8127A01bdb311378Ed32F5b81690DD917dBa35',
        "position_inspector"    : '0x550056A68cB155b6Cc3DeF4A7FA656260e7842e2',
        "DAI-USDC.e"            : "0xdcC8A6bA71A6C0053cBB32F935e9B4B64d465ea3",
        "cbETH-ETH"             : "0x2CeBCF66F023AA88003593804504a8DF882D12E6",
        "ETH-USDC.e"            : "0x06e6736cA9e922766279A22b75A600Fe8B8473B6",
        "DAI-USDC"              : "0x1B55d94B553475e7561fab889bf88Fe4f491D29c",
        "ETH-USDC"              : "0x3D70b2F31F75dC84acDd5e1588695221959b2d37",
        "ETH-MAV"               : "0xE401e8Bb08d1104A7F4c70C6Ec58F6f21DCbd941",
        "ETH-DAI"               : "0x5BDb08Ae195C8F085704582A27D566028A719265"

    }
}

THRUSTER_CONTRACTS = {
    'Blast':{
        'router'                : '0x337827814155ECBf24D20231fCA4444F530C0555',
    }
}

SYNCSWAP_CONTRACTS = {
    'zkSync':{
        "paymaster"             : '0x0c08f298A75A090DC4C0BB4CaA4204B8B9D156c1',
        "router"                : "0x9B5def958d0f3b6955cBEa4D5B7809b2fb26b059",
        "classic_pool_factory"  : '0xf2DAd89f2788a8CD54625C60b55cD3d2D0ACa7Cb'
    },
    'Scroll':{
        "router"                : '0x80e38291e06339d10AAB483C65695D004dBD5C69',
        "classic_pool_factory"  : '0x37BAc764494c8db4e54BDE72f6965beA9fa0AC2d'
    },
    'Linea':{
        "router"                : '0x80e38291e06339d10AAB483C65695D004dBD5C69',
        "classic_pool_factory"  : '0x37BAc764494c8db4e54BDE72f6965beA9fa0AC2d'
    }
}

OWLTO_CONTRACT = {
    'zkSync':{
        'check_in': '0xD48e3caf0D948203434646a3f3e80f8Ee18007dc'
    },
    'Scroll': {
        'check_in': '0xE6FEcA764B7548127672C189D303eb956c3Ba372'
    },
    'Linea': {
        'check_in': '0xd7487D1ff3b2433B32E6d4c333F70A462B99F300'
    },
    'Blast': {
        'check_in': '0xEff847da094d82f852cF4c2678e28fA39285DBfe'
    },
    'Manta': {
        'check_in': '0x6977c769391BBf0C45286F78B056Ff3B54830270'
    },
    'BNB Chain': {
        'check_in': '0x872Fc5fEd2d1261ABa4e234a47F473c9a3da2724'
    },
    'Base': {
        'check_in': '0x26637c9fDbD5Ecdd76a9E21Db7ea533e1B0713b6'
    }
}

BEBOP_CONTRACTS = {
    'Taiko': {
        'router': '0xbbbbbBB520d69a9775E85b458C58c648259FAD5F'
    }
}

QUICKSWAP_CONTRACTS = {
    'Polygon zkEVM': {
        "router": "0xF6Ad3CcF71Abb3E12beCf6b3D2a74C963859ADCd",
        "quoter": "0x55BeE1bD3Eb9986f6d2d963278de09eE92a3eF1D",
    }
}

STARGATE_CONTRACTS = {
    'Ethereum': {
        'router': '0x8731d54E9D02c286767d56ac03e8037C07e01e98',
        'router_eth': '0x77b2043768d28E9C9aB44E1aBfC95944bcE57931',
        'router_usdc': '0xc026395860Db2d07ee33e05fE50ed7bD583189C7',
        'router_usdt': '0x933597a323Eb81cAe705C5bC29985172fd5A3973',
        'router_eth_backend': '0xb1b2eeF380f21747944f46d28f683cD1FBB4d03c',
        'bridge': '0x296F55F8Fb28E498B858d0BcDA06D955B2Cb3f97',
        'factory': '0x06D538690AF257Da524f25D0CD52fD85b1c2173E',
        'stg_token': '0xAf5191B0De278C7286d6C7CC6ab6BB8A73bA2Cd6',
        'fee_library': '0x8C3085D9a554884124C998CDB7f6d7219E9C1e6F',
        'composer': '0xeCc19E177d24551aA7ed6Bc6FE566eCa726CC8a9',
        'widget_swap': '0x10d16248bED1E0D0c7cF94fFD99A50c336c7Bcdc',
        'ETH': '0x101816545F6bd2b1076434B54383a1E633390A2E',
        'USDC': '0xdf0770dF86a8034b3EFEf0A1Bb3c889B8332FF56',
        'USDT': '0x38EA452219524Bb87e18dE1C24D3bB59510BD783',
        'USDD': '0x692953e758c3669290cb1677180c64183cEe374e',
        'DAI': '0x0Faf1d2d3CED330824de3B8200fc8dc6E397850d',
        'FRAX': '0xfA0F307783AC21C39E939ACFF795e27b650F6e68',
        'sUSD': '0x590d4f8A68583639f215f675F3a259Ed84790580',
        'LUSD': '0xE8F55368C82D38bbbbDb5533e7F56AfC2E978CC2',
        'MAI': '0x9cef9a0b1bE0D289ac9f4a98ff317c33EAA84eb8',
        'METIS': '0xd8772edBF88bBa2667ed011542343b0eDDaCDa47',
        'metis.USDT': '0x430Ebff5E3E80A6C58E7e6ADA1d90F5c28AA116d',
        'lp_staking': '0xB0D502E938ed5f4df2E681fE6E419ff29631d62b',
        'lp_staking_time_metis': '0x1c3000b8f475A958b87c73a5cc5780Ab763122FC',
    },
    'BNB Chain': {
        'router': '0x4a364f8c717cAAD9A442737Eb7b8A55cc6cf18D8',
        'router_usdt': '0x138EB30f73BC423c6455C53df6D89CB01d9eBc63',
        'bridge': '0x6694340fc020c5E6B96567843da2df01b2CE1eb6',
        'factory': '0xe7Ec689f432f29383f217e36e680B5C855051f25',
        'stg_token': '0xB0D502E938ed5f4df2E681fE6E419ff29631d62b',
        'fee_library':'0xCA6522116e8611A346D53Cc2005AC4192e3fc2BC',
        'composer': '0xeCc19E177d24551aA7ed6Bc6FE566eCa726CC8a9',
        'widget_swap': '0x10d16248bED1E0D0c7cF94fFD99A50c336c7Bcdc',
        'USDT': '0x9aA83081AA06AF7208Dcc7A4cB72C94d057D2cda',
        'BUSD': '0x98a5737749490856b401DB5Dc27F522fC314A4e1',
        'USDD': '0x4e145a589e4c03cBe3d28520e4BF3089834289Df',
        'MAI': '0x7BfD7f2498C4796f10b6C611D9db393D3052510C',
        'METIS': '0xD4CEc732b3B135eC52a3c0bc8Ce4b8cFb9dacE46',
        'metis.USDT': '0x68C6c27fB0e02285829e69240BE16f32C5f8bEFe',
        'lp_staking': '0x3052A0F6ab15b4AE1df39962d5DdEFacA86DaB47',
        'lp_staking_time_metis': '0x2c6dcEd426D265045737Ff55C2D746C11b2F457a',
        'otf_wrapper': '0x86355F02119bdBC28ED6A4D5E0cA327Ca7730fFF',
    },
    'Avalanche':{
        'router': '0x45A01E4e04F14f7A4a6702c74187c5F6222033cd',
        'router_usdc': '0x5634c4a5FEd09819E3c46D86A965Dd9447d86e47',
        'router_usdt': '0x12dC9256Acc9895B076f6638D628382881e62CeE',
        'bridge': '0x9d1B1669c73b033DFe47ae5a0164Ab96df25B944',
        'factory': '0x808d7c71ad2ba3FA531b068a2417C63106BC0949',
        'stg_token': '0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590',
        'fee_library': '0x5E8eC15ACB5Aa94D5f0589E54441b31c5e0B992d',
        'composer': '0xeCc19E177d24551aA7ed6Bc6FE566eCa726CC8a9',
        'widget_swap': '0x10d16248bED1E0D0c7cF94fFD99A50c336c7Bcdc',
        'USDC': '0x1205f31718499dBf1fCa446663B532Ef87481fe1',
        'USDT': '0x29e38769f23701A2e4A8Ef0492e19dA4604Be62c',
        'FRAX': '0x1c272232Df0bb6225dA87f4dEcD9d37c32f63Eea',
        'MAI': '0x8736f92646B2542B3e5F3c63590cA7Fe313e283B',
        'metis.USDT': '0xEAe5c2F6B25933deB62f754f239111413A0A25ef',
        'lp_staking': '0x8731d54E9D02c286767d56ac03e8037C07e01e98',
    },
    'Polygon': {
        'router': '0x45A01E4e04F14f7A4a6702c74187c5F6222033cd',
        'router_usdc': '0x9Aa02D4Fae7F58b8E8f34c66E756cC734DAc7fe4',
        'router_usdt': '0xd47b03ee6d86Cf251ee7860FB2ACf9f91B9fD4d7',
        'bridge': '0x9d1B1669c73b033DFe47ae5a0164Ab96df25B944',
        'factory': '0x808d7c71ad2ba3FA531b068a2417C63106BC0949',
        'stg_token': '0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590',
        'fee_library': '0xb279b324Ea5648bE6402ABc727173A225383494C',
        'composer': '0xeCc19E177d24551aA7ed6Bc6FE566eCa726CC8a9',
        'widget_swap': '0x10d16248bED1E0D0c7cF94fFD99A50c336c7Bcdc',
        'USDC': '0x1205f31718499dBf1fCa446663B532Ef87481fe1',
        'USDT': '0x29e38769f23701A2e4A8Ef0492e19dA4604Be62c',
        'DAI': '0x1c272232Df0bb6225dA87f4dEcD9d37c32f63Eea',
        'MAI': '0x8736f92646B2542B3e5F3c63590cA7Fe313e283B',
        'lp_staking': '0x8731d54E9D02c286767d56ac03e8037C07e01e98',
    },
    'Arbitrum': {
        'router': '0x53Bf833A5d6c4ddA888F69c22C88C9f356a41614',
        'router_eth': '0xA45B5130f36CDcA45667738e2a258AB09f4A5f7F',
        'router_usdc': '0xe8CDF27AcD73a434D661C84887215F7598e7d0d3',
        'router_usdt': '0xcE8CcA271Ebc0533920C83d39F417ED6A0abB7D0',
        'router_eth_backend':  '0xb1b2eeF380f21747944f46d28f683cD1FBB4d03c',
        'bridge': '0x352d8275AAE3e0c2404d9f68f6cEE084B5bEB3DD',
        'factory': '0x55bDb4164D28FBaF0898e0eF14a589ac09Ac9970',
        'stg_token': '0x6694340fc020c5E6B96567843da2df01b2CE1eb6',
        'fee_library':'0x1cF31666c06ac3401ed0C1c6346C4A9425dd7De4',
        'composer': '0xeCc19E177d24551aA7ed6Bc6FE566eCa726CC8a9',
        'widget_swap': '0x10d16248bED1E0D0c7cF94fFD99A50c336c7Bcdc',
        'ETH': '0x915A55e36A01285A14f05dE6e81ED9cE89772f8e',
        'USDC': '0x892785f33CdeE22A30AEF750F285E18c18040c3e',
        'USDT': '0xB6CfcF89a7B22988bfC96632aC2A9D6daB60d641',
        'FRAX': '0xaa4BF442F024820B2C28Cd0FD72b82c63e66F56C',
        'MAI': '0xF39B7Be294cB36dE8c510e267B82bb588705d977',
        'LUSD': '0x600E576F9d853c95d58029093A16EE49646F3ca5',
        'lp_staking_time': '0x9774558534036Ff2E236331546691b4eB70594b1',
    },
    'Optimism':{
        'router': '0xB0D502E938ed5f4df2E681fE6E419ff29631d62b',
        'router_eth': '0xe8CDF27AcD73a434D661C84887215F7598e7d0d3',
        'router_usdc': '0xcE8CcA271Ebc0533920C83d39F417ED6A0abB7D0',
        'router_usdt': '0x19cFCE47eD54a88614648DC3f19A5980097007dD',
        'router_eth_backend': '0xb1b2eeF380f21747944f46d28f683cD1FBB4d03c',
        'bridge': '0x701a95707A0290AC8B90b3719e8EE5b210360883',
        'factory': '0xE3B53AF74a4BF62Ae5511055290838050bf764Df',
        'stg_token': '0x296F55F8Fb28E498B858d0BcDA06D955B2Cb3f97',
        'fee_library': '0x505eCDF2f14Cd4f1f413d04624b009A449D38D7E',
        'composer': '0xeCc19E177d24551aA7ed6Bc6FE566eCa726CC8a9',
        'widget_swap': '0x10d16248bED1E0D0c7cF94fFD99A50c336c7Bcdc',
        'ETH': '0xd22363e3762cA7339569F3d33EADe20127D5F98C',
        'USDC': '0xDecC0c09c3B5f6e92EF4184125D5648a66E35298',
        'DAI': '0x165137624F1f692e69659f944BF69DE02874ee27',
        'FRAX': '0x368605D9C6243A80903b9e326f1Cddde088B8924',
        'sUSD': '0x2F8bC9081c7FCFeC25b9f41a50d97EaA592058ae',
        'LUSD': '0x3533F5e279bDBf550272a199a223dA798D9eff78',
        'MAI': '0x5421FA1A48f9FF81e4580557E86C7C0D24C18036',
        'lp_staking_time': '0x4DeA9e918c6289a52cd469cAC652727B7b412Cd2',
    },
    'Fantom':{
        'router': '0xAf5191B0De278C7286d6C7CC6ab6BB8A73bA2Cd6',
        'bridge': '0x45A01E4e04F14f7A4a6702c74187c5F6222033cd',
        'factory': '0x9d1B1669c73b033DFe47ae5a0164Ab96df25B944',
        'stg_token': '0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590',
        'fee_library': '0x616a68BD6DAd19e066661C7278611487d4072839',
        'composer': '0xeCc19E177d24551aA7ed6Bc6FE566eCa726CC8a9',
        'widget_swap': '0x10d16248bED1E0D0c7cF94fFD99A50c336c7Bcdc',
        'USDC': '0xc647ce76ec30033aa319d472ae9f4462068f2ad7',
        'lp_staking': '0x224D8Fd7aB6AD4c6eb4611Ce56EF35Dec2277F03',
    },
    'zkSync':{
        'otf_wrapper': '0xDAc7479e5F7c01CC59bbF7c1C4EDF5604ADA1FF2',
        'MAV': '0x787c09494Ec8Bcb24DcAf8659E7d5D69979eE508',
    },
    'Metis':{
        'router': '0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590',
        'router_eth': '0x36ed193dc7160D3858EC250e69D12B03Ca087D08',
        'router_usdt': '0x4dCBFC0249e8d5032F89D6461218a9D2eFff5125',
        'bridge': '0x45f1A95A4D3f3836523F5c83673c797f4d4d263B',
        'factory': '0xAF54BE5B6eEc24d6BFACf1cce4eaF680A8239398',
        'stg_token': '',
        'fee_library': '0x55bDb4164D28FBaF0898e0eF14a589ac09Ac9970',
        'composer': '0xeCc19E177d24551aA7ed6Bc6FE566eCa726CC8a9',
        'widget_swap': '0x10d16248bED1E0D0c7cF94fFD99A50c336c7Bcdc',
        'METIS': '0xAad094F6A75A14417d39f04E690fC216f080A41a',
        'm.USDT': '0x2b60473a7C41Deb80EDdaafD5560e963440eb632',
        'lp_staking_time_metis': '0x45A01E4e04F14f7A4a6702c74187c5F6222033cd',
    },
    'Base':{
        'router': '0x45f1A95A4D3f3836523F5c83673c797f4d4d263B',
        'router_eth': '0xdc181Bd607330aeeBEF6ea62e03e5e1Fb4B6F7C7',
        'router_usdc': '0x27a16dc786820B16E5c9028b75B99F6f604b5d26',
        'bridge': '0xAF54BE5B6eEc24d6BFACf1cce4eaF680A8239398',
        'factory': '0xAf5191B0De278C7286d6C7CC6ab6BB8A73bA2Cd6',
        'stg_token': '0xE3B53AF74a4BF62Ae5511055290838050bf764Df',
        'fee_library': '0x9d1b1669c73b033dfe47ae5a0164ab96df25b944',
        'composer': '0xeCc19E177d24551aA7ed6Bc6FE566eCa726CC8a9',
        'widget_swap': '0x10d16248bED1E0D0c7cF94fFD99A50c336c7Bcdc',
        'ETH': '0x28fc411f9e1c480AD312b3d9C60c22b965015c6B',
        'USDC': '0x4c80E24119CFB836cdF0a6b53dc23F04F7e652CA',
        'LPStakingTime.sol': '0x06Eb48763f117c7Be887296CDcdfad2E4092739C',
        'otf_wrapper': '0x36d4686e19c052787D7f24E6913cEbC025714895',
        'MAV': '0x787c09494Ec8Bcb24DcAf8659E7d5D69979eE508',
    },
    'Linea':{
        'router': '0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590',
        'router_eth': '0x81F6138153d473E8c5EcebD3DC8Cd4903506B075',
        'bridge': '0x45f1A95A4D3f3836523F5c83673c797f4d4d263B',
        'factory': '0xaf54be5b6eec24d6bfacf1cce4eaf680a8239398 ',
        'stg_token': '0x808d7c71ad2ba3FA531b068a2417C63106BC0949 ',
        'fee_library': '0x45A01E4e04F14f7A4a6702c74187c5F6222033cd',
        'composer': '0xeCc19E177d24551aA7ed6Bc6FE566eCa726CC8a9',
        'widget_swap': '0x10d16248bED1E0D0c7cF94fFD99A50c336c7Bcdc',
        'ETH': '0xAad094F6A75A14417d39f04E690fC216f080A41a',
        'lp_staking_time': '0x4a364f8c717cAAD9A442737Eb7b8A55cc6cf18D8',
    },
    'Kava':{
        'router': '0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590',
        'router_usdt': '0x41A5b0470D96656Fb3e8f68A218b39AdBca3420b',
        'bridge': '0x45f1A95A4D3f3836523F5c83673c797f4d4d263B',
        'factory': '0xAF54BE5B6eEc24d6BFACf1cce4eaF680A8239398 ',
        'stg_token': '0x83c30eb8bc9ad7C56532895840039E62659896ea ',
        'fee_library': '0x45a01e4e04f14f7a4a6702c74187c5f6222033cd',
        'composer': '0xeCc19E177d24551aA7ed6Bc6FE566eCa726CC8a9',
        'widget_swap': '0x10d16248bED1E0D0c7cF94fFD99A50c336c7Bcdc',
        'USDT': '0xAad094F6A75A14417d39f04E690fC216f080A41a',
        'lp_staking_time': '0x35F78Adf283Fe87732AbC9747d9f6630dF33276C',
    },
    'Mantle':{
        'router': '0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590',
        'router_eth': '0x4c1d3Fc3fC3c177c3b633427c2F769276c547463',
        'router_usdc': '0xAc290Ad4e0c891FDc295ca4F0a6214cf6dC6acDC',
        'router_usdt': '0xa81274AFac523D639DbcA2C32c1470f1600cCEBe',
        'bridge': '0x45f1A95A4D3f3836523F5c83673c797f4d4d263B',
        'factory': '0xAF54BE5B6eEc24d6BFACf1cce4eaF680A8239398 ',
        'stg_token': '0x8731d54E9D02c286767d56ac03e8037C07e01e98 ',
        'fee_library': '0x45A01E4e04F14f7A4a6702c74187c5F6222033cd',
        'composer': '0x296F55F8Fb28E498B858d0BcDA06D955B2Cb3f97',
        'widget_swap': '0x06D538690AF257Da524f25D0CD52fD85b1c2173E',
        'USDC': '0xAad094F6A75A14417d39f04E690fC216f080A41a',
        'USDT': '0x2b60473a7C41Deb80EDdaafD5560e963440eb632',
        'lp_staking_time': '0x352d8275AAE3e0c2404d9f68f6cEE084B5bEB3DD',
    },
    'Scroll': {
        'router_eth': "0xC2b638Cb5042c1B3c5d5C969361fB50569840583",
        'router_usdc': "0x3Fc69CC4A842838bCDC9499178740226062b14E4",
    }
}

VESTG_ADDRESS = {
     "Ethereum": "0x0e42acBD23FAee03249DAFF896b78d7e79fBD58E",
     "BNB Chain": "0xD4888870C8686c748232719051b677791dBDa26D",
     "Avalanche": "0xCa0F57D295bbcE554DA2c07b005b7d6565a58fCE",
     "Polygon": "0x3AB2DA31bBD886A7eDF68a6b60D3CDe657D3A15D",
     "Arbitrum": "0xfBd849E6007f9BC3CC2D6Eb159c045B8dc660268",
     "Optimist": "0x43d2761ed16C89A2C4342e2B16A3C61Ccf88f05B",
     "Fantom": "0x933421675cDC8c280e5F21f0e061E77849293dba",
}

SPACEFI_CONTRACTS = {
    'zkSync':{
        "router": '0xbE7D1FD1f6748bbDefC4fbaCafBb11C6Fc506d1d',
    },
    'Scroll':{
        "router": '0x18b71386418A9FCa5Ae7165E31c385a5130011b6'
    }
}

WOOFI_CONTRACTS = {
    'zkSync':{
        "router"                : '0x09873bfECA34F1Acd0a7e55cDA591f05d8a75369'
    },
    'Linea':{
        "router"                : '0x4c4AF8DBc524681930a27b2F1Af5bcC8062E6fB7'
    },
    'Base':{
        "router"                : '0x4c4AF8DBc524681930a27b2F1Af5bcC8062E6fB7'
    },
    'Polygon':{
        "router"                : '0x817Eb46D60762442Da3D931Ff51a30334CA39B74'
    },
    'Arbitrum':{
        "router"                : '0x4c4AF8DBc524681930a27b2F1Af5bcC8062E6fB7'
    },
    'Optimism':{
        "router"                : '0x4c4AF8DBc524681930a27b2F1Af5bcC8062E6fB7'
    },
    'Polygon zkEVM':{
        "router"                : '0x39d361E66798155813b907A70D6c2e3FdaFB0877'
    }
}

STARGATE_STG_CONFIG_CHECKERS = {
    "Arbitrum": "0x177d36dBE2271A4DdB2Ad8304d82628eb921d790",
    "Avalanche": "0xCD2E3622d483C7Dc855F72e5eafAdCD577ac78B4",
    "Base": "0xcb566e3B6934Fa77258d68ea18E931fa75e1aaAa",
    "BNB Chain": "0xA27A2cA24DD28Ce14Fb5f5844b59851F03DCf182",
    "Ethereum": "0x902F09715B6303d4173037652FA7377e5b98089E",
    "Fantom": "0x52EEA5c490fB89c7A0084B32FEAB854eefF07c82",
    "Kava": "0xcb566e3B6934Fa77258d68ea18E931fa75e1aaAa",
    "Mantle": "0xcb566e3B6934Fa77258d68ea18E931fa75e1aaAa",
    "opBNB": "0x3A73033C0b1407574C76BdBAc67f126f6b4a9AA9",
    "Optimism": "0x81E792e5a9003CC1C8BF5569A00f34b65d75b017",
    "Polygon": "0x75dC8e5F50C8221a82CA6aF64aF811caA983B65f",
    "Scroll": "0xA658742d33ebd2ce2F0bdFf73515Aa797Fd161D9",
    "Linea": "0xA658742d33ebd2ce2F0bdFf73515Aa797Fd161D9",
    "Polygon zkEVM": "0xA658742d33ebd2ce2F0bdFf73515Aa797Fd161D9",
    "zkSync": "0x9923573104957bF457a3C4DF0e21c8b389Dd43df",
    "Zora": "0xA658742d33ebd2ce2F0bdFf73515Aa797Fd161D9",
}

HYPERLANE_DATA = {
     'domains': {
          'Neutron': 1853125230,
          'Injective': 6909546,
          'InEVM': 2525,
          'Manta': 169,
          'Ethereum': 1,
          'Nautilus': 22222,
          'Celestia': 123456789,
          'Solana': 1399811149,
          'BNB Chain': 56,
          # 'Cosmos': 1234,
          'Arbitrum': 42161,
          'Viction': 88,
     },
     'paths': {
          'Ethereum-InEVM': {
               "": ""
          },
          'InEVM-Ethereum':{
               "": ""
          },
          'Ethereum-Viction': {
               "ETH": {
                    "contract": "0x15b5D6B614242B118AA404528A7f3E2Ad241e4A4"
               }
          },
          'Viction-Ethereum': {
               "": ""
          },
          "Arbitrum-Neutron": {
               "TIA.n": {
                    "contract": "0xD56734d7f9979dD94FAE3d67C7e928234e71cD4C"
               },
               "ECLIP": {
                    "contract": "0x93ca0d85837FF83158Cd14D65B169CdB223b1921"
               },
          },
          "Neutron-Arbitrum": {
               "contract_address": "neutron1jyyjd3x0jhgswgm6nnctxvzla8ypx50tew3ayxxwkrjfxhvje6kqzvzudq",
               "denom": "ibc/773B4D0A3CD667B2275D5A4A7A2F0909C0BA0F4059C0B9181E680DDF4965DCC7"
          },
          "Manta-Neutron": {
               "TIA.n": {
                    "contract": "0x6Fae4D9935E2fcb11fC79a64e917fb2BF14DaFaa"
               },
          },
          "Neutron-Manta": {
               "contract_address": "neutron1ch7x3xgpnj62weyes8vfada35zff6z59kt2psqhnx9gjnt2ttqdqtva3pa",
               "denom": "ibc/773B4D0A3CD667B2275D5A4A7A2F0909C0BA0F4059C0B9181E680DDF4965DCC7"
          },
          "InEVM-Injective": {
               "INJ": {
                    "contract": "0x26f32245fCF5Ad53159E875d5Cae62aEcf19c2d4"
               },
          },
          "Injective-InEVM": {
               "contract_address": "inj1mv9tjvkaw7x8w8y9vds8pkfq46g2vcfkjehc6k",
               "denom": "inj"
          },
          "Celestia-Arbitrum": {
               "contract_address": "neutron1jyyjd3x0jhgswgm6nnctxvzla8ypx50tew3ayxxwkrjfxhvje6kqzvzudq",
               "denom": "ibc/773B4D0A3CD667B2275D5A4A7A2F0909C0BA0F4059C0B9181E680DDF4965DCC7"
          },
          "Celestia-Manta": {
               "contract_address": "neutron1jyyjd3x0jhgswgm6nnctxvzla8ypx50tew3ayxxwkrjfxhvje6kqzvzudq",
               "denom": "ibc/773B4D0A3CD667B2275D5A4A7A2F0909C0BA0F4059C0B9181E680DDF4965DCC7"
          }
     }
}

USENEXUS_CONTRACTS = {
    'Arbitrum': {
        'router': '0xD56734d7f9979dD94FAE3d67C7e928234e71cD4C'
    },
    'Ethereum': {
        'router': '0xED56728fb977b0bBdacf65bCdD5e17Bb7e84504f'
    },
    'Manta': {
        'router': '0x6Fae4D9935E2fcb11fC79a64e917fb2BF14DaFaa'
    },
    'InEVM': {
        'router': '0x26f32245fCF5Ad53159E875d5Cae62aEcf19c2d4'
    }
}

NAUTILUS_CONTRACTS = {
    'Nautilus': {
        'ZBC': '0x4501bBE6e731A4bC5c60C03A77435b2f6d5e9Fe7',
        'WETH': '0x182E8d7c5F1B06201b102123FC7dF0EaeB445a7B',
        'USDT': '0xBDa330Ea8F3005C421C8088e638fBB64fA71b9e0',
        'USDC': '0xB2723928400AE5778f6A3C69D7Ca9e90FC430180'
    },
    'BNB Chain': {
        'ZBC': '0xC27980812E2E66491FD457D488509b7E04144b98',
        'WETH': '0x2a6822dc5639B3FE70dE6b65B9Ff872e554162Fa',
        'USDT': '0xb7d36720a16A1F9Cfc1f7910Ac49f03965401a36',
        'USDC': '0x6937a62f93a56D2AE9392Fa1649b830ca37F3ea4'
    },
    'Solana': {
        'ZBC': 'EJqwFjvVJSAxH8Ur2PYuMfdvoJeutjmH6GkoEFQ4MdSa'
    }
}

GETMINT_HYPERLANE_DATA = {
    "Polygon": {
        'hNFT': "0x11b965675AaAFB77aB738BC797663677278d16b2"
    },
    "BNB Chain ": {
        'hNFT': "0x11b965675AaAFB77aB738BC797663677278d16b2"
    },
    "Arbitrum": {
        'hNFT': "0x11b965675AaAFB77aB738BC797663677278d16b2"
    },
    "Optimism": {
        'hNFT': "0x11b965675AaAFB77aB738BC797663677278d16b2"
    },
    "Gnosis": {
        'hNFT': "0x11b965675AaAFB77aB738BC797663677278d16b2"
    },
    "Base": {
        'hNFT': "0x11b965675AaAFB77aB738BC797663677278d16b2"
    },
    "Scroll": {
        'hNFT': "0x11b965675AaAFB77aB738BC797663677278d16b2"
    },
    "Celo": {
        'hNFT': "0x11b965675AaAFB77aB738BC797663677278d16b2"
    },
    "Avalanche": {
        'hNFT': "0x11b965675AaAFB77aB738BC797663677278d16b2"
    },
}

WOMEX_HYPERLANE_DATA = {
    "Polygon": {
        'hNFT': "0xBc05f46c3286372B86dD9c03e67B72E85B75a018"
    },
    "BNB Chain ": {
        'hNFT': "0xBc05f46c3286372B86dD9c03e67B72E85B75a018"
    },
    "Arbitrum": {
        'hNFT': "0xBc05f46c3286372B86dD9c03e67B72E85B75a018"
    },
    "Optimism": {
        'hNFT': "0xBc05f46c3286372B86dD9c03e67B72E85B75a018"
    },
    "Gnosis": {
        'hNFT': "0xBc05f46c3286372B86dD9c03e67B72E85B75a018"
    },
    "Base": {
        'hNFT': "0xBc05f46c3286372B86dD9c03e67B72E85B75a018"
    },
    "Scroll": {
        'hNFT': "0xBc05f46c3286372B86dD9c03e67B72E85B75a018"
    },
    "Celo": {
        'hNFT': "0xBc05f46c3286372B86dD9c03e67B72E85B75a018"
    },
    "Avalanche": {
        'hNFT': "0xBc05f46c3286372B86dD9c03e67B72E85B75a018"
    },
}

AMBIENT_CONTRACT = {
    'Scroll': {
        'router'                : '0xaaaaAAAACB71BF2C8CaE522EA5fa455571A74106',
        'quoter'                : '0x62223e90605845Cf5CC6DAE6E0de4CDA130d6DDf'
    },
    'Blast': {
        'router'                : '0xaAaaaAAAFfe404EE9433EEf0094b6382D81fb958'
    }
}

VELOCORE_CONTRACTS = {
    'zkSync':{
        "router": '0xf5E67261CB357eDb6C7719fEFAFaaB280cB5E2A6',
        "multicall": '0xF9cda624FBC7e059355ce98a31693d299FACd963',
    },
    'Linea':{
        "router": '0x1d0188c4B276A09366D05d6Be06aF61a73bC7535',
        "multicall": '0xcA11bde05977b3631167028862bE2a173976CA11',
    }
}

SUSHISWAP_CONTRACTS = {
    'Base': {
        "router": "0xFB7eF66a7e61224DD6FcD0D7d9C3be5C8B049b9f",
        "quoter": "0xb1E835Dc2785b52265711e17fCCb0fd018226a6e",
    },
    'Arbitrum Nova':{
        "router": "0xc14Ee6B248787847527e11b8d7Cf257b212f7a9F",
        "quoter": "0xb1E835Dc2785b52265711e17fCCb0fd018226a6e",
    },
    'Scroll':{
        "router": "0x33d91116e0370970444B0281AB117e161fEbFcdD",
        "quoter": "0xe43ca1Dee3F0fc1e2df73A0745674545F11A59F5",
    },
    'Arbitrum':{
        "router": "0x8A21F6768C1f8075791D08546Dadf6daA0bE820c",
        "quoter": "0x0524E833cCD057e4d7A296e3aaAb9f7675964Ce1",
    }
}

DACKIESWAP_CONTRACTS = {
    'InEVM': {
        "router": "0x1A4B306Ba14D3Fb8A49925675F8eDB7eF607c422",
        "quoter": "0x3D237AC6D2f425D2E890Cc99198818cc1FA48870",
    }
}

IZUMI_CONTRACTS = {
    'zkSync': {
        "quoter"                : '0x30C089574551516e5F1169C32C6D429C92bf3CD7',
        "router"                : '0x943ac2310D9BC703d6AB5e5e76876e212100f894'
    },
    'Linea': {
        "quoter"                : '0xe6805638db944eA605e774e72c6F0D15Fb6a1347',
        "router"                : '0x032b241De86a8660f1Ae0691a4760B426EA246d7'
    },
    'Taiko': {
        "quoter"                : '0x2C6Df0fDbCE9D2Ded2B52A117126F2Dc991f770f',
        "router"                : '0x04830cfCED9772b8ACbAF76Cfc7A630Ad82c9148'
    },
    'Base': {
        "quoter"                : '0x2db0AFD0045F3518c77eC6591a542e326Befd3D7',
        "router"                : '0x02F55D53DcE23B4AA962CC68b0f685f26143Bdb2'
    },
    'Scroll': {
        "quoter"                : '0x3EF68D3f7664b2805D4E88381b64868a56f88bC4',
        "router"                : '0x2db0AFD0045F3518c77eC6591a542e326Befd3D7'
    },
    'Manta': {
        "quoter"                : '0x33531bDBFE34fa6Fd5963D0423f7699775AacaaF',
        "router"                : '0x3EF68D3f7664b2805D4E88381b64868a56f88bC4'
    }
}

TRADERJOE_CONTRACTS = {
    'Arbitrum': {
        "router": '0xb4315e873dBcf96Ffd0acd8EA43f689D8c20fB30',
        "quoter": '0xd76019A16606FDa4651f636D9751f500Ed776250',
    }
}

RUBYSCORE_CONTRACTS = {
    "Base": {
        "vote_contract": "0xe10Add2ad591A7AC3CA46788a06290De017b9fB4",
    },
    "Linea": {
        "vote_contract": "0xe10Add2ad591A7AC3CA46788a06290De017b9fB4",
    },
    "Polygon zkEVM": {
        "vote_contract": "0xe10Add2ad591A7AC3CA46788a06290De017b9fB4",
    },
    "zkSync": {
        "vote_contract": "0xCb84d512F0C9943D3BC6B4Be8801aC8Aa6621a54",
    },
    "Scroll": {
        "vote_contract": "0xe10Add2ad591A7AC3CA46788a06290De017b9fB4",
    },
    "Manta": {
        "vote_contract": "0xF57Cb671D50535126694Ce5Cc3CeBe3F32794896",
    },
    "Blast": {
        "vote_contract": "0xbDB018e21AD1e5756853fe008793a474d329991b",
    },
    "Zora": {
        "vote_contract": "0xDC3D8318Fbaec2de49281843f5bba22e78338146",
    },
    "Taiko": {
        "vote_contract": "0x4D1E2145082d0AB0fDa4a973dC4887C7295e21aB",
    },
    "Mantle": {
        "vote_contract": "0x4D1E2145082d0AB0fDa4a973dC4887C7295e21aB",
    }
}

SEAMLESS_CONTRACTS = {
    'Base':{
        "landing"               : '0xaeeB3898edE6a6e86864688383E211132BAa1Af3',
        "pool_proxy"            : '0x8F44Fd754285aa6A2b8B9B97739B79746e0475a7',
        "weth_atoken"           : '0x48bf8fCd44e2977c8a9A744658431A8e6C0d866c',
        "sUSDcb_token"          : '0x13A13869B814Be8F13B86e9875aB51bda882E391'
    }
}

ERALEND_CONTRACTS = {
    'zkSync': {
        "landing"               : '0x22D8b71599e14F20a49a397b88c1C878c86F5579',
        "collateral"            : '0xC955d5fa053d88E7338317cc6589635cD5B2cf09'
    }
}

AAVE_CONTRACTS = {
    'Arbitrum':{
        "weth_gateway"          : '0xecD4bd3121F9FD604ffaC631bF6d41ec12f1fafb',
        "pool_proxy"            : '0x794a61358D6845594F94dc1DB02A252b5b4814aD',
        "weth_atoken"           : '0xe50fA9b3c56FfB159cB0FCA61F5c9D750e8128c8'
    },
    'Base': {
        "weth_gateway"          : '0x8be473dCfA93132658821E67CbEB684ec8Ea2E74',
        "pool_proxy"            : '0xA238Dd80C259a72e81d7e4664a9801593F98d1c5',
        "weth_atoken"           : '0xD4a0e0b9149BCee3C920d2E00b5dE09138fd8bb7'
    },
    'Optimism': {
        "weth_gateway"          : '0xe9E52021f4e11DEAD8661812A0A6c8627abA2a54',
        "pool_proxy"            : '0x794a61358D6845594F94dc1DB02A252b5b4814aD',
        "weth_atoken"           : '0xe50fA9b3c56FfB159cB0FCA61F5c9D750e8128c8'
    },
    'Scroll': {
        "weth_gateway"          : '0xFF75A4B698E3Ec95E608ac0f22A03B8368E05F5D',
        "pool_proxy"            : '0x11fCfe756c05AD438e312a7fd934381537D3cFfe',
        "weth_atoken"           : '0xf301805bE1Df81102C957f6d4Ce29d2B8c056B2a'
    },
    # 'Polygon':{ # todo not done
    #     "weth_gateway"          : '0x767b4A087c11d7581Ac95eaFfc1FeBFA26bad3d2',
    #     "pool_proxy"            : '0x4d9429246EA989C9CeE203B43F6d1C7D83e3B8F8',
    #     "weth_atoken"           : '0x9002ecb8a06060e3b56669c6B8F18E1c3b119914'
    # },
    'BNB Chain':{
        "weth_gateway"          : '0xd91d1331db4F436DaF47Ec9Dd86deCb8EEF946B4',
        "pool_proxy"            : '0x6807dc923806fE8Fd134338EABCA509979a7e0cB',
        "weth_atoken"           : '0x9B00a09492a626678E5A3009982191586C444Df9',
    },
    # 'Avalanche':{
    #     "weth_gateway"          : '0x2DeC8BCE3471eD65B1bB558Fa28439D45bF446d0',
    #     "pool_proxy"            : '0x794a61358D6845594F94dc1DB02A252b5b4814aD',
    #     "weth_atoken"           : '0x53a3Aa617afE3C12550a93BA6262430010037B04',
    # }
}

ZEROLEND_CONTRACTS = {
    'zkSync':{
        "landing"               : '0x767b4A087c11d7581Ac95eaFfc1FeBFA26bad3d2',
        "pool_proxy"            : '0x4d9429246EA989C9CeE203B43F6d1C7D83e3B8F8',
        "weth_atoken"           : '0x9002ecb8a06060e3b56669c6B8F18E1c3b119914'
    },
    'Blast':{
        "landing"               : '0xFaDFb0BC400427663020887e7c8073D03A35dc3c',
        "pool_proxy"            : '0xa70B0F3C2470AbBE104BdB3F3aaa9C7C54BEA7A8',
        "weth_atoken"           : '0x53a3Aa617afE3C12550a93BA6262430010037B04',
        "usdb_atoken"           : '0x23A58cbe25E36e26639bdD969B0531d3aD5F9c34'
    }
}

ELIXIR_CONTRACTS = {
    'Ethereum':{
        "landing"               : '0x1F75881DC0707b5236f739b5B64A87c211294Abb',
        "eth_usdc_router"       : '0x1F75881DC0707b5236f739b5B64A87c211294Abb',
    },
    'Arbitrum': {
        "landing"               : '0x79865208f5dc18a476F49e6dBFd7d79785CB8cD8',
        "eth_usdc_router"       : '0x79865208f5dc18a476F49e6dBFd7d79785CB8cD8',
    },
}


PANCAKE_CONTRACTS = {
    'zkSync': {
        "router"                : '0xf8b59f3c3Ab33200ec80a8A58b2aA5F5D2a8944C',
        "quoter"                : '0x3d146FcE6c1006857750cBe8aF44f76a28041CCc'
    },
    'Arbitrum': {
        "router"                : '0x32226588378236Fd0c7c4053999F88aC0e5cAc77',
        "quoter"                : '0xB048Bbc1Ee6b733FFfCFb9e9CeF7375518e25997'
    },
    'Base': {
        "router"                : '0x678Aa4bF4E210cf2166753e054d5b7c31cc7fa86',
        "quoter"                : '0xB048Bbc1Ee6b733FFfCFb9e9CeF7375518e25997'
    },
    'Linea': {
        "router"                : '0x678Aa4bF4E210cf2166753e054d5b7c31cc7fa86',
        "quoter"                : '0xB048Bbc1Ee6b733FFfCFb9e9CeF7375518e25997'
    }
}

ORBITER_CONTRACTS = {
    "evm_contracts"          : {
        'zkSync'         :'0xBF3922a0cEBbcD718e715e83d9187cC4BbA23f11',
        'Zora'           :'0x13e46b2a3f8512ed4682a8fb8b560589fe3c2172',
        'Arbitrum'       :'0xD9D74a29307cc6Fc8BF424ee4217f1A587FBc8Dc',
        'Arbitrum Nova'  :'0xD9D74a29307cc6Fc8BF424ee4217f1A587FBc8Dc',
        'Base'           :'0xD9D74a29307cc6Fc8BF424ee4217f1A587FBc8Dc',
        'Linea'          :'0xD9D74a29307cc6Fc8BF424ee4217f1A587FBc8Dc',
        'Manta'          :'0xD9D74a29307cc6Fc8BF424ee4217f1A587FBc8Dc',
        'Polygon'        :'0xD9D74a29307cc6Fc8BF424ee4217f1A587FBc8Dc',
        'Polygon zkEVM'  :'0xD9D74a29307cc6Fc8BF424ee4217f1A587FBc8Dc',
    },
    "stark_contract"        : 0x173f81c529191726c6e7287e24626fe24760ac44dae2a1f7e02080230f8458b
}

RHINO_CONTRACTS = {
    'nft_common': '0x812dE7B8cC9dC7ad5Bc929d3337BFB617Dcc7949',
    'nft_rare'  : '0xdD01108F870F087B54c28aCF1a8bBAf6f6A851Ae'
}

UNISWAP_CONTRACTS = {
    'Arbitrum': {
        "router": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
        "quoter": "0x61fFE014bA17989E743c5F6cB21bF9697530B21e",
    },
    'Optimism': {
        "router": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
        "quoter": "0x61fFE014bA17989E743c5F6cB21bF9697530B21e",
    },
    'Base': {
        "router": "0x2626664c2603336E57B271c5C0b26F421741e481",
        "quoter": "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a",
    },
    'Polygon': {
        "router": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
        "quoter": "0x61fFE014bA17989E743c5F6cB21bF9697530B21e",
    }
}

BUNGEE_CONTRACTS = {
    'zkSync':{
        'gas_refuel': '0x7Ee459D7fDe8b4a3C22b9c8C7aa52AbadDd9fFD5',
    },
    'Ethereum':{
        'gas_refuel': '0xb584D4bE1A5470CA1a8778E9B86c81e165204599'
    },
    'Base':{
        'gas_refuel': '0xe8c5b8488feafb5df316be73ede3bdc26571a773'
    },
    'Gnosis':{
        'gas_refuel': '0xBE51D38547992293c89CC589105784ab60b004A9'
    },
    'BNB Chain':{
        'gas_refuel': '0xBE51D38547992293c89CC589105784ab60b004A9'
    },
    'Polygon':{
        'gas_refuel': '0xAC313d7491910516E06FBfC2A0b5BB49bb072D91'
    },
    'Polygon zkEVM':{
        'gas_refuel': '0x555A64968E4803e27669D64e349Ef3d18FCa0895'
    },
    'Arbitrum':{
        'gas_refuel': '0xc0E02AA55d10e38855e13B64A8E1387A04681A00',
        'claim': '0x659A3A109789b19fe6B6cB36389eE77F1807C54f'
    },
    'Avalanche':{
        'gas_refuel': '0x040993fbF458b95871Cd2D73Ee2E09F4AF6d56bB'
    },
    'Optimism':{
        'gas_refuel': '0x5800249621DA520aDFdCa16da20d8A5Fc0f814d8'
    }
}

WHALE_CONTRACTS_PER_CHAINS = {
    "Arbitrum": {
        'ONFT'                  : '0x26E9934024cdC7fcc9f390973d4D9ac1FA954a37',
        'refuel'                : '0x218de7fAB4310497C2aCf8523d8701b5F2F4D1C7'
    },
    "Arbirtum Nova": {
        'ONFT'                  : '0x1010a05759a0a7Daa665f12Ec677ff5034Ecd35F',
        'refuel'                : '0xBe2E226923641Dc4C77583bC71332ecd99597862'
    },
    "Base": {
        'ONFT'                  : '0xa0d013b84FBAeFF5AbFc92A412a44572382dCA08',
        'refuel'                : '0x72913DeD90F5Bb415bD74cdccfc944E9887E9790'
    },
    "Linea": {
        'ONFT'                  : '0x84f4c0A290B5607fee0f2A1CDe5348540fecF6A1',
        'refuel'                : '0x9aeAa45d415fFE75dC4Ba50658584479bAf110Ec'
    },
    "Polygon": {
        'ONFT'                  : '0xE1c907503B8d1545AFD5A89cc44FC1E538A132DA',
        'refuel'                : '0x45265fB77A51e3B4ec70142f993F1654A8f7ab32'
    },
    "Optimism": {
        'ONFT'                  : '0xe87492ae9151769412F40af251d1D2793271e699',
        'refuel'                : '0x83Ff86c252a41578a7301219Aa23ab6e4F2FdeD3'
    },
    "Scroll": {
        'ONFT'                  : '0xa0d013b84FBAeFF5AbFc92A412a44572382dCA08',
        'refuel'                : '0xba800cD922F9C4d935fAb96e4a346538bbf29D8c'
    },
    "Polygon zkEVM": {
        'ONFT'                  : '0xeDc03C234882FA785e7084B2C7E13BC8b7B6a4e3',
        'refuel'                : '0x82d5a068ba58ad31c419275474333B8696B3641d'
    },
    "zkSync": {
        'ONFT'                  : '0xF09A71F6CC8DE983dD58Ca474cBC33de43DDEBa9',
        'refuel'                : '0x06a2ce74Bc6021851157a003A97D9D8f900543D1'
    },
    "Zora": {
        'ONFT'                  : '0x82d5a068ba58ad31c419275474333B8696B3641d',
        'refuel'                : '0xeDc03C234882FA785e7084B2C7E13BC8b7B6a4e3'
    },
    "Ethereum": {
        'ONFT'                  : '',
        'refuel'                : ''
    },
    "Avalanche": {
        'ONFT'                  : '0x54C71EBBd27520bCbE3E3973a4B579A27035ACD3',
        'refuel'                : '0x3Aa96e35525f15cE0a5521ECBc11B2acD23973CF'
    },
    "BNB Chain": {
        'ONFT'                  : '0x006E23eb40eBc1805783e3a6c39283bcF5799368',
        'refuel'                : '0x6D096d86F1fE43aed8A073DAd9823C987A450f0e'
    },
    "Moonbeam": {
        'ONFT'                  : '0xd709e73c5213Fd291d0BfA55A7D934B741398d96',
        'refuel'                : '0xb3dd9b6Cd0f14f921E21094c213de746ceE4a2bC'
    },
    "Harmony": {
        'ONFT'                  : '0x36314E3fd0Ff6243e971814613fe73A78f29085E',
        'refuel'                : '0xeDc03C234882FA785e7084B2C7E13BC8b7B6a4e3'
    },
    "Telos": {
        'ONFT'                  : '',
        'refuel'                : ''
    },
    "Celo": {
        'ONFT'                  : '0xb24b54a2013F4Ff5Df2214559CBF1745C1750b2A',
        'refuel'                : '0xBcEe7fB1B98ea4e38Eb52c2E026134d54273ED44'
    },
    "Gnosis": {
        'ONFT'                  : '0xe9EbD35Ea4aCCb97e0F5BF3CDA31fe3Ac90111Cc',
        'refuel'                : '0x21b3035F2e1C43DF018f2810A321F62f14554209'
    },
    "CoreDAO": {
        'ONFT'                  : '0x82d5a068ba58ad31c419275474333B8696B3641d',
        'refuel'                : '0xeDc03C234882FA785e7084B2C7E13BC8b7B6a4e3'
    },
    "TomoChain": {
        'ONFT'                  : '',
        'refuel'                : ''
    },
    "Conflux": {
        'ONFT'                  : '',
        'refuel'                : ''
    },
    "Orderly": {
        'ONFT'                  : '',
        'refuel'                : ''
    },
    "Horizen EON": {
        'ONFT'                  : '',
        'refuel'                : ''
    },
    "Metis": {
        'ONFT'                  : '0x82d5a068ba58ad31c419275474333B8696B3641d',
        'refuel'                : '0xeDc03C234882FA785e7084B2C7E13BC8b7B6a4e3'
    },
    "Astar": {
        'ONFT'                  : '',
        'refuel'                : ''
    },
    "OpBNB": {
        'ONFT'                  : '0x9aeAa45d415fFE75dC4Ba50658584479bAf110Ec',
        'refuel'                : '0x84f4c0A290B5607fee0f2A1CDe5348540fecF6A1'
    },
    "Mantle": {
        'ONFT'                  : '0x84f4c0A290B5607fee0f2A1CDe5348540fecF6A1',
        'refuel'                : '0xeDc03C234882FA785e7084B2C7E13BC8b7B6a4e3'
    },
    "Moonriver": {
        'ONFT'                  : '0xeDc03C234882FA785e7084B2C7E13BC8b7B6a4e3',
        'refuel'                : '0x82d5a068ba58ad31c419275474333B8696B3641d'
    },
    "Klaytn": {
        'ONFT'                  : '0xa0d013b84FBAeFF5AbFc92A412a44572382dCA08',
        'refuel'                : '0xBcB4bc8fe7faba16C8A06186aB1703709a24C6bf'
    },
    "Kava": {
        'ONFT'                  : '0xBcEe7fB1B98ea4e38Eb52c2E026134d54273ED44',
        'refuel'                : '0x82d5a068ba58ad31c419275474333B8696B3641d'
    },
    "Fantom": {
        'ONFT'                  : '0x82d5a068ba58ad31c419275474333B8696B3641d',
        'refuel'                : '0xb30b4ff71d44C544eDb7A06aceb0008ADa040c78'
    },
    "Aurora": {
        'ONFT'                : '',
        'refuel'              : ''
    },
    "Canto": {
        'refuel'                : '',
        'ONFT'                  : ''
    },
    "DFK": {
        'refuel'                : '',
        'endpoint'              : ''
    },
    "Fuse": {
        'ONFT'                : '0x82d5a068ba58ad31c419275474333B8696B3641d',
        'refuel'              : '0xeDc03C234882FA785e7084B2C7E13BC8b7B6a4e3'
    },
    "Goerli": {
        'refuel'                : '',
        'endpoint'              : ''
    },
    "Meter": {
        'ONFT'                : '0xfdcac2c2091b3ce88203fb2defb8c9f98edcb904',
        'refuel'              : '0xf9481cc0d342a0d4d533f77d334a24dfbf1d719d'
    },
    "OKX Chain": {
        'refuel'                : '',
        'endpoint'              : ''
    },
    "Shimmer": {
        'ONFT'                : '0x84f4c0A290B5607fee0f2A1CDe5348540fecF6A1',
        'refuel'              : '0x84f4c0A290B5607fee0f2A1CDe5348540fecF6A1'
    },
    "Tenet": {
        'refuel'                : '',
        'endpoint'              :  ''
    },
    "XPLA": {
        'refuel'                : '',
        'endpoint'              : ''
    }
}

ZERIUS_CONTRACT_PER_CHAINS = {
    "Arbitrum": {
        'ONFT'                  : '0x250c34D06857b9C0A036d44F86d2c1Abe514B3Da',
        'refuel'                : '0x412aea168aDd34361aFEf6a2e3FC01928Fba1248'
    },
    "Arbirtum Nova": {
        'ONFT'                  : '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7',
        'refuel'                : '0x3Fc5913D35105f338cEfcB3a7a0768c48E2Ade8E'
    },
    "Base": {
        'ONFT'                  : '0x178608fFe2Cca5d36f3Fc6e69426c4D3A5A74A41',
        'refuel'                : '0x9415AD63EdF2e0de7D8B9D8FeE4b939dd1e52F2C'
    },
    "Linea": {
        'ONFT'                  : '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7',
        'refuel'                : '0x5B209E7c81DEaad0ffb8b76b696dBb4633A318CD'
    },
    "Polygon": {
        'ONFT'                  : '0x178608fFe2Cca5d36f3Fc6e69426c4D3A5A74A41',
        'refuel'                : '0x2ef766b59e4603250265EcC468cF38a6a00b84b3'
    },
    "Optimism": {
        'ONFT'                  : '0x178608fFe2Cca5d36f3Fc6e69426c4D3A5A74A41',
        'refuel'                : '0x2076BDd52Af431ba0E5411b3dd9B5eeDa31BB9Eb'
    },
    "Scroll": {
        'ONFT'                  : '0xEB22C3e221080eAD305CAE5f37F0753970d973Cd',
        'refuel'                : '0xB074f8D92b930D3415DA6bA80F6D38f69ee4B9cf'
    },
    "Polygon zkEVM": {
        'ONFT'                  : '0x4c5AeDA35d8F0F7b67d6EB547eAB1df75aA23Eaf',
        'refuel'                : '0xBAf5C493a4c364cBD2CA83C355E75F0ff7042945'
    },
    "zkSync": {
        'ONFT'                  : '0x7dA50bD0fb3C2E868069d9271A2aeb7eD943c2D6',
        'refuel'                : '0xeC8Afef7aFe586EB523c228B6BAf3171b1f6dD95'
    },
    "Zora": {
        'ONFT'                  : '0x178608fFe2Cca5d36f3Fc6e69426c4D3A5A74A41',
        'refuel'                : '0x1fe2c567169d39CCc5299727FfAC96362b2Ab90E'
    },
    "Ethereum": {
        'ONFT'                  : '0x178608fFe2Cca5d36f3Fc6e69426c4D3A5A74A41',
        'refuel'                : ''
    },
    "Avalanche": {
        'ONFT'                  : '0x178608fFe2Cca5d36f3Fc6e69426c4D3A5A74A41',
        'refuel'                : '0x5B209E7c81DEaad0ffb8b76b696dBb4633A318CD'
    },
    "BNB Chain": {
        'ONFT'                  : '0x250c34D06857b9C0A036d44F86d2c1Abe514B3Da',
        'refuel'                : '0x5B209E7c81DEaad0ffb8b76b696dBb4633A318CD'
    },
    "Moonbeam": {
        'ONFT'                  : '0x4c5AeDA35d8F0F7b67d6EB547eAB1df75aA23Eaf',
        'refuel'                : '0xb0bea3bB2d6EDDD2014952ABd744660bAeF9747d'
    },
    "Harmony": {
        'ONFT'                  : '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7',
        'refuel'                : '0x5B209E7c81DEaad0ffb8b76b696dBb4633A318CD'
    },
    "Telos": {
        'ONFT'                  : '',
        'refuel'                : ''
    },
    "Celo": {
        'ONFT'                  : '0x4c5AeDA35d8F0F7b67d6EB547eAB1df75aA23Eaf',
        'refuel'                : '0xFF21d5a3a8e3E8BA2576e967888Deea583ff02f8'
    },
    "Gnosis": {
        'ONFT'                  : '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7',
        'refuel'                : '0x1fe2c567169d39CCc5299727FfAC96362b2Ab90E'
    },
    "CoreDAO": {
        'ONFT'                  : '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7',
        'refuel'                : '0xB47D82aA70f839dC27a34573f135eD6dE6CED9A5'
    },
    "TomoChain": {
        'ONFT'                  : '',
        'refuel'                : ''
    },
    "Conflux": {
        'ONFT'                  : '',
        'refuel'                : '0x1fe2c567169d39CCc5299727FfAC96362b2Ab90E'
    },
    "Orderly": {
        'ONFT'                  : '',
        'refuel'                : '0x1fe2c567169d39CCc5299727FfAC96362b2Ab90E'
    },
    "Horizen EON": {
        'ONFT'                  : '',
        'refuel'                : '0x1fe2c567169d39CCc5299727FfAC96362b2Ab90E'
    },
    "Metis": {
        'ONFT'                  : '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7',
        'refuel'                : '0x1b07F1f4F860e72c9367e718a30e38130114AD22'
    },
    "Astar": {
        'ONFT'                  : '',
        'refuel'                : ''
    },
    "OpBNB": {
        'refuel'                : '',
        'endpoint'              : ''
    },
    "Mantle": {
        'refuel'                : '',
        'endpoint'              : ''
    },
    "Moonriver": {
        'refuel'                : '',
        'endpoint'              : ''
    },
    "Klaytn": {
        'refuel'                : '',
        'ONFT'              : ''
    },
    "Kava": {
        'refuel'                : '',
        'endpoint'              : ''
    },
    "Fantom": {
        'refuel'                : '',
        'ONFT'                  : '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7'
    },
    "Aurora": {
        'refuel': '',
        'endpoint': ''
    },
    "Canto": {
        'refuel': '',
        'ONFT'                  : '0x5188368a92B49F30f4Cf9bEF64635bCf8459c7A7'
    },
    "DFK": {
        'refuel': '',
        'endpoint': ''
    },
    "Fuse": {
        'refuel': '',
        'endpoint': ''
    },
    "Goerli": {
        'refuel': '',
        'endpoint': ''
    },
    "Meter": {
        'refuel': '',
        'endpoint': ''
    },
    "OKX Chain": {
        'refuel': '',
        'endpoint': ''
    },
    "Shimmer": {
        'refuel': '',
        'endpoint': ''
    },
    "Tenet": {
        'refuel': '',
        'endpoint': ''
    },
    "XPLA": {
        'refuel': '',
        'endpoint': ''
    }
}

DMAIL_CONTRACT = {
    'zkSync': {
        'core'              : '0x981F198286E40F9979274E0876636E9144B8FB8E'
    },
    'Starknet': {
        'core'              : 0x0454f0bd015e730e5adbb4f080b075fdbf55654ff41ee336203aa2e1ac4d4309
    },
    'Base':{
        'core'              : '0x47fbe95e981C0Df9737B6971B451fB15fdC989d9'
    },
    'Optimism':{
        'core'              : '0x64812F1212f6276068A0726f4695a6637DA3E4F8'
    },
    'Scroll':{
        'core'              : '0x47fbe95e981C0Df9737B6971B451fB15fdC989d9'
    },
    'Linea':{
        'core'              : '0xD1A3abf42f9E66BE86cfDEa8c5C2c74f041c5e14'
    },
    'Manta':{
        'core'              : '0xC0b920c31c1D9047D043b201e6b3956eDb1A0374'
    }
}

MAILZERO_CONTRACT = {
    'mail_contract'         : '0xc94025c2eA9512857BD8E1e611aB9b773b769350'
}

MYSWAP_CONTRACT = {
    'router'                : 0x010884171baf1914edc28d7afb619b40a4051cfae78a094a55d230f19e944a28
}

LAYERBANK_CONTRACTS = {
    'Linea':{
        'landing'               : '0x43Eac5BFEa14531B8DE0B334E123eA98325de866',
        'pool'                  : '0x9E9aec6a296f94C8530e2dD01FF3E9c61555D39a'
    },
    'Scroll':{
        'landing'               : '0xEC53c830f4444a8A56455c6836b5D2aA794289Aa',
        'pool'                  : '0x274C3795dadfEbf562932992bF241ae087e0a98C'
    }
}

BASILISK_CONTRACTS = {
    'zkSync': {
        "landing"               : '0x1e8F1099a3fe6D2c1A960528394F4fEB8f8A288D',
        "collateral"            : '0x4085f99720e699106bc483dAb6CAED171EdA8D15'
    }
}

AMBIENT_CONTRACTS = {
    'Scroll': {
        "landing"               : '0x1e8F1099a3fe6D2c1A960528394F4fEB8f8A288D',
        "collateral"            : '0x4085f99720e699106bc483dAb6CAED171EdA8D15'
    }
}

MOONWELL_CONTRACTS = {
    'Base':{
        'landing'               : '0x70778cfcFC475c7eA0f24cC625Baf6EaE475D0c9',
        'weth_pool'             : '0x628ff693426583D9a7FB391E54366292F509D457',
        'market'                : '0xfBb21d0380beE3312B33c4353c8936a0F13EF26C'
    }
}

KEOM_CONTRACTS = {
    'Polygon zkEVM':{
        'landing'               : '0xee1727f5074E747716637e1776B7F7C7133f16b1',
        'market'                : '0x6EA32f626e3A5c41547235ebBdf861526e11f482'
    }
}

OMNISEA_CONTRACT = {
    'zkSync':{
        'drop_factory'          : "0x8d25e53D707433122f051D7977f98dC615cBEb87"
    },
    'Scroll':{
        'drop_factory'          : "0x470Ab53A2E939Bee3Cc9d0064034cfF925a9c8c5"
    },
    'Linea':{
        'drop_factory'          : "0xCa68A9Acf7C6E364d23382Bcb7ad06c5B29ddc44"
    },
    'Base':{
        'drop_factory'          : "0xA8be4FED3E144a121e7916A0cD31B841DbF3618B"
    }
}

ROCKETSAM_CONTRACTS = {
    "Zora": [
        "0x634607B44e21F4b71e7bD5e19d5b8E4dC99Ab9C4",
        "0x1077df51A4059477826549101a30a70b9579A08B",
        "0x802DbB9efE447f8e4f578EB7add3F7e43E89C529",
        "0x0c9Bfb785E6582A15d6523252675abaA7350Bf76",
        "0x288df8088905D71Ff052bf052f3A0ff11A6CDa46",
        "0x2B4a7822F3de8bd6cb0552f562b40a391890E945",
        "0x553a8EFa12d333c864c89CB809D68268C836B70a",
        "0x5ae3cB086887A6FB7662eE58Cf1d5113E69bBA62",
        "0x1feF777Fb93Aa45a6Cefcf5507c665b64b301FB3",
        "0x80C7E6B91a33b2D956F01092B1E60EEc6e957dc9",
    ],
    "Scroll": [
        "0x634607B44e21F4b71e7bD5e19d5b8E4dC99Ab9C4",
        "0x1077df51A4059477826549101a30a70b9579A08B",
        "0x802DbB9efE447f8e4f578EB7add3F7e43E89C529",
        "0x0c9Bfb785E6582A15d6523252675abaA7350Bf76",
        "0x288df8088905D71Ff052bf052f3A0ff11A6CDa46",
        "0x2B4a7822F3de8bd6cb0552f562b40a391890E945",
        "0x553a8EFa12d333c864c89CB809D68268C836B70a",
        "0x5ae3cB086887A6FB7662eE58Cf1d5113E69bBA62",
        "0x1feF777Fb93Aa45a6Cefcf5507c665b64b301FB3",
        "0x0557D4C04BB994719b087d2950841BF25cf39899",
    ],
    "Nova": [
        "0x80C7E6B91a33b2D956F01092B1E60EEc6e957dc9",
        "0x634607B44e21F4b71e7bD5e19d5b8E4dC99Ab9C4",
        "0x1077df51A4059477826549101a30a70b9579A08B",
        "0x802DbB9efE447f8e4f578EB7add3F7e43E89C529",
        "0x0c9Bfb785E6582A15d6523252675abaA7350Bf76",
        "0x288df8088905D71Ff052bf052f3A0ff11A6CDa46",
        "0x2B4a7822F3de8bd6cb0552f562b40a391890E945",
        "0x553a8EFa12d333c864c89CB809D68268C836B70a",
        "0x5ae3cB086887A6FB7662eE58Cf1d5113E69bBA62",
        "0x1feF777Fb93Aa45a6Cefcf5507c665b64b301FB3",
    ],
    "zkSync": [
        "0xbc6C8BbBD06b6785cF898C3a69DbAE56527dEF10",
        "0x267e930bb2cb5d3d62564c20b947ad8839c8f7b6",
        "0x5b35d48acdc790ebb94523a100a20e97c937de29",
        "0xb959a457c54b03d8bf1d126c3baca8ee2cd967f2",
        "0x65b82bd5a83ff082f723ebf4187b7739ad13e230",
        "0xe771b992d2af7d0d99bc93c83cc9c254787e47a8",
        "0x0b6662b53560ca1b4b22e15bd3cf692e864a733c",
        "0xe6bcb3c91982f5f63e4b19b8130a10767762e2a9",
        "0x07068c8e44a4f4816b3921178ccec6cd4d9a4e14",
        "0x59f6cef0843f3506b214055ad6fd3c385f83d1ad",
    ],
    "Linea": [
        "0x80C7E6B91a33b2D956F01092B1E60EEc6e957dc9",
        "0x1077df51A4059477826549101a30a70b9579A08B",
        "0x802DbB9efE447f8e4f578EB7add3F7e43E89C529",
        "0x0c9Bfb785E6582A15d6523252675abaA7350Bf76",
        "0x288df8088905D71Ff052bf052f3A0ff11A6CDa46",
        "0x2B4a7822F3de8bd6cb0552f562b40a391890E945",
        "0x553a8EFa12d333c864c89CB809D68268C836B70a",
        "0x5ae3cB086887A6FB7662eE58Cf1d5113E69bBA62",
        "0x1feF777Fb93Aa45a6Cefcf5507c665b64b301FB3",
        "0x0557D4C04BB994719b087d2950841BF25cf39899",
    ],
    "Base": [
        "0x634607B44e21F4b71e7bD5e19d5b8E4dC99Ab9C4",
        "0x1077df51A4059477826549101a30a70b9579A08B",
        "0x802DbB9efE447f8e4f578EB7add3F7e43E89C529",
        "0x0c9Bfb785E6582A15d6523252675abaA7350Bf76",
        "0x288df8088905D71Ff052bf052f3A0ff11A6CDa46",
        "0x2B4a7822F3de8bd6cb0552f562b40a391890E945",
        "0x553a8EFa12d333c864c89CB809D68268C836B70a",
        "0x5ae3cB086887A6FB7662eE58Cf1d5113E69bBA62",
        "0x1feF777Fb93Aa45a6Cefcf5507c665b64b301FB3",
        "0x0557D4C04BB994719b087d2950841BF25cf39899"
    ],
}

NOGEM_CONTRACTS_PER_CHAINS = {
    "Arbitrum": {  # ArbitrumRPC
        'refuel'                : '0x2212291025d65D6cFe91De3f0e1a6cAd4dC4AE36',
        'gas_station'           : '0x663f02eb2d47f6993366fa61f8dfa27efbae85d4',
        'HNFT'                  : '0x6d65c9156B7EF63159919Ed130277fb39a4F56b4',
        'HFT'                   : '0x2d71Dde9dba6eF70AA26C0163437D230A25915cA',
        'ONFT'                  : '0x96e1Bf9e743407B909A281210C58cE0990AacEd9',
        'endpoint'              : '0xAa58e77238f0E4A565343a89A79b4aDDD744d649'
    },
    "Arbirtum Nova": {  # Arbitrum_novaRPC
        'refuel'                : '',
        'gas_station'           : '0xe4D8aBB420033F64289048184Bbd1Ae175E578F6',
        'ONFT'                  : '0x7564b019e013d90302BdD6FB6C9763d5989bEd0c',
        'endpoint'              : '0x484c402B0c8254BD555B68827239BAcE7F491023'
    },
    "Base": {  # BaseRPC
        'refuel'                : '0xC2b7ED18184d3EAa08bD03418d2929D452dbd6Fa',
        'HNFT'                  : '0xE80C7830949FF7907885cE4397F41Fe36549a4Cb',
        'HFT'                   : '0x2d71Dde9dba6eF70AA26C0163437D230A25915cA',
        'gas_station'           : '0xFb7EF0BbD8bFB5f129F995FbC34F4D786cCC63CF',
        'ONFT'                  : '0x8D5ba31f120157369ED4474338beA521109B1200',
        'endpoint'              : '0xF882c982a95F4D3e8187eFE12713835406d11840'
    },
    "Linea": {  # LineaRPC
        'refuel'                : '0x2809702F7900748fd579bF7d2B44b17437110cc7',
        'gas_station'           : '0xE73c6F1B6F43142Ea545053DaAB6Fc2c514DfeAA',
        'ONFT'                  : '0xB77F101f3382d55d56B43b2bc6Cf86E3E0d2CDbd',
        'endpoint'              : '0xDB3Bb6D5a8EeEAfc64C66C176900E6B82b23dd5f'
    },
    "Manta": {  # MantaRPC
        'refuel'                : '0x5bF3487c5fE99907A9a0d7f32D05eB3B2B8a0143',
        'gas_station'           : '0xE73c6F1B6F43142Ea545053DaAB6Fc2c514DfeAA',
        'HNFT'                  : '0x100b19e5f7ebd0eb65cb09A5533217D21a1535b6',
        'HFT'                   : '0x2d71Dde9dba6eF70AA26C0163437D230A25915cA',
        'ONFT'                  : '0xa2F3809254dD9Bd7E5c31e7E5D4b423a7d610BeD',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Polygon": {  # PolygonRPC
        'refuel'                : '0xf705B54bAA04A6C3306BD5421A49f9F4DC27c4C4',
        'gas_station'           : '0x2809702f7900748fd579bf7d2b44b17437110cc7',
        'HNFT'                  : '0x4d2bEEABff0DdC5007Cd59B499654d8573Aa306B',
        'HFT'                   : '0x2d71Dde9dba6eF70AA26C0163437D230A25915cA',
        'ONFT'                  : '0xa6ce244C423Af2bCef522fc5Fbc1df28528Da2e0',
        'endpoint'              : '0xa184998eC58dc1dA77a1F9f1e361541257A50CF4'
    },
    "Optimism": {  # OptimismRPC
        'refuel'                : '0x6d594b9fcb39e7e8942b431c0826beeae25ba39a',
        'gas_station'           : '0xE73c6F1B6F43142Ea545053DaAB6Fc2c514DfeAA',
        'HNFT'                  : '0x9e95502466fd3ab0a9C503c344C9d6a2A77F175B',
        'HFT'                   : '0x2d71Dde9dba6eF70AA26C0163437D230A25915cA',
        'ONFT'                  : '0x68217eAd11a77f559E29460a4665257a6A163877',
        'endpoint'              : '0xa2C203d7EF78ed80810da8404090f926d67Cd892'
    },
    "Scroll": {  # ScrollRPC
        'refuel'                : '',
        'gas_station'           : '0x9cE5f55c5CF1EA63D1CB3ac4EfC7FBe07e83916B',
        'HNFT'                  : '0x3bDc0495F96123750B2FF52c7a57Ce25578C4439',
        'HFT'                   : '0x2d71Dde9dba6eF70AA26C0163437D230A25915cA',
        'ONFT'                  : '0x6aa62615C117CEd068093D4c7BFf78289ceA945A',
        'endpoint'              : '0x6E55472109E6aBE4054a8E8b8d9EdFfCb31032C5'
    },
    "Polygon zkEVM": {  # Polygon_ZKEVM_RPC
        'refuel'                : '',
        'gas_station'           : '0xE73c6F1B6F43142Ea545053DaAB6Fc2c514DfeAA',
        'ONFT'                  : '',
        'endpoint'              : '0xb58f5110855fBEF7A715d325D60543E7D4c18143'
    },
    "zkSync": {  # zkSyncEraRPC
        'refuel'                : '',
        'ONFT'                  : '0xBEc36178ff53DEac60B741174057EA7587f35b03',
        'endpoint'              : '0x9b896c0e23220469C7AE69cb4BbAE391eAa4C8da'
    },
    "Zora": {  # ZoraRPC
        'refuel'                : '0xAE3474976AB102077d399f360d695719fd2F1525',
        'gas_station'           : '0xE73c6F1B6F43142Ea545053DaAB6Fc2c514DfeAA',
        'ONFT'                  : '0x1Ba667B038b8fAee90F1E41a84d79A9c8E0837fD',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Ethereum": {  # EthereumRPC
        'refuel'                : '',
        'gas_station'           : '',
        'ONFT'                  : '',
        'endpoint'              : '0x66A71Dcef29A0fFBDBE3c6a460a3B5BC225Cd675'
    },
    "Avalanche": {  # AvalancheRPC
        'refuel'                : '0x1Ad837f828be78C4CF90BCe5426d592f7e8c1a6f',
        'gas_station'           : '0x9020Cb8D5516497F25e5Cd0877f563fe9Ed2daEa',
        'HNFT'                  : '0xC9b73b0214e644ca112ffCeAF7fDc150c6e5A310',
        'HFT'                   : '0x2d71Dde9dba6eF70AA26C0163437D230A25915cA',
        'ONFT'                  : '0xe25D5dCfA8Be6e7933A1335d1A23FB3A67f1a16A',
        'endpoint'              : '0x3c2269811836af69497E5F486A85D7316753cf62'
    },
    "BNB Chain": {  # BSC_RPC
        'refuel'                : '0x9f865ccCbb885d3770b2786cEB5c727Eb31e47ed',
        'gas_station'           : '0xE7Dba4c592114f821822a7e9eA490541C6121Abb',
        'HNFT'                  : '0x4394a538E1325F5214DdC113293f87f4E8897b09',
        'HFT'                   : '0x2d71Dde9dba6eF70AA26C0163437D230A25915cA',
        'ONFT'                  : '0xcd5cA2b4a23046f3c1c9c5ABFe9ED8737b77BFBd',
        'endpoint'              : '0x3c2269811836af69497E5F486A85D7316753cf62'
    },
    "Moonbeam": {  # MoonbeamRPC
        'refuel'                : '',
        'gas_station'           : '0x36c83bf151078404bf4927AeF40C14FD862B88e4',
        'HNFT'                  : '0xfa0aCcf6386942e7aC8Ab00Fc7C91f8b641AfA79',
        'HFT'                   : '0x2d71Dde9dba6eF70AA26C0163437D230A25915cA',
        'ONFT'                  : '',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Harmony": {  # HarmonyRPC
        'refuel'                : '',
        'gas_station'           : '0x36c83bf151078404bf4927AeF40C14FD862B88e4',
        'ONFT'                  : '',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Telos": {  # TelosRPC
        'refuel'                : '0x0A7a3C0f088fdfBe92Fabdc5CB0279faC07CA553',
        'gas_station'           : '0xE73c6F1B6F43142Ea545053DaAB6Fc2c514DfeAA',
        'ONFT'                  : '0x92E5b93af8fB4eE8b1db0ac8dF85a6Bfa15651eE',
        'endpoint'              : '0x66A71Dcef29A0fFBDBE3c6a460a3B5BC225Cd675'
    },
    "Celo": {  # CeloRPC
        'refuel'                : '0xfa0aCcf6386942e7aC8Ab00Fc7C91f8b641AfA79',
        'gas_station'           : '0xA991694fd6d9DA350cdFD6D3f9c8E125Ce5B3185',
        'HNFT'                  : '0xD5B53bA6D596C4C47060Aca2963C0EDD2Df8e6e4',
        'HFT'                   : '0x2d71Dde9dba6eF70AA26C0163437D230A25915cA',
        'ONFT'                  : '0xEE9E828C04bA68c28eD7B29425380A2Ff8b5e3Ae',
        'endpoint'              : '0x3A73033C0b1407574C76BdBAc67f126f6b4a9AA9'
    },
    "Gnosis": {  # GnosisRPC
        'refuel'                : '0x92E5b93af8fB4eE8b1db0ac8dF85a6Bfa15651eE',
        'gas_station'           : '0xFb7EF0BbD8bFB5f129F995FbC34F4D786cCC63CF',
        'HNFT'                  : '0x51332f35F3D29c8d137fA5C8E0C2ce4Afbfca498',
        'HFT'                   : '0x2d71Dde9dba6eF70AA26C0163437D230A25915cA',
        'ONFT'                  : '0x612361f307751BE1B7B73cE6Af4d613754a64C2B',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "CoreDAO": {  # CoreRPC
        'refuel'                : '0xe4D8aBB420033F64289048184Bbd1Ae175E578F6',
        'gas_station'           : '0xFb7EF0BbD8bFB5f129F995FbC34F4D786cCC63CF',
        'ONFT'                  : '0x1f55dbaE710b9Ed5b1cBc8d4F5F4dfb6d966a2A2',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "TomoChain": {  # TomoChainRPC
        'refuel'                : '',
        'gas_station'           : '',
        'ONFT'                  : '',
        'endpoint'              : ''
    },
    "Conflux": {  # ConfluxRPC
        'refuel'                : '0x8c1943A30e5A0072903FDb90BF424Bdb7095C80E',
        'gas_station'           : '0xFb7EF0BbD8bFB5f129F995FbC34F4D786cCC63CF',
        'ONFT'                  : '0x36c83bf151078404bf4927AeF40C14FD862B88e4',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Orderly": {  # OrderlyRPC
        'refuel'                : '0xd575825c903AAc4D04439600B6d0d22f0E3a9367',
        'gas_station'           : '0x36c83bf151078404bf4927AeF40C14FD862B88e4',
        'ONFT'                  : '0x59FBcA19b8d71FC264Bf2D97506e6a37E64AF510',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Horizen EON": {  # HorizenRPC
        'refuel'                : '',
        'gas_station'           : '0xE1ba542dBCB25351557F4Cc7dFa743877A38a1e0',
        'ONFT'                  : '',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Metis": {  # MetisRPC
        'refuel'                : '',
        'gas_station'           : '0xFb7EF0BbD8bFB5f129F995FbC34F4D786cCC63CF',
        'ONFT'                  : '0x13e541AD6987572B7A586b46Fb95b9f0fce78230',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Astar": {  # AstarRPC
        'refuel'                : '0xA991694fd6d9DA350cdFD6D3f9c8E125Ce5B3185',
        'gas_station'           : '0xE73c6F1B6F43142Ea545053DaAB6Fc2c514DfeAA',
        'ONFT'                  : '0x7D8083C47DE0CB33180e1B130F6de78a41AeBe75',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "OpBNB": {  # OpBNB_RPC
        'refuel'                : '0xCeeB6BF11C6160D7cA3F531ce49329Ee82bed6d7',
        'gas_station'           : '0xAc9319982Bf2E64e4C41146c912a35F237180375',
        'ONFT'                  : '0xCcb4cA93560994b6F2760B99d8fCe6Aeddd9fc00',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Mantle": {  # MantleRPC
        'refuel'                : '0x6D594b9FCb39E7E8942b431C0826BEeaE25bA39a',
        'gas_station'           : '0xd8c12333aC7b6e24416F9175E242bD302f4dFd19',
        'ONFT'                  : '0xE73c6F1B6F43142Ea545053DaAB6Fc2c514DfeAA',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Moonriver": {  # MoonriverRPC
        'refuel'                : '0x7D8083C47DE0CB33180e1B130F6de78a41AeBe75',
        'gas_station'           : '0xE73c6F1B6F43142Ea545053DaAB6Fc2c514DfeAA',
        'ONFT'                  : '',
        'endpoint'              : '0x7004396C99D5690da76A7C59057C5f3A53e01704'
    },
    "Klaytn": {  # KlaytnRPC
        'refuel'                : '0x6d594b9fcb39e7e8942b431c0826beeae25ba39a',
        'gas_station'           : '0x5359a9a6351147Ba66a2C750c746743d73BdBeDD',
        'ONFT'                  : '0x36c83bf151078404bf4927aef40c14fd862b88e4',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Kava": {  # KavaRPC
        'refuel'                : '0x2212291025d65D6cFe91De3f0e1a6cAd4dC4AE36',
        'gas_station'           : '0x5E4bca80c6af462DE4d7678c59B558873f0049d0',
        'ONFT'                  : '0xfa0aCcf6386942e7aC8Ab00Fc7C91f8b641AfA79',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Fantom": {  # FantomRPC
        'refuel'                : '0xa6ce244C423Af2bCef522fc5Fbc1df28528Da2e0',
        'gas_station'           : '0x6D594b9FCb39E7E8942b431C0826BEeaE25bA39a',
        'ONFT'                  : '0x076FC64046E50A78267563470A159B6AbDDe9192',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Aurora": {  # AuroraRPC
        'refuel'                : '0x6D594b9FCb39E7E8942b431C0826BEeaE25bA39a',
        'gas_station'           : '0xFb7EF0BbD8bFB5f129F995FbC34F4D786cCC63CF',
        'ONFT'                  : '0x01fC53d4C349704970D3Cb3B25505B9E4452AC42',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Canto": {  # CantoRPC
        'refuel'                : '',
        'gas_station'           : '',
        'ONFT'                  : '',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "DFK": {  # DFK_RPC
        'refuel'                : '',
        'gas_station'           : '',
        'ONFT'                  : '',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Fuse": {  # FuseRPC
        'refuel'                : '0xE7Dba4c592114f821822a7e9eA490541C6121Abb',
        'gas_station'           : '0xFb7EF0BbD8bFB5f129F995FbC34F4D786cCC63CF',
        'ONFT'                  : '0x1Ba667B038b8fAee90F1E41a84d79A9c8E0837fD',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Goerli": {  # GoerliRPC
        'refuel'                : '',
        'gas_station'           : '',
        'ONFT'                  : '',
        'endpoint'              : ''
    },
    "Meter": {  # MeterRPC
        'refuel'                : '',
        'gas_station'           : '',
        'ONFT'                  : '',
        'endpoint'              : '0xa3a8e19253Ab400acDac1cB0eA36B88664D8DedF'
    },
    "OKX Chain": {  # OKX_RPC
        'refuel'                : '0x5bF3487c5fE99907A9a0d7f32D05eB3B2B8a0143',
        'gas_station'           : '0xE73c6F1B6F43142Ea545053DaAB6Fc2c514DfeAA',
        'ONFT'                  : '0xA194aa46612FEF6C3263986C02652e54b5Fd780c',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Shimmer": {  # ShimmerRPC
        'refuel'                : '',
        'gas_station'           : '',
        'ONFT'                  : '',
        'endpoint'              : '0xC1b15d3B262bEeC0e3565C11C9e0F6134BdaCB36'
    },
    "Tenet": {  # TenetRPC
        'refuel'                : '0x711b03d666D4D0DbDa70aB52a269Ef8B0FfAb443',
        'gas_station'           : '0xFb7EF0BbD8bFB5f129F995FbC34F4D786cCC63CF',
        'ONFT'                  : '0x61b9aaFB29fE7391fa29c61d9cD5BcB9dE1e07C6',
        'endpoint'              : '0x2D61DCDD36F10b22176E0433B86F74567d529aAa'
    },
    "XPLA": {  # XPLA_RPC
        'refuel'                : '0x59FBcA19b8d71FC264Bf2D97506e6a37E64AF510',
        'gas_station'           : '0xE73c6F1B6F43142Ea545053DaAB6Fc2c514DfeAA',
        'ONFT'                  : '0xfED33D64740122fB090352eAf7B497D092fC2A0f',
        'endpoint'              : '0xC1b15d3B262bEeC0e3565C11C9e0F6134BdaCB36'
    },
    "LootChain": {  # LootChainRPC
        'refuel'                : '0xAc9319982Bf2E64e4C41146c912a35F237180375',
        'gas_station'           : '0xE1ba542dBCB25351557F4Cc7dFa743877A38a1e0',
        'ONFT'                  : '0x34EA96D233aFA4083eD7da9EA30893094af82F21',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Beam": {  # BeamRPC
        'refuel'                : '0xFb7EF0BbD8bFB5f129F995FbC34F4D786cCC63CF',
        'gas_station'           : '',
        'ONFT'                  : '0xa5A3C7719590F675552b3D257947AA2A5bfbC4db',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "InEVM": {   # InEVM_RPC
        'refuel'                : '',
        'gas_station'           : '',
        'ONFT'                  : '',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Rarible": {   # RaribleRPC
        'refuel'                : '0x982Db01501C862eCC8f1C9BDF4A48d7742C822Fa',
        'gas_station'           : '0x77DbDd3c9Ea256F7570ec754f2819f1b9cfA6185',
        'ONFT'                  : '0xE47b05F2026a82048caAECf5caE58e5AAE2405eA',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    }
}

L2PASS_CONTRACTS_PER_CHAINS = {
    "Arbitrum": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xAa58e77238f0E4A565343a89A79b4aDDD744d649'
    },
    "Arbitrum Nova": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x484c402B0c8254BD555B68827239BAcE7F491023'
    },
    "Base": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xF882c982a95F4D3e8187eFE12713835406d11840'
    },
    "Linea": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xDB3Bb6D5a8EeEAfc64C66C176900E6B82b23dd5f'
    },
    "Manta": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Polygon": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x042002711e4d7A7Fc486742a85dBf096beeb0420',
        'endpoint'              : '0xa184998eC58dc1dA77a1F9f1e361541257A50CF4'
    },
    "Optimism": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xa2C203d7EF78ed80810da8404090f926d67Cd892'
    },
    "Scroll": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x6E55472109E6aBE4054a8E8b8d9EdFfCb31032C5'
    },
    "Polygon zkEVM": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xb58f5110855fBEF7A715d325D60543E7D4c18143'
    },
    "zkSync": {
        'refuel'                : '',
        'ONFT'                  : '0x8582525114212C2815F13d96Ed5158553287a166',
        'endpoint'              : '0x9b896c0e23220469C7AE69cb4BbAE391eAa4C8da'
    },
    "Zora": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Ethereum": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x66A71Dcef29A0fFBDBE3c6a460a3B5BC225Cd675'
    },
    "Avalanche": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x3c2269811836af69497E5F486A85D7316753cf62'
    },
    "BNB Chain": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x3c2269811836af69497E5F486A85D7316753cf62'
    },
    "Moonbeam": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Harmony": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Telos": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x66A71Dcef29A0fFBDBE3c6a460a3B5BC225Cd675'
    },
    "Celo": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x3A73033C0b1407574C76BdBAc67f126f6b4a9AA9'
    },
    "Gnosis": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Core": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "TomoChain": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : ''
    },
    "Conflux": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Orderly": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Horizen": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Metis": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Astar": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "OpBNB": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Mantle": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Moonriver": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x7004396C99D5690da76A7C59057C5f3A53e01704'
    },
    "Klaytn": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Kava": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Fantom": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Aurora": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Canto": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "DFK": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Fuse": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Goerli": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : ''
    },
    "Meter": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xa3a8e19253Ab400acDac1cB0eA36B88664D8DedF'
    },
    "OKX Chain": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Shimmer": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xC1b15d3B262bEeC0e3565C11C9e0F6134BdaCB36'
    },
    "Tenet": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0x2D61DCDD36F10b22176E0433B86F74567d529aAa'
    },
    "XPLA": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222',
        'endpoint'              : '0xC1b15d3B262bEeC0e3565C11C9e0F6134BdaCB36'
    },
    "LootChain": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0xE47b05F2026a82048caAECf5caE58e5AAE2405eA',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Beam": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0xE47b05F2026a82048caAECf5caE58e5AAE2405eA',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "InEVM": {
        'refuel'                : '0x222228060E7Efbb1D78BB5D454581910e3922222',
        'gas_station'           : '0x0000c74e9931C7D6c1a6e811fE96a8a808E06969',
        'ONFT'                  : '0xE47b05F2026a82048caAECf5caE58e5AAE2405eA',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    }
}

MERKLY_HYPERLANE_INFO = {
    'Manta': ('0x75DAa6Eb3748C33b5fB3716465DAD9658BE42A8D', 169),
    'Optimism': ('0xC110E7FAA95680c79937CCACa3d1caB7902bE25e', 10),
    'BNB Chain': ('0xae4789D7C596fdED0e135Bca007152c87a0756f5', 56),
    'Arbitrum':  ('0x233888F5Dc1d3C0360b559aBc029675290DAFa70', 42161),
    'Polygon':  ('0x0cb0354E9C51960a7875724343dfC37B93d32609', 137),
    'Base':  ('0x0cb0354E9C51960a7875724343dfC37B93d32609', 8453),
    'Scroll':  ('0xc0faBF14f8ad908b2dCE4C8aA2e7c1a6bD069957', 534352),
    'Linea':  ('0x8F2161c83F46B46628cb591358dE4a89A63eEABf', 59144),
    # "gnosis":"0x98Ee7E8f0A0D18F393805cf99A56ce6B33ea1B21",
    # "mantle":"0xf4368751f99127F052AFa993aEc3C6393AcA5466",
    "Zora": ("0x8028d4f11d10730B12Ae011474F9db8140F112F4", 7777777),
    # "ethereum":"0x64D9b639aE85a1e436c1752889c5C40699f3887C",
    # "manta pacific":"0x75DAa6Eb3748C33b5fB3716465DAD9658BE42A8D",
    # "mode":"0x9970cB23f10dBd95B8A3E643f3A6A6ABB6f3cB9b",
    # "x layer":"0x444791b5cA0E0BdC2De93467f430fbe925b35487",
    # "ancient8":"0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218",
    # "zetachain":"0xe35030B407C96C037190B63646AC1Eb34F43Cc2b",
    # "redstone":"0x49bF21531991742b0c1797230758992769771CcD",
    # "sei":"0x97aa7b7501FA0fe66649DE7394b9794fa40aEF02",
    # "taiko":"0xb08ab8cBd0226D8335fB0Cb88ce47FAfC9C47096",
    # "bob":"0xEF62b433Ca3AC8b151c4a255de3eD3dA4e60AdD2",
    # "world chain":"0x6E55472109E6aBE4054a8E8b8d9EdFfCb31032C5",
    # "zircuit":"0xA5f471A19fdB367Ea80c4c82ecd30eA94090d549",
}

RENZO_BRIDGE_INFO = {
    'Arbitrum': ('0xB26bBfC6d1F469C821Ea25099017862e7368F4E8', 42161),
    'Optimism': ('0xacEB607CdF59EB8022Cc0699eEF3eCF246d149e2', 10),
    'Base': ('0x2552516453368e42705D791F674b312b8b87CD9e', 8453),
    'Blast': ('0x486b39378f99f073A3043C6Aabe8666876A8F3C5', 81457),
    'BNB Chain': ('0xE00C6185a5c19219F1FFeD213b4406a254968c26', 56),
    'Mode': ('0xC59336D8edDa9722B4f1Ec104007191Ec16f7087', 34443),
    'Linea': ('0xC59336D8edDa9722B4f1Ec104007191Ec16f7087', 59144),
    'Ethereum': ('0xC59336D8edDa9722B4f1Ec104007191Ec16f7087', 1),
    # 'Fraxtal': ('0x3aE8635A4D581d40a6Edfb3f2ED480f9532994F5', 0),  # ChainId needed
    # 'Zircuit': ('0x2552516453368e42705D791F674b312b8b87CD9e', 0)  # ChainId needed
}

MERKLY_NFT_WORMHOLE_INFO = {
    'Optimism': ('0xE4c8D341570ed4e23798e238a92673EbaB787775', 0.0003, 24),
    'Celo': ('0x5C526129887cB4053302Ea6Acd1e203106fcBB96', 1.4, 14),
    'Avalanche': ('0x217b089caAB28D6F577D96189dE2716b5Ab6a07A', 0.028, 6),
    'Klaytn': ('0x9b316174D37d158148aB6F2A6AE0c61739cA785E', 1.3, 13),
    'BNB Chain': ('0x451d8bA3fcF9F5d0549099B2834198F14554Bd6e', 0.0019, 4),
    'Moonbeam': ('0x8958311Ded31bf6Fd3993d52DD064f79e26a7336', 1.4, 16),
    'Fantom': ('0x2f6c1Dfe8e7337e1cE90f2ba57f6eE1e60c1F772', 1.35, 10),
    'Arbitrum': ('0x353b31d68254B380fd2966b2E84131dBE1D486d5', 0.0003, 23),
    'Polygon': ('0x28527ebb5c97bb11abd6c2c74d24045b4e4865ef', 0.6, 5),
    'Base': ('0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218', 0.0003, 30),
    'Ethereum': ('0xF80cf52922B512B22D46aA8916BD7767524305d9', 0.0003, 2),
}

MERKLY_TOKENS_WORMHOLE_INFO = {
   'Optimism': ('0x660991a4e549B2032dCAF781b85a8FE1dF176BB6', 0.0000021, 24),
   'Celo': ('0x5c17938e1317a05682CC7026F63C0396C84706C8', 0.0089485, 14),
   'Avalanche': ('0x28527ebb5C97BB11aBd6c2C74D24045b4e4865eF', 0.00033, 6),
   'Klaytn': ('0x9AA7AC03CAA440c392B9C9D25a728b429E172a92', 0.027, 13),
   'BNB Chain': ('0x41cc0c5Dbd2539191945f395B17cEb597BCE1C9A', 0.0000201775, 4),
   'Moonbeam': ('0x3cc4313f8e5E413a54095D48DB1869f80f929056', 0.02, 16),
   'Fantom': ('0xCd8EAE908E27b9046ca7845DA22f6d3cdf367588', 0.018, 10),
   'Arbitrum': ('0x456A5d70f5E1f23ec5B074144477817447551439', 0.0000021, 23),
   'Polygon': ('0x81143d533675D79b490Bb3B3a00421b1CAEce3D9', 0.0063, 5),
   'Base': ('0x2e3e4Cc4c99fEaac88097b1Bc279c7e372BfBdFE', 0.0000021, 30),
   'Ethereum': ('0xac998bda5B8bc9483c90eFBe8B70E11D3C0E8f6f', 0.0000021, 2),
}

MERKLY_CONTRACTS_PER_CHAINS = {
    "Arbitrum": {
        'refuel'                : '0x4Ae8CEBcCD7027820ba83188DFD73CCAD0A92806',
        'p_refuel'              : '0x85Fd2DA31262d26471c738Ce357a3767635A0956',
        'ONFT'                  : '0xAa58e77238f0E4A565343a89A79b4aDDD744d649',
        'WNFT'                  : '0x353b31d68254B380fd2966b2E84131dBE1D486d5',
        'PNFT'                  : '0xEF62b433Ca3AC8b151c4a255de3eD3dA4e60AdD2',
        'HNFT'                  : '0x7daC480d20f322D2ef108A59A465CCb5749371c4',
        'WOFT'                  : '0x456A5d70f5E1f23ec5B074144477817447551439',
        'HOFT'                  : '0xFD34afDFbaC1E47aFC539235420e4bE4A206f26D',
        'endpoint'              : '0xAa58e77238f0E4A565343a89A79b4aDDD744d649'
    },
    "Arbitrum Nova": {
        'refuel'                : '0xB6789dACf323d60F650628dC1da344d502bC41E3',
        'p_refuel'              : '0xc9857E3e87054d38c6b76E48a567f0F50A878076',
        'ONFT'                  : '0x484c402B0c8254BD555B68827239BAcE7F491023',
        'PNFT'                  : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'endpoint'              : '0x484c402B0c8254BD555B68827239BAcE7F491023'
    },
    "Base": {
        'refuel'                : '0x6bf98654205B1AC38645880Ae20fc00B0bB9FFCA',
        'p_refuel'              : '0xeFD942537D53003A6d73Ce02562A002DcD0D5663',
        'ONFT'                  : '0xF882c982a95F4D3e8187eFE12713835406d11840',
        'WNFT'                  : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'PNFT'                  : '0xbA32747EF144B5eA6a01A18f7756034e23C998ae',
        'HNFT'                  : '0x7dac480d20f322d2ef108a59a465ccb5749371c4',
        'WOFT'                  : '0x2e3e4Cc4c99fEaac88097b1Bc279c7e372BfBdFE',
        'HOFT'                  : '0x5454cF5584939f7f884e95DBA33FECd6D40B8fE2',
        'endpoint'              : '0xF882c982a95F4D3e8187eFE12713835406d11840'
    },
    "Linea": {
        'refuel'                : '0xc9B753d73B17DDb5E87093ff04A9e31845a43af0',
        'p_refuel'              : '0x87afd765be55c44DC2D61f16d9b02b452292D497',
        'ONFT'                  : '0xDB3Bb6D5a8EeEAfc64C66C176900E6B82b23dd5f',
        'HOFT'                  : '0xc92A74918Ebb35CA91d7029b7528e0b49fA60B47',
        'HNFT'                  : '0xC6EDe374Df7763ad70166C4d85d8066A8fb8D272',
        'PNFT'                  : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'endpoint'              : '0xDB3Bb6D5a8EeEAfc64C66C176900E6B82b23dd5f'
    },
    "Manta": {
        'refuel'                : '0xc62C04F7CD4B47729027c138FABD99aFA5db1222',
        'ONFT'                  : '0xc072c3EbAf165955C5aAd2DbB4293f771de6dbd3',
        'HNFT'                  : '0xb1d2B9446A9d1550e8d409C0F9745c5A2f10D332',
        'HOFT'                  : '0xc7a66e3A9d1a84dC60f8a630C3eC3D84aCFBE5EC',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Polygon": {
        'refuel'                : '0x0E1f20075C90Ab31FC2Dd91E536e6990262CF76d',
        'p_refuel'              : '0xb1d2B9446A9d1550e8d409C0F9745c5A2f10D332',
        'ONFT'                  : '0xa184998eC58dc1dA77a1F9f1e361541257A50CF4',
        'WNFT'                  : '0x28527ebb5C97BB11aBd6c2C74D24045b4e4865eF',
        'PNFT'                  : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'HNFT'                  : '0x7daC480d20f322D2ef108A59A465CCb5749371c4',
        'WOFT'                  : '0x81143d533675D79b490Bb3B3a00421b1CAEce3D9',
        'HOFT'                  : '0x574E69C50e7D13B3d1B364BF0D48285A5aE2dF56',
        'endpoint'              : '0xa184998eC58dc1dA77a1F9f1e361541257A50CF4'
    },
    "Optimism": {
        'refuel'                : '0xD7bA4057f43a7C4d4A34634b2A3151a60BF78f0d',
        'p_refuel'              : '0x1812d05671EefA040ac605a0198476dEd081d520',
        'ONFT'                  : '0xa2C203d7EF78ed80810da8404090f926d67Cd892',
        'WNFT'                  : '0xE4c8D341570ed4e23798e238a92673EbaB787775',
        'PNFT'                  : '0xAFa5f9313F1F2b599173f24807a882F498Be118c',
        'HNFT'                  : '0x2a5c54c625220cb2166C94DD9329be1F8785977D',
        'WOFT'                  : '0x660991a4e549B2032dCAF781b85a8FE1dF176BB6',
        'HOFT'                  : '0x32F05f390217990404392a4DdAF39D31Db4aFf77',
        'endpoint'              : '0xa2C203d7EF78ed80810da8404090f926d67Cd892'
    },
    "Scroll": {
        'refuel'                : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'ONFT'                  : '0x6E55472109E6aBE4054a8E8b8d9EdFfCb31032C5',
        'PNFT'                  : '0x61bb3852947a370946AbdBA8fa9cF45ec472F83f',
        'HNFT'                  : '0x7daC480d20f322D2ef108A59A465CCb5749371c4',
        'HOFT'                  : '0x904550e0D182cd4aEe0D305891c666a212EC8F01',
        'endpoint'              : '0x6E55472109E6aBE4054a8E8b8d9EdFfCb31032C5'
    },
    "Polygon zkEVM": {
        'refuel'                : '0xE62d19Df93D84b3552498260188D19A772296B10',
        'ONFT'                  : '0xb58f5110855fBEF7A715d325D60543E7D4c18143',
        'HNFT'                  : '0x7daC480d20f322D2ef108A59A465CCb5749371c4',
        'HOFT'                  : '0x46B4eDaA761eF8d2934e9F7AAf32B5Bf2C9C9F67',
        'endpoint'              : '0xb58f5110855fBEF7A715d325D60543E7D4c18143'
    },
    "zkSync": {
        'refuel'                : '0x5673B6e6e51dE3479B8deB22dF46B12308db5E1e',
        'ONFT'                  : '0x6dd28C2c5B91DD63b4d4E78EcAC7139878371768',
        'endpoint'              : '0x9b896c0e23220469C7AE69cb4BbAE391eAa4C8da'
    },
    "Zora": {
        'refuel'                : '0x461fcCF240CA4884Cc5413a5742F1bC56fAf7A0C',
        'ONFT'                  : '0xFFd57B46BD670B0461c7C3EBBaEDC4CdB7c4FB80',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Ethereum": {
        'refuel'                : '0xAFa5f9313F1F2b599173f24807a882F498Be118c',
        'ONFT'                  : '0x6f6aE8851a460406bBB3c929a415d2Df9305AcD5',
        'WNFT'                  : '0xF80cf52922B512B22D46aA8916BD7767524305d9',
        'PNFT'                  : '0x41Ca0f2A9a3fE8Aa15135574C37E3e7083d2CE7e',
        'HNFT'                  : '0x7daC480d20f322D2ef108A59A465CCb5749371c4',
        'WOFT'                  : '0xac998bda5B8bc9483c90eFBe8B70E11D3C0E8f6f',
        'HOFT'                  : '0xf3D41b377c93fA5C3b0071966f1811c5063fAD40',
        'endpoint'              : '0x66A71Dcef29A0fFBDBE3c6a460a3B5BC225Cd675'
    },
    "Avalanche": {
        'refuel'                : '0x5C9BBE51F7F19f8c77DF7a3ADa35aB434aAA86c5',
        'p_refuel'              : '0xA7512E71869fddc26aCDb0BAddd3cBBd79f9D238',
        'ONFT'                  : '0xE030543b943bdCd6559711Ec8d344389C66e1D56',
        'WNFT'                  : '0x217b089caAB28D6F577D96189dE2716b5Ab6a07A',
        'PNFT'                  : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'HNFT'                  : '0x7daC480d20f322D2ef108A59A465CCb5749371c4',
        'WOFT'                  : '0x28527ebb5C97BB11aBd6c2C74D24045b4e4865eF',
        'HOFT'                  : '0x904550e0D182cd4aEe0D305891c666a212EC8F01',
        'endpoint'              : '0x3c2269811836af69497E5F486A85D7316753cf62'
    },
    "BNB Chain": {
        'refuel'                : '0xeF1eAE0457e8D56A003d781569489Bc5466E574b',
        'p_refuel'              : '0x717b00Eacc4e3D028B4B5221743973C752F9f9a2',
        'ONFT'                  : '0xFDc9018aF0E37AbF89233554C937eB5068127080',
        'WNFT'                  : '0x451d8bA3fcF9F5d0549099B2834198F14554Bd6e',
        'PNFT'                  : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'HNFT'                  : '0xf3D41b377c93fA5C3b0071966f1811c5063fAD40',
        'WOFT'                  : '0x41cc0c5Dbd2539191945f395B17cEb597BCE1C9A',
        'HOFT'                  : '0x7b4f475d32f9c65de1834A578859F9823bE3c5Cf',
        'endpoint'              : '0x3c2269811836af69497E5F486A85D7316753cf62'
    },
    "Moonbeam": {
        'refuel'                : '0x671861008497782F7108D908D4dF18eBf9598b82',
        'p_refuel'              : '0x9D94295C22395b41326d80c371cC1A0A546b9a81',
        'ONFT'                  : '0x766b7aC73b0B33fc282BdE1929db023da1fe6458',
        'WNFT'                  : '0x8958311Ded31bf6Fd3993d52DD064f79e26a7336',
        'PNFT'                  : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'HNFT'                  : '0x7daC480d20f322D2ef108A59A465CCb5749371c4',
        'WOFT'                  : '0x3cc4313f8e5E413a54095D48DB1869f80f929056',
        'HOFT'                  : '0xf3D41b377c93fA5C3b0071966f1811c5063fAD40',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Harmony": {
        'refuel'                : '0x671861008497782F7108D908D4dF18eBf9598b82',
        'ONFT'                  : '0x885ef5813E46ab6EFb10567b50b77aAAD4d258ce',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Telos": {
        'refuel'                : '0x2935a2804E4F902E722B64C51a831Bce2526a576',
        'ONFT'                  : '0x85b1C838E38203E420d59ad84d2f53E14b2e50C3',
        'endpoint'              : '0x66A71Dcef29A0fFBDBE3c6a460a3B5BC225Cd675'
    },
    "Celo": {
        'refuel'                : '0xC20A842e1Fc2681920C1A190552A2f13C46e7fCF',
        'p_refuel'              : '0x719ceF05ea6F14De274DB6c99BB35e854c29FB38',
        'ONFT'                  : '0xE33519C400B8F040E73aeDa2f45DfDD4634A7cA0',
        'WNFT'                  : '0x5C526129887cB4053302Ea6Acd1e203106fcBB96',
        'PNFT'                  : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'HNFT'                  : '0x7f4CFDf669d7a5d4Adb05917081634875E21Df47',
        'WOFT'                  : '0x5c17938e1317a05682CC7026F63C0396C84706C8',
        'HOFT'                  : '0xad8676147360dBc010504aB69C7f1b1877109527',
        'endpoint'              : '0x3A73033C0b1407574C76BdBAc67f126f6b4a9AA9'
    },
    "Gnosis": {
        'refuel'                : '0x556F119C7433b2232294FB3De267747745A1dAb4',
        'p_refuel'              : '0x81143d533675D79b490Bb3B3a00421b1CAEce3D9',
        'ONFT'                  : '0xb58f5110855fBEF7A715d325D60543E7D4c18143',
        'PNFT'                  : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'HNFT'                  : '0x7dac480d20f322d2ef108a59a465ccb5749371c4',
        'HOFT'                  : '0xFD34afDFbaC1E47aFC539235420e4bE4A206f26D',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Core": {
        'refuel'                : '0xa513F61Bc23F0eB1FC0aC4d9dab376d79bC7F3cB',
        'p_refuel'                : '0x81143d533675D79b490Bb3B3a00421b1CAEce3D9',
        'ONFT'                  : '0xCA230856343C300f0cc2Bd77C89F0fCBeDc45B0f',
        'PNFT'                  : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "TomoChain": {
        'refuel'                : '0x457Fd60FFA26576E226252092c98921f12E90FbB',
        'ONFT'                  : '0xE47b05F2026a82048caAECf5caE58e5AAE2405eA',
        'endpoint'              : ''
    },
    "Conflux": {
        'refuel'                : '0xE47b05F2026a82048caAECf5caE58e5AAE2405eA',
        'ONFT'                  : '0xDB3Bb6D5a8EeEAfc64C66C176900E6B82b23dd5f',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Orderly": {
        'refuel'                : '0x6f6aE8851a460406bBB3c929a415d2Df9305AcD5',
        'ONFT'                  : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Horizen": {
        'refuel'                : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'ONFT'                  : '0x6E55472109E6aBE4054a8E8b8d9EdFfCb31032C5',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Metis": {
        'refuel'                : '0xF450A7b8abfc99D1cDEf6656163399aD762d51Cc',
        'p_refuel'                : '0x0DC20f0DB970BfB1bB688C3d68Ea6251727D919c',
        'ONFT'                  : '0x2E228120c0AF2dE3A74D744B25B24D1fb28CE5B4',
        'PNFT'                  : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Astar": {
        'refuel'                : '0x4fc0D96f3d70b4D9b75671Ab92e7Be01CaBE3863',
        'ONFT'                  : '0xc072c3EbAf165955C5aAd2DbB4293f771de6dbd3',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "OpBNB": {
        'refuel'                : '0x457Fd60FFA26576E226252092c98921f12E90FbB',
        'ONFT'                  : '0xE47b05F2026a82048caAECf5caE58e5AAE2405eA',
        'PNFT'                  : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Mantle": {
        'refuel'                : '0xE7D454d096d38b22e0C30470e7FB20B1B2aCf70D',
        'p_refuel'              : '0xc011Bc0aec1eA0f2A85553C4eBc23fe75F2E1F32',
        'ONFT'                  : '0x5200543580e7ad49FBCb4690c4556D3a6A022584',
        'PNFT'                  : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Moonriver": {
        'refuel'                : '0xd379c3D0930d70022B3C6EBA8217e4B990705540',
        'ONFT'                  : '0x97337A9710BEB17b8D77cA9175dEFBA5e9AFE62e',
        'endpoint'              : '0x7004396C99D5690da76A7C59057C5f3A53e01704'
    },
    "Klaytn": {
        'refuel'                : '0x79DB0f1A83f8e743550EeB5DD5B0B83334F2F083',
        'ONFT'                  : '0xD02FFAe68d902453b44a9e45Dc257AcA54fB88b2',
        'WNFT'                  : '0x9b316174D37d158148aB6F2A6AE0c61739cA785E',
        'WOFT'                  : '0x9AA7AC03CAA440c392B9C9D25a728b429E172a92',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Kava": {
        'refuel'                : '0x4c24Ba5177365b4c0eBae62b31945d830a858673',
        'ONFT'                  : '0x04866796aabB6B58e6bC4d91A2aE99105b2C58AE',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Fantom": {
        'refuel'                : '0xF56605276cefffe32DFD8B6bF80B93c2A6840136',
        'p_refuel'                : '0x57fFC973Fe8bc128a340202506b343eb9c8e9A16',
        'ONFT'                  : '0x97337A9710BEB17b8D77cA9175dEFBA5e9AFE62e',
        'WNFT'                  : '0x2f6c1Dfe8e7337e1cE90f2ba57f6eE1e60c1F772',
        'PNFT'                  : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'WOFT'                  : '0xCd8EAE908E27b9046ca7845DA22f6d3cdf367588',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Aurora": {
        'refuel'                : '0xf1CD5b12211664FFaf62Af7E5E5C27b1b558aBa2',
        'ONFT'                  : '0xc62C04F7CD4B47729027c138FABD99aFA5db1222',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "Canto": {
        'refuel'                : '0x4c24Ba5177365b4c0eBae62b31945d830a858673',
        'ONFT'                  : '0x426A8Dc7263A439e92972eE2200DA21EC6cEEcfa',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "DFK": {
        'refuel'                : '0x457Fd60FFA26576E226252092c98921f12E90FbB',
        'ONFT'                  : '0xf1A3BCb8c74aA8ef255E0a358d98a9E2b4A97A59',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Fuse": {
        'refuel'                : '0xf6b88C4a86965170dd42DBB8b53e790B3490b912',
        'ONFT'                  : '0xFFd57B46BD670B0461c7C3EBBaEDC4CdB7c4FB80',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Goerli": {
        'refuel'                : '0x95716171f7737CB8D387c621999589bDD04E6A35',
        'ONFT'                  : '0x885ef5813E46ab6EFb10567b50b77aAAD4d258ce',
        'endpoint'              : ''
    },
    "Meter": {
        'refuel'                : '0xB6c5e0d2ffC3Fc80c8D3F5A8b86b7A796A2c5782',
        'ONFT'                  : '0xd81A2E87232b4FDd27FBE16107D8dEAAa2D14181',
        'endpoint'              : '0xa3a8e19253Ab400acDac1cB0eA36B88664D8DedF'
    },
    "OKX Chain": {
        'refuel'                : '0x148CaF6FfBaBa15F35deE7e2813d1F4c6da288F3',
        'ONFT'                  : '0xa0a54dADc2a1F198C58Fd0739BA7dF40Ffd366Dc',
        'endpoint'              : '0x9740FF91F1985D8d2B71494aE1A2f723bb3Ed9E4'
    },
    "Shimmer": {
        'refuel'                : '0x5BA99F0E6A42cdfAb564921a382551D8AfEAad61',
        'ONFT'                  : '0x1712147B84f91A389d2f843B8b3Cc675E6648d80',
        'endpoint'              : '0xC1b15d3B262bEeC0e3565C11C9e0F6134BdaCB36'
    },
    "Tenet": {
        'refuel'                : '0x2935a2804E4F902E722B64C51a831Bce2526a576',
        'ONFT'                  : '0x83d8476eBccf8094d80D7b2165375a3Ec4E93034',
        'endpoint'              : '0x2D61DCDD36F10b22176E0433B86F74567d529aAa'
    },
    "XPLA": {
        'refuel'                : '0xB75Bf6fcdf431a6462a0669326d9118aB48D3307',
        'ONFT'                  : '0xC29086BE89557469ae915dd9Dcaa6c093ab4648A',
        'endpoint'              : '0xC1b15d3B262bEeC0e3565C11C9e0F6134BdaCB36'
    },
    "LootChain": {
        'refuel'                : '0xE47b05F2026a82048caAECf5caE58e5AAE2405eA',
        'ONFT'                  : '0x5f45Cd59BA7F2f6bcD935663F68Ee1dEbE3B8a10',
        'endpoint'              : '0xb6319cC6c8c27A8F5dAF0dD3DF91EA35C4720dd7'
    },
    "ZKFair": {
        'refuel'                : '0x6E55472109E6aBE4054a8E8b8d9EdFfCb31032C5',
        'ONFT'                  : '0xc072c3EbAf165955C5aAd2DbB4293f771de6dbd3',
        'endpoint'              : ''
    },
    "Beam": {
        'refuel'                : '0x7dFb5E7808B5eb4fB8b9e7169537575f6fF1a218',
        'ONFT'                  : '0x6f6aE8851a460406bBB3c929a415d2Df9305AcD5',
        'endpoint'              : ''
    },
    "InEVM": {
        'refuel'                : '0x6f6aE8851a460406bBB3c929a415d2Df9305AcD5',
        'ONFT'                  : '0x6E55472109E6aBE4054a8E8b8d9EdFfCb31032C5',
        'endpoint'              : ''
    },
    "Rarible": {
        'refuel'                : '0x4fc0D96f3d70b4D9b75671Ab92e7Be01CaBE3863',
        'ONFT'                  : '0x6Ca118bdF9BD900Da5D3d85094D92C5B3b9c0DA5',
        'HNFT'                  : '0xDc09f06D11dFC7703BF8f3049E2CcF4507bEA1ab',
        'HOFT'                  : '0xd9371FFFd58D57bfC65e897e18DAF88C88ec273E',
        'endpoint'              : ''
    },
    "Blast": {
        'refuel'                : '0xc072c3EbAf165955C5aAd2DbB4293f771de6dbd3',
        'ONFT'                  : '0x6E55472109E6aBE4054a8E8b8d9EdFfCb31032C5',
        'HNFT'                  : '0x814490128eB60e6FCB56a38B46FC9FC37726414a',
        'HOFT'                  : '0xfD7c029D1F1198826302F5F6c9CD482c06F0D72f',
        'endpoint'              : ''
    },
}

RANGO_CONTRACTS = {
    'Ethereum': {
        "router": "0x69460570c93f9DE5E2edbC3052bf10125f0Ca22d"
    },
    'Arbitrum': {
        "router": "0x69460570c93f9DE5E2edbC3052bf10125f0Ca22d"
    },
    'Optimism': {
        "router": "0x69460570c93f9DE5E2edbC3052bf10125f0Ca22d"
    },
    'Linea': {
        "router": '0x69460570c93f9DE5E2edbC3052bf10125f0Ca22d'
    },
    'Scroll': {
        "router": '0x69460570c93f9DE5E2edbC3052bf10125f0Ca22d'
    },
    'Base': {
        "router": '0x69460570c93f9DE5E2edbC3052bf10125f0Ca22d'
    }
}

ODOS_CONTRACTS = {
    'Ethereum': {
        "router": "0xCf5540fFFCdC3d510B18bFcA6d2b9987b0772559"
    },
    'Arbitrum': {
        "router": "0xa669e7A0d4b3e4Fa48af2dE86BD4CD7126Be4e13"
    },
    'Optimism': {
        "router": "0xCa423977156BB05b13A2BA3b76Bc5419E2fE9680"
    },
    'zkSync': {
        "router": '0x4bBa932E9792A2b917D47830C93a9BC79320E4f7'
    },
    'Base': {
        "router": '0x19cEeAd7105607Cd444F5ad10dd51356436095a1'
    },
    'BNB Chain': {
        "router": '0x89b8AA89FDd0507a99d334CBe3C808fAFC7d850E'
    },
    'Avalanche': {
        "router": '0x88de50B233052e4Fb783d4F6db78Cc34fEa3e9FC'
    },
    'Polygon': {
        "router": '0x4E3288c9ca110bCC82bf38F09A7b425c095d92Bf'
    }
}
XYFINANCE_CONTRACTS = {
    'Arbitrum': {
        "router"                : "0x062b1Db694F6A437e3c028FC60dd6feA7444308c"
    },
    'Ethereum': {
        "router"                : "0xFfB9faf89165585Ad4b25F81332Ead96986a2681"
    },
    'Optimism': {
        "router"                : "0xF8d342db903F266de73B10a1e46601Bb08a3c195"
    },
    'zkSync':{
        "router"                : '0x30E63157bD0bA74C814B786F6eA2ed9549507b46'
    },
    'Base':{
        "router"                : '0x6aCd0Ec9405CcB701c57A88849C4F1CD85a3f3ab'
    },
    'Linea':{
        "router"                : '0xc693C8AAD9745588e95995fef4570d6DcEF98000'
    },
    'Scroll':{
        "router"                : '0x22bf2A9fcAab9dc96526097318f459eF74277042'
    },
    'Avalanche':{
        "router"                : '0xa0c0F962DECD78D7CDE5707895603CBA74C02989'
    },
    'Polygon':{
        "router"                : '0xa1fB1F1E5382844Ee2D1BD69Ef07D5A6Abcbd388'
    },
    'BNB Chain':{
        "router"                : '0xDF921bc47aa6eCdB278f8C259D6a7Fef5702f1A9'
    }
}

OPENOCEAN_CONTRACTS = {
    'Ethereum': {
        "router"                : "0x6352a56caadC4F1E25CD6c75970Fa768A3304e64"
    },
    'Arbitrum': {
        "router"                : "0x6352a56caadC4F1E25CD6c75970Fa768A3304e64"
    },
    'Optimism':{
        "router"                : "0x6352a56caadC4F1E25CD6c75970Fa768A3304e64"
    },
    'zkSync':{
        "router"                : '0x36A1aCbbCAfca2468b85011DDD16E7Cb4d673230'
    },
    'Base':{
        "router"                : '0x6352a56caadC4F1E25CD6c75970Fa768A3304e64'
    },
    'Linea':{
        "router"                : '0x6352a56caadC4F1E25CD6c75970Fa768A3304e64'
    },
    'Scroll':{
        "router"                : '0x6352a56caadC4F1E25CD6c75970Fa768A3304e64'
    },
    'Polygon':{
        "router"                : '0x6352a56caadC4F1E25CD6c75970Fa768A3304e64'
    },
    'BNB Chain': {
        "router"                : '0x6352a56caadC4F1E25CD6c75970Fa768A3304e64'
    },
    'Avalanche': {
        "router"                : '0x6352a56caadC4F1E25CD6c75970Fa768A3304e64'
    },
    'Manta': {
        "router"                : '0x6352a56caadC4F1E25CD6c75970Fa768A3304e64'
    },
    'Blast': {
        "router"                : '0x6352a56caadC4F1E25CD6c75970Fa768A3304e64'
    }
}

ONEINCH_CONTRACTS = {
    'Ethereum': {
        "router"                : "0x1111111254EEB25477B68fb85Ed929f73A960582"
    },
    'Arbitrum': {
        "router"                : "0x1111111254EEB25477B68fb85Ed929f73A960582"
    },
    'Optimism':{
        "router"                : "0x1111111254EEB25477B68fb85Ed929f73A960582"
    },
    'zkSync':{
        "router"                : '0x6e2B76966cbD9cF4cC2Fa0D76d24d5241E0ABC2F'
    },
    'Base':{
        "router"                : '0x1111111254EEB25477B68fb85Ed929f73A960582'
    },
    'Polygon':{
        "router"                : '0x1111111254EEB25477B68fb85Ed929f73A960582'
    },
    'BNB Chain':{
        "router"                : '0x1111111254fb6c44bAC0beD2854e76F90643097d'
    },
    'Avalanche':{
        "router"                : '0x1111111254EEB25477B68fb85Ed929f73A960582'
    }
}

DBK_GENESIS_NFT_CONTRACT = '0x633b7472E1641D59334886a7692107D6332B1ff0'
BRIDGE_TO_DBK_CONTRACT = '0x63CA00232F471bE2A3Bf3C4e95Bc1d2B3EA5DB92'

SQUID_ROUTER_CONTRACT = '0xce16F69375520ab01377ce7B88f5BA8C48F8D666'
POLYGON_SCHOLAR_NFT_CONTRACT = '0x436d5567F47e3723313a739D8cFB83D2ACc35d15'

TOKENS_FOR_SWAPS = {
    'Ethereum': {
        'ETH': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        'WETH': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        'USDC': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
        'USDT': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    },
    'Arbitrum': {
        "ETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        'USDC': '0xaf88d065e77c8cC2239327C5EDb3A432268e5831',
        'USDC.e': '0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8',
        'USDT': '0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9',
    },
    'Manta': {
        "ETH": "0x0Dc808adcE2099A9F62AA87D9670745AbA741746",
        "WETH": "0x0Dc808adcE2099A9F62AA87D9670745AbA741746",
        'USDC': '0x09Bc4E0D864854c6aFB6eB9A9cdF58aC190D0dF9',
        'USDT': '0x201EBa5CC46D216Ce6DC03F6a759e8E766e956aE',
    },
    'Polygon': {
        'WPOL': "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        'WMATIC': "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        'WETH': "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        'USDC': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
        'USDT': '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',
    },
    'BNB Chain': {
        'BNB': '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
        'WBNB': '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
        'WETH': '0x2170Ed0880ac9A755fd29B2688956BD959F933F8',
        'USDT': '0x55d398326f99059fF775485246999027B3197955',
        'USDC': '0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d',
    },
    "Avalanche": {
        'WETH': '0x49D5c2BdFfac6CE2BFdB6640F4F80f226bc10bAB',
        'USDC': '0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E',
        'USDC.e': '0xA7D7079b0FEaD91F3e65f86E8915Cb59c1a4C664',
        'USDT': '0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7',
    },
    'Arbitrum Nova': {
        "ETH": "0x722E8BdD2ce80A4422E880164f2079488e115365",
        "WETH": "0x722E8BdD2ce80A4422E880164f2079488e115365",
        "USDC": "0x750ba8b76187092B0D1E87E28daaf484d1b5273b",
    },
    'Blast': {
        "ETH": "0x4300000000000000000000000000000000000004",
        "WETH": "0x4300000000000000000000000000000000000004",
        "USDB": "0x4300000000000000000000000000000000000003",
    },
    'Zora': {
        "ETH": "0x4200000000000000000000000000000000000006",
        "WETH": "0x4200000000000000000000000000000000000006"
    },
    "Optimism": {
        "ETH": "0x4200000000000000000000000000000000000006",
        "WETH": "0x4200000000000000000000000000000000000006",
        "USDC": "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",
        "USDT": "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58",
        "USDC.e": "0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
    },
    "Polygon zkEVM": {
        'ETH': "0x4F9A0e7FD2Bf6067db6994CF12E4495Df938E6e9",
        'WETH': "0x4F9A0e7FD2Bf6067db6994CF12E4495Df938E6e9",
    },
    "zkSync": {
        "ETH": "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
        "WETH": "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
        "USDC": "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4",
        "USDC.e": "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4",
        "USDT": "0x493257fD37EDB34451f62EDf8D2a0C418852bA4C",
    },
    "Taiko": {
        "ETH": "0xA51894664A773981C6C112C43ce576f315d5b1B6",
        "WETH": "0xA51894664A773981C6C112C43ce576f315d5b1B6",
        "USDC": "0x07d83526730c7438048D55A4fc0b850e2aaB6f0b",
    },
    "Base": {
        "ETH": "0x4200000000000000000000000000000000000006",
        "WETH": "0x4200000000000000000000000000000000000006",
        'USDC.e': '0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA',
    },
    "Linea": {
        "ETH": "0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f",
        "WETH": "0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f",
        "USDT": "0xA219439258ca9da29E9Cc4cE5596924745e12B93",
        "USDC": "0x176211869cA2b568f2A7D4EE941E073a821EE1ff",
    },
    "Scroll": {
        "ETH": "0x5300000000000000000000000000000000000004",
        "WETH": "0x5300000000000000000000000000000000000004",
        "USDT": "0xf55BEC9cafDbE8730f096Aa55dad6D22d44099Df",
        "USDC": "0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4",
    },
    "Solana": {
        "SOL": "11111111111111111111111111111111",
        "WSOL": 'So11111111111111111111111111111111111111112',
        "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        "USDT": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
    },
    'InEVM': {
        'INJ': '0x69011706b3f6C6eaeD7D2Bc13801558B4fd94CBF',
        'WINJ': '0x69011706b3f6C6eaeD7D2Bc13801558B4fd94CBF',
        'USDC': '0x8358D8291e3bEDb04804975eEa0fe9fe0fAfB147',
    }
}

TOKENS_PER_CHAIN = {
    'Ethereum': {
        'ETH': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        'WETH': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        'ZRO': '0x6985884C4392D348587B19cb9eAAf157F13271cd',
        'USDC': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
        'USDT': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
        'TIA.n': '0x15b5D6B614242B118AA404528A7f3E2Ad241e4A4',
        'STG': '0xAf5191B0De278C7286d6C7CC6ab6BB8A73bA2Cd6',
        'USDV': '0x0E573Ce2736Dd9637A0b21058352e1667925C7a8',
        'MAV': '0x7448c7456a97769F6cD04F1E83A4a23cCdC46aBD',
        'ezETH': '0xbf5495Efe5DB9ce00f80364C8B423567e58d2110'
    },
    'Arbitrum': {
        "ETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "ZRO": "0x6985884C4392D348587B19cb9eAAf157F13271cd",
        'USDC': '0xaf88d065e77c8cC2239327C5EDb3A432268e5831',
        'USDC.e': '0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8',
        'USDT': '0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9',
        'fUSDC': '0x4CFA50B7Ce747e2D61724fcAc57f24B748FF2b2A',
        'TIA.n': '0xD56734d7f9979dD94FAE3d67C7e928234e71cD4C',
        'STG': '0x6694340fc020c5E6B96567843da2df01b2CE1eb6',
        'USDV': '0x323665443CEf804A3b5206103304BD4872EA4253',
        'ezETH': '0x2416092f143378750bb29b79eD961ab195CcEea5'
    },
    'Manta': {
        "ETH": "0x0Dc808adcE2099A9F62AA87D9670745AbA741746",
        "WETH": "0x0Dc808adcE2099A9F62AA87D9670745AbA741746",
        'USDC': '0x09Bc4E0D864854c6aFB6eB9A9cdF58aC190D0dF9',
        'USDT': '0x201EBa5CC46D216Ce6DC03F6a759e8E766e956aE',
        'TIA.n': '0x6Fae4D9935E2fcb11fC79a64e917fb2BF14DaFaa',
    },
    'Polygon': {
        'POL': "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        'WPOL': "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        'MATIC': "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        'WMATIC': "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        'WETH': "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        'ZRO': "0x6985884C4392D348587B19cb9eAAf157F13271cd",
        'USDC': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
        'USDT': '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',
        'STG': '0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590',
        'USDV': '0x323665443CEf804A3b5206103304BD4872EA4253',
    },
    'BNB Chain': {
        'BNB': '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
        'WBNB': '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
        'WETH': '0x2170Ed0880ac9A755fd29B2688956BD959F933F8',
        'USDT': '0x55d398326f99059fF775485246999027B3197955',
        'ZRO': '0x6985884C4392D348587B19cb9eAAf157F13271cd',
        'USDC': '0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d',
        'ZBC': '0x37a56cdcD83Dce2868f721De58cB3830C44C6303',
        'STG': '0xB0D502E938ed5f4df2E681fE6E419ff29631d62b',
        'USDV': '0x323665443CEf804A3b5206103304BD4872EA4253',
        'MAV': '0xd691d9a68C887BDF34DA8c36f63487333ACfD103',
        'ezETH': '0x2416092f143378750bb29b79eD961ab195CcEea5'
    },
    "Avalanche": {
        'AVAX': '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7',
        'WAVAX': '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7',
        'WETH': '0x49D5c2BdFfac6CE2BFdB6640F4F80f226bc10bAB',
        'ZRO': '0x6985884C4392D348587B19cb9eAAf157F13271cd',
        'USDC': '0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E',
        'USDC.e': '0xA7D7079b0FEaD91F3e65f86E8915Cb59c1a4C664',
        'USDT': '0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7',
        'STG': '0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590',
        'USDV': '0x323665443CEf804A3b5206103304BD4872EA4253',
    },
    'Arbitrum Nova': {
        "ETH": "0x722E8BdD2ce80A4422E880164f2079488e115365",
        "WETH": "0x722E8BdD2ce80A4422E880164f2079488e115365",
        "USDC": "0x750ba8b76187092B0D1E87E28daaf484d1b5273b",
        "DAI": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1"
    },
    'Blast': {
        "ETH": "0x4300000000000000000000000000000000000004",
        "WETH": "0x4300000000000000000000000000000000000004",
        "USDB": "0x4300000000000000000000000000000000000003",
        'ezETH': '0x2416092f143378750bb29b79eD961ab195CcEea5'
    },
    'Zora': {
        "ETH": "0x4200000000000000000000000000000000000006",
        "WETH": "0x4200000000000000000000000000000000000006"
    },
    'Fantom': {
        'USDC': '0x28a92dde19D9989F39A49905d7C9C2FAc7799bDf',
        'STG': '0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590',
    },
    "Optimism": {
        "ETH": "0x4200000000000000000000000000000000000006",
        "ZRO": "0x6985884C4392D348587B19cb9eAAf157F13271cd",
        "WETH": "0x4200000000000000000000000000000000000006",
        "OP": "0x4200000000000000000000000000000000000042",
        "USDC": "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",
        "USDT": "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58",
        "USDC.e": "0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
        "DAI": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
        'STG': '0x296F55F8Fb28E498B858d0BcDA06D955B2Cb3f97',
        'USDV': '0x323665443CEf804A3b5206103304BD4872EA4253',
        'ezETH': '0x2416092f143378750bb29b79eD961ab195CcEea5'
    },
    "Mode": {
        'ezETH': '0x2416092f143378750bb29b79eD961ab195CcEea5'
    },
    "Polygon zkEVM": {
        'ETH': "0x4F9A0e7FD2Bf6067db6994CF12E4495Df938E6e9",
        'WETH': "0x4F9A0e7FD2Bf6067db6994CF12E4495Df938E6e9",
    },
    "zkSync": {
        "ETH": "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
        "WETH": "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
        'MAV': '0x787c09494Ec8Bcb24DcAf8659E7d5D69979eE508',
        "USDC": "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4",
        "USDC.e": "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4",
        "USDT": "0x493257fD37EDB34451f62EDf8D2a0C418852bA4C",
    },
    "Taiko": {
        "ETH": "0xA51894664A773981C6C112C43ce576f315d5b1B6",
        "WETH": "0xA51894664A773981C6C112C43ce576f315d5b1B6",
        "TAIKO": "0xA9d23408b9bA935c230493c40C73824Df71A0975",
        "USDC": "0x07d83526730c7438048D55A4fc0b850e2aaB6f0b"
    },
    "Base": {
        "ETH": "0x4200000000000000000000000000000000000006",
        "WETH": "0x4200000000000000000000000000000000000006",
        'ZRO': '0x6985884C4392D348587B19cb9eAAf157F13271cd',
        'USDC': '0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA',
        'USDC.e': '0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA',
        'STG': '0xE3B53AF74a4BF62Ae5511055290838050bf764Df',
        'MAV': '0x64b88c73A5DfA78D1713fE1b4c69a22d7E0faAa7',
        'ezETH': '0x2416092f143378750bb29b79eD961ab195CcEea5'
    },
    "Linea": {
        "ETH": "0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f",
        "WETH": "0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f",
        "USDT": "0xA219439258ca9da29E9Cc4cE5596924745e12B93",
        "USDC": "0x176211869cA2b568f2A7D4EE941E073a821EE1ff",
        'STG': '0x808d7c71ad2ba3FA531b068a2417C63106BC0949',
        'ezETH': '0x2416092f143378750bb29b79eD961ab195CcEea5'
    },
    "Scroll": {
        "ETH": "0x5300000000000000000000000000000000000004",
        "WETH": "0x5300000000000000000000000000000000000004",
        "wrsETH": "0xa25b25548B4C98B0c7d3d27dcA5D5ca743d68b7F",
        "USDT": "0xf55BEC9cafDbE8730f096Aa55dad6D22d44099Df",
        "USDC": "0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4",
    },
    'Kava':{
        'USDT': '0x919C1c267BC06a7039e03fcc2eF738525769109c',
        'STG': '0x83c30eb8bc9ad7C56532895840039E62659896ea',
    },
    'Mantle': {
        'USDC': '0x09Bc4E0D864854c6aFB6eB9A9cdF58aC190D0dF9',
        'USDT': '0x201EBa5CC46D216Ce6DC03F6a759e8E766e956aE',
        'STG': '0x8731d54E9D02c286767d56ac03e8037C07e01e98',
    },
    "CoreDAO": {
        "USDC": '0xa4151B2B3e269645181dCcF2D426cE75fcbDeca9',
        "USDT": '0x900101d06A7426441Ae63e9AB3B9b0F63Be145F1',
    },
    "Gravity": {
        "G": '0xa4151B2B3e269645181dCcF2D426cE75fcbDeca9',
        "ETH": '0xf6f832466Cd6C21967E0D954109403f36Bc8ceaA',
    },
    "xLayer": {
        "OKB": "0xe538905cf8410324e03A5A23C1c177a474D59b2b",
        "WOKB": "0xe538905cf8410324e03A5A23C1c177a474D59b2b",
        "ETH": "0x5A77f1443D16ee5761d310e38b62f77f726bC71c",
        "WETH": "0x5A77f1443D16ee5761d310e38b62f77f726bC71c",
        "USDC": '0x74b7F16337b8972027F6196A17a631aC6dE26d22',
        "USDT": '0x1E4a5963aBFD975d8c9021ce480b42188849D41d',
    },
    'Nautilus': {
        'ZBC' : '0x4501bBE6e731A4bC5c60C03A77435b2f6d5e9Fe7',
        'WETH': '0x182E8d7c5F1B06201b102123FC7dF0EaeB445a7B',
        'USDT': '0xBDa330Ea8F3005C421C8088e638fBB64fA71b9e0',
        'USDC': '0xB2723928400AE5778f6A3C69D7Ca9e90FC430180'
    },
    "Solana": {
        "SOL": "11111111111111111111111111111111",
        "WSOL": 'So11111111111111111111111111111111111111112',
        "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        "USDT": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
        'JUP': 'JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN',
        "ZBC": "wzbcJyhGhQDLTV1S99apZiiBdE4jmYfbw99saMMdP59"
    },
    'Neutron': {
        'ECLIP': 'factory/neutron10sr06r3qkhn7xzpw3339wuj77hu06mzna6uht0/eclip',
        'TIA': 'ibc/773B4D0A3CD667B2275D5A4A7A2F0909C0BA0F4059C0B9181E680DDF4965DCC7',
        'TIA.n': 'ibc/773B4D0A3CD667B2275D5A4A7A2F0909C0BA0F4059C0B9181E680DDF4965DCC7',
        'NTRN': 'untrn',
        'ATOM': 'ibc/C4CFF46FD6DE35CA4CF4CE031E643C8FDC9BA4B99AE598E9B0ED98FE3A2319F9',
        'USDC': 'ibc/B559A80D62249C8AA07A380E2A2BEA6E5CA9A6F079C912C3A9E9B494105E4F81',
    },
    'InEVM': {
        'INJ': '0x69011706b3f6C6eaeD7D2Bc13801558B4fd94CBF',
        'WINJ': '0x69011706b3f6C6eaeD7D2Bc13801558B4fd94CBF',
        'USDC': '0x8358D8291e3bEDb04804975eEa0fe9fe0fAfB147',
    },
    'Celestia': {
        'TIA': 'utia',
        'TIA.n': 'utia',
    },
    'Injective': {
        'INJ': 'inj',
    }
}

LAYERSWAP_CHAIN_NAME = {
    'Arbitrum'             : 'ARBITRUM_MAINNET',
    "Arbitrum Nova"        : 'ARBITRUMNOVA_MAINNET',
    "Base"                 : 'BASE_MAINNET',
    "Linea"                : 'LINEA_MAINNET',
    "Manta"                : 'MANTA_MAINNET',
    "Polygon"              : 'POLYGON_MAINNET',
    "Optimism"             : 'OPTIMISM_MAINNET',
    "Scroll"               : 'SCROLL_MAINNET',
    "Starknet"             : 'STARKNET_MAINNET',
    "Polygon zkEVM"        : 'POLYGONZK_MAINNET',
    "zkSync"               : 'ZKSYNCERA_MAINNET',
    "Zora"                 : 'ZORA_MAINNET',
    "Ethereum"             : 'ETHEREUM_MAINNET',
    "Avalanche"            : 'AVAX_MAINNET',
    "BNB Chain"            : 'BSC_MAINNET',
    "OpBNB"                : 'OPBNB_MAINNET',
    "Mantle"               : 'MANTLE_MAINNET',
    "Blast"                : 'BLAST_MAINNET',
}

ORBITER_CHAINS_INFO = {
    'Arbitrum':       {'chainId': 42161,        'id': 2},
    'Arbitrum Nova':  {'chainId': 42170,        'id': 16},
    'Base':           {'chainId': 8453,         'id': 21},
    'Linea':          {'chainId': 59144,        'id': 23},
    'Manta':          {'chainId': 169,          'id': 31},
    'Polygon':        {'chainId': 137,          'id': 6},
    'Optimism':       {'chainId': 10,           'id': 7},
    'Scroll':         {'chainId': 534352,       'id': 19},
    'Starknet':       {'chainId': 'SN_MAIN',    'id': 4},
    'Polygon zkEVM':  {'chainId': 1101,         'id': 17},
    'zkSync':         {'chainId': 324,          'id': 14},
    'Zora':           {'chainId': 7777777,      'id': 30},
    'Ethereum':       {'chainId': 1,            'id': 1},
    'BNB Chain':      {'chainId': 56,           'id': 15},
    'Metis':          {'chainId': 1088,         'id': 10},
    'OpBNB':          {'chainId': 204,          'id': 25},
    'Mantle':         {'chainId': 5000,         'id': 24},
    'ZKFair':         {'chainId': 42766,        'id': 38},
    'Blast':          {'chainId': 81457,        'id': 40},
    'Taiko':          {'chainId': 167000,       'id': 20},
    'Gravity':        {'chainId': 1625,         'id': 75}
}

RHINO_CHAIN_INFO = {
    "Arbitrum": 'ARBITRUM',
    "Arbitrum Nova": 'ARBITRUMNOVA',
    "Base": 'BASE',
    "Linea": 'LINEA',
    "Manta": 'MANTA',
    "Polygon": 'MATIC_POS',
    "Optimism": 'OPTIMISM',
    "Scroll": 'SCROLL',
    "Starknet": 'STARKNET',
    "Polygon zkEVM": 'ZKEVM',
    "zkSync": 'ZKSYNC',
    "Taiko": 'TAIKO',
}

STARGATE_POOLS_ID = {
    'Ethereum': {
        'USDC': 1,
        'USDT': 2,
        'ETH': 13,
    },
    'BNB Chain': {
        'USDT': 2,
    },
    'Avalanche': {
        'USDC': 1,
        'USDT': 2,
    },
    'Polygon': {
        'USDC': 1,
        'USDT': 2,
    },
    'Arbitrum': {
        'USDC': 1,
        'USDT': 2,
        'ETH': 13,
    },
    'Optimism':{
        'USDC': 1,
        'ETH': 13,
    },
    'Fantom':{
        'USDC': 21
    },
    'Base':{
        'USDC': 1,
        'ETH': 13
    },
    'Linea':{
        'ETH': 13
    },
    'Kava':{
        'USDT': 2,
    },
    'Mantle':{
        'USDC': 1,
        'USDT': 2,
    }
}

CHAIN_IDS = {
    "Arbitrum":  42161,
    "Arbitrum Nova":  42170,
    "Base":  8453,
    "Linea":  59144,
    "Manta":  169,
    "Polygon":  137,
    "Optimism":  10,
    "Scroll":  534352,
    # 9":  'SN_MAIN',
    "Polygon zkEVM": 1101,
    "zkSync": 324,
    "Zora": 7777777,
    "Ethereum": 1,
    "Avalanche": 43114,
    "BNB Chain": 56,
    "Moonbeam": 1284,
    "Harmony": 1666600000,
    "Telos": 40,
    "Celo": 42220,
    "Gnosis": 100,
    "Core": 1116,
    "TomoChain": 88,
    "Conflux": 1030,
    "Orderly": 291,
    "Horizen": 7332,
    "Metis": 1088,
    "Astar": 592,
    "OpBNB": 204,
    "Mantle": 5000,
    "Moonriver": 1285,
    "Klaytn": 8217,
    "Kava": 2222,
    "Fantom": 250,
    "Aurora": 1313161554,
    "Canto": 7700,
    "DFK": 53935,
    "Fuse": 122,
    "Goerli": 5,
    "Meter": 82,
    "OKX Chain": 66,
    "Shimmer": 148,
    "Tenet": 1559,
    "XPLA": 37,
    "LootChain": 5151706,
    "ZKFair": 42766,
    "Beam": 4337,
    "InEVM": 2525,
    "Rarible": 0,
    "Blast": 81457,
    "Mode": 34443,
    "Celestia": "celestia",
    "Neutron": "neutron",
    "Injective": "injective",
    "Nautilus": 7565164,
    "Solana": 196,
    "xLayer": 196,
    "Taiko": 167000
}

CHAIN_NAME_FROM_ID = {
    42161: 'Arbitrum',
    42170: 'Arbitrum Nova',
    8453: 'Base',
    59144: 'Linea',
    169: 'Manta',
    56: 'BNB Chain',
    137: 'Polygon',
    10: 'Optimism',
    81457: 'Blast',
    534352: 'Scroll',
    'SN_MAIN': 'Starknet',
    1101: 'Polygon zkEVM',
    324: 'zkSync',
    7777777: 'Zora',
    1: 'Ethereum',
    7565164: 'Solana',
    196: 'xLayer',
    167000: 'Taiko',
    20240603: 'Dbk'
}

CELESTIA_VALIDATORS = [
    "celestiavaloper1qzjfrpp4tygdz7ptxj8j9p458ddlym88kp99fr",
    "celestiavaloper1qx43f066sh6728avms4qq09cj2a3mg83dgjh22",
    "celestiavaloper1qxeza0sa037u35p3ze8p7ka7emajvydnyjlp07",
    "celestiavaloper1q8teur40emyun60et4wh5z6yj5669stgz8xs59",
    "celestiavaloper1q2kaajedxm0r5xc0twdqz6atap96502d67yjyj",
    "celestiavaloper1qdfdh8stxpkj4zz46x2n9ejyyy9h0c86425yjm",
    "celestiavaloper1qwddh85mqar9fgug8w0zveulvxkeup7tyxtpa3",
    "celestiavaloper1qnnhmk0dsyfzu6jcq5aznc3f20t05rj0400wkg",
    "celestiavaloper1qe8uuf5x69c526h4nzxwv4ltftr73v7q5qhs58",
    "celestiavaloper1q66sqadh6tftulm56h2dnh8aqf7ykjtn0m2mhs",
    "celestiavaloper1p9qvp4xrhthhnxtvmaz6m5qcxaqd83567w2g9m",
    "celestiavaloper1psfkjf8vc5fxd5jw667mcvxw6a67fgvp62n4nd",
    "celestiavaloper1pnzrk7yzx0nr9xrcjyswj7ram4qxlrfz28xvn6",
    "celestiavaloper1pmn4cjwf26hkcpvyl322glhpdpcemcel8ca2vl",
    "celestiavaloper1pavac9yrlgwyw6v9yx84sttc96n9ee9zrja2u7",
    "celestiavaloper1zqjpfxtv3yp6kdlgra4hc9zehxgvpaw82hxr5w",
    "celestiavaloper1zdrz4w2pwwffdvmpum0626vycel9caay9n3pll",
    "celestiavaloper1zwr65gn3jlck0s8qcf6t8xpqlq7zl5na8rluuu",
    "celestiavaloper1z7nt4vlvafwp7d8l8x5c7yq0t3ta6dyh7zfddm",
    "celestiavaloper1rq8kvlncjvs42hmrx90dcff2tdshj5k73yzh0g",
    "celestiavaloper1rrkk74mgyn2ylf5q27zwe8069n2qfyelkqwz7d",
    "celestiavaloper1ryyzale2qcp3e35k0ze3kc0mpfdtw9jagcss3k",
    "celestiavaloper1ry3453n79p9nlzcq7nm6yqfyluzqn0d4fehnat",
    "celestiavaloper1r5xt7twqmh39ky72f4txxjrhlt2z0qwwmdal8c",
    "celestiavaloper1r4kqtye4dzacmrwnh6f057p50pdjm8g59tlhhg",
    "celestiavaloper1rcm7tth05klgkqpucdhm5hexnk49dfda3l3hak",
    "celestiavaloper1rcaaaaavkvvvux8nrxav7mjv06rxvrvyas869z",
    "celestiavaloper1yqd33ekzwswh0tnzl7mxltz82hlh72qdfcy7l0",
    "celestiavaloper1yraa2gnhdlwms4keqq0gekv2ese6wteqvuccel",
    "celestiavaloper1yxrf303ewxrwndex9cxj0mg24vekrpqsjrlly3",
    "celestiavaloper1ydzsellc42dzqcq489hs8dwhwtalacpr2c5myf",
    "celestiavaloper1ywty5ca86ggtk7fvmd5qett9qcz0prz6hc2kh4",
    "celestiavaloper1yknsyf9ws4ugtv3r9g43kwqkne4zmrupcxhlth",
    "celestiavaloper1yecxnyegvgm5dwsx0r3jsgr74ju6mlxdwkxx8g",
    "celestiavaloper19y52qzj4hxw0u68krfptkjlm77cvth8dgum7yu",
    "celestiavaloper19f0w9svr905fhefusyx4z8sf83j6et0g57nch8",
    "celestiavaloper19v94c3z7ckarwsum76kaagma0wqsqhh5nl5zqg",
    "celestiavaloper19vn0yfcfzzx07vfp7fzlffw0xl7k80e6md97ra",
    "celestiavaloper19dvmjlp7sghr80tcgc2pv42td78e2ycj3lsgv7",
    "celestiavaloper19nxz9gats6w3ywmkm5pr69sv7jxqm0027htflh",
    "celestiavaloper19kr4f4ndyek6kwa0vt3w4un8he0tkekufa8t2g",
    "celestiavaloper1xqc7w3pe38kg4tswjt7mnvks7gy4p38vtsuycj",
    "celestiavaloper1x20lytyf6zkcrv5edpkfkn8sz578qg5spge2ru",
    "celestiavaloper1xwazl8ftks4gn00y5x3c47auquc62ssu374n2m",
    "celestiavaloper1xjm7d7d0x9krjdmwgnhdzpww6wwg93z2874vh4",
    "celestiavaloper1xesqr8vjvy34jhu027zd70ypl0nnev5ejgmszq",
    "celestiavaloper18zav8ypa78rxr5anw34cutx8stqpspgs3hehv7",
    "celestiavaloper189ecvq5avj0wehrcfnagpd5sd8pup9aqmdglmr",
    "celestiavaloper18xfv6pjlttunzfswgn65rpv8njhupu7yp775j5",
    "celestiavaloper18d70dws4r8y4z7mt6um6g4x6nnr0zdcuv5y88m",
    "celestiavaloper18eym8mr6wjs7at6dvlswk45fsxfej2kur2wue9",
    "celestiavaloper187fhh435s76juewsmrey5yv3ljq4vppt7z4e69",
    "celestiavaloper18700j95ka7wyx6ezxykc0veluhexrmfh3smjeg",
    "celestiavaloper187avawwq7qhanrkxf45mayztdqsr49hu8lezdh",
    "celestiavaloper18l7hjs332espnntj7pczkpe5ycxk8ngaqk898n",
    "celestiavaloper1g98nwdkuysv9mgepq2nwaawx69l3tnl0gct7ph",
    "celestiavaloper1gfn5m2vjqk4kcdg2zwhzgpvu60jz0f9duhu594",
    "celestiavaloper1g2ddhmtycepd6wlet9e9tvjy6hs5nuhf7dku6k",
    "celestiavaloper1gvfzqhgqgk8u7l877vnnz6vmnnwwj7622grq0s",
    "celestiavaloper1gh5v92dy3dhjz7yg89eaz7ec5gjrkscc5zy7l4",
    "celestiavaloper1ge55g82gqy74a4hdjhza7d8c9njlw2hlf8wu7x",
    "celestiavaloper1geuw5f6u3n5l4ne2d2nze3fehxf023f7s8h08t",
    "celestiavaloper1gmyy5pqtswkyfw7uverv6tpq9x8me5kyqhmahr",
    "celestiavaloper1gm7txvnd539ruc86mkz2sgnz3r456e86g9psl4",
    "celestiavaloper1g7tvm67fs93n0hqaveqxfg5dpw6zdquqmr8hdk",
    "celestiavaloper1gl0rg3g0pkcpr8umj2hvlhha06ecjd65yt96z5",
    "celestiavaloper1fyw0qppar97easavw07n876ktv0a4vpptawt09",
    "celestiavaloper1ftmw4wh8dq2ljw0xq3xgg00dl7l20se3lrml7q",
    "celestiavaloper12zvew6zvvz9qajhwscuc6jrauma5a9tzvf5jey",
    "celestiavaloper12rausrkf9acjz03fw8rmqzaa64tln6ruzhk6y8",
    "celestiavaloper12gr4z6ngd3ejemg7gx8lp385fpqx7m84s2z804",
    "celestiavaloper12t63cy8kn5n7qw77xvjn00ymcr0uuvz2vh8p79",
    "celestiavaloper125xazqstxpav7ekrt4w8km7ccdu8ytj40xug70",
    "celestiavaloper12lh3gp4mw7jzt3gymd7dukfvwra4h5jazke59f",
    "celestiavaloper1tzm96yvupy3egtpg6uw0s2f4c85qayw3afwetd",
    "celestiavaloper1tspp5zxln9q0rlh6deayq90my08jwsp0wuvj9s",
    "celestiavaloper1tsxgd3plf7und8jwjq8swmuhzglmy3fpq9r5vs",
    "celestiavaloper1t345w0vxnyyrf4eh43lpd3jl7z378rtsdn9tz3",
    "celestiavaloper1v987evnk7hsqct7smdqpxqprhvlcxgt43kyewc",
    "celestiavaloper1vfydl5r98zev8xc7j0mus28r63jcklsu63vuah",
    "celestiavaloper1vfkgjmjxkvj0kfnzf5jkjzkj7wn3ms8d83ljks",
    "celestiavaloper1vvl900jjjhqk5n50s2aaqyw4cf9wamk6k3uf6j",
    "celestiavaloper1vdp8q3v72mntewqqak56yk3gzz7h5ukmeym9hk",
    "celestiavaloper1vsyrh5y4g7xkuewwny83wt2kdw2yvqdm8230ma",
    "celestiavaloper1vje2he3pcq3w5udyvla7zm9qd5yes6hzffsjxj",
    "celestiavaloper1v5hrqlv8dqgzvy0pwzqzg0gxy899rm4klzxm07",
    "celestiavaloper1vl2ef86uxflhdy2qvy9f7qdpwzuw5jmax92qya",
    "celestiavaloper1vl3dkus7g0cj4lg0e2jrqk2reukmlht0ee7cr4",
    "celestiavaloper1vlugkygcx9dng7lsc03wjw997zq855xywma3pj",
    "celestiavaloper1d28qfq3dxsaqy6mv3ahph2t6qk3gv6svqcngjv",
    "celestiavaloper1ddg8la0rc8h5mzm7mlheszw3rl4ecy5xnrh0ss",
    "celestiavaloper1dsyuamue2p3l0z753pyrtegs52ftrg960re06j",
    "celestiavaloper1djqecw6nn5tydxq0shan7srv8j65clsfmnxcfu",
    "celestiavaloper1demcj83q7nxt6gtqxlu7qsmwqpt4jspj3alr92",
    "celestiavaloper1d6k327c5te7e2k70k69eugv8qaamhc8k9rtjy6",
    "celestiavaloper1damrk07qmchr6g9xu4w7m4hr7actkwtv60t4m6",
    "celestiavaloper1dlsl4u42ycahzjfwc6td6upgsup9tt7cz8vqm4",
    "celestiavaloper1w8hktwz3fdxgfuxezlj3jseatfdttjr4pw0vkh",
    "celestiavaloper1wdx408hmdr9zejrn2a2pgxt6z3punv8q7rph8g",
    "celestiavaloper1wd6zaem7p47xsek9zzpu2naj5d5cn2hsx0mf82",
    "celestiavaloper1wenhatrwx68d8fd5uezs2k2092s5p4mky7905a",
    "celestiavaloper1wu24jxpn9j0580ehjz344d58cf3t7lzrrgqmnr",
    "celestiavaloper10gfnn7a3d4r85tljtq455ztd0sat3y9symq42t",
    "celestiavaloper10f8l8m4879h40848rsvxat797t3a5ghgdsjgzl",
    "celestiavaloper10ds4ew40h4uhpt59ashnf7c06f0qnylnu566xk",
    "celestiavaloper100p9yrthtjfwxkj9jpmvv8e8jk53d60nw5jatj",
    "celestiavaloper107lwx458gy345ag2afx9a7e2kkl7x49y3433gj",
    "celestiavaloper1sr3c55jauh7hzddhycqxe5eatwezxtlmuthv09",
    "celestiavaloper1symf474wnypes2d3mecllqk6l26rwz8mcn83ug",
    "celestiavaloper1s95cm5ux6spxuae2lzhaj04evu47vaeskgh7lq",
    "celestiavaloper1sgwxehgp99tftpxwruzg239gvelg423vztggz7",
    "celestiavaloper1st4h4ymu52hwtl3s0n298t6adj0vputx8jw8xt",
    "celestiavaloper1s0lankh33kprer2l22nank5rvsuh9ksa2xcd2y",
    "celestiavaloper1sjpn0l03xw9m8v9qg5f7yfknydxmqxezvljss4",
    "celestiavaloper1snun9qqk9eussvyhkqm03lz6f265ekhnnlw043",
    "celestiavaloper1skc8aut895jvg4hdxx7q89sus5x63edel6qlpd",
    "celestiavaloper1sl97x54v0u3extuj2zrf7h0qrrtpgpslfrjjry",
    "celestiavaloper1slnzmhg3kwhc2c5y9atrt5jtmt3sauzzp4tguj",
    "celestiavaloper13zy2js8k2yk57275kt9rrqngrdgxxt7nq2jsk8",
    "celestiavaloper139mu0a0ucz0gmrkavm5wjar2lpx7yvxq3e25e5",
    "celestiavaloper138jl42zlxue4wpvnugcdqhxjmyd2vpt6qhs5ls",
    "celestiavaloper133t4gpv4vhpqgfn9gr8l4u423zrglg8rkqeupr",
    "celestiavaloper135w0ugccxxjjz6n4wn2mw2qzreevu67x6u70cd",
    "celestiavaloper1j8sspsjnzqd2k8uxjy7rp9ggwu8nc2hjda62d4",
    "celestiavaloper1jgqewpzn7dww5tlpnkypm72fm8tjznmw7ll7ls",
    "celestiavaloper1j2jq259d3rrc24876gwxg0ksp0lhd8gy49k6st",
    "celestiavaloper1jkuw8rxxrsgn9pq009987kzelkp46cgcaa7lhj",
    "celestiavaloper1nr6c7x6lqkfkzyl39eu58r628rr5n5p27y3h54",
    "celestiavaloper1nxdm2vdl9xmmekauu3yfhq49t6vqc5cph2dj3s",
    "celestiavaloper1nttcw852wga4y4gww3hu70djg9d4fu4cc9l08p",
    "celestiavaloper1nwu3ugynh8m6r7aphv0uxnca84t7gnruvyye9c",
    "celestiavaloper1n3mhyp9fvcmuu8l0q8qvjy07x0rql8q4tg7kxw",
    "celestiavaloper1njzuxja7aa7w2d69ldg2r8c6qhjzfcd42huq0x",
    "celestiavaloper1nna7k5lywn99cd63elcfqm6p8c5c4qcuuqws9l",
    "celestiavaloper15rvv4zjul0q6plky862et5mxqqgqk535eup7u2",
    "celestiavaloper15930tdsdke8w8fqe5mspfftktahsdavhdvhp0d",
    "celestiavaloper1593ns00rftlqp2gyu6wdmrqpgv5frv0hsf4sw2",
    "celestiavaloper159aprf7gl0u8vqkle6jwkkthkm2vxz9nxzmr2d",
    "celestiavaloper15kpw453rgqrranltr8pcy9muryf3jjd7esw38j",
    "celestiavaloper15cthwscatflw8wndmetj38w9j9y0t4clfa2fkn",
    "celestiavaloper15c40l9eu6zjsrq034hsvtfk00dlz7sfuzkgx8x",
    "celestiavaloper15urq2dtp9qce4fyc85m6upwm9xul3049gwdz0x",
    "celestiavaloper14vzdtwyl0gmw0tavuaxgkxeghs36vcvttm3vp7",
    "celestiavaloper14v4ush42xewyeuuldf6jtdz0a7pxg5fwrlumwf",
    "celestiavaloper140l6y2gp3gxvay6qtn70re7z2s0gn57zcvqd22",
    "celestiavaloper143lwrn72d44r80cvak3mty35asg57ay5pygdmx",
    "celestiavaloper14nq28mnq3cknlxhnr0n2pxekueu34wfjgp266c",
    "celestiavaloper14ntfv0qkg8522xe0pvrfgqxcmnj5x466v8z3tl",
    "celestiavaloper1463wx5xkus5hyugyecvlhv9qpxklz62kyhwcts",
    "celestiavaloper14lpj0cetmg4ayshv5nlckjt0whwlvfdcpu9ux6",
    "celestiavaloper1k8t8ms0l4jsn3g35mltajxt8wa59k00v9wq735",
    "celestiavaloper1kflqv5m0kdgsuw78lcveq00y4emmuxnu7y2kh7",
    "celestiavaloper1kd94m7dsh87fdqs2mcdpqz0as64mp6f0mq3nge",
    "celestiavaloper1knn88yl08ctsdrtxvfp39jywt7rph9ptv7532y",
    "celestiavaloper1kl5nxl54xt3g6k5k4zlk48udfcx8gkz2nfwzgl",
    "celestiavaloper1hpzkv3kn2dy4n4sufvl5zq935m03kdfcqv64tj",
    "celestiavaloper1h9lx8ct4ut2ewn39azz9ypfjxtd7k3anuhpdyj",
    "celestiavaloper1hvhyunq7qvykzvrcnhjj4xnkcla58xustq98lx",
    "celestiavaloper1hn75f7n74p2qct3mk5782yzfw7kvq05rzekwuu",
    "celestiavaloper1hm2d8e6nd5ngtlte3hlded03vgj3rer94vmdml",
    "celestiavaloper1hu642mjeyhgud86kk8a9n5pyfl6las8kwlp62t",
    "celestiavaloper1cqgzxhn3dqd58xexz8yley2wntdvym4emzvpd7",
    "celestiavaloper1cz6yhs3d5q60jfajzfprxrpcxzr8xs2jft585y",
    "celestiavaloper1cydgz3dtxpqd8j8t2k3wh9wa9vc28tkt3wq30k",
    "celestiavaloper1c9ye54e3pzwm3e0zpdlel6pnavrj9qqvjeqh0m",
    "celestiavaloper1cgd8qkqgmwytfm0l78fujgxeusm5p0c8ckdvyu",
    "celestiavaloper1cs37tvmahavw8xcnzcgyz342sh0al37ma4zqat",
    "celestiavaloper1cmaga4f6f7pttuwzfldn9067ld3090uw0e6zq8",
    "celestiavaloper1clf3nqp89h97umhl4fmcqr642jz6rszcxegjc6",
    "celestiavaloper1cl4wey8vvr43u7h59kqwhtx7qyc24h295tshkv",
    "celestiavaloper1eqnc2e69j88k95r6u6s27ad2y8mw9hpngg9msw",
    "celestiavaloper1e2p4u5vqwgum7pm9vhp0yjvl58gvhfc6yfatw4",
    "celestiavaloper1evu846d408jdz5ju4883gtq9pnjvs8hz9cqnwr",
    "celestiavaloper1ej2es5fjztqjcd4pwa0zyvaevtjd2y5wh8xeg4",
    "celestiavaloper1ekr44a2fss4emywwke36cuem46fmatdvw5ks3k",
    "celestiavaloper1ehkfl7palwrh6w2hhr2yfrgrq8jetgucdv9hfp",
    "celestiavaloper1emku8jrvf9dzu80n3sx7wx50chpgjhrws9x62u",
    "celestiavaloper1eualhqh07w7p45g45hvrjagkcxsfnflzdw5jzg",
    "celestiavaloper1e7jh5dt02ee5k6vrfls0ttuxyj9k0g5as4fxux",
    "celestiavaloper16szyeg97a0th858sg3zxalvkq20f6nt0wfpef8",
    "celestiavaloper16exsjvmv5wvnhgu76jhdfs8yqdg0lkynphettt",
    "celestiavaloper1mpt4chntuewyktq64fgrszjp6ly7we5a3t4a8l",
    "celestiavaloper1mrguq0xxlffujne270k90s3vmjetxcr48qnu7m",
    "celestiavaloper1mxdrnzy48vy6ancvhcn9f7g82qz6rdqq3xnrng",
    "celestiavaloper1mwan9sg7dx7epagenprt47w7z3yzz0m9r45asv",
    "celestiavaloper1m07mptc7nhz2qk55qa8xeyqt992sktddtwkvt4",
    "celestiavaloper1mns7w2r823yq2xjtf3mtlemq0l5pqvuzksez78",
    "celestiavaloper1m58punvt32u07ra4p6x7krgxakye3m90rzgm4c",
    "celestiavaloper1mhux0vt6qszz8qwv8axggt02jjm7tuvdfhz78j",
    "celestiavaloper1murrqgqahxevedty0nzqrn5hj434fvffxufxcl",
    "celestiavaloper1m77eksxfz9q50qejnqf720sns7q0xtx8uzxnhs",
    "celestiavaloper1uqj5ul7jtpskk9ste9mfv6jvh0y3w34vtpz3gw",
    "celestiavaloper1u825srldhev7t4wnd3hplhrphahjfk7ff3wfdr",
    "celestiavaloper1ute9v07e2244yttam4n3ynquc4yj60ma7nyypn",
    "celestiavaloper1uvytvhunccudw8fzaxvsrumec53nawyj939gj9",
    "celestiavaloper1uw5jj229cjuanluduy0f0kmaej4qnl3rhsa5e5",
    "celestiavaloper1uwmf03ke52vld2sa9khs0nslpgzwsm5xs5e4pn",
    "celestiavaloper1un77nfm6axkhkupe8fk4xl6fd4adz3y59fucpu",
    "celestiavaloper1u4vhh70lwlt2va7hw5evzl6sap92t0m9nqzmud",
    "celestiavaloper1uau0wsngp9rxampkfwg93ztkyju29e48u0cr65",
    "celestiavaloper1ax83exaawlmy5p2qn22gcynrchwdntt5xvj0qu",
    "celestiavaloper1a45xq89mrtg8sutfzlf9w7l4xz56mq5fche67c",
    "celestiavaloper1ac4mnwg79gyvd0x5trl2fgjv07lgfas02jf378",
    "celestiavaloper1amxp3ah9anq4pmpnsknls7sql3kras9hs8pu0g",
    "celestiavaloper1auqmdc2pnx5gxvakjdsc9v9zc4y2ga0hcaxg9x",
    "celestiavaloper1a74k6chmgked2c5rl8memt4rcngxe5cepsqxw8",
    "celestiavaloper17p8y0sm76zhrtjny98tknevafvlq9860ehykz3",
    "celestiavaloper17z4ssnhfa4wyz979vmzdvdzh2q4rched4e24jp",
    "celestiavaloper17srrapx2cvqyyy4rg3menq0hn86py8f3klelhl",
    "celestiavaloper17h2x3j7u44qkrq0sk8ul0r2qr440rwgj8g0ng0",
    "celestiavaloper17hw6htgj2vadkutyurtq7568g9gz9kz4x7d5tm",
    "celestiavaloper1lqfqp2w65pjsu6hg3qg4qfp4t2t6da4a3gg8ad",
    "celestiavaloper1lrzxwu4dmy8030waevcpft7rpxjjz26csrtqm4",
    "celestiavaloper1lrgfctaxspw8tw52csevj8rexpxk4x92y6dz8y",
    "celestiavaloper1l0zmpm02u240crndlj7hkvlj5azuglv4emfczt",
    "celestiavaloper1lm4jtr6wjwpamz2e9wlgzdazly3vnwqy53t5t4",
]

OKX_NETWORKS_NAME = {
    1                       : 'ETH-ERC20',
    2                       : 'ETH-Arbitrum One',
    3                       : 'ETH-Optimism',
    4                       : 'ETH-zkSync Era',
    5                       : 'ETH-Linea',
    6                       : 'ETH-Base',
    7                       : 'AVAX-Avalanche C-Chain',
    8                       : 'BNB-BSC',
    # 9                     : 'BNB-OPBNB',
    10                      : 'CELO-CELO',
    11                      : 'GLMR-Moonbeam',
    12                      : 'MOVR-Moonriver',
    13                      : 'METIS-Metis',
    14                      : 'CORE-CORE',
    15                      : 'CFX-CFX_EVM',
    16                      : 'KLAY-Klaytn',
    17                      : 'FTM-Fantom',
    18                      : 'POL-Polygon',
    19                      : 'USDT-Arbitrum One',
    20                      : 'USDT-Avalanche C-Chain',
    21                      : 'USDT-Optimism',
    22                      : 'USDT-Polygon',
    23                      : 'USDT-BSC',
    24                      : 'USDT-ERC20',
    25                      : 'USDC-Arbitrum One',
    26                      : 'USDC-Avalanche C-Chain',
    27                      : 'USDC-Optimism',
    28                      : 'USDC-Polygon',
    29                      : 'USDC-Optimism (Bridged)',
    30                      : 'USDC-Polygon (Bridged)',
    31                      : 'USDC-BSC',
    32                      : 'USDC-ERC20',
    # 33                      : 'STG-Arbitrum One',
    # 34                      : 'STG-BSC',
    # 35                      : 'STG-Avalanche C-Chain',
    # 36                      : 'STG-Fantom',
    # 37                      : 'USDV-BSC',
    38                       : 'ARB-Arbitrum One',
    # 39                      : "MAV-BASE",
    # 40                      : "MAV-ZKSYNCERA",
    41                      : "OP-Optimism",
    42                      : "INJ-INJ",
    43                      : "TIA-Celestia",
    # 44                      : "NTRN-NTRN",
    47                      : "SOL-Solana",
    48                      : "OKB-X Layer",
}

BINGX_NETWORKS_NAME = {
    1                       : "ETH-ERC20",
    2                       : "ETH-ARBITRUM",
    3                       : "ETH-OPTIMISM",
    4                       : "ETH-ZKSYNCERA",
    5                       : "ETH-LINEA",
    6                       : "ETH-BASE",
    7                       : 'AVAX-AVAX-C',
    8                       : 'BNB-BEP20',
    # 9                      : 'BNB-OPBNB',
    # 10                      : 'CELO-CELO',
    # 11                    : 'GLMR-Moonbeam',
    # 12                    : 'MOVR-Moonriver',
    13                      : 'METIS-METIS',
    # 14                    : 'CORE-CORE',
    15                      : 'CFX-CFX',
    16                      : 'KLAY-KLAYTN',
    17                      : 'FTM-FANTOM',
    18                      : 'POL-POLYGON',
    19                      : 'USDT-ARBITRUM',
    # 20                    : 'USDT-Avalanche',
    21                      : 'USDT-OPTIMISM',
    22                      : 'USDT-POLYGON',
    23                      : 'USDT-BEP20',
    24                      : 'USDT-ERC20',
    25                      : 'USDC-Arbitrum One (Circle)',
    26                      : 'USDC-AVAX-C',
    27                      : 'USDC-Optimism (Circle)',
    28                      : 'USDC-Polygon (Circle)',
    29                      : 'USDC-Optimism (Bridged)',
    30                      : 'USDC-Polygon (Bridged)',
    31                      : 'USDC-BEP20',
    32                      : 'USDC-ERC20',
    33                      : 'STG-ARBITRUM',
    34                      : 'STG-BEP20',
    # 35                      : 'STG-AVAX-C',
    # 36                      : 'STG-FTM',
    # 37                      : 'USDV-BSC',
    38                      : 'ARB-ARBITRUM',
    # 39                      : "MAV-BASE",
    40                      : "MAV-ZKSYNCERA",
    41                      : "OP-OPTIMISM",
    # 42                      : "INJ-INJ",
    # 43                      : "TIA-TIA",
    44                      : "NTRN-NTRN",
    47                      : "SOL-SOL",
}

BINANCE_NETWORKS_NAME = {
    1                       : "ETH-ETH",
    2                       : "ETH-ARBITRUM",
    3                       : "ETH-OPTIMISM",
    4                       : "ETH-ZKSYNCERA",
    # 5                     : "ETH-LINEA",
    6                       : "ETH-BASE",
    7                       : 'AVAX-AVAXC',
    8                       : 'BNB-BSC',
    9                       : 'BNB-OPBNB',
    10                      : 'CELO-CELO',
    11                      : 'GLMR-Moonbeam',
    12                      : 'MOVR-Moonriver',
    # 13                    : 'METIS-METIS',
    # 14                    : 'CORE-CORE',
    15                      : 'CFX-CFX',
    16                      : 'KLAY-KLAYTN',
    17                      : 'FTM-FANTOM',
    18                      : 'POL-MATIC',
    19                      : 'USDT-ARBITRUM',
    20                      : 'USDT-AVAXC',
    21                      : 'USDT-OPTIMISM',
    22                      : 'USDT-MATIC',
    23                      : 'USDT-BSC',
    24                      : 'USDT-ETH',
    25                      : 'USDC-ARBITRUM',
    26                      : 'USDC-AVAXC',
    27                      : 'USDC-OPTIMISM',
    28                      : 'USDC-MATIC',
    # 29                    : 'USDC-Optimism (Bridged)',
    # 30                    : 'USDC-Polygon (Bridged)',
    31                      : 'USDC-BSC',
    32                      : 'USDC-ETH',
    33                      : 'STG-ARBITRUM',
    34                      : 'STG-BSC',
    35                      : 'STG-AVAXC',
    36                      : 'STG-FTM',
    # 37                      : 'USDV-BSC',
    38                      : 'ARB-ARBITRUM',
    39                      : "MAV-BASE",
    40                      : "MAV-ZKSYNCERA",
    41                      : "OP-OPTIMISM",
    42                      : "INJ-INJ",
    43                      : "TIA-TIA",
    44                      : "NTRN-NTRN",
    45                      : "ETH-MANTA",
    46                      : "ETH-BSC",
    47                      : "SOL-SOL",
}

BITGET_NETWORKS_NAME = {
    1                       : "ETH-ETH",
    2                       : "ETH-ArbitrumOne",
    3                       : "ETH-Optimism",
    4                       : "ETH-zkSyncEra",
    # 5                     : "ETH-LINEA",
    6                       : "ETH-BASE",
    7                       : 'AVAX-C-Chain',
    8                       : 'BNB-BEP20',
    # 9                     : 'BNB-OPBNB',
    10                      : 'CELO-CELO',
    11                      : 'GLMR-Moonbeam',
    12                      : 'MOVR-MOVR',
    13                      : 'METIS-MetisToken',
    14                      : 'CORE-CoreDAO',
    15                      : 'CFX-CFX',
    16                      : 'KLAY-Klaytn',
    17                      : 'FTM-Fantom',
    18                      : 'POL-Polygon',
    19                      : 'USDT-ArbitrumOne',
    20                      : 'USDT-C-Chain',
    21                      : 'USDT-Optimism',
    22                      : 'USDT-Polygon',
    23                      : 'USDT-BEP20',
    24                      : 'USDT-ERC20',
    25                      : 'USDC-ArbitrumOne',
    26                      : 'USDC-C-Chain',
    27                      : 'USDC-OPTIMISM',
    28                      : 'USDC-POLYGON',
    # 29                      : 'USDC-Optimism (Bridged)',
    # 30                      : 'USDC-Polygon (Bridged)',
    31                      : 'USDC-BEP20',
    32                      : 'USDC-ERC20',
    33                      : 'STG-ArbitrumOne',
    # 34                      : 'STG-BEP20',
    # 35                      : 'STG-FANTOM',
    # 36                      : 'STG-C-Chain',
    37                      : 'USDV-BEP20',
    38                      : 'ARB-ArbitrumOne',
    # 39                      : "MAV-BASE",
    # 40                      : "MAV-ZKSYNCERA",
    41                      : "OP-Optimism",
    42                      : "INJ-INJECTIVE",
    43                      : "TIA-Celestia",
    44                      : "NTRN-NEUTRON",
    47                      : "SOL-SOL",
}

STARGATE_ENDPOINTS_ID = {
    'Arbitrum': 30110,
    'Aurora': 30211,
    'Avalanche': 30106,
    'BNB Chain': 30102,
    'Base': 30184,
    'Ethereum': 30101,
    'Kava': 30177,
    'Klaytn': 30150,
    'Linea': 30183,
    'Mantle': 30181,
    'Metis': 30151,
    'Optimism': 30111,
    'Polygon': 30109,
    'Scroll': 30214
}

CEX_WRAPPED_ID = {
     1                          : "Ethereum",
     2                          : "Arbitrum",
     3                          : "Optimism",
     4                          : "zkSync",
     5                          : "Linea",
     6                          : "Base",
     7                          : "Avalanche",
     8                          : "BNB Chain",
     9                          : "OpBNB",
     10                         : "Celo",
     11                         : "Moonbeam",
     12                         : "Moonriver",
     13                         : "Metis",
     14                         : "CoreDAO",
     15                         : "Conflux",
     16                         : "Klaytn",
     17                         : "Fantom",
     18                         : "Polygon",
     19                         : "Arbitrum",
     20                         : "Avalanche",
     21                         : "Optimism",
     22                         : "Polygon",
     23                         : "BNB Chain",
     24                         : "Ethereum",
     25                         : "Arbitrum",
     26                         : "Avalanche",
     27                         : "Optimism",
     28                         : "Polygon",
     29                         : "Optimism",
     30                         : "Polygon",
     31                         : "BNB Chain",
     32                         : "Ethereum",
     33                         : "Arbitrum",
     34                         : "BNB Chain",
     35                         : "Avalanche",
     36                         : "Fantom",
     37                         : "BNB Chain",
     38                         : "Arbtirum",
     39                         : "Base",
     40                         : "zkSync",
     41                         : "Optimism",
     42                         : "Injective",
     43                         : "Celestia",
     44                         : "Neutron",
     45                         : "Manta",
     46                         : "BNB Chain",
     47                         : "Solana",
     48                         : "xLayer",
}

TOKEN_API_INFO = {
    'coingecko': {
        'COREDAO': 'coredaoorg',
        'JEWEL': 'defi-kingdoms',
        'SMR': 'shimmer',
        'TOMOE': 'tomoe',
        'ZBC': 'zebec-protocol'
    },
    'binance': [
        'ETH',
        'ASTR',
        'AVAX',
        'BNB',
        'WBNB',
        'CELO',
        'CFX',
        'FTM',
        'GETH'
        'ONE',
        'ZEN',
        'KAVA',
        'KLAY',
        'AGLD',
        'METIS',
        'GLMR',
        'MOVR',
        'POL',
        'WPOL'
        'BEAM',
        'INJ',
        'WETH',
        'WETH.e',
        'STG',
        'MAV',
        'ARB',
        'OP',
        'TIA',
        'TIA.n',
        'NTRN',
        'ZRO',
        'SOL',
        'ezETH',
        'wrsETH'
    ],
    'gate': [
        'TAIKO',
        'CANTO',
        'FUSE',
        'MNT',
        'MTR',
        'OKT',
        'TLOS',
        'TENET',
        'XPLA',
        'CORE'
    ],
    'stables': [
        'xDAI',
        'DAI',
        'USDT',
        'USDC',
        'USDC.e',
        'BUSD',
        'USDbC',
        'fUSDC',
        'USDB'
    ]
}

OMNICHAIN_NETWORKS_DATA = {
    'Arbitrum':             (110, 'ETH'),
    'Arbitrum Nova':        (175, 'ETH'),
    'Astar':                (210, 'ASTR'),
    'Aurora':               (211, 'ETH'),
    'Avalanche':            (106, 'AVAX'),
    'BNB Chain':            (102, 'BNB'),
    'Base':                 (184, 'ETH'),
    'Canto':                (159, 'CANTO'),
    'Celo':                 (125, 'CELO'),
    'Conflux':              (212, 'CFX'),
    'CoreDAO':              (153, 'COREDAO'),
    'DFK':                  (115, 'JEWEL'),
    'Ethereum':             (101, 'ETH'),
    'Fantom':               (112, 'FTM'),
    'Fuse':                 (138, 'FUSE'),
    'Goerli':               (145, 'GETH'),
    'Gnosis':               (145, 'xDAI'),
    'Harmony ONE':          (116, 'ONE'),
    'Horizen EON':          (215, 'ZEN'),
    'Kava':                 (177, 'KAVA'),
    'Klaytn':               (150, 'KLAY'),
    'Linea':                (183, 'ETH'),
    'Loot':                 (197, 'AGLD'),
    'Manta':                (217, 'ETH'),
    'Mantle':               (181, 'MNT'),
    'Meter':                (176, 'MTR'),
    'Metis':                (151, 'METIS'),
    'Moonbeam':             (126, 'GLMR'),
    'Moonriver':            (167, 'MOVR'),
    'OKX Chain':            (155, 'OKT'),
    'Optimism':             (111, 'ETH'),
    'Orderly':              (213, 'ETH'),
    'Polygon':              (109, 'MATIC'),
    'Polygon zkEVM':        (158, 'ETH'),
    'Scroll':               (214, 'ETH'),
    'ShimmerEVM':           (230, 'SMR'),
    'Telos':                (199, 'TLOS'),
    'TomoChain':            (196, 'TOMOE'),
    'Tenet':                (173, 'TENET'),
    'XPLA':                 (216, 'XPLA'),
    'Zora':                 (195, 'ETH'),
    'opBNB':                (202, 'BNB'),
    'zkSync':               (165, 'ETH'),
    'Beam':                 (198, 'BEAM'),
    'InEVM':                (234, 'INJ'),
    'Rarible':              (235, 'ETH'),
    'Blast':                (243, 'ETH'),
    'Mode':                 (260, 'ETH'),
    'Celestia':             (0, 'TIA'),
    'Neutron':              (0, 'NTRN'),
    'Injective':            (0, 'INJ'),
    'Nautilus':             (0, 'ZBC'),
    'Solana':               (0, 'SOL'),
}

CHAIN_NAME = {
    0: 'OMNI-CHAIN',
    1: 'Arbitrum',
    2: 'Arbitrum Nova',
    3: 'Base',
    4: 'Linea',
    5: 'Manta',
    6: 'Polygon',
    7: 'Optimism',
    8: 'Scroll',
    9: 'Starknet',
    10: 'Polygon zkEVM',
    11: 'zkSync',
    12: 'Zora',
    13: 'Ethereum',
    14: 'Avalanche',
    15: 'BNB Chain',
    16: 'Moonbeam',
    17: 'Harmony ONE',
    18: 'Telos',
    19: 'Celo',
    20: 'Gnosis',
    21: 'CoreDAO',
    22: 'TomoChai',
    23: 'Conflux',
    24: 'Orderly',
    25: 'Horizen',
    26: 'Metis',
    27: 'Astar',
    28: 'OpBNB',
    29: 'Mantle',
    30: 'Moonriver',
    31: 'Klaytn',
    32: 'Kava',
    33: 'Fantom',
    34: 'Aurora',
    35: 'Canto',
    36: 'DFK',
    37: 'Fuse',
    38: 'Goerli',
    39: 'Meter',
    40: 'OKX-Chain',
    41: 'Shimmer',
    42: 'Tenet',
    43: 'XPLA',
    44: 'LootChain',
    45: 'ZKFair',
    46: 'Beam',
    47: 'InEVM',
    48: 'Rarible',
    49: 'Blast',
    50: 'Mode',
    56: 'xLayer',
    57: 'Taiko',
    58: 'DBK',
}


TITLE = """
 ______     __   __     __   __     __     __  __     __     __         ______     ______   ______     ______    
/\  __ \   /\ "-.\ \   /\ "-.\ \   /\ \   /\ \_\ \   /\ \   /\ \       /\  __ \   /\__  _\ /\  __ \   /\  == \   
\ \  __ \  \ \ \-.  \  \ \ \-.  \  \ \ \  \ \  __ \  \ \ \  \ \ \____  \ \  __ \  \/_/\ \/ \ \ \/\ \  \ \  __<   
 \ \_\ \_\  \ \_\ "\_\  \ \_\ "\_\  \ \_\  \ \_\ \_\  \ \_\  \ \_____\  \ \_\ \_\    \ \_\  \ \_____\  \ \_\ \_\ 
  \/_/\/_/   \/_/ \/_/   \/_/ \/_/   \/_/   \/_/\/_/   \/_/   \/_____/   \/_/\/_/     \/_/   \/_____/   \/_/ /_/                                                                                                                                                                                                     
"""

(
    ACCOUNT_NAMES, EVM_PRIVATE_KEYS, MNEMONICS, SOLANA_PRIVATE_KEYS, PROXIES, OKX_EVM_WALLETS, BITGET_EVM_WALLETS,
    OKX_INJ_WALLETS, BITGET_INJ_WALLETS, OKX_TIA_WALLETS, BITGET_TIA_WALLETS, BITGET_NTRN_WALLETS
) = get_accounts_data()
