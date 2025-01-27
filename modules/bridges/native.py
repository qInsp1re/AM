from modules import Bridge, Logger
from dev_settings import Settings


class NativeBridge(Bridge, Logger):
    def __init__(self, client):
        self.client = client
        Logger.__init__(self)
        Bridge.__init__(self, client)

    @staticmethod
    async def get_bridge_class(from_chain_id, to_chain_id):
        from functions import ZkSync, Scroll, PolygonZkEVM, Linea, Base, Zora

        class_info = {
            8453: Base,
            59144: Linea,
            534352: Scroll,
            1101: PolygonZkEVM,
            324: ZkSync,
            7777777: Zora,
        }

        needed_chain_id = to_chain_id if from_chain_id == 1 else from_chain_id

        return class_info[needed_chain_id]

    async def bridge(self, bridge_data: tuple, need_check: bool = False):
        (from_chain_id, to_chain_id, amount, from_token_name,
         to_token_name, from_token_address, to_token_address, chain_to_name) = bridge_data

        if need_check:
            return 0

        bridge_class = await self.get_bridge_class(from_chain_id, to_chain_id)

        old_balance_data_on_dst = await self.client.wait_for_receiving(
            chain_to_name=chain_to_name, token_name=to_token_name, token_address=to_token_address,
            check_balance_on_dst=True
        )

        if from_chain_id == 1:
            await bridge_class(self.client).deposit(amount)
        elif to_chain_id == 7777777 or from_chain_id == 7777777:
            await bridge_class(self.client).bridge(amount, to_chain_id)
        else:
            await bridge_class(self.client).withdraw(amount)

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
