import random

from modules import Logger, CosmosClient
from modules.interfaces import SoftwareExceptionWithoutRetry
from dev_settings import Settings
from utils.tools import gas_checker, helper


class SimpleCosmos(Logger):
    def __init__(self, client: CosmosClient):
        self.client = client
        Logger.__init__(self)

        self.network = self.client.network.name
        self.deposit_contract = None
        self.withdraw_contract = None

    def get_cosmos_address(self):
        from cosmpy.aerial.wallet import LocalWallet
        from cosmpy.crypto.address import Address

        if self.client.network.name == 'Injective':
            self.client.network_prefix = 'inj'

            from utils.inj_derivation import PrivateKey

            cosmos_private_key = PrivateKey.generate()[1]
            cosmos_public_key = cosmos_private_key.to_public_key()
            cosmos_pre_address = cosmos_public_key.to_address()
            return Address(cosmos_pre_address.to_acc_bech32(), prefix=self.client.network_prefix)

        else:
            wallet = LocalWallet.generate(self.client.network_prefix)
            public_key = wallet.public_key()
            return Address(public_key, prefix=self.client.network_prefix)

    @helper
    @gas_checker
    async def transfer_native(self, amount: float):
        token_name = self.client.token[1:].upper()

        if amount > 0.01:
            raise SoftwareExceptionWithoutRetry(
                f'Are you sure about transferring more than 0.01 {token_name} to a random address?')

        random_address = f"{self.get_cosmos_address()}"

        self.logger_msg(
            *self.client.acc_info,
            msg=f'Transfer {amount} {token_name} to random {self.client.network.name} address'
        )

        return await self.client.send_tokens(address=random_address, amount=amount, without_fee_support=True)

    @helper
    @gas_checker
    async def transfer_native_to_cex(self, amount: float):
        from utils.tools import get_wallet_for_deposit

        if amount > 0.5:
            raise SoftwareExceptionWithoutRetry(
                f'Are you sure about transferring more than 0.005{self.client.token} to CEX address?')

        deposit_network = {
            'Celestia': 43,
            'Neutron': 44,
            'Injective': 42
        }[self.client.network.name]

        cex_name = {
            0: 'Stop',
            1: "Bitget",
            2: "OKX"
        }[random.choice(Settings.TRANSFER_COSMOS_CEXS[self.client.network.name])]

        if cex_name == 'Stop':
            self.logger_msg(
                *self.client.acc_info,
                msg=f"You are disable {self.client.network.name} transfers", type_msg='warning'
            )
            return True

        cex_address = get_wallet_for_deposit(self, deposit_network, cex_name=cex_name)
        token_name = self.client.token[1:].upper()

        self.logger_msg(
            *self.client.acc_info,
            msg=f"Transfer {amount} {token_name} to your {cex_name} address: {cex_address}"
        )

        return await self.client.send_tokens(address=cex_address, amount=amount, without_fee_support=True)
