import random

from modules import Logger, Client
from config.abi import DBK_GENESIS_NFT_CONTRACT_ABI, BRIDGE_FROM_DBK_TO_ETH_CONTRACT_ABI
from utils.tools import helper, gas_checker
from config.constants import DBK_GENESIS_NFT_CONTRACT, BRIDGE_TO_DBK_CONTRACT
from dev_settings import Settings


class DBK(Logger):
    def __init__(self, client: Client):
        self.client = client
        Logger.__init__(self)

    async def bridge(self):
        eth_client = await self.client.new_client('Ethereum')
        bridge_contract = eth_client.get_contract(BRIDGE_TO_DBK_CONTRACT, BRIDGE_FROM_DBK_TO_ETH_CONTRACT_ABI)
        self.logger_msg(*eth_client.acc_info, msg=f"Bridging ETH from Ethereum to DBK chain")
        amount_in_wei = self.client.to_wei(round(random.uniform(*Settings.DBK_BRIDGE_AMOUNT), 6))

        transaction = await bridge_contract.functions.depositTransaction(
            self.client.address,
            amount_in_wei,
            21000,
            False,
            "0x"
        ).build_transaction(await eth_client.prepare_transaction(value=amount_in_wei))

        old_balance_data_on_dst = await eth_client.wait_for_receiving(
            chain_to_name='DBK',
            check_balance_on_dst=True
        )

        await eth_client.send_transaction(transaction)

        self.logger_msg(
            *eth_client.acc_info,
            msg=f"Bridge complete. Note: wait a little for receiving funds", type_msg='success'
        )

        if Settings.WAIT_FOR_RECEIPT_BRIDGE:
            res = await eth_client.wait_for_receiving(
                old_balance_data=old_balance_data_on_dst,
                chain_to_name="DBK"
            )
            await eth_client.session.close()
            return res
        else:
            await eth_client.session.close()
            return True

    @helper
    @gas_checker
    async def mint(self):
        balance = await self.client.get_token_balance()
        if float(f"{balance[1]:.8f}") < 0.0001:
            await self.bridge()
        nft_contract = self.client.get_contract(DBK_GENESIS_NFT_CONTRACT, DBK_GENESIS_NFT_CONTRACT_ABI)
        self.logger_msg(*self.client.acc_info, msg="Minting DBK Genesis NFT")
        transaction = await nft_contract.functions.mint().build_transaction(
            await self.client.prepare_transaction()
        )
        return await self.client.send_transaction(transaction)
