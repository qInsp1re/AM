import json
import random

from eth_abi import abi
from web3 import AsyncWeb3
from modules import Logger, Client, CosmosClient
from modules.interfaces import Bridge, BridgeExceptionWithoutRetry, SoftwareExceptionWithoutRetry
from utils.tools import gas_checker, helper
from config.constants import (
    TOKENS_PER_CHAIN, CHAIN_IDS, ETH_MASK,
    POLYGON_SCHOLAR_NFT_CONTRACT
)
from config.abi import SQUID_SCHOLAR_NFT_CONTRACT_ABI


class SquidRouter(Bridge, Logger):
    def __init__(self, client: Client | CosmosClient):
        self.client = client
        Logger.__init__(self)
        Bridge.__init__(self, client)
        self.network = self.client.network.name

    async def get_quote(
            self, dst_chain_id, dst_client_address, from_token_address, to_token_address, amount_in_wei, cosmos_mode,
            enable_express
    ):
        url = "https://api.squidrouter.com/v1/route"

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"123\", \"Chromium\";v=\"123\", \"Not.A/Brand\";v=\"23\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "x-integrator-id": "squid-swap-widget",
            "referrer": "https://app.squidrouter.com/",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "body": "null",
            "method": "GET",
            "mode": "cors",
            "credentials": "omit"
        }

        params = {
            "fromChain": self.client.chain_id,
            "fromToken": from_token_address,
            "fromAddress": f"{self.client.address}",
            "fromAmount": amount_in_wei,
            "toChain": dst_chain_id,
            "toToken": to_token_address,
            "toAddress": dst_client_address,
            "quoteOnly": "false",
            "slippage": 1.5,
            "enableExpress": "false" if not enable_express else "true"
        }

        if cosmos_mode:
            from functions import CosmosClient
            from functions import OsmosisRPC
            self.client.module_input_data["network"] = OsmosisRPC
            cosmos_client = CosmosClient(self.client.module_input_data)
            await cosmos_client.session.close()

            params['fallbackAddresses[]'] = json.dumps({
                "address": f"{cosmos_client.address}",
                "coinType": 118
            })

        response = await self.make_request(url=url, params=params, headers=headers)

        if response['route']:
            return response['route']

        raise BridgeExceptionWithoutRetry(f'Bad request to SquidRouter API: {await response.text()}')

    @helper
    @gas_checker
    async def bridge(self, bridge_data: tuple, swap_mode: bool = False):

        if swap_mode:
            src_chain_name = dst_chain_name = self.client.network.name
            from_token_name, to_token_name, amount, amount_in_wei = bridge_data
        else:
            src_chain_name, dst_chain_name, from_token_name, to_token_name, amount, amount_in_wei = bridge_data

        types_info = {
            'Celestia': 1,
            'Neutron': 1,
            'Injective': 1,
        }

        source_chain_type = types_info.get(src_chain_name, 0)
        destination_chain_type = types_info.get(dst_chain_name, 0)

        decimals = await self.client.get_decimals(from_token_name) if from_token_name != self.client.token else 18
        amount_in_wei = self.client.to_wei(amount, decimals=decimals)

        cosmos_mode = False
        enable_express = False
        if from_token_name in ['BNB', 'MATIC', 'AVAX', 'ETH']:
            from_token_address = ETH_MASK
        else:
            from_token_address = TOKENS_PER_CHAIN[src_chain_name][from_token_name]

        if to_token_name in ['BNB', 'MATIC', 'AVAX', 'ETH']:
            to_token_address = ETH_MASK
        else:
            to_token_address = TOKENS_PER_CHAIN[dst_chain_name][to_token_name]

        if not source_chain_type and destination_chain_type:
            from modules import CosmosClient
            from functions import CelestiaRPC, NeutronRPC, INJ_RPC

            rpc = {
                'Celestia': CelestiaRPC,
                'Neutron': NeutronRPC,
                'Injective': INJ_RPC,
            }[dst_chain_name]

            cosmos_mode = True
            self.client.module_input_data["network"] = rpc
            cosmos_client = CosmosClient(self.client.module_input_data)
            await cosmos_client.session.close()
            dst_client_address = f"{cosmos_client.address}"
            dst_chain_id_onchain = cosmos_client.chain_id

        elif source_chain_type and not destination_chain_type:
            from modules import Client
            from functions import ArbitrumRPC
            self.client.module_input_data["network"] = ArbitrumRPC
            evm_client = Client(self.client.module_input_data)

            cosmos_mode = True
            enable_express = True
            await evm_client.session.close()
            dst_client_address = f"{evm_client.address}"
            dst_chain_id_onchain = CHAIN_IDS[dst_chain_name]
        else:
            dst_chain_id_onchain = CHAIN_IDS[dst_chain_name]
            dst_client_address = self.client.address

        quoted_route = await self.get_quote(
            dst_chain_id_onchain, dst_client_address, from_token_address, to_token_address, amount_in_wei,
            cosmos_mode=cosmos_mode, enable_express=enable_express
        )

        if from_token_name == self.client.token or f"u{from_token_name.lower()}" == self.client.token:

            gas_cost = int(random.uniform(0.0001, 0.00015) * 10 ** 18)
            fee_cost = sum([int(fee_data['amount']) for fee_data in quoted_route['estimate']['feeCosts']])
            amount = round(amount, 6) - ((fee_cost + gas_cost) / 10 ** decimals)

            if amount < 0:
                raise SoftwareExceptionWithoutRetry('Account balance < bridge fee')

            amount_in_wei = self.client.to_wei(amount, decimals)

            quoted_route = await self.get_quote(
                dst_chain_id_onchain, dst_client_address, from_token_address, to_token_address, amount_in_wei,
                cosmos_mode=cosmos_mode, enable_express=enable_express
            )

        if amount < 0:
            raise SoftwareExceptionWithoutRetry('Account balance < bridge fee')

        bridge_info = f'{self.client.network.name} -> {to_token_name} {dst_chain_name}'
        self.logger_msg(
            *self.client.acc_info, msg=f'Bridge on SquidRouter: {amount:.6f} {from_token_name} {bridge_info}.'
            # Fee: {fee_info:.4f} {from_token_name}'
        )

        if not source_chain_type:
            to_address = AsyncWeb3().to_checksum_address(quoted_route['transactionRequest']['targetAddress'])
            tx_data = quoted_route['transactionRequest']['data']
            value = int(quoted_route['transactionRequest']['value'])

            if from_token_name != self.client.token:
                await self.client.check_for_approved(from_token_address, to_address, amount_in_wei)

            transaction = await self.client.prepare_transaction(value=value) | {
                'to': to_address,
                'data': tx_data,
            }

            old_balance_data_on_dst = await self.client.wait_for_receiving(
                chain_to_name=dst_chain_name, token_name=to_token_name, token_address=to_token_address,
                check_balance_on_dst=True
            )

            await self.client.send_transaction(transaction)

        else:
            raise SoftwareExceptionWithoutRetry('Software do not support Cosmos -> EVM route')
            # class CustomDict(dict):
            #     def __init__(self, *args, **kwargs):
            #         super().__init__(*args, **kwargs)
            #         self.DESCRIPTOR = Descriptor()  # Инициализация атрибута DESCRIPTOR
            #
            #     def set_descriptor(self, value):
            #         self.DESCRIPTOR.full_name = value
            #
            #     def get_descriptor(self):
            #         return self.DESCRIPTOR.full_name
            #
            # class Descriptor:
            #     def __init__(self):
            #         self.full_name = None
            #
            # tx_data = CustomDict(json.loads(quoted_route['transactionRequest']['data']))
            # tx_data.DESCRIPTOR.full_name = tx_data['msgTypeUrl']
            # # gas_fee = quoted_route['transactionRequest']['data']
            # # gas_limit = int(quoted_route['transactionRequest']['gasLimit'])
            #
            # import math
            # gas_limit = random.randint(235000, 245000)
            # gas_fee = math.ceil(gas_limit * self.client.network_config.fee_minimum_gas_price)
            #
            # timeout_height = Height(revision_number=0, revision_height=0)
            # coin = Coin(amount=str(tx_data['msg']['token']['amount']), denom=tx_data['msg']['token']['denom'])
            # msg = MsgTransfer(
            #     source_port="transfer",
            #     source_channel=channel,
            #     token=coin,
            #     sender=f"{self.client.address}",
            #     receiver=f"{dst_address}",
            #     timeout_height=timeout_height,
            #     timeout_timestamp=timestamp,
            # )
            #
            #
            # # if self.client.network.name == 'Celestia':
            # #     amount_in_wei -= int(gas_fee * 5)  # fee support for bridge
            # #value = int(quoted_route['transactionRequest']['value'])
            #
            # old_balance_on_dst = await self.client.wait_for_receiving(
            #     token_name=to_token_name, chain_id=dst_chain_id, check_balance_on_dst=True
            # )
            #
            # await self.client.send_transaction(tx_data, gas_fee=gas_fee, gas_limit=gas_limit)

        self.logger_msg(*self.client.acc_info,
                        msg=f"Bridge complete. Note: wait a little for receiving funds", type_msg='success')

        return await self.client.wait_for_receiving(
                chain_to_name=dst_chain_name, token_name=to_token_name, token_address=to_token_address,
                old_balance_data=old_balance_data_on_dst,
        )

    async def get_data(self, approve_calldata: str, transfer_calldata: str, claim_calldata: str, from_amount: int):
        url = 'https://api.squidrouter.com/v1/route'

        params = {
            "fromChain": 42161,
            "fromToken": ETH_MASK,
            "fromAddress": self.client.address,
            "fromAmount": from_amount,
            "toChain": 137,
            "toToken": TOKENS_PER_CHAIN['Polygon']['USDC'],
            "toAddress": self.client.address,
            "quoteOnly": 'false',
            "slippage": 1.5,
            "enableExpress": 'true',
            "customContractCalls": json.dumps([
                {
                    "callType": 0,
                    "target": TOKENS_PER_CHAIN['Polygon']['USDC'],
                    "value": "0",
                    "callData": approve_calldata,
                    "payload": {
                        "tokenAddress": TOKENS_PER_CHAIN['Polygon']['USDC'],
                        "inputPos": 1
                    },
                    "estimatedGas": "40000"
                },
                {
                    "callType": 0,
                    "target": POLYGON_SCHOLAR_NFT_CONTRACT,
                    "value": "0",
                    "callData": claim_calldata,
                    "payload": {
                        "tokenAddress": "0x",
                        "inputPos": 1
                    },
                    "estimatedGas": "210000"
                },
                {
                    "callType": 0,
                    "target": TOKENS_PER_CHAIN['Polygon']['USDC'],
                    "value": "0",
                    "callData": transfer_calldata,
                    "payload": {
                        "tokenAddress": TOKENS_PER_CHAIN['Polygon']['USDC'],
                        "inputPos": 1
                    },
                    "estimatedGas": "40000"
                }
            ])
        }

        response = await self.make_request(url=url, params=params)
        data = response['route']['transactionRequest']['data']
        value = int(response['route']['transactionRequest']['value'])
        target_address = response['route']['transactionRequest']['targetAddress']

        return data, value, target_address

    async def get_from_amount(self):
        url = 'https://api.squidrouter.com/v1/token-price'

        params = {
            "chainId": 42161,
            "tokenAddress": ETH_MASK
        }

        response = await self.make_request(url=url, params=params)
        eth_price = response['price']
        from_amount = int(1 / eth_price * 1.03 * 1e+18)

        return from_amount

    @helper
    @gas_checker
    async def mint(self):
        self.logger_msg(*self.client.acc_info, msg="Minting Squid Scholar NFT")

        polygon_usdc_contract = self.client.get_contract(TOKENS_PER_CHAIN['Polygon']['USDC'])

        polygon_nft_scholar_contract = self.client.get_contract(
            POLYGON_SCHOLAR_NFT_CONTRACT, SQUID_SCHOLAR_NFT_CONTRACT_ABI
        )

        approve_calldata = polygon_usdc_contract.encodeABI(
            fn_name='approve',
            args=[
                POLYGON_SCHOLAR_NFT_CONTRACT,
                2 ** 256 - 1
            ]
        )

        transfer_calldata = polygon_usdc_contract.encodeABI(
            fn_name='transfer',
            args=[
                self.client.address,
                0
            ]
        )

        claim_calldata = polygon_nft_scholar_contract.encodeABI(
            fn_name='claim',
            args=[
                self.client.address,
                1,
                TOKENS_PER_CHAIN['Polygon']['USDC'],
                1000000,
                [
                    [
                        abi.encode(['uint256'], [0])
                    ],
                    2 ** 256 - 1,
                    1000000,
                    TOKENS_PER_CHAIN['Polygon']['USDC'],
                ],
                '0x'
            ]
        )

        from_amount = await self.get_from_amount()
        data, value, target_address = await self.get_data(approve_calldata, transfer_calldata,
                                                          claim_calldata, from_amount)

        transaction = (await self.client.prepare_transaction()) | {
            "to": target_address,
            "data": data,
            "value": value,
        }

        return await self.client.send_transaction(transaction)
