import uuid

from modules.interfaces import SoftwareException
from dev_settings import Settings
from config.constants import TOKENS_PER_CHAIN, CHAIN_NAME_FROM_ID
from general_settings import SLIPPAGE, UNLIMITED_APPROVE
from modules import RequestClient, Logger


class Rango(RequestClient, Logger):
    def __init__(self, client):
        self.client = client
        Logger.__init__(self)
        RequestClient.__init__(self, client)
        self.network = self.client.network.name

    async def get_quote(
            self, from_token_address, to_token_address, from_token_name, to_token_name, amount, dst_chain_name
    ):
        api_key = 'ffde5b24-ee86-4f47-a1c8-b22d8f639a38'

        url = f"https://api.rango.exchange:443/routing/best?apiKey={api_key}"

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7",
            "content-type": "application/json",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"123\", \"Google Chrome\";v=\"123\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "x-rango-id": f"{uuid.uuid4()}",
            "referrer": "https://app.rango.exchange/",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "method": "POST",
            "mode": "cors",
            "credentials": "omit"
        }

        scr_chain_name = self.client.network.name.upper() if self.client.network.name != 'Ethereum' else 'ETH'
        dst_chain_name = dst_chain_name.upper() if dst_chain_name != 'Ethereum' else 'ETH'

        quote_payload = {
            "amount": amount,
            "from": {
                "address": from_token_address,
                "blockchain": scr_chain_name,
                "symbol": from_token_name
            },
            "to": {
                "address": to_token_address,
                "blockchain": dst_chain_name,
                "symbol": to_token_name
            },
            "connectedWallets": [
                {
                    "blockchain": "ETH",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "BSC",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "ARBITRUM",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "POLYGON",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "ZKSYNC",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "OPTIMISM",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "AVAX_CCHAIN",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "POLYGONZK",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "BASE",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "LINEA",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "SCROLL",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "BLAST",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "METIS",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "CRONOS",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "AURORA",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "BOBA",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "MOONBEAM",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "MOONRIVER",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "OKC",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "HECO",
                    "addresses": [
                        self.client.address
                    ]
                },
                {
                    "blockchain": "CELO",
                    "addresses": [
                        self.client.address
                    ]
                }
            ],
            "selectedWallets": {
                scr_chain_name: self.client.address,
                dst_chain_name: self.client.address,
            },
            "slippage": 1,
            "swapperGroups": [],
            "swappersGroupsExclude": True,
            "enableCentralizedSwappers": True
        }

        response = await self.make_request(method='POST', url=url, headers=headers, json=quote_payload)

        if response.get('result'):
            return response
        error = response.get('diagnosisMessages')
        raise SoftwareException(
            error[0] if error else f"Can`t find route for swap {amount} {from_token_name} -> {to_token_name}")

    async def get_swap_data(self, request_id, step_len):

        api_key = 'ffde5b24-ee86-4f47-a1c8-b22d8f639a38'

        url = f"https://api.rango.exchange/tx/create?apiKey={api_key}"

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7",
            "content-type": "application/json",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "referrer": "https://app.rango.exchange/",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "method": "POST",
            "mode": "cors",
            "credentials": "omit"
        }

        swap_payload = {
            "userSettings": {
                "slippage": SLIPPAGE,
                "infiniteApprove": UNLIMITED_APPROVE
            },
            "validations": {
                "balance": True,
                "fee": True,
                "approve": False
            },
            "requestId": request_id,
            "step": step_len
        }

        response = await self.make_request(method='POST', url=url, headers=headers, json=swap_payload)
        if not response.get('error'):
            return response
        raise SoftwareException(response.get('error'))

    async def bridge(self, bridge_data: tuple = None, need_check: bool = False):

        if need_check:
            return 0

        if len(bridge_data) == 8:
            (from_chain, to_chain, amount, from_token_name, to_token_name,
             from_token_address, to_token_address, chain_to_name) = bridge_data

            decimals = await self.client.get_decimals(token_address=from_token_address)
            amount_in_wei = self.client.to_wei(amount, decimals)
            dst_chain_name = CHAIN_NAME_FROM_ID[to_chain]
            from_token_address = None if from_token_name == self.client.token else from_token_address
        else:
            tokens_data = TOKENS_PER_CHAIN[self.client.network.name]
            src_chain_name, dst_chain_name, from_token_name, to_token_name, amount, amount_in_wei = bridge_data
            from_token_address = None if from_token_name == self.client.token else tokens_data[from_token_name]

        bridge_info = f'{self.client.network.name} -> {to_token_name} {dst_chain_name}'
        self.logger_msg(*self.client.acc_info, msg=f'Bridge on Rango: {amount} {from_token_name} {bridge_info}')

        if to_token_name in ['BNB', 'MATIC', 'AVAX', 'ETH']:
            to_token_address = None
        else:
            to_token_address = TOKENS_PER_CHAIN[dst_chain_name][to_token_name]

        data = from_token_address, to_token_address, from_token_name, to_token_name, amount

        quote_data = await self.get_quote(*data, dst_chain_name)
        swap_data = await self.get_swap_data(quote_data['requestId'], len(quote_data["result"]['swaps']))

        contract_address = self.client.w3.to_checksum_address(swap_data['transaction']['to'])

        if from_token_name != 'ETH':
            await self.client.check_for_approved(from_token_address, contract_address, amount_in_wei)

        tx_params = (await self.client.prepare_transaction(value=amount_in_wei if from_token_name == "ETH" else 0)) | {
            'data': swap_data['transaction']['data'],
            'to': contract_address
        }

        old_balance_data_on_dst = await self.client.wait_for_receiving(
            chain_to_name=dst_chain_name, token_name=to_token_name, token_address=to_token_address,
            check_balance_on_dst=True
        )

        await self.client.send_transaction(tx_params)

        if Settings.WAIT_FOR_RECEIPT:

            self.logger_msg(
                *self.client.acc_info, msg=f"Bridge complete. Note: wait a little for receiving funds",
                type_msg='success'
            )

            return await self.client.wait_for_receiving(
                chain_to_name=dst_chain_name, token_name=to_token_name, token_address=to_token_address,
                old_balance_data=old_balance_data_on_dst,
            )
        else:
            return True
