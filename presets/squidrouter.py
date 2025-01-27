CLASSIC_ROUTES_BLOCKS_COUNT = [1, 1]  # Количество блоков к работе для одного аккаунта. Указывайте от 1 до 7 блоков

ADD_FEE_SUPPORT_FOR_TXS = True  # софт добавит в маршрут первым модулем fee_support_withdraw. см. FEE_SUPPORT_DATA

CLASSIC_ROUTES_MODULES_USING = [
    # при наличии блоков (круглые скобки для маршрута), софт будет их мешать для каждого аккаунта
    ['okx_custom_withdraw_4'],  # см. OKX_CUSTOM_WITHDRAW_4
    (  # блок работы с SquidRouter (4 случайных бриджа ETH между Arbitrum, Optimism, Base, Linea
        ['smart_wrap_eth', 'smart_transfer_eth', 'smart_random_approve', None],
        ['bridge_l2pass', 'bridge_nogem', 'bridge_merkly', 'bridge_zerius', None, None],
        ['smart_organic_swaps', 'smart_organic_landings', None],
        ['bridge_squidrouter'],
        ['bridge_hyperlane_nft', 'bridge_hyperlane_token', 'bridge_getmint', 'bridge_womex', 'bridge_nogem_hnft', None],
        ['bridge_squidrouter'],
        ['smart_organic_swaps', 'smart_organic_landings', None],
        ['bridge_squidrouter'],
        ['fee_support_withdraw_for_arb'],
        ['mint_squid_scholar_nft'],
        ['bridge_hyperlane_nft', 'bridge_hyperlane_token', 'bridge_getmint', 'bridge_womex', 'bridge_nogem_hnft', None],
        ['bridge_squidrouter'],
        ['smart_organic_swaps', 'smart_organic_landings', None],
        ['bridge_getmint', 'bridge_womex', 'bridge_hyperlane_nft', 'bridge_hyperlane_token', None],
    ),
    ['okx_deposit'],
]
