import random

from general_settings import REF_LINK_DEBRDIGE
from modules import Logger, Client, SolanaClient
from modules.interfaces import Bridge, SoftwareExceptionWithoutRetry
from utils.tools import gas_checker, helper
from config.constants import (
    CHAIN_NAME_FROM_ID, ZERO_ADDRESS, TOKENS_PER_CHAIN, CHAIN_IDS
)


class DeBridge(Bridge, Logger):
    def __init__(self, client: Client | SolanaClient):
        self.client = client
        Logger.__init__(self)
        Bridge.__init__(self, client)
        self.network = self.client.network.name

    async def send_signature(self):
        url = "https://stats-api.dln.trade/api/TermsAndConditions/signConditions"

        terms = ("I am not the person or entities who reside in, are citizens of, are incorporated in, or have a"
                 " registered office in the United States of America or any Prohibited Localities, as defined in "
                 "the Terms of Use.\nI will not in the future access this site or use DLN dApp while located within "
                 "the United States any Prohibited Localities, as defined in the Terms of Use.\nI am not using, and"
                 " will not in the future use, a VPN to mask my physical location from a restricted territory.\nI am"
                 " lawfully permitted to access this site and use DLN dApp under the laws of the jurisdiction on which"
                 " I reside and am located.\nI understand the risks associated with entering into using DLN Network"
                 " protocols.")

        signature = await self.client.sign_message(message=terms)

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "content-type": "application/json-patch+json",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Chromium\";v=\"123\", \"Microsoft Edge\";v=\"123\", \"Not-A.Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "referrer": "https://app.debridge.finance/",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "method": "POST",
            "mode": "cors",
            "credentials": "omit"
        }

        payload = {
            'signatoryAddress': f"{self.client.address}",
            'signature': signature
        }

        return await self.make_request(method="POST", url=url, headers=headers, json=payload, without_response=True)

    async def get_signed(self):
        url = f"https://stats-api.dln.trade/api/TermsAndConditions/{self.client.address}/hasSigned"

        headers = {
            "accept": "text/plain",
            "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Chromium\";v=\"123\", \"Microsoft Edge\";v=\"123\", \"Not-A.Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "referrer": "https://app.debridge.finance/",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "body": 'null',
            "method": "GET",
            "mode": "cors",
            "credentials": "omit"
        }

        response = await self.make_request(url=url, headers=headers)

        if not response:
            self.logger_msg(
                *self.client.acc_info, msg=f'New wallet on deBridge.finance, send signature to server...'
            )
            return await self.send_signature()
        return True

    async def get_quote(
            self, to_chain_id, from_token_address, to_token_address, amount_in_wei, src_chain_name, dst_chain_name,
            from_token_name, to_token_name
    ):
        url = 'https://deswap.debridge.finance/v1.0/dln/order/quote'

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Chromium\";v=\"123\", \"Microsoft Edge\";v=\"123\", \"Not-A.Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "referrer": "https://app.debridge.finance/",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "method": "GET",
            "mode": "cors",
            "credentials": "omit"
        }

        params = {
            'srcChainId': self.client.chain_id,
            'srcChainTokenIn': from_token_address,
            'srcChainTokenInAmount': amount_in_wei,
            'dstChainTokenOutAmount': 'auto',
            'dstChainId': to_chain_id,
            'dstChainTokenOut': to_token_address,
            'prependOperatingExpenses': 'true',
            'additionalTakerRewardBps': 0,
        }

        try:
            response = await self.make_request(url=url, params=params, headers=headers)
        except Exception as error:
            if 'Response status: 500' in str(error):
                route = f'{from_token_name} {src_chain_name} -> {to_token_name} {dst_chain_name}'
                raise SoftwareExceptionWithoutRetry(f'deBridge do not support: {route}')
            else:
                raise error

        fix_fee = int(response['fixFee'])
        prepended_fee = int(response['prependedOperatingExpenseCost'])

        if from_token_name != self.client.token:
            allowance_address = response["tx"]["allowanceTarget"]
            allowance_value = int(response["tx"]["allowanceValue"])
        else:
            allowance_address = 0
            allowance_value = 0

        return fix_fee, prepended_fee, allowance_address, allowance_value

    async def create_tx(self, to_chain_id, from_token_address, to_token_address, amount_in_wei):
        url = 'https://deswap.debridge.finance/v1.0/dln/order/create-tx'

        headers = {
                "accept": "application/json, text/plain, */*",
                "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                "priority": "u=1, i",
                "sec-ch-ua": "\"Chromium\";v=\"123\", \"Microsoft Edge\";v=\"123\", \"Not-A.Brand\";v=\"99\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "referrer": "https://app.debridge.finance/",
                "referrerPolicy": "strict-origin-when-cross-origin",
                "method": "GET",
                "mode": "cors",
                "credentials": "omit"
        }

        if to_chain_id != 7565164:
            from functions import Client
            evm_client = Client(self.client.module_input_data)

            dst_client_address = f"{evm_client.address}"
            await evm_client.session.close()
        else:
            from functions import SolanaClient
            solana_client = SolanaClient(self.client.module_input_data)

            dst_client_address = f"{solana_client.address}"
            await solana_client.session.close()

        params = {
            'srcChainId': self.client.chain_id,
            'srcChainTokenIn': from_token_address,
            'srcChainTokenInAmount': amount_in_wei,
            'dstChainId': to_chain_id,
            'dstChainTokenOut': to_token_address,
            'dstChainTokenOutRecipient': dst_client_address,
            'senderAddress': f"{self.client.address}",
            'srcChainOrderAuthorityAddress': f"{self.client.address}",
            'referralCode': random.choice(REF_LINK_DEBRDIGE),
            'srcChainRefundAddress': f"{self.client.address}",
            'dstChainOrderAuthorityAddress': dst_client_address,
            'enableEstimate': 'false',
            'prependOperatingExpenses': 'true',
            'additionalTakerRewardBps': 0,
            'deBridgeApp': 'DESWAP',
            'ptp': 'false',
        }

        response = await self.make_request(url=url, params=params, headers=headers)

        points_amount = response['userPoints']

        self.logger_msg(
            *self.client.acc_info, msg=f'Successfully found a route, will rewarded with {points_amount} POINTS',
            type_msg='success'
        )

        tx_data = response['tx']['data']

        if self.client.network.name == 'Solana':
            return tx_data

        contract_address = response['tx']['to']
        value = int(response['tx']['value'])
        return tx_data, contract_address, value

    @helper
    @gas_checker
    async def bridge(self, bridge_data: tuple, swap_mode:bool = False):

        src_chain_name, dst_chain_name, from_token_name, to_token_name, amount, amount_in_wei = bridge_data

        dst_chain_id_onchain = CHAIN_IDS[dst_chain_name]
        decimals = await self.client.get_decimals(from_token_name)
        amount_in_wei = self.client.to_wei(amount, decimals=decimals)

        if from_token_name == self.client.token and src_chain_name != 'Solana':
            from_token_address = ZERO_ADDRESS
        else:
            from_token_address = TOKENS_PER_CHAIN[src_chain_name][from_token_name]

        if to_token_name in ['BNB', 'MATIC', 'AVAX', 'ETH']:
            to_token_address = ZERO_ADDRESS
        else:
            to_token_address = TOKENS_PER_CHAIN[dst_chain_name][to_token_name]

        fix_fee, prepended_fee, allowance_address, allowance_value = await self.get_quote(
            dst_chain_id_onchain, from_token_address, to_token_address, amount_in_wei, src_chain_name, dst_chain_name,
            from_token_name, to_token_name
        )

        scr_chain_cf = {
            'Base': 6,
            'Linea': 9,
            'Scroll': 3,
            'Optimism': 7,
            'Arbitrum': 7,
            'zkSync': 7,
            'BNB Chain': 5,
            'Polygon': 5,
            'Avalanche': 6,
        }.get(self.client.network.name, 3)

        if swap_mode:
            scr_chain_cf *= 5

        if from_token_name == self.client.token:
            fee_in_wei = int(fix_fee + prepended_fee * scr_chain_cf)
            amount_in_wei -= fee_in_wei
        else:
            fee_in_wei = int(prepended_fee)
            amount_in_wei -= int(fee_in_wei * 1.1)

        fee_info = fee_in_wei / 10 ** decimals
        amount = float(amount_in_wei / 10 ** decimals)

        if amount < 0:
            raise SoftwareExceptionWithoutRetry('Account balance < bridge fee')

        bridge_info = f'{self.client.network.name} -> {to_token_name} {CHAIN_NAME_FROM_ID[dst_chain_id_onchain]}'
        self.logger_msg(
            *self.client.acc_info,
            msg=f'Bridge on deBridge: {amount:.6f} {from_token_name} {bridge_info}. Fee: {fee_info:.4f} {from_token_name}'
        )

        await self.get_signed()

        if self.client.network.name != 'Solana':

            tx_data, to_address, value = await self.create_tx(
                dst_chain_id_onchain, from_token_address, to_token_address, amount_in_wei
            )

            if from_token_name != self.client.token:
                await self.client.check_for_approved(from_token_address, allowance_address, allowance_value)

            transaction = await self.client.prepare_transaction(value=value) | {
                'to': to_address,
                'data': tx_data
            }
        else:
            tx_data = await self.create_tx(
                dst_chain_id_onchain, from_token_address, to_token_address, amount_in_wei
            )

            transaction = await self.client.create_v0_message(bytes.fromhex(tx_data))

        old_balance_data_on_dst = await self.client.wait_for_receiving(
            chain_to_name=dst_chain_name, token_name=to_token_name, token_address=to_token_address,
            check_balance_on_dst=True
        )

        if self.client.network.name != 'Solana':
            await self.client.send_transaction(transaction)
        else:
            await self.client.send_transaction(message=transaction)

        self.logger_msg(*self.client.acc_info,
                        msg=f"Bridge complete. Note: wait a little for receiving funds", type_msg='success')

        return await self.client.wait_for_receiving(
                chain_to_name=dst_chain_name, token_name=to_token_name, token_address=to_token_address,
                old_balance_data=old_balance_data_on_dst,
        )
