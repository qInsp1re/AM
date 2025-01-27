from config.constants import BASILISK_CONTRACTS
from config.abi import BASILISK_ABI
from modules.interfaces import SoftwareException
from dev_settings import Settings
from utils.tools import gas_checker, helper
from modules import Landing, Logger, Client


class Basilisk(Landing, Logger):
    def __init__(self, client: Client):
        self.client = client
        Logger.__init__(self)

        self.landing_contract = self.client.get_contract(
            BASILISK_CONTRACTS[self.client.network.name]['landing'], BASILISK_ABI)
        self.collateral_contract = self.client.get_contract(
            BASILISK_CONTRACTS[self.client.network.name]['collateral'], BASILISK_ABI)

    @helper
    @gas_checker
    async def deposit(self, amount: float = None, amount_in_wei: int = None):

        if not amount:
            amount = await self.client.get_smart_amount(Settings.LANDINGS_AMOUNT)
            amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(*self.client.acc_info, msg=f'Deposit to Basilisk: {amount} ETH')

        tx_params = (await self.client.prepare_transaction()) | {
            'to': BASILISK_CONTRACTS['landing'],
            'value': amount_in_wei,
            'data': '0x1249c58b'
        }

        return await self.client.send_transaction(tx_params)

    @helper
    @gas_checker
    async def withdraw(self):
        self.logger_msg(*self.client.acc_info, msg=f'Withdraw from Basilisk')

        liquidity_balance = await self.landing_contract.functions.balanceOf(self.client.address).call()

        if liquidity_balance != 0:

            tx_params = await self.client.prepare_transaction()

            transaction = await self.landing_contract.functions.redeem(
                liquidity_balance
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)
        else:
            raise SoftwareException("Insufficient balance on Basilisk!")

    @helper
    @gas_checker
    async def enable_collateral(self):
        self.logger_msg(*self.client.acc_info, msg=f'Enable collateral on Basilisk')

        tx_params = await self.client.prepare_transaction()

        transaction = await self.collateral_contract.functions.enterMarkets(
            [BASILISK_CONTRACTS['landing']]
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)

    @helper
    @gas_checker
    async def disable_collateral(self):
        self.logger_msg(*self.client.acc_info, msg=f'Disable collateral on Basilisk')

        tx_params = await self.client.prepare_transaction()

        transaction = await self.collateral_contract.functions.exitMarket(
            BASILISK_CONTRACTS['landing']
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)
