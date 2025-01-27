from modules import RequestClient, Logger
from utils.tools import gas_checker, helper
from config.constants import TOKENS_PER_CHAIN, ETH_MASK


class OpenOcean(RequestClient, Logger):
    def __init__(self, client):
        self.client = client
        Logger.__init__(self)
        RequestClient.__init__(self, client)
        self.network = self.client.network.name

    async def build_swap_transaction(self, from_token_address: str, to_token_address: str, amount: float):

        url = f'https://open-api.openocean.finance/v3/{self.client.chain_id}/swap_quote'

        params = {
            'chain': self.client.chain_id,
            'inTokenAddress': from_token_address,
            'outTokenAddress': to_token_address,
            'amount': f"{amount}",
            'gasPrice': str(self.client.w3.from_wei(await self.client.w3.eth.gas_price, 'gwei')),
            'slippage': 3,
            'account': self.client.address
        }

        return await self.make_request(url=url, params=params)

    @helper
    @gas_checker
    async def swap(self, swap_data: list):
        from_token_name, to_token_name, amount, amount_in_wei = swap_data

        self.logger_msg(*self.client.acc_info, msg=f"Swap on OpenOcean: {amount} {from_token_name} -> {to_token_name}")

        token_data = TOKENS_PER_CHAIN[self.network]

        if '0x' not in from_token_name:
            from_token_address = ETH_MASK if from_token_name == self.client.token else token_data[from_token_name]
        else:
            from_token_address = ETH_MASK if from_token_name == self.client.token else from_token_name

        if '0x' not in to_token_name:
            to_token_address = ETH_MASK if to_token_name == self.client.token else token_data[to_token_name]
        else:
            to_token_address = ETH_MASK if to_token_name == self.client.token else to_token_name

        swap_quote_data = await self.build_swap_transaction(from_token_address, to_token_address, amount)
        contract_address = self.client.w3.to_checksum_address(swap_quote_data["data"]["to"])

        if from_token_name != "ETH":
            await self.client.check_for_approved(
                from_token_address, contract_address, amount_in_wei, unlimited_approve=True
            )

        tx_params = (await self.client.prepare_transaction()) | {
            "to": contract_address,
            "data": swap_quote_data["data"]["data"],
            "value": int(swap_quote_data["data"]["value"])
        }

        return await self.client.send_transaction(tx_params)
