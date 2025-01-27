from config.constants import KEOM_CONTRACTS
from config.abi import KEOM_ABI
from modules.interfaces import SoftwareException
from dev_settings import Settings
from utils.tools import gas_checker, helper
from modules import Landing, Logger


class Keom(Landing, Logger):
    def __init__(self, client):
        self.client = client
        Logger.__init__(self)

        self.network = self.client.network.name
        self.landing_contract = self.client.get_contract(
            KEOM_CONTRACTS[self.network]['landing'], KEOM_ABI['landing']
        )
        self.market_contract = self.client.get_contract(
            KEOM_CONTRACTS[self.network]['market'], KEOM_ABI['weth_pool']
        )

    @helper
    @gas_checker
    async def deposit(self, amount: float = None, amount_in_wei: int = None):

        if not amount:
            amount = await self.client.get_smart_amount(Settings.LANDINGS_AMOUNT)
            amount_in_wei = self.client.to_wei(amount)

        self.client.logger_msg(*self.client.acc_info, msg=f'Deposit to Keom: {amount} ETH')

        transaction = await self.landing_contract.functions.mint().build_transaction(
            await self.client.prepare_transaction(value=amount_in_wei)
        )

        return await self.client.send_transaction(transaction)

    @helper
    @gas_checker
    async def withdraw(self):
        liquidity_balance_in_wei = await self.landing_contract.functions.balanceOf(self.client.address).call()

        liquidity_balance = f"{liquidity_balance_in_wei / 10 ** 18:.4f}"

        self.client.logger_msg(*self.client.acc_info, msg=f'Withdraw {liquidity_balance} oETH from Keom')

        if liquidity_balance_in_wei != 0:

            tx_params = await self.client.prepare_transaction()

            transaction = await self.landing_contract.functions.redeem(
                liquidity_balance_in_wei,
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)
        else:
            raise SoftwareException("Insufficient balance on Keom!")

    @helper
    @gas_checker
    async def enable_collateral(self):
        self.client.logger_msg(*self.client.acc_info, msg=f'Enable collateral on Keom')

        tx_params = await self.client.prepare_transaction()

        transaction = await self.market_contract.functions.enterMarkets(
            [self.landing_contract.address]
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)

    @helper
    @gas_checker
    async def disable_collateral(self):
        self.client.logger_msg(*self.client.acc_info, msg=f'Disable collateral on Keom')

        tx_params = await self.client.prepare_transaction()

        transaction = await self.market_contract.functions.exitMarket(
            self.landing_contract.address
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)
