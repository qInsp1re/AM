import random

from modules.interfaces import SoftwareException
from dev_settings import Settings
from utils.tools import gas_checker, helper
from config.constants import SEAMLESS_CONTRACTS, TOKENS_PER_CHAIN
from config.abi import SEAMLESS_ABI
from modules import Landing, Logger, Client


class Seamless(Landing, Logger):
    def __init__(self, client: Client):
        self.client = client
        Logger.__init__(self)
        self.network = self.client.network.name
        self.landing_contract = self.client.get_contract(
            SEAMLESS_CONTRACTS[self.network]['landing'], SEAMLESS_ABI['landing']
        )
        self.proxy_contract = self.client.get_contract(
            SEAMLESS_CONTRACTS[self.network]['pool_proxy'], SEAMLESS_ABI['pool_proxy']
        )

    @helper
    @gas_checker
    async def deposit(self, amount: float = None, amount_in_wei: int = None):

        if not amount:
            amount = await self.client.get_smart_amount(Settings.LANDINGS_AMOUNT)
            amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(*self.client.acc_info, msg=f'Deposit to Seamless: {amount} ETH')

        tx_params = await self.client.prepare_transaction(value=amount_in_wei)

        transaction = await self.landing_contract.functions.depositETH(
            SEAMLESS_CONTRACTS[self.network]['pool_proxy'],
            self.client.address,
            0
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)

    @helper
    @gas_checker
    async def withdraw(self):

        liquidity_balance = await self.client.get_contract(
            SEAMLESS_CONTRACTS[self.network]['weth_atoken']
        ).functions.balanceOf(self.client.address).call()

        if liquidity_balance != 0:

            self.logger_msg(
                *self.client.acc_info, msg=f'Withdraw {liquidity_balance / 10 ** 18:.5f} sETH from Seamless'
            )

            await self.client.check_for_approved(
                SEAMLESS_CONTRACTS[self.network]['weth_atoken'], SEAMLESS_CONTRACTS[self.network]['landing'],
                liquidity_balance, unlimited_approve=True
            )

            tx_params = await self.client.prepare_transaction()

            transaction = await self.landing_contract.functions.withdrawETH(
                SEAMLESS_CONTRACTS[self.network]['pool_proxy'],
                2 ** 256 - 1,
                self.client.address
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)

        else:
            raise SoftwareException('Insufficient balance on Seamless!')

    @helper
    @gas_checker
    async def enable_collateral(self):
        self.logger_msg(*self.client.acc_info, msg=f'Enable collateral on Seamless')

        tx_params = await self.client.prepare_transaction()

        transaction = await self.proxy_contract.functions.setUserUseReserveAsCollateral(
            TOKENS_PER_CHAIN[self.client.network.name][random.choice(['ETH', 'USDC.e'])],
            True
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)

    @helper
    @gas_checker
    async def disable_collateral(self):
        self.logger_msg(*self.client.acc_info, msg=f'Disable collateral on Seamless')

        tx_params = await self.client.prepare_transaction()

        transaction = await self.proxy_contract.functions.setUserUseReserveAsCollateral(
            TOKENS_PER_CHAIN[self.client.network.name][random.choice(['ETH', 'USDC.e'])],
            False
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)
