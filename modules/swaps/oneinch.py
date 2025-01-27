import asyncio

from modules import RequestClient, Logger
from utils.tools import gas_checker, helper
from general_settings import ONEINCH_API_KEY
from config.constants import TOKENS_PER_CHAIN, ETH_MASK


class OneInch(RequestClient, Logger):
    def __init__(self, client):
        self.client = client
        Logger.__init__(self)
        RequestClient.__init__(self, client)
        self.network = self.client.network.name

    async def get_contract_address(self):
        url = f"https://api.1inch.dev/swap/v5.2/{self.client.chain_id}/approve/spender"

        headers = {
            'Authorization': f'Bearer {ONEINCH_API_KEY}',
            'accept': 'application/json'
        }

        return await self.make_request(url=url, headers=headers)

    async def build_swap_transaction(self, from_token_address: str, to_token_address: str, amount: int):

        url = f"https://api.1inch.dev/swap/v5.2/{self.client.chain_id}/swap"

        headers = {
            'Authorization': f'Bearer {ONEINCH_API_KEY}',
        }

        params = {
            "src": from_token_address,
            "dst": to_token_address,
            "amount": amount,
            "from": self.client.address,
            "slippage": 2,
            "disableEstimate": "true",
        }

        return await self.make_request(url=url, params=params, headers=headers)

    @helper
    @gas_checker
    async def swap(self, swap_data: list):
        from_token_name, to_token_name, amount, amount_in_wei = swap_data

        self.logger_msg(*self.client.acc_info, msg=f"Swap on 1INCH: {amount} {from_token_name} -> {to_token_name}")

        token_data = TOKENS_PER_CHAIN[self.network]

        chain_token_name = self.client.token

        if '0x' not in from_token_name:
            from_token_address = ETH_MASK if from_token_name == self.client.token else token_data[from_token_name]
        else:
            from_token_address = ETH_MASK if from_token_name == self.client.token else from_token_name

        if '0x' not in to_token_name:
            to_token_address = ETH_MASK if to_token_name == self.client.token else token_data[to_token_name]
        else:
            to_token_address = ETH_MASK if to_token_name == self.client.token else to_token_name

        contract_address = self.client.w3.to_checksum_address((await self.get_contract_address())['address'])

        if from_token_name != chain_token_name:
            await self.client.check_for_approved(from_token_address, contract_address, amount_in_wei)

        await asyncio.sleep(5)

        swap_quote_data = await self.build_swap_transaction(from_token_address, to_token_address, amount_in_wei)

        tx_param = (await self.client.prepare_transaction()) | {
            "to": contract_address,
            "data": swap_quote_data["tx"]["data"],
            "value": int(swap_quote_data["tx"]["value"]),
        }

        return await self.client.send_transaction(tx_param)
