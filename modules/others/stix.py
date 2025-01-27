from modules import Logger, Client
from utils.tools import helper, gas_checker
from config.constants import ETH_MASK
from eth_abi import encode


class Stix(Logger):
    def __init__(self, client: Client):
        self.client = client
        Logger.__init__(self)

    @helper
    @gas_checker
    async def mint_pass(self):
        self.logger_msg(*self.client.acc_info, msg=f"Minting the STIX Launch Tournament Pass")

        function_signature = '0x84bb1e42'
        encoded_parameters = encode(
            ['address', 'uint256', 'address', 'uint256', '(bytes32[],uint256,uint256,address)', 'bytes'],
            [f"{self.client.address}", 1, ETH_MASK, 0, ([bytes(32)], 1, 0, ETH_MASK), bytes()]
        )
        data = function_signature + encoded_parameters.hex()

        try:
            transaction = await self.client.prepare_transaction() | {
                'to': '0xa7891c87933BB99Db006b60D8Cb7cf68141B492f',
                'data': data
            }

            return await self.client.send_transaction(transaction)

        except Exception as error:
            if '!Qty' in str(error):
                self.logger_msg(
                    *self.client.acc_info,
                    msg=f"STIX Launch Tournament Pass has already been minted", type_msg='warning'
                )

            else:
                self.logger_msg(
                    *self.client.acc_info,
                    msg=f"Impossible to mint the STIX Launch Tournament Pass. Error: {error}", type_msg='error'
                )
