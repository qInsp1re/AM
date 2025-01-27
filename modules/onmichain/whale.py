import random

from eth_abi import abi
from utils.tools import sleep, helper
from modules import Refuel, Logger, RequestClient
from modules.interfaces import SoftwareException
from config.constants import (
    WHALE_CONTRACTS_PER_CHAINS,
    OMNICHAIN_NETWORKS_DATA,
    ZERO_ADDRESS
)
from config.abi import WHALE_ABI


class Whale(Refuel, Logger, RequestClient):
    def __init__(self, client):
        self.client = client
        Logger.__init__(self)
        RequestClient.__init__(self, client)

    async def get_estimate_send_fee(self, contract, adapter_params, dst_chain_id, nft_id):
        estimate_gas_bridge_fee = (await contract.functions.estimateSendFee(
            dst_chain_id,
            self.client.address,
            nft_id,
            False,
            adapter_params
        ).call())[0]

        return estimate_gas_bridge_fee

    async def get_nft_id(self):
        url = 'https://whale-app.com/api/user/get-nft-ids'

        disable_networks = [
            ''
        ]

        payload = {
            'address': self.client.address,
            'chainId': self.client.network.chain_id if self.client.network.name not in disable_networks else 0
        }

        response = await self.make_request(method='POST', url=url, json=payload)

        if response:
            return int(random.choice(list(response)))
        return False

    @helper
    async def refuel(self, refuel_data: dict, need_check: bool = False):

        dst_chain_name, refuel_amount = random.choice(list(refuel_data.items()))
        dst_chain_id, dst_native_name = OMNICHAIN_NETWORKS_DATA[dst_chain_name]
        dst_amount = await self.client.get_smart_amount(refuel_amount)

        if not need_check:
            refuel_info = f'{dst_amount} {dst_native_name} to {dst_chain_name} from {self.client.network.name}'
            self.logger_msg(*self.client.acc_info, msg=f'Refuel on Whale: {refuel_info}')

        whale_contracts = WHALE_CONTRACTS_PER_CHAINS[self.client.network.name]
        refuel_contract = self.client.get_contract(whale_contracts['refuel'], WHALE_ABI['refuel'])

        dst_native_gas_amount = int(dst_amount * 10 ** 18)
        dst_contract_address = WHALE_CONTRACTS_PER_CHAINS[dst_chain_name]['refuel']

        gas_limit = await refuel_contract.functions.minDstGasLookup(dst_chain_id, 0).call()

        if gas_limit == 0 and not need_check:
            raise SoftwareException('This refuel path is not active!')

        adapter_params = abi.encode(["uint16", "uint64", "uint256"],
                                    [2, gas_limit, dst_native_gas_amount])

        adapter_params = self.client.w3.to_hex(adapter_params[30:]) + self.client.address[2:].lower()

        try:
            estimate_send_fee = (await refuel_contract.functions.estimateSendFee(
                dst_chain_id,
                dst_contract_address,
                adapter_params
            ).call())[0]

            transaction = await refuel_contract.functions.bridgeGas(
                dst_chain_id,
                self.client.address,
                adapter_params
            ).build_transaction(await self.client.prepare_transaction(value=estimate_send_fee))

            if need_check:
                return True

            tx_result = await self.client.send_transaction(transaction, need_hash=True)

            result = True
            if isinstance(tx_result, bool):
                result = tx_result
            else:
                if self.client.network.name != 'Polygon':
                    result = await self.client.wait_for_l0_received(tx_result)

            return result

        except Exception as error:
            if not need_check:
                await self.client.handling_rpc_errors(error)

    async def mint(self, onft_contract):
        mint_price = await onft_contract.functions.fee().call()

        self.logger_msg(
            *self.client.acc_info,
            msg=f"Mint Whale NFT on {self.client.network.name}. "
                f"Gas Price: {(mint_price / 10 ** 18):.5f} {self.client.network.token}")

        tx_params = await self.client.prepare_transaction(value=mint_price)

        transaction = await onft_contract.functions.mint().build_transaction(tx_params)

        result = await self.client.send_transaction(transaction)

        if self.client.network.name == 'Polygon':
            await sleep(self, 300, 400)
        else:
            await sleep(self, 100, 200)

        return result

    @helper
    async def bridge(self, chain_to_name: str, need_check: bool = False):
        onft_contract = self.client.get_contract(
            WHALE_CONTRACTS_PER_CHAINS[self.client.network.name]['ONFT'], WHALE_ABI['ONFT']
        )
        dst_chain_id, _ = OMNICHAIN_NETWORKS_DATA[chain_to_name]

        if not need_check:
            nft_id = await self.get_nft_id()
            if not nft_id:
                await self.mint(onft_contract)
                nft_id = await self.get_nft_id()

            self.logger_msg(
                *self.client.acc_info,
                msg=f"Bridge Whale NFT from {self.client.network.name} to {chain_to_name}. ID: {nft_id}")
        else:
            nft_id = await onft_contract.functions.nextMintId().call()

        try:
            version, gas_limit = 1, 200000

            adapter_params = abi.encode(["uint16", "uint256"],
                                        [version, gas_limit])

            adapter_params = self.client.w3.to_hex(adapter_params[30:])

            estimate_send_fee = await self.get_estimate_send_fee(onft_contract, adapter_params, dst_chain_id, nft_id)

            if need_check:
                mint_price = await onft_contract.functions.fee().call()
                value = int(estimate_send_fee + 0.0005)
                if await self.client.w3.eth.get_balance(self.client.address) > value + mint_price:
                    return True
                return False

            tx_params = await self.client.prepare_transaction(value=estimate_send_fee)

            transaction = await onft_contract.functions.sendFrom(
                self.client.address,
                dst_chain_id,
                self.client.address,
                nft_id,
                self.client.address,
                ZERO_ADDRESS,
                adapter_params
            ).build_transaction(tx_params)

            tx_result = await self.client.send_transaction(transaction, need_hash=True)

            result = True
            if isinstance(tx_result, bool):
                result = tx_result
            else:
                if self.client.network.name != 'Polygon':
                    result = await self.client.wait_for_l0_received(tx_result)

            return result

        except Exception as error:
            if not need_check:
                await self.client.handling_rpc_errors(error)