CLASSIC_ROUTES_BLOCKS_COUNT = [7, 7]  # Количество блоков к работе для одного аккаунта. Указывайте от 1 до 7 блоков

ADD_FEE_SUPPORT_FOR_TXS = True  # софт добавит в маршрут первым модулем fee_support_withdraw. см. FEE_SUPPORT_DATA

CLASSIC_ROUTES_MODULES_USING = [
    # при наличии блоков (круглые скобки для маршрута), софт будет их мешать для каждого аккаунта
    ['okx_custom_withdraw_4'],  # см. OKX_CUSTOM_WITHDRAW_4
    (  # блок работы с Merkly (4 случайных бриджа ETH между Arbitrum, Optimism, Base
        ['smart_wrap_eth', 'smart_transfer_eth', 'smart_random_approve', None],
        ['bridge_l2pass', 'bridge_nogem', 'bridge_merkly', 'bridge_zerius', None, None],
        ['smart_organic_swaps', 'smart_organic_landings', None],
        ['bridge_hyperlane_merkly'],
        ['bridge_hyperlane_nft', 'bridge_hyperlane_token', 'bridge_getmint', 'bridge_womex', 'bridge_nogem_hnft', None],
        ['bridge_hyperlane_merkly', 'bridge_superform'],
        ['bridge_hyperlane_nft', 'bridge_hyperlane_token', 'bridge_getmint', 'bridge_womex', 'bridge_nogem_hnft', None],
        ['bridge_hyperlane_merkly'],
        ['smart_organic_swaps', 'smart_organic_landings', None],
        ['bridge_hyperlane_merkly', None],
        ['bridge_getmint', 'bridge_womex', 'bridge_hyperlane_nft', 'bridge_hyperlane_token', None],
    ),
    (  # блок работы с inEVM (4 бриджа INJ между Injective и inEVM
        ['okx_custom_withdraw_2'],  # см. OKX_CUSTOM_WITHDRAW_2
        ['smart_wrap_eth', 'smart_transfer_eth', 'smart_random_approve', None],
        ['smart_transfer_cosmos', 'smart_transfer_cosmos_to_cex', None],
        ['bridge_hyperlane_nft', 'bridge_hyperlane_token', 'bridge_getmint', 'bridge_womex', 'bridge_nogem_hnft', None],
        ['bridge_inevm'],
        ['smart_organic_swaps', None],
        ['bridge_inevm'],
        ['smart_transfer_cosmos', 'smart_transfer_cosmos_to_cex', None],
        ['bridge_inevm'],
        ['smart_organic_swaps', None],
        ['bridge_hyperlane_nft', 'bridge_hyperlane_token', 'bridge_getmint', 'bridge_womex', 'bridge_nogem_hnft', None],
        ['bridge_inevm'],
        ['smart_transfer_cosmos', 'smart_transfer_cosmos_to_cex', None],
        ['okx_custom_deposit_1'],
    ),
    (  # блок работы с UseNexus (5 бриджей TIA.n по строгому маршруту (Celestia->Neutron->ARB->Neutron->Celestia))
        ['bitget_custom_withdraw_1'],  # см. BITGET_CUSTOM_WITHDRAW_1
        ['binance_custom_withdraw_1'],  # см. BINANCE_CUSTOM_WITHDRAW_1
        ['fee_support_withdraw_for_arb'],  # см. OKX_CUSTOM_WITHDRAW_3
        ['smart_wrap_eth', 'smart_transfer_eth', 'smart_random_approve', None],
        ['smart_stake_tia', 'smart_transfer_cosmos', 'smart_transfer_cosmos_to_cex', None],
        ['bridge_hyperlane_nft', 'bridge_hyperlane_token', 'bridge_getmint', 'bridge_womex', 'bridge_nogem_hnft', None],
        ['bridge_usenexus'],
        ['bridge_hyperlane_nft', 'bridge_hyperlane_token', 'bridge_getmint', 'bridge_womex', 'bridge_nogem_hnft', None],
        ['bridge_usenexus'],
        ['bridge_hyperlane_nft', 'bridge_hyperlane_token', 'bridge_getmint', 'bridge_womex', 'bridge_nogem_hnft', None],
        ['bridge_usenexus'],
        ['bridge_hyperlane_nft', 'bridge_hyperlane_token', 'bridge_getmint', 'bridge_womex', 'bridge_nogem_hnft', None],
        ['bridge_usenexus'],
        ['smart_stake_tia', 'smart_transfer_cosmos', 'smart_transfer_cosmos_to_cex', None],
        ['bitget_deposit'],
    ),
    (  # блок работы с Nautilus (4 бриджа USDT между BNB Chain и Nautilus)
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
        ['smart_organic_swaps', None],
        ['bitget_deposit'],
    ),
    ['okx_deposit'],
]
