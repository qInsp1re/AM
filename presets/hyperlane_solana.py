ONEINCH_SWAP_AMOUNT = ("85", "90")

BITGET_WITHDRAW_DATA = [
    [8, ('80', '100')],
]

BITGET_DEPOSIT_DATA = [
    [8, ('100', '100'), 0, (0.4, 0.5)],
]

NAUTILUS_CHAINS = ["Nautilus", "Solana"]
NAUTILUS_TOKENS = ['ZBC', 'ZBC']
NAUTILUS_AMOUNT = ('100', '100')
NAUTILUS_BRIDGE_COUNT = 1
NAUTILUS_RUN_TIMES = 1
NAUTILUS_AMOUNT_LIMITER = 0, (0, 0)

CLASSIC_ROUTES_BLOCKS_COUNT = [1, 1]  # Количество блоков к работе для одного аккаунта. Указывайте от 1 до 7 блоков

ADD_FEE_SUPPORT_FOR_TXS = True  # софт добавит в маршрут первым модулем fee_support_withdraw. см. FEE_SUPPORT_DATA

CLASSIC_ROUTES_MODULES_USING = [
    # при наличии блоков (круглые скобки для маршрута), софт будет их мешать для каждого аккаунта
    (  # блок работы с Nautilus (4 бриджа ZBC между Solana и Nautilus)
        ['bitget_custom_withdraw_2'],  # см. BITGET_CUSTOM_WITHDRAW_2
        ['smart_wrap_eth', 'smart_transfer_eth', 'smart_random_approve', None],
        ['bridge_hyperlane_nft', 'bridge_hyperlane_token', 'bridge_getmint', 'bridge_womex', 'bridge_nogem_hnft', None],
        ['swap_bnb_to_zbc_bsc'],
        ['refuel_nautilus'],
        ['bridge_hyperlane_nft', 'bridge_hyperlane_token', 'bridge_getmint', 'bridge_womex', 'bridge_nogem_hnft', None],
        ['bridge_nautilus'],
        ['bridge_l2pass', 'bridge_nogem', 'bridge_merkly', 'bridge_zerius', None, None],
        ['bridge_nautilus'],
        ['smart_organic_swaps', None],
        ['bridge_nautilus'],
        ['bridge_hyperlane_nft', 'bridge_hyperlane_token', 'bridge_getmint', 'bridge_womex', 'bridge_nogem_hnft', None],
        ['bridge_nautilus'],
        ['swap_bnb_to_zbc_bsc'],
        ['refuel_nautilus'],
        ['smart_organic_swaps', None],
        ['bitget_deposit'],
    )
]
