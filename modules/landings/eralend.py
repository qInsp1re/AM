from config.constants import ERALEND_CONTRACTS
from config.abi import ERALEND_ABI
from modules.interfaces import SoftwareException
from dev_settings import Settings
from utils.tools import gas_checker, helper
from modules import Landing, Logger, Client


class EraLend(Landing, Logger):
    def __init__(self, client: Client):
        self.client = client
        Logger.__init__(self)

        self.landing_contract = self.client.get_contract(
            ERALEND_CONTRACTS[self.client.network.name]['landing'], ERALEND_ABI
        )
        self.collateral_contract = self.client.get_contract(
            ERALEND_CONTRACTS[self.client.network.name]['collateral'], ERALEND_ABI
        )

    @helper
    @gas_checker
    async def deposit(self, amount: float = None, amount_in_wei: int = None):

        if not amount:
            amount = await self.client.get_smart_amount(Settings.LANDINGS_AMOUNT)
            amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(*self.client.acc_info, msg=f'Deposit to EraLend: {amount} ETH')

        tx_params = (await self.client.prepare_transaction()) | {
            'to': ERALEND_CONTRACTS['landing'],
            'value': amount_in_wei,
            'data': '0x1249c58b'
        }

        return await self.client.send_transaction(tx_params)

    @helper
    @gas_checker
    async def withdraw(self):
        liquidity_balance = await self.landing_contract.functions.balanceOfUnderlying(self.client.address).call()

        if liquidity_balance != 0:

            self.logger_msg(*self.client.acc_info, msg=f'Withdraw {liquidity_balance / 10 ** 18:.5f} from EraLend')

            tx_params = await self.client.prepare_transaction()

            transaction = await self.landing_contract.functions.redeemUnderlying(
                liquidity_balance
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)

        else:
            raise SoftwareException(f'Insufficient balance on EraLend!')

    @helper
    @gas_checker
    async def enable_collateral(self):
        self.logger_msg(*self.client.acc_info, msg=f'Enable collateral on EraLend')

        tx_params = await self.client.prepare_transaction()

        transaction = await self.collateral_contract.functions.enterMarkets(
            [ERALEND_CONTRACTS['landing']]
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)

    @helper
    @gas_checker
    async def disable_collateral(self):
        self.logger_msg(*self.client.acc_info, msg=f'Disable collateral on EraLend')

        tx_params = await self.client.prepare_transaction()

        transaction = await self.collateral_contract.functions.exitMarket(
            ERALEND_CONTRACTS['landing']
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)
