import base64
from modules import RequestClient, Logger, SolanaClient
from utils.tools import gas_checker, helper
from config.constants import TOKENS_PER_CHAIN


class Jupiter(RequestClient, Logger):
    def __init__(self, client: SolanaClient):
        self.client = client
        Logger.__init__(self)
        RequestClient.__init__(self, client)
        self.network = self.client.network.name

    async def get_quote(self, from_token_address:str, to_token_address:str, amount_in_wei: int):
        url = 'https://quote-api.jup.ag/v6/quote'

        headers = {
            "accept": "application/json",
            "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"123\", \"Chromium\";v=\"123\", \"Not.A/Brand\";v=\"23\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "referrer": "https://station.jup.ag/",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "body": 'null',
            "method": "GET",
            "mode": "cors",
            "credentials": "omit"
        }

        params = {
            "inputMint": from_token_address, #"So11111111111111111111111111111111111111112",
            "outputMint": to_token_address, #"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            "amount": int(amount_in_wei),
        }

        return await self.make_request(url=url, params=params, headers=headers)

    async def get_swap_ixs(self, quote):
        ixs_url = 'https://quote-api.jup.ag/v6/swap'

        payload = {
            "userPublicKey": f"{self.client.wallet.pubkey()}",
            "quoteResponse": quote
        }

        return await self.make_request("POST", url=ixs_url, json=payload)

    @helper
    @gas_checker
    async def swap(self, swap_data: list):
        from_token_name, to_token_name, amount, amount_in_wei = swap_data

        self.logger_msg(*self.client.acc_info, msg=f"Swap on Jupiter: {amount} {from_token_name} -> {to_token_name}")

        token_data = TOKENS_PER_CHAIN[self.network]
        chain_token_name = self.client.token
        from_token_address = token_data['WSOL'] if from_token_name == chain_token_name else token_data[from_token_name]
        to_token_address = token_data['WSOL'] if to_token_name == chain_token_name else token_data[to_token_name]

        quote = await self.get_quote(from_token_address, to_token_address, amount_in_wei)
        instructions = await self.get_swap_ixs(quote)

        raw_tx_bytes = base64.b64decode(instructions['swapTransaction'])
        transaction = await self.client.create_v0_message(raw_tx_bytes)

        return await self.client.send_transaction(message=transaction)

