from modules.interfaces import SoftwareException
from dev_settings import Settings
from utils.tools import gas_checker, helper
from config.constants import AAVE_CONTRACTS, TOKENS_PER_CHAIN
from config.abi import AAVE_ABI
from modules import Landing, Logger


class Aave(Landing, Logger):
    def __init__(self, client):
        self.client = client
        Logger.__init__(self)
        self.network = self.client.network.name
        self.weth_gateway_contract = self.client.get_contract(
            AAVE_CONTRACTS[self.network]['weth_gateway'], AAVE_ABI['weth_gateway']
        )
        self.proxy_contract = self.client.get_contract(
            AAVE_CONTRACTS[self.network]['pool_proxy'], AAVE_ABI['pool_proxy']
        )

    @helper
    @gas_checker
    async def deposit(self, amount: float = None, amount_in_wei: int = None):

        if not amount:
            amount = await self.client.get_smart_amount(Settings.LANDINGS_AMOUNT)
            amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(*self.client.acc_info, msg=f'Deposit to AAVE: {amount} ETH')

        tx_params = await self.client.prepare_transaction(value=amount_in_wei)

        transaction = await self.weth_gateway_contract.functions.depositETH(
            AAVE_CONTRACTS[self.network]['pool_proxy'],
            self.client.address,
            0
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)

    @helper
    @gas_checker
    async def withdraw(self):

        liquidity_balance = await self.client.get_contract(
            AAVE_CONTRACTS[self.network]['weth_atoken']
        ).functions.balanceOf(self.client.address).call()

        if liquidity_balance != 0:

            self.logger_msg(
                *self.client.acc_info, msg=f'Withdraw {liquidity_balance / 10 ** 18:.5f} ETH liquidity from AAVE'
            )

            await self.client.check_for_approved(
                AAVE_CONTRACTS[self.network]['weth_atoken'], AAVE_CONTRACTS[self.network]['weth_gateway'],
                liquidity_balance
            )

            tx_params = await self.client.prepare_transaction()

            transaction = await self.weth_gateway_contract.functions.withdrawETH(
                AAVE_CONTRACTS[self.network]['pool_proxy'],
                liquidity_balance,
                self.client.address
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)

        else:
            raise SoftwareException('Insufficient balance on AAVE!')

    @helper
    @gas_checker
    async def enable_collateral(self):
        self.logger_msg(*self.client.acc_info, msg=f'Enable collateral on AAVE')

        tx_params = await self.client.prepare_transaction()

        transaction = await self.proxy_contract.functions.setUserUseReserveAsCollateral(
            TOKENS_PER_CHAIN[self.client.network.name]['ETH'],
            True
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)

    @helper
    @gas_checker
    async def disable_collateral(self):
        self.logger_msg(*self.client.acc_info, msg=f'Disable collateral on AAVE')

        tx_params = await self.client.prepare_transaction()

        transaction = await self.proxy_contract.functions.setUserUseReserveAsCollateral(
            TOKENS_PER_CHAIN[self.client.network.name]['ETH'],
            False
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)
