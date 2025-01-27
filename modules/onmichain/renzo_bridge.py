from modules import Logger, Client

from modules.interfaces import SoftwareExceptionWithoutRetry
from dev_settings import Settings
from eth_abi import abi
from utils.tools import helper
from config.constants import (
    RENZO_BRIDGE_INFO,
    TOKENS_PER_CHAIN
)
from config.abi import RENZO_ABI


class RenzoBridge(Logger):
    def __init__(self, client: Client):
        self.client = client
        Logger.__init__(self)

    @helper
    async def bridge_token(self, bridge_data):
        src_chain_name, dst_chain_name, src_token_name, dsr_token_name, amount, amount_in_wei = bridge_data

        contract_address, _, = RENZO_BRIDGE_INFO[src_chain_name]
        _, dst_chain_id = RENZO_BRIDGE_INFO[dst_chain_name]

        bridge_contract = self.client.get_contract(contract_address, RENZO_ABI['bridge'])

        bridge_fee = (await bridge_contract.functions.quoteGasPayment(
            dst_chain_id
        ).call())

        fee = bridge_fee / 10 ** 18

        await self.client.check_for_approved(
            TOKENS_PER_CHAIN[src_chain_name]['ezETH'], bridge_contract.address, amount_in_wei
        )

        bridge_info = f'{amount} {src_token_name} {src_chain_name} -> {dsr_token_name} {dst_chain_name}'
        self.logger_msg(*self.client.acc_info, msg=f"Bridge ezETH on Renzo: {bridge_info}. Fee: {fee:.5f}")

        if self.client.network.name not in ['Polygon', 'BNB Chain'] and int(amount_in_wei - bridge_fee) < 0:
            raise SoftwareExceptionWithoutRetry('Account balance - bridge fee < 0')

        dst_address = abi.encode(['address'], [self.client.address])

        transaction = await bridge_contract.functions.transferRemote(
            dst_chain_id,
            dst_address,
            amount_in_wei
        ).build_transaction(await self.client.prepare_transaction(value=bridge_fee))

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
