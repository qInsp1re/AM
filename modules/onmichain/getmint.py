from general_settings import HELP_SOFTWARE
from modules import Refuel, Logger, Client
from modules.interfaces import Minter
from eth_abi import encode
from utils.tools import helper, sleep
from config.constants import (
    GETMINT_HYPERLANE_DATA,
    CHAIN_IDS
)
from config.abi import GETMINT_ABI


class GetMint(Refuel, Minter, Logger):
    def __init__(self, client: Client):
        self.client = client
        Logger.__init__(self)

    async def wnft_bridge(self):
        pass

    async def wt_bridge(self):
        pass

    async def pnft_bridge(self):
        pass

    async def p_refuel(self):
        pass

    async def ht_bridge(self):
        pass

    async def refuel(self):
        pass

    async def get_nft_id(self, tx_hash):
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

    async def mint(self, hnft_contract):
        mint_price = await hnft_contract.functions.mintFee().call()

        self.logger_msg(
            *self.client.acc_info,
            msg=f"Mint GetMint NFT on {self.client.network.name}. "
                f"Mint Price: {(mint_price / 10 ** 18):.5f} {self.client.network.token}"
        )

        tx_params = await self.client.prepare_transaction(value=mint_price)

        if HELP_SOFTWARE:
            transaction = await hnft_contract.functions.mintWithReferrer(
                '0x000000a679C2FB345dDEfbaE3c42beE92c0Fb7A5'
            ).build_transaction(tx_params)
        else:
            transaction = await hnft_contract.functions.mint().build_transaction(tx_params)

        tx_hash = await self.client.send_transaction(transaction, need_hash=True)

        if self.client.network.name == 'Polygon':
            await sleep(self, 300, 400)
        else:
            await sleep(self, 100, 200)

        return tx_hash

    @helper
    async def hnft_bridge(self, chain_to_name, need_check: bool = False):
        hnft_contract = self.client.get_contract(
            GETMINT_HYPERLANE_DATA[self.client.network.name]['hNFT'], GETMINT_ABI['hNFT']
        )

        dst_chain_name, dst_chain_id = chain_to_name, CHAIN_IDS[chain_to_name]

        if not need_check:
            tx_hash = await self.mint(hnft_contract)
            nft_id = await self.get_nft_id(tx_hash)

            self.logger_msg(
                *self.client.acc_info,
                msg=f"Bridge GetMint NFT from {self.client.network.name} to {dst_chain_name}. ID: {nft_id}")
        else:
            nft_id = await hnft_contract.functions.minTokenId().call()

        encoded_address = encode(["address"], [self.client.address])

        try:
            bridge_fee = await hnft_contract.functions.bridgeFee().call()
            hyperlane_fee = await hnft_contract.functions.getHyperlaneMessageFee(dst_chain_id).call()

            value = int(bridge_fee + hyperlane_fee)
            mint_price = await hnft_contract.functions.mintFee().call()
            if need_check:
                if await self.client.w3.eth.get_balance(self.client.address) > int(value + mint_price + 0.0005):
                    return True
                return False

            tx_params = await self.client.prepare_transaction(value=value)

            transaction = await hnft_contract.functions.transferRemote(
                dst_chain_id,
                encoded_address,
                nft_id,
            ).build_transaction(tx_params)

            if need_check:
                return True

            return await self.client.send_transaction(transaction, need_hash=True)

        except Exception as error:
            if not need_check:
                await self.client.handling_rpc_errors(error)
