import random

from modules import Refuel, Logger, Client, RequestClient
from modules.interfaces import SoftwareException, Bridge, BridgeExceptionWithoutRetry
from dev_settings import Settings
from utils.tools import gas_checker, helper
from config.constants import (
    BUNGEE_CONTRACTS,
    CHAIN_NAME_FROM_ID, ETH_MASK, TOKENS_PER_CHAIN, CHAIN_IDS
)
from config.abi import BUNGEE_ABI


class Bungee(Refuel, Bridge, Logger, RequestClient):
    def __init__(self, client: Client):
        self.client = client
        Logger.__init__(self)
        Bridge.__init__(self, client)
        RequestClient.__init__(self, client)
        self.network = self.client.network.name

    async def get_limits_data(self):
        url = 'https://refuel.socket.tech/chains'

        async with self.client.session.get(url=url) as response:
            if response.status == 200:
                data = await response.json()
                network_name = self.network if self.network != 'BNB Chain' else 'BSC'
                return [chain for chain in data['result'] if chain['name'] == network_name][0]
            raise SoftwareException(f'Bad request to Bungee API: {response.status}')

    @helper
    async def refuel(self, refuel_data: dict, need_check: bool = False):
        dst_chain_name, refuel_amount = random.choice(list(refuel_data.items()))
        dst_amount = await self.client.get_smart_amount(refuel_amount)

        refuel_contract = self.client.get_contract(BUNGEE_CONTRACTS[self.network]['gas_refuel'], BUNGEE_ABI['refuel'])

        refuel_info = f'{dst_amount} {self.client.network.token} from {self.client.network.name} to {dst_chain_name}'
        if not need_check:
            self.logger_msg(*self.client.acc_info, msg=f'Refuel on Bungee: {refuel_info}')

        refuel_limits_data = await self.get_limits_data()

        if refuel_limits_data['isSendingEnabled']:
            dst_chain_id = CHAIN_IDS[f'{dst_chain_name}']
            limits_dst_chain_data = {}

            for chain_limits in refuel_limits_data['limits']:
                if chain_limits['chainId'] == dst_chain_id:
                    limits_dst_chain_data = chain_limits
                    break

            if 'isEnabled' in limits_dst_chain_data and limits_dst_chain_data['isEnabled']:
                min_amount_in_wei = int(limits_dst_chain_data['minAmount'])
                max_amount_in_wei = int(limits_dst_chain_data['maxAmount'])

                min_amount = round(self.client.w3.from_wei(min_amount_in_wei, 'ether') * 100000, 6) / 100000
                max_amount = round(self.client.w3.from_wei(max_amount_in_wei, 'ether') * 100000, 6) / 100000

                amount_in_wei = self.client.to_wei(dst_amount)

                if min_amount_in_wei <= amount_in_wei <= max_amount_in_wei:

                    if await self.client.w3.eth.get_balance(self.client.address) >= amount_in_wei:

                        tx_params = await self.client.prepare_transaction(value=amount_in_wei)

                        transaction = await refuel_contract.functions.depositNativeToken(
                            dst_chain_id,
                            self.client.address
                        ).build_transaction(tx_params)

                        if need_check:
                            return True

                        return await self.client.send_transaction(transaction)

                    else:
                        raise SoftwareException("Insufficient balance!")
                else:
                    raise SoftwareException(f'Limit range for refuel: {min_amount} - {max_amount} ETH!')
            else:
                raise SoftwareException('Destination chain refuel is not active!')
        else:
            raise SoftwareException('Source chain refuel is not active!')

    async def get_quote(self, to_chain_id, from_token_address, to_token_address, amount, need_check):
        url = 'https://api.socket.tech/v2/quote'

        wanted_route = {
            1:  'across',
            2:  'cctp',
            3:  'celer',
            4:  'connext',
            5:  'stargateV2Bus',
            6:  'refuel-bridge',
            7:  'synapse',
            8:  'symbiosis',
            9:  'hop',
            10:  'hyphen',

        }.get(Settings.BUNGEE_ROUTE_TYPE, False)

        params = {
                    "fromChainId": self.client.chain_id,
                    "toChainId": to_chain_id,
                    "fromTokenAddress": from_token_address,
                    "toTokenAddress": to_token_address,
                    "fromAmount": amount,
                    "userAddress": self.client.address,
                    "singleTxOnly": "false",
                    "bridgeWithGas": "false",
                    "sort": "output",
                    "defaultSwapSlippage": 0.5,
                    "bridgeWithInsurance": "true",
                    "isContractCall": "false",
                    "showAutoRoutes": "false",
                }
        response = await self.make_request(url=url, params=params, headers=self.headers)

        final_route = None
        if response['success']:
            all_routes = response['result']['routes']
            if wanted_route:
                for route in all_routes:
                    if route['usedBridgeNames'][0] == wanted_route and int(route['totalUserTx']) == 1:
                        final_route = route
                        break

            if final_route and need_check:
                return final_route
            elif not final_route and need_check:
                if all_routes:
                    return all_routes[0]
                from_chain_name = CHAIN_NAME_FROM_ID[self.client.chain_id]
                to_chain_name = CHAIN_NAME_FROM_ID[to_chain_id]
                raise SoftwareException(
                    f'Bungee | Can`t find a route for bridge from {from_chain_name} to {to_chain_name}!'
                )
            elif final_route:
                if not need_check:
                    self.logger_msg(
                        *self.client.acc_info,
                        msg=f'Successfully found {wanted_route.capitalize()} route. Initialize bridge...',
                        type_msg='success'
                    )
            else:
                self.logger_msg(
                    *self.client.acc_info,
                    msg=f'Will take {all_routes[0]["usedBridgeNames"][0].capitalize()} route. Initialize bridge...',
                )
                final_route = all_routes[0]

            if final_route['extraData']:
                rewards = final_route['extraData'].get('rewards')
                if rewards:
                    for reward in rewards:
                        amount_in_wei = int(reward['amount'])
                        decimals = int(reward['asset']['decimals'])
                        amount = round(amount_in_wei / 10 ** decimals, 3)
                        symbol = reward['asset']['symbol']
                        amount_in_usd = round(float(reward['amountInUsd']), 2)
                        chain_name = f"{CHAIN_NAME_FROM_ID[int(reward['chainId'])]} chain"

                        self.logger_msg(
                            *self.client.acc_info,
                            msg=f'This TX will be rewarded with {amount} {symbol} ({amount_in_usd}$) in {chain_name}',
                            type_msg='success'
                        )
            return final_route

        raise BridgeExceptionWithoutRetry(f'Bad request to Bungee API: {await response.text()}')

    async def build_tx(self, route:dict):
        url = 'https://api.socket.tech/v2/build-tx'

        payload = {
            'route': route
        }

        response = await self.make_request(method="POST", url=url, json=payload, headers=self.headers)

        if response['success']:
            tx_data = response['result']['txData']
            value = int(response['result']['value'], 16)
            contract_address = self.client.w3.to_checksum_address(response['result']['txTarget'])

            return tx_data, value, contract_address
        raise BridgeExceptionWithoutRetry(f'Bad request to Bungee API: {await response.text()}')

    @helper
    async def bridge(self, bridge_data: tuple, need_check: bool = False):
        (from_chain_id, to_chain_id, amount, from_token_name,
         to_token_name, from_token_address, to_token_address, chain_to_name) = bridge_data

        if not need_check:
            bridge_info = f'{self.client.network.name} -> {to_token_name} {chain_to_name}'
            self.logger_msg(*self.client.acc_info, msg=f'Bridge on Bungee: {amount} {from_token_name} {bridge_info}')

        decimals = await self.client.get_decimals(token_address=from_token_address)
        amount_in_wei = self.client.to_wei(amount, decimals=decimals)

        if from_token_name == self.client.token:
            from_token_address = ETH_MASK
        else:
            from_token_address = TOKENS_PER_CHAIN[self.client.network.name][from_token_name]

        if to_token_name in ['BNB', 'MATIC', 'AVAX', 'ETH']:
            to_token_address = ETH_MASK
        else:
            to_token_address = TOKENS_PER_CHAIN[chain_to_name][to_token_name]

        route_data = await self.get_quote(to_chain_id, from_token_address, to_token_address, amount_in_wei, need_check)

        if need_check:
            token_price = await self.get_token_price(from_token_name)
            return float(route_data['totalGasFeesInUsd']) / token_price

        tx_data, value, to_address = await self.build_tx(route_data)

        if from_token_name != self.client.token:
            await self.client.check_for_approved(from_token_address, to_address, amount_in_wei)

        transaction = await self.client.prepare_transaction(value=value) | {
            'to': to_address,
            'data': tx_data
        }

        old_balance_data_on_dst = await self.client.wait_for_receiving(
            chain_to_name=chain_to_name, token_name=to_token_name, token_address=to_token_address,
            check_balance_on_dst=True
        )

        await self.client.send_transaction(transaction)

        self.logger_msg(
            *self.client.acc_info, msg=f"Bridge complete. Note: wait a little for receiving funds",
            type_msg='success'
        )

        if Settings.WAIT_FOR_RECEIPT_BRIDGE:
            return await self.client.wait_for_receiving(
                chain_to_name=chain_to_name, token_name=to_token_name, token_address=to_token_address,
                old_balance_data=old_balance_data_on_dst,
            )

        return True

    @helper
    @gas_checker
    async def claim_rewards(self):
        url = 'https://microservices.socket.tech/loki/rewards/get-claim-data'

        params = {
            'address': self.client.address
        }

        claim_contract = self.client.get_contract(BUNGEE_CONTRACTS[self.network]['claim'], BUNGEE_ABI['claim'])

        response = await self.make_request(url=url, params=params)

        if response['success']:
            rewards = response['result']
            if rewards:
                for reward in rewards:
                    claimable_amount_in_wei = int(reward['claimableAmount'])
                    claimed_amount_in_wei = int(reward['claimedAmount'])
                    pending_amount_in_wei = int(reward['pendingAmount'])
                    merkle_proof = reward['proof']
                    symbol = reward['asset']['symbol']
                    decimals = int(reward['asset']['decimals'])
                    chain_id = int(reward['asset']['chainId'])

                    if claimable_amount_in_wei != 0:

                        clmbl_amount = claimable_amount_in_wei / 10 ** decimals
                        clmd_amount = claimed_amount_in_wei / 10 ** decimals
                        pend_amount = pending_amount_in_wei / 10 ** decimals

                        self.logger_msg(
                            *self.client.acc_info,
                            msg=f'Claimable: {clmbl_amount:.3f} ${symbol}. Claimed: {clmd_amount:.3f} ${symbol}.'
                                f' Pending: {pend_amount:.3f} ${symbol}', type_msg='success')

                        self.logger_msg(
                            *self.client.acc_info,
                            msg=f'Start claiming {clmbl_amount} ${symbol} on {CHAIN_NAME_FROM_ID[chain_id]} chain'
                        )

                        transaction = await claim_contract.functions.claim(
                            self.client.address,
                            claimable_amount_in_wei,
                            merkle_proof
                        ).build_transaction(await self.client.prepare_transaction())

                        await self.client.send_transaction(transaction)
            else:
                self.logger_msg(*self.client.acc_info, msg=f'No tokens are available for claiming')

            return True

        raise BridgeExceptionWithoutRetry(f'Bad request to Bungee API: {await response.text()}')
