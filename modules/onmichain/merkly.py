import random

from eth_typing import HexStr
from modules import Refuel, Logger, Client
from eth_abi import abi
from decimal import Decimal

from modules.interfaces import SoftwareException, Minter, SoftwareExceptionWithoutRetry
from dev_settings import Settings
from utils.tools import helper, sleep
from config.constants import (
    MERKLY_CONTRACTS_PER_CHAINS,
    OMNICHAIN_NETWORKS_DATA, MERKLY_NFT_WORMHOLE_INFO,
    MERKLY_TOKENS_WORMHOLE_INFO, ZERO_ADDRESS, CHAIN_IDS, MERKLY_HYPERLANE_INFO,
    TOKENS_PER_CHAIN
)
from config.abi import MERKLY_ABI


class Merkly(Refuel, Minter, Logger):
    def __init__(self, client: Client):
        self.client = client
        Logger.__init__(self)

    async def get_nft_id(self, tx_hash: HexStr):
        tx_receipt = await self.client.w3.eth.get_transaction_receipt(tx_hash)

        if self.client.network.name == 'zkSync':
            nft_id = int((tx_receipt.logs[2].topics[3]).hex(), 16)
            if not nft_id:
                nft_id = int((tx_receipt.logs[3].topics[3]).hex(), 16)
        elif self.client.network.name == 'Polygon':
            nft_id = int((tx_receipt.logs[1].topics[3]).hex(), 16)
        else:
            nft_id = int((tx_receipt.logs[0].topics[3]).hex(), 16)
        return nft_id

    async def get_estimate_send_fee(self, contract, adapter_params, dst_chain_id, nft_id):
        estimate_gas_bridge_fee = (await contract.functions.estimateSendFee(
            dst_chain_id,
            self.client.address,
            nft_id,
            False,
            adapter_params
        ).call())[0]

        return estimate_gas_bridge_fee

    async def mint(self, onft_contract):
        mint_price = await onft_contract.functions.fee().call()
        nft_name = await onft_contract.functions.name().call()

        self.logger_msg(
            *self.client.acc_info,
            msg=f"Mint {nft_name} NFT on {self.client.network.name}. "
                f"Price: {(mint_price / 10 ** 18):.5f} {self.client.network.token}")

        tx_params = await self.client.prepare_transaction(value=mint_price)
        transaction = await onft_contract.functions.mint().build_transaction(tx_params)

        return await self.client.send_transaction(transaction, need_hash=True)

    @helper
    async def refuel(self, refuel_data: dict, need_check: bool = False):
        dst_chain_name, refuel_amount = random.choice(list(refuel_data.items()))
        dst_chain_id, dst_native_name = OMNICHAIN_NETWORKS_DATA[dst_chain_name]
        dst_amount = await self.client.get_smart_amount(refuel_amount)

        if not need_check:
            refuel_info = f'{dst_amount} {dst_native_name} to {dst_chain_name} from {self.client.network.name}'
            self.logger_msg(*self.client.acc_info, msg=f'Refuel on Merkly: {refuel_info}')

        merkly_contracts = MERKLY_CONTRACTS_PER_CHAINS[self.client.network.name]
        refuel_contract = self.client.get_contract(merkly_contracts['refuel'], MERKLY_ABI['refuel'])

        dst_native_gas_amount = int(dst_amount * 10 ** 18)
        dst_contract_address = MERKLY_CONTRACTS_PER_CHAINS[dst_chain_name]['refuel']

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

    @helper
    async def bridge(self, chain_to_name: int, need_check: bool = False):
        onft_contract = self.client.get_contract(
            MERKLY_CONTRACTS_PER_CHAINS[self.client.network.name]['ONFT'], MERKLY_ABI['ONFT']
        )
        dst_chain_id, _ = OMNICHAIN_NETWORKS_DATA[chain_to_name]

        if not need_check:
            tx_hash = await self.mint(onft_contract)
            nft_id = await self.get_nft_id(tx_hash)
            await sleep(self, 5, 10)

            self.logger_msg(
                *self.client.acc_info,
                msg=f"Bridge Merkly NFT from {self.client.network.name} to {chain_to_name}. ID: {nft_id}")
        else:
            nft_id = await onft_contract.functions.nextMintId().call()

        version, gas_limit = 1, 200000

        adapter_params = abi.encode(["uint16", "uint256"],
                                    [version, gas_limit])

        adapter_params = self.client.w3.to_hex(adapter_params[30:])

        try:
            estimate_send_fee = await self.get_estimate_send_fee(onft_contract, adapter_params, dst_chain_id, nft_id)

            if need_check:
                mint_price = await onft_contract.functions.fee().call()

                value = int(estimate_send_fee + 0.0004)
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

    @helper
    async def wnft_bridge(self, chain_to_name: int, need_check: bool = False):

        onft_contract = self.client.get_contract(
            MERKLY_CONTRACTS_PER_CHAINS[self.client.network.name]['WNFT'], MERKLY_ABI['WNFT']
        )

        _, mint_price, _ = MERKLY_NFT_WORMHOLE_INFO[self.client.network.name]
        wnft_contract, _, wormhole_id = MERKLY_NFT_WORMHOLE_INFO[chain_to_name]

        estimate_fee = (await onft_contract.functions.quoteBridge(
            wormhole_id,
            0,
            200000
        ).call())[0]

        mint_price_in_wei = int(Decimal(f"{mint_price}") * 10 ** 18)

        if not need_check:
            self.logger_msg(
                *self.client.acc_info,
                msg=f"Mint NFT on Merkly Wormhole. Network: {self.client.network.name}."
                    f" Price for mint: {mint_price} {self.client.network.token}")

        try:
            transaction = await onft_contract.functions.mint(
                1
            ).build_transaction(await self.client.prepare_transaction(value=mint_price_in_wei))

            tx_hash = await self.client.send_transaction(transaction, need_hash=True)

            nft_id = await self.get_nft_id(tx_hash)

            await sleep(self, 5, 8)

            self.logger_msg(
                *self.client.acc_info,
                msg=f"Bridge NFT on Merkly Wormhole from {self.client.network.name} -> {chain_to_name}."
                    f" Price for bridge: "
                    f"{(estimate_fee / 10 ** 18):.6f} {self.client.network.token}")

            transaction = await onft_contract.functions.transferNFT(
                wormhole_id,
                wnft_contract,
                nft_id,
                0,
                200000,
                wormhole_id,
                self.client.address
            ).build_transaction(await self.client.prepare_transaction(value=estimate_fee))

            if need_check:
                return True

            return await self.client.send_transaction(transaction)

        except Exception as error:
            if not need_check:
                await self.client.handling_rpc_errors(error)

    @helper
    async def wt_bridge(self, bridge_data: int, need_check: bool = False):
        tokens_amount_mint, tokens_amount_bridge, chain_to_name = bridge_data

        oft_contract = self.client.get_contract(
            MERKLY_CONTRACTS_PER_CHAINS[self.client.network.name]['WOFT'], MERKLY_ABI['WOFT']
        )

        _, mint_price, _ = MERKLY_TOKENS_WORMHOLE_INFO[self.client.network.name]
        woft_contract, _, wormhole_id = MERKLY_TOKENS_WORMHOLE_INFO[chain_to_name]

        estimate_fee = (await oft_contract.functions.quoteBridge(
            wormhole_id,
            0,
            200000
        ).call())[0]

        token_balance = round((await oft_contract.functions.balanceOf(self.client.address).call()) / 10 ** 18)

        if (token_balance == 0 and need_check) or (token_balance < tokens_amount_bridge and not need_check):

            mint_price_in_wei = int(mint_price * tokens_amount_mint * 10 ** 18)

            self.logger_msg(
                *self.client.acc_info,
                msg=f"Mint {tokens_amount_mint} WMEKL on Merkly Wormhole. Network: {self.client.network.name}."
                    f" Price for mint: {mint_price * tokens_amount_mint:.6f} {self.client.network.token}")

            transaction = await oft_contract.functions.mint(
                self.client.address,
                tokens_amount_mint
            ).build_transaction(await self.client.prepare_transaction(value=mint_price_in_wei))

            await self.client.send_transaction(transaction)

            await sleep(self, 5, 8)
        else:
            if not need_check:
                self.logger_msg(
                    *self.client.acc_info,
                    msg=f"Have enough WMEKL balance: {token_balance}. Network: {self.client.network.name}",
                    type_msg='success')

        if not need_check:
            self.logger_msg(
                *self.client.acc_info,
                msg=f"Bridge tokens on Merkly Wormhole from {self.client.network.name} -> {chain_to_name}."
                    f" Price for bridge: {(estimate_fee / 10 ** 18):.6f} {self.client.network.token}")
        try:
            transaction = await oft_contract.functions.bridge(
                wormhole_id,
                woft_contract,
                int(tokens_amount_bridge * 10 ** 18),
                0,
                200000,
                wormhole_id,
                self.client.address
            ).build_transaction(await self.client.prepare_transaction(value=estimate_fee))

            if need_check:
                return True

            return await self.client.send_transaction(transaction)

        except Exception as error:
            if not need_check:
                await self.client.handling_rpc_errors(error)

    @helper
    async def hnft_bridge(self, chain_to_name: int, need_check: bool = False):
        onft_contract = self.client.get_contract(
            MERKLY_CONTRACTS_PER_CHAINS[self.client.network.name]['HNFT'], MERKLY_ABI['HNFT']
        )

        dst_chain_id = CHAIN_IDS[chain_to_name]

        estimate_fee = (await onft_contract.functions.quoteBridge(
            dst_chain_id
        ).call())

        mint_price = await onft_contract.functions.fee().call()

        value = int(estimate_fee + mint_price + 0.0005)

        if (await self.client.w3.eth.get_balance(self.client.address) > value) and need_check:
            return True
        elif need_check:
            return False

        self.logger_msg(
            *self.client.acc_info,
            msg=f"Mint NFT on Merkly Hyperlane. Network: {self.client.network.name}."
                f" Price for mint: {mint_price / 10 ** 18:5f} {self.client.network.token}")

        try:
            transaction = await onft_contract.functions.mint(
                1
            ).build_transaction(await self.client.prepare_transaction(value=mint_price))

            tx_hash = await self.client.send_transaction(transaction, need_hash=True)

            nft_id = await self.get_nft_id(tx_hash)

            await sleep(self, 5, 8)

            self.logger_msg(
                *self.client.acc_info,
                msg=f"Bridge NFT on Merkly Hyperlane from {self.client.network.name} -> {chain_to_name}."
                    f" Price for bridge: "
                    f"{(estimate_fee / 10 ** 18):.6f} {self.client.network.token}")

            transaction = await onft_contract.functions.bridgeNFT(
                dst_chain_id,
                nft_id
            ).build_transaction(await self.client.prepare_transaction(value=estimate_fee))

            return await self.client.send_transaction(transaction)
        except Exception as error:
            await self.client.handling_rpc_errors(error)

    @helper
    async def ht_bridge(self, bridge_data: tuple, need_check: bool = False):
        tokens_amount_mint, tokens_amount_bridge, chain_to_name = bridge_data

        oft_contract = self.client.get_contract(
            MERKLY_CONTRACTS_PER_CHAINS[self.client.network.name]['HOFT'], MERKLY_ABI['HOFT']
        )

        dst_chain_name = chain_to_name
        dst_chain_id = CHAIN_IDS[dst_chain_name]

        estimate_fee = await oft_contract.functions.quoteBridge(
            dst_chain_id,
        ).call()

        mint_price = (await oft_contract.functions.fee().call()) * tokens_amount_mint

        value = int(estimate_fee + mint_price + 0.0002)
        if (await self.client.w3.eth.get_balance(self.client.address) > value) and need_check:
            return True
        elif need_check:
            return False

        token_balance = round((await oft_contract.functions.balanceOf(self.client.address).call()) / 10 ** 18)

        if (token_balance == 0 and need_check) or (token_balance < tokens_amount_bridge and not need_check):

            self.logger_msg(
                *self.client.acc_info,
                msg=f"Mint {tokens_amount_mint} HMEKL on Merkly Hyperlane. Network: {self.client.network.name}."
                    f" Price for mint: {mint_price / 10 ** 18:.6f} {self.client.network.token}")

            transaction = await oft_contract.functions.mint(
                self.client.address,
                tokens_amount_mint
            ).build_transaction(await self.client.prepare_transaction(value=mint_price))

            await self.client.send_transaction(transaction)

            await sleep(self, 5, 8)
        else:
            self.logger_msg(
                *self.client.acc_info,
                msg=f"Have enough HMEKL balance: {token_balance}. Network: {self.client.network.name}",
                type_msg='success')

        self.logger_msg(
            *self.client.acc_info,
            msg=f"Bridge tokens on Merkly Hyperlane from {self.client.network.name} -> {dst_chain_name}."
                f" Price for bridge: {(estimate_fee / 10 ** 18):.6f} {self.client.network.token}")

        try:
            transaction = await oft_contract.functions.bridgeHFT(
                dst_chain_id,
                int(tokens_amount_bridge * 10 ** 18)
            ).build_transaction(await self.client.prepare_transaction(value=estimate_fee))

            return await self.client.send_transaction(transaction)
        except Exception as error:
            await self.client.handling_rpc_errors(error)

    @helper
    async def bridge_token(self, bridge_data):
        src_chain_name, dst_chain_name, src_token_name, dsr_token_name, amount, amount_in_wei = bridge_data

        contract_address, _, = MERKLY_HYPERLANE_INFO[src_chain_name]
        _, dst_chain_id = MERKLY_HYPERLANE_INFO[dst_chain_name]

        bridge_contract = self.client.get_contract(contract_address, MERKLY_ABI['HL_bridge'])

        bridge_fee = (await bridge_contract.functions.quoteBridge(
            dst_chain_id,
            amount_in_wei
        ).call())

        fee = bridge_fee / 10 ** 18

        if self.client.network.name not in ['Polygon', 'BNB Chain']:
            amount = round(float(amount) - fee - 0.0003, 6)  # ETH удержание комиссии
            amount_in_wei = int(amount * 10 ** 18)
        else:
            await self.client.check_for_approved(
                TOKENS_PER_CHAIN[src_chain_name]['WETH'], bridge_contract.address, amount_in_wei
            )

        bridge_info = f'{amount} {src_token_name} {src_chain_name} -> {dsr_token_name} {dst_chain_name}'
        self.logger_msg(*self.client.acc_info, msg=f"Bridge ETH on Merkly Hyperlane: {bridge_info}. Fee: {fee:.5f}")

        if self.client.network.name not in ['Polygon', 'BNB Chain'] and int(amount_in_wei - bridge_fee) < 0:
            raise SoftwareExceptionWithoutRetry('Account balance - bridge fee < 0')

        if self.client.network.chain_id in [56, 137]:
            transaction = await bridge_contract.functions.bridgeWETH(
                dst_chain_id,
                amount_in_wei
            ).build_transaction(await self.client.prepare_transaction(value=bridge_fee))
        else:
            transaction = await bridge_contract.functions.bridgeETH(
                dst_chain_id,
                amount_in_wei
            ).build_transaction(await self.client.prepare_transaction(value=int(amount_in_wei + bridge_fee)))

        old_balance_data_on_dst = await self.client.wait_for_receiving(
            chain_to_name=dst_chain_name, token_name=dsr_token_name,
            check_balance_on_dst=True
        )

        await self.client.send_transaction(transaction)

        if Settings.WAIT_FOR_RECEIPT:
            self.logger_msg(
                *self.client.acc_info, msg=f"Bridge complete. Note: wait a little for receiving funds",
                type_msg='success'
            )

            return await self.client.wait_for_receiving(
                chain_to_name=dst_chain_name, token_name=dsr_token_name,
                old_balance_data=old_balance_data_on_dst,
            )
        else:
            return True
