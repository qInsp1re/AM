import random

from modules import Refuel, Logger, Client
from modules.interfaces import Minter
from eth_abi import encode
from utils.tools import helper, sleep
from config.constants import (
    L2PASS_CONTRACTS_PER_CHAINS,
    OMNICHAIN_NETWORKS_DATA, ZERO_ADDRESS
)
from config.abi import L2PASS_ABI


class L2Pass(Refuel, Minter, Logger):
    def __init__(self, client: Client):
        self.client = client
        Logger.__init__(self)

    async def get_nft_id(self, contract):
        balance_nft = await contract.functions.balanceOf(self.client.address).call()
        nft_ids = []
        for i in range(balance_nft):
            nft_ids.append(await contract.functions.tokenOfOwnerByIndex(self.client.address, i).call())
        if nft_ids:
            return nft_ids[-1]
        return False

    async def get_estimate_send_fee(self, contract, adapter_params, dst_chain_id, nft_id):
        estimate_gas_bridge_fee = (await contract.functions.estimateSendFee(
            dst_chain_id,
            self.client.address,
            nft_id,
            False,
            adapter_params
        ).call())[0]

        return estimate_gas_bridge_fee

    @helper
    async def refuel(self, refuel_data: dict, need_check: bool = False):
        dst_chain_name, refuel_amount = random.choice(list(refuel_data.items()))
        dst_chain_id, dst_native_name = OMNICHAIN_NETWORKS_DATA[dst_chain_name]
        dst_amount = await self.client.get_smart_amount(refuel_amount)

        if not need_check:
            refuel_info = f'{dst_amount} {dst_native_name} to {dst_chain_name} from {self.client.network.name}'
            self.logger_msg(*self.client.acc_info, msg=f'Refuel on L2Pass: {refuel_info}')

        l2pass_contracts = L2PASS_CONTRACTS_PER_CHAINS[self.client.network.name]
        refuel_contract = self.client.get_contract(l2pass_contracts['refuel'], L2PASS_ABI['refuel'])

        dst_native_gas_amount = int(dst_amount * 10 ** 18)
        dst_contract_address = L2PASS_CONTRACTS_PER_CHAINS[dst_chain_name]['refuel']

        try:
            estimate_send_fee = (await refuel_contract.functions.estimateGasRefuelFee(
                dst_chain_id,
                dst_native_gas_amount,
                dst_contract_address,
                False
            ).call())[0]

            transaction = await refuel_contract.functions.gasRefuel(
                dst_chain_id,
                ZERO_ADDRESS,
                dst_native_gas_amount,
                self.client.address
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
        mint_price = await onft_contract.functions.mintPrice().call()

        self.logger_msg(
            *self.client.acc_info,
            msg=f"Mint L2Pass NFT on {self.client.network.name}. "
                f"Mint Price: {(mint_price / 10 ** 18):.5f} {self.client.network.token}")

        tx_params = await self.client.prepare_transaction(value=mint_price)

        transaction = await onft_contract.functions.mintWithReferral(
            1,
            '0x000000a679C2FB345dDEfbaE3c42beE92c0Fb7A5'
        ).build_transaction(tx_params)

        result = await self.client.send_transaction(transaction)

        if self.client.network.name == 'Polygon':
            await sleep(self, 300, 400)
        else:
            await sleep(self, 100, 200)

        return result

    @helper
    async def bridge(self, chain_to_name: int, need_check: bool = False):
        onft_contract = self.client.get_contract(
            L2PASS_CONTRACTS_PER_CHAINS[self.client.network.name]['ONFT'], L2PASS_ABI['ONFT']
        )

        dst_chain_id, _, = OMNICHAIN_NETWORKS_DATA[chain_to_name]

        if not need_check:
            nft_id = await self.get_nft_id(onft_contract)

            if not nft_id:
                await self.mint(onft_contract)
                nft_id = await self.get_nft_id(onft_contract)

            self.logger_msg(
                *self.client.acc_info,
                msg=f"Bridge L2Pass NFT from {self.client.network.name} to {chain_to_name}. ID: {nft_id}")
        else:
            nft_id = await onft_contract.functions.nextMintId().call()

        version, gas_limit = 1, 200000

        adapter_params = encode(["uint16", "uint256"],
                                [version, gas_limit])

        adapter_params = self.client.w3.to_hex(adapter_params[30:])

        try:
            send_price = await onft_contract.functions.sendPrice().call()

            estimate_send_fee = await self.get_estimate_send_fee(onft_contract, adapter_params, dst_chain_id, nft_id)
            mint_price = await onft_contract.functions.mintPrice().call()

            value = int(estimate_send_fee + send_price + 0.0005)

            if need_check:
                if await self.client.w3.eth.get_balance(self.client.address) > value + mint_price:
                    return True
                return False

            tx_params = await self.client.prepare_transaction(value=value)

            transaction = await onft_contract.functions.sendFrom(
                self.client.address,
                dst_chain_id,
                self.client.address,
                nft_id,
                self.client.address,
                ZERO_ADDRESS,
                adapter_params
            ).build_transaction(tx_params)

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
