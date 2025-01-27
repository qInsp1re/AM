from modules.interfaces import SoftwareExceptionWithoutRetry
from dev_settings import Settings
from utils.tools import gas_checker, helper
from config.constants import ELIXIR_CONTRACTS, TOKENS_PER_CHAIN
from config.abi import ELIXIR_ABI
from modules import Landing, Logger, RequestClient


class Elixir(Landing, Logger, RequestClient):
    def __init__(self, client):
        self.client = client
        Logger.__init__(self)
        RequestClient.__init__(self, client)
        self.network = self.client.network.name
        self.usdc_pool_contract = self.client.get_contract(
            ELIXIR_CONTRACTS[self.network]['eth_usdc_router'], ELIXIR_ABI['eth_usdc_router']
        )

    @helper
    @gas_checker
    async def deposit(self):
        landing_contract = self.client.get_contract(
            ELIXIR_CONTRACTS[self.network]['landing'], ELIXIR_ABI['landing']
        )

        amount = await self.client.get_smart_amount(Settings.ELIXIR_AMOUNT)
        amount_in_wei = self.client.to_wei(amount)
        eth_price = await self.get_token_price('ETH')

        if amount * eth_price < 100:
            raise SoftwareExceptionWithoutRetry('You can`t deposit lower than 100$ in ETH')

        self.logger_msg(*self.client.acc_info, msg=f'Deposit to Elixir: {amount} ETH')

        tx_params = await self.client.prepare_transaction(value=amount_in_wei)

        transaction = await landing_contract.functions.deposit().build_transaction(tx_params)

        return await self.client.send_transaction(transaction)

    @helper
    async def deposit_usdc(self):
        eth_balance = await self.client.get_token_balance()
        if float(f"{eth_balance[1]:.8f}") < 0.005:
            raise SoftwareExceptionWithoutRetry('You must have at least 0.005 ETH in Arbitrum chain to add supply')

        usdc_contract = TOKENS_PER_CHAIN[self.network]['USDC']
        usdc_balance = await self.client.get_token_balance('USDC', token_address=usdc_contract)
        if float(f"{usdc_balance[1]:.8f}") < Settings.ELIXIR_USDC_AMOUNT:
            raise SoftwareExceptionWithoutRetry(
                f'You must have at least {Settings.ELIXIR_USDC_AMOUNT} USDC in Arbitrum chain to add supply'
            )

        decimals = await self.client.get_decimals(token_address=usdc_contract)
        amount_in_wei = self.client.to_wei(Settings.ELIXIR_USDC_AMOUNT, decimals=decimals)

        await self.client.check_for_approved(usdc_contract, self.usdc_pool_contract.address, amount_in_wei)

        self.logger_msg(*self.client.acc_info, msg=f'Adding {Settings.ELIXIR_USDC_AMOUNT} USDC to ETH-USDC pool on Elixir')

        transaction = await self.usdc_pool_contract.functions.deposit(
            2,
            amount_in_wei,
            self.client.address
        ).build_transaction(await self.client.prepare_transaction())

        return await self.client.send_transaction(transaction)

    @helper
    async def withdraw_usdc(self):
        balance_in_wei = (await self.usdc_pool_contract.functions.getUserActiveAmount(
            2,
            self.client.address
        ).call())

        if balance_in_wei == 0:
            raise SoftwareExceptionWithoutRetry('You must have add supply before withdrawing it')

        self.logger_msg(
            *self.client.acc_info, msg=f'Withdrawing {balance_in_wei / 10 ** 6:.8f} USDC from ETH-USDC pool on Elixir'
        )

        transaction = await self.usdc_pool_contract.functions.withdraw(
            2,
            balance_in_wei
        ).build_transaction(await self.client.prepare_transaction())

        return await self.client.send_transaction(transaction)

    async def withdraw(self):
        pass
