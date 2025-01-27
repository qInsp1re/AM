from time import time
from modules import DEX, Logger, Client
from utils.tools import gas_checker, helper
from config.constants import (
    TRADERJOE_CONTRACTS,
    TOKENS_PER_CHAIN
)
from config.abi import TRADERJOE_ABI


class TraderJoeXyz(DEX, Logger):
    def __init__(self, client: Client):
        self.client = client
        Logger.__init__(self)
        self.network = self.client.network.name
        self.router_contract = self.client.get_contract(
            TRADERJOE_CONTRACTS[self.network]['router'], TRADERJOE_ABI['router']
        )
        self.quoter_contract = self.client.get_contract(
            TRADERJOE_CONTRACTS[self.network]['quoter'], TRADERJOE_ABI['quoter']
        )

    async def get_min_amount_out(self, from_token_address, to_token_address, amount_in_wei: int):
        quote_data = await self.quoter_contract.functions.findBestPathFromAmountIn(
            [
                from_token_address,
                # TOKENS_PER_CHAIN[self.network]['USDT'],
                # TOKENS_PER_CHAIN[self.network]['USDC.e'],
                to_token_address,
            ],
            amount_in_wei
        ).call()

        tokens_path, liquidity_book, pait_bin1, pait_bin2, quote_info, _, _ = quote_data

        return tokens_path, pait_bin1, pait_bin2, int(quote_info[1] - (quote_info[1] / 100 * 1))

    @helper
    @gas_checker
    async def swap(self, swap_data: list):
        from_token_name, to_token_name, amount, amount_in_wei = swap_data

        self.logger_msg(*self.client.acc_info, msg=f'Swap on Trader Joe: {amount} {from_token_name} -> {to_token_name}')

        from_token_address = TOKENS_PER_CHAIN[self.network][from_token_name]
        to_token_address = TOKENS_PER_CHAIN[self.network][to_token_name]

        deadline = int(time()) + 1800
        tokens_path, pait_bin1, pait_bin2, min_amount_out = await self.get_min_amount_out(
            from_token_address, to_token_address, amount_in_wei
        )

        await self.client.price_impact_defender(from_token_name, amount, to_token_name, min_amount_out)

        if from_token_name != 'ETH':
            await self.client.check_for_approved(
                from_token_address, TRADERJOE_CONTRACTS[self.network]['router'], amount_in_wei
            )

        path = [
            pait_bin1,
            pait_bin2,
            tokens_path
        ]

        full_data = (
            min_amount_out,
            path,
            self.client.address,
            deadline
        )

        tx_params = await self.client.prepare_transaction(value=amount_in_wei if from_token_name == 'ETH' else 0)
        if from_token_name == 'ETH':
            transaction = await self.router_contract.functions.swapExactNATIVEForTokens(
                *full_data
            ).build_transaction(tx_params)
        elif to_token_name == 'ETH':
            transaction = await self.router_contract.functions.swapExactTokensForNATIVE(
                amount_in_wei,
                *full_data
            ).build_transaction(tx_params)
        else:
            transaction = await self.router_contract.functions.swapExactTokensForTokens(
                amount_in_wei,
                *full_data
            ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)
