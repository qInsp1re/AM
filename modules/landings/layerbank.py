from config.constants import LAYERBANK_CONTRACTS
from config.abi import LAYERBANK_ABI
from modules.interfaces import SoftwareException
from dev_settings import Settings
from utils.tools import gas_checker, helper
from modules import Landing, Logger, Client


class LayerBank(Landing, Logger):
    def __init__(self, client: Client):
        self.client = client
        Logger.__init__(self)

        self.network = self.client.network.name
        self.landing_contract = self.client.get_contract(
            LAYERBANK_CONTRACTS[self.network]['landing'], LAYERBANK_ABI['landing']
        )
        self.pool_contract = self.client.get_contract(
            LAYERBANK_CONTRACTS[self.network]['pool'], LAYERBANK_ABI['pool']
        )

    @helper
    @gas_checker
    async def deposit(self, amount: float = None, amount_in_wei: int = None):

        if not amount:
            amount = await self.client.get_smart_amount(Settings.LANDINGS_AMOUNT)
            amount_in_wei = self.client.to_wei(amount)

        self.client.logger_msg(*self.client.acc_info, msg=f'Deposit to LayerBank: {amount} ETH')

        tx_params = await self.client.prepare_transaction(value=amount_in_wei)

        transaction = await self.landing_contract.functions.supply(
            LAYERBANK_CONTRACTS[self.network]['pool'],
            amount_in_wei
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)

    @helper
    @gas_checker
    async def withdraw(self):
        liquidity_balance_in_wei = await self.pool_contract.functions.underlyingBalanceOf(self.client.address).call()

        liquidity_balance = f"{liquidity_balance_in_wei / 10 ** 18:.4f}"

        if liquidity_balance_in_wei != 0:

            self.client.logger_msg(*self.client.acc_info, msg=f'Withdraw {liquidity_balance} ETH from LayerBank')

            tx_params = await self.client.prepare_transaction()

            transaction = await self.landing_contract.functions.redeemUnderlying(
                LAYERBANK_CONTRACTS[self.network]['pool'],
                liquidity_balance_in_wei,
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)
        else:
            raise SoftwareException("Insufficient balance on LayerBank!")

    @helper
    @gas_checker
    async def enable_collateral(self):
        self.client.logger_msg(*self.client.acc_info, msg=f'Enable collateral on LayerBank')

        tx_params = await self.client.prepare_transaction()

        transaction = await self.landing_contract.functions.enterMarkets(
            [LAYERBANK_CONTRACTS[self.network]['pool']]
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)

    @helper
    @gas_checker
    async def disable_collateral(self):
        self.client.logger_msg(*self.client.acc_info, msg=f'Disable collateral on LayerBank')

        tx_params = await self.client.prepare_transaction()

        transaction = await self.landing_contract.functions.exitMarket(
            LAYERBANK_CONTRACTS[self.network]['pool']
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)
