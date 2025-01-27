import os
import random

from eth_account import Account
from modules import Blockchain, Logger, Client
from modules.interfaces import SoftwareException, SoftwareExceptionWithoutRetry
from utils.tools import gas_checker, helper
from dev_settings import Settings
from config.constants import (
    TOKENS_PER_CHAIN,
    NATIVE_CONTRACTS_PER_CHAIN,
    CHAIN_NAME, ZERO_ADDRESS,
)
from config.abi import ZKSYNC_CONTRACT_ABI, WETH_ABI, NATIVE_ABI


class SimpleEVM(Logger):
    def __init__(self, client: Client):
        self.client = client
        Logger.__init__(self)

        self.network = self.client.network.name
        self.token_contract = self.client.get_contract(
            TOKENS_PER_CHAIN[self.network][f'W{self.client.token}'], WETH_ABI
        )
        self.deposit_contract = None
        self.withdraw_contract = None

    @helper
    @gas_checker
    async def deploy_contract(self):

        self.logger_msg(*self.client.acc_info, msg=f"Deploy '0x' contract on {self.client.network.name}")

        transaction = await self.client.prepare_transaction() | {
            'data': 'Ox'
        }

        return await self.client.send_transaction(transaction)

    @helper
    @gas_checker
    async def transfer_eth_to_myself(self, amount: float = None):

        if not amount:
            amount = await self.client.get_smart_amount(Settings.TRANSFER_AMOUNT)

        amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(
            *self.client.acc_info,
            msg=f"Transfer {amount} {self.client.token} to your own address: {self.client.address}"
        )

        tx_params = await self.client.prepare_transaction(value=amount_in_wei) | {
            "to": self.client.address,
            "data": "0x"
        }

        return await self.client.send_transaction(tx_params)

    @helper
    @gas_checker
    async def transfer_eth(self, amount: float = None):

        if not amount:
            amount = await self.client.get_smart_amount(Settings.TRANSFER_AMOUNT)

        amount_in_wei = self.client.to_wei(amount)

        if amount > 0.0001:
            raise SoftwareExceptionWithoutRetry(
                f'Are you sure about transferring more than 0.0001{self.client.token} to a random address?')

        random_address = Account.create().address
        token_name = self.client.token

        self.logger_msg(
            *self.client.acc_info,
            msg=f'Transfer {token_name} to random {self.client.network.name} address: {amount} {token_name}'
        )

        if await self.client.w3.eth.get_balance(self.client.address) > amount_in_wei:

            tx_params = (await self.client.prepare_transaction(value=amount_in_wei)) | {
                'to': random_address,
                'data': "0x"
            }

            return await self.client.send_transaction(tx_params)

        else:
            raise SoftwareException('Insufficient balance!')

    @helper
    @gas_checker
    async def wrap_eth(self, amount: float = None):

        if not amount:
            amount = await self.client.get_smart_amount(Settings.WRAPS_AMOUNT)

        amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(*self.client.acc_info, msg=f'Wrap {amount} ETH')

        if await self.client.w3.eth.get_balance(self.client.address) > amount_in_wei:

            tx_params = await self.client.prepare_transaction(value=amount_in_wei)
            transaction = await self.token_contract.functions.deposit().build_transaction(tx_params)

            return await self.client.send_transaction(transaction)

        else:
            raise SoftwareException('Insufficient balance!')

    @helper
    @gas_checker
    async def unwrap_eth(self, amount: float = None):

        if not amount:
            amount_in_wei = await self.client.get_contract(
                TOKENS_PER_CHAIN[self.client.network.name][f'W{self.client.token}']
            ).functions.balanceOf(self.client.address).call()

            amount = round(amount_in_wei / 10 ** 18, 6)
        else:
            amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(*self.client.acc_info, msg=f'Unwrap {amount:.6f} WETH')

        tx_params = await self.client.prepare_transaction()

        transaction = await self.token_contract.functions.withdraw(
            amount_in_wei
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)


class Scroll(Blockchain, SimpleEVM):
    def __init__(self, client):
        SimpleEVM.__init__(self, client)
        Blockchain.__init__(self, client)
        self.deposit_contract = self.client.get_contract(
            NATIVE_CONTRACTS_PER_CHAIN['Scroll']['deposit'],
            NATIVE_ABI['Scroll']['deposit']
        )
        self.withdraw_contract = self.client.get_contract(
            NATIVE_CONTRACTS_PER_CHAIN['Scroll']['withdraw'],
            NATIVE_ABI['Scroll']['withdraw']
        )

        self.oracle_contract = self.client.get_contract(
            NATIVE_CONTRACTS_PER_CHAIN['Scroll']["oracle"],
            NATIVE_ABI['Scroll']['oracle']
        )

    @helper
    @gas_checker
    async def deposit(self, amount:float):
        amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(*self.client.acc_info, msg=f'Bridge {amount} ETH ERC20 -> Scroll')

        if await self.client.w3.eth.get_balance(self.client.address) > amount_in_wei:

            gas_limit = 168000
            gas_price = await self.client.w3.eth.gas_price

            bridge_fee = int(gas_limit * gas_price / 4)

            tx_params = await self.client.prepare_transaction(value=amount_in_wei + bridge_fee)

            transaction = await self.deposit_contract.functions.sendMessage(
                self.client.address,
                amount_in_wei,
                '0x',
                168000,
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)

        else:
            raise SoftwareException('Insufficient balance!')

    @helper
    @gas_checker
    async def withdraw(self, amount:float):
        amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(*self.client.acc_info, msg=f'Withdraw {amount} ETH Scroll -> ERC20')

        if await self.client.w3.eth.get_balance(self.client.address) > amount_in_wei:

            tx_params = await self.client.prepare_transaction(value=amount_in_wei)

            transaction = await self.withdraw_contract.functions.withdrawETH(
                amount_in_wei,
                0
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)

        else:
            raise SoftwareException('Insufficient balance!')


class ZkSync(Blockchain, SimpleEVM):
    def __init__(self, client):
        SimpleEVM.__init__(self, client)
        Blockchain.__init__(self, client)

        self.deposit_contract = self.client.get_contract(
            NATIVE_CONTRACTS_PER_CHAIN['zkSync']['deposit'],
            NATIVE_ABI['zkSync']['deposit']
        )
        self.withdraw_contract = self.client.get_contract(
            NATIVE_CONTRACTS_PER_CHAIN['zkSync']['withdraw'],
            NATIVE_ABI['zkSync']['withdraw']
        )

    @helper
    @gas_checker
    async def deploy_contract(self):
        contract_deployer = NATIVE_CONTRACTS_PER_CHAIN['zkSync']['contact_deployer']
        contract = self.client.get_contract(contract_deployer, ZKSYNC_CONTRACT_ABI)

        salt = f"0x{os.urandom(32).hex()}"
        byte_code_hash = '0x01000021a88a3dee3b0944ff9cbf36cb51c26df19b404d38a115a2a2e3ee5b88'

        self.logger_msg(*self.client.acc_info, msg=f"Deploy contract on {self.client.network.name} with Merkly")

        transaction = await contract.functions.create(
            salt,
            byte_code_hash,
            '0x'
        ).build_transaction(await self.client.prepare_transaction())

        return await self.client.send_transaction(transaction)

    @helper
    @gas_checker
    async def deposit(self, amount:float):
        amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(*self.client.acc_info, msg=f'Bridge on txSync: {amount} ETH ERC20 -> zkSync Era')

        if await self.client.w3.eth.get_balance(self.client.address) > amount_in_wei:

            gas_limit = random.randint(750000, 1000000)

            base_cost_in_wei = int((await self.deposit_contract.functions.l2TransactionBaseCost(
                await self.client.w3.eth.gas_price,
                gas_limit,
                800
            ).call()) * 1.2)

            tx_params = await self.client.prepare_transaction(value=amount_in_wei + base_cost_in_wei)

            transaction = await self.deposit_contract.functions.requestL2Transaction(
                self.client.address,
                amount_in_wei,
                "0x",
                gas_limit,
                800,
                [],
                self.client.address
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)

        else:
            raise SoftwareException('Bridge on txSync | Insufficient balance!')

    @helper
    @gas_checker
    async def withdraw(self, amount:float):
        amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(*self.client.acc_info, msg=f'Withdraw on txSync: {amount} ETH zkSync Era -> ERC20')

        if await self.client.w3.eth.get_balance(self.client.address) > amount_in_wei:

            tx_params = await self.client.prepare_transaction(value=amount_in_wei)

            transaction = await self.withdraw_contract.functions.withdraw(
                self.client.address,
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)

        else:
            raise SoftwareException('Withdraw on txSync | Insufficient balance!')


class Base(Blockchain, SimpleEVM):
    def __init__(self, client):
        SimpleEVM.__init__(self, client)
        Blockchain.__init__(self, client)

        self.deposit_contract = self.client.get_contract(
            NATIVE_CONTRACTS_PER_CHAIN['Base']['deposit'],
            NATIVE_ABI['Base']['deposit']
        )
        self.withdraw_contract = self.client.get_contract(
            NATIVE_CONTRACTS_PER_CHAIN['Base']['withdraw'],
            NATIVE_ABI['Base']['withdraw']
        )

    @helper
    @gas_checker
    async def deposit(self, amount: float):
        amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(*self.client.acc_info, msg=f'Bridge on Base Bridge: {amount} ETH ERC20 -> Base')

        if await self.client.w3.eth.get_balance(self.client.address) > amount_in_wei:

            tx_params = await self.client.prepare_transaction(value=amount_in_wei)

            transaction = await self.deposit_contract.functions.depositTransaction(
                self.client.address,
                amount_in_wei,
                100000,
                False,
                "0x01"
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)

        else:
            raise SoftwareException('Insufficient balance!')

    @helper
    @gas_checker
    async def withdraw(self, amount:float):
        amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(*self.client.acc_info, msg=f'Withdraw on Base Bridge: {amount} ETH Base -> ERC20')

        if await self.client.w3.eth.get_balance(self.client.address) > amount_in_wei:

            tx_params = await self.client.prepare_transaction(value=amount_in_wei)

            transaction = await self.withdraw_contract.functions.initiateWithdrawal(
                self.client.address,
                100000,
                '0x01'
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)

        else:
            raise SoftwareException('Insufficient balance!')


class Linea(Blockchain, SimpleEVM):
    def __init__(self, client: Client):
        SimpleEVM.__init__(self, client)
        Blockchain.__init__(self, client)

        self.deposit_contract = self.client.get_contract(
            NATIVE_CONTRACTS_PER_CHAIN['Linea']['deposit'],
            NATIVE_ABI['Linea']['deposit']
        )
        self.withdraw_contract = self.client.get_contract(
            NATIVE_CONTRACTS_PER_CHAIN['Linea']['withdraw'],
            NATIVE_ABI['Linea']['withdraw']
        )

    async def get_bridge_fee(self, from_l1: bool = True):
        margin = 2
        gas_limit = 106000
        new_client = await self.client.new_client(4 if from_l1 else 13)
        bridge_fee = int(margin * gas_limit * await new_client.w3.eth.gas_price)

        await new_client.session.close()
        return bridge_fee

    @helper
    @gas_checker
    async def deposit(self, amount:float):
        amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(*self.client.acc_info, msg=f'Bridge {amount} ETH ERC20 -> Linea')

        if await self.client.w3.eth.get_balance(self.client.address) > amount_in_wei:

            bridge_fee = await self.get_bridge_fee()

            tx_params = await self.client.prepare_transaction(value=amount_in_wei + bridge_fee)

            transaction = await self.deposit_contract.functions.sendMessage(
                self.client.address,
                bridge_fee,
                "0x"
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)

        else:
            raise SoftwareException('Insufficient balance!')

    @helper
    @gas_checker
    async def withdraw(self, amount:float):
        amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(*self.client.acc_info, msg=f'Withdraw {amount} ETH Linea -> ERC20')

        if await self.client.w3.eth.get_balance(self.client.address) > amount_in_wei:

            bridge_fee = await self.get_bridge_fee(from_l1=False)

            tx_params = await self.client.prepare_transaction(value=amount_in_wei + bridge_fee)

            transaction = await self.withdraw_contract.functions.sendMessage(
                amount_in_wei,
                bridge_fee,
                0
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)

        else:
            raise SoftwareException('Insufficient balance!')


class ArbitrumNova(Blockchain, SimpleEVM):
    def __init__(self, client):
        SimpleEVM.__init__(self, client)
        Blockchain.__init__(self, client)


class PolygonZkEVM(Blockchain, SimpleEVM):
    def __init__(self, client):
        SimpleEVM.__init__(self, client)
        Blockchain.__init__(self, client)
        self.deposit_contract = self.client.get_contract(
            NATIVE_CONTRACTS_PER_CHAIN['PolygonZkEVM']['deposit'],
            NATIVE_ABI['PolygonZkEVM']['deposit']
        )
        self.withdraw_contract = self.client.get_contract(
            NATIVE_CONTRACTS_PER_CHAIN['PolygonZkEVM']['withdraw'],
            NATIVE_ABI['PolygonZkEVM']['withdraw']
        )

    @helper
    @gas_checker
    async def deposit(self, amount:float):
        amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(*self.client.acc_info, msg=f'Bridge {amount} ETH ERC20 -> PolygonZkEVM')

        if await self.client.w3.eth.get_balance(self.client.address) > amount_in_wei:

            tx_params = await self.client.prepare_transaction(value=amount_in_wei)

            transaction = await self.deposit_contract.functions.bridgeAsset(
                1,
                self.client.address,
                amount_in_wei,
                ZERO_ADDRESS,
                True,
                "0x"
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)

        else:
            raise SoftwareException('Insufficient balance!')

    @helper
    @gas_checker
    async def withdraw(self, amount:float):
        amount_in_wei = self.client.to_wei(amount)

        self.logger_msg(*self.client.acc_info, msg=f'Withdraw {amount} ETH Polygon zkEVM -> ERC20')

        if await self.client.w3.eth.get_balance(self.client.address) > amount_in_wei:

            tx_params = await self.client.prepare_transaction(value=amount_in_wei)

            transaction = await self.deposit_contract.functions.bridgeAsset(
                0,
                self.client.address,
                amount_in_wei,
                ZERO_ADDRESS,
                True,
                "0x"
            ).build_transaction(tx_params)

            return await self.client.send_transaction(transaction)

        else:
            raise SoftwareException('Insufficient balance!')


class Ethereum(Blockchain, SimpleEVM):
    def __init__(self, client):
        SimpleEVM.__init__(self, client)
        Blockchain.__init__(self, client)


class Blast(Blockchain, SimpleEVM):
    def __init__(self, client):
        SimpleEVM.__init__(self, client)
        Blockchain.__init__(self, client)


class Zora(Blockchain, SimpleEVM):
    def __init__(self, client: Client):
        SimpleEVM.__init__(self, client)
        Blockchain.__init__(self, client)

    async def get_bridge_info(self, amount_in_wei, chain_to_name):
        url = f'https://api-{chain_to_name.lower()}.reservoir.tools/execute/call/v1'

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "content-type": "application/json",
            "sec-ch-ua": '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "Origin": "https://bridge.zora.energy",
            "Referer": "https://bridge.zora.energy/",
            "sec-fetch-site": "cross-site",
            "x-rkc-version": "1.11.2",
            "referrer": "https://bridge.zora.energy/",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "method": "POST",
            "mode": "cors",
            "credentials": "omit"
        }

        options_headres = {
            "accept": "*/*",
            "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "referrer": "https://bridge.zora.energy/",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "method": "OPTIONS",
            "mode": "cors",
            "credentials": "omit"
        }

        payload = {
            "user": self.client.address,
            "txs": [
                {
                    "to": self.client.address,
                    "value": f"{amount_in_wei}",
                    "data": "0x"
                }
            ],
            "originChainId": self.client.network.chain_id
        }

        await self.client.session.options(url=url, headers=options_headres)

        data = (await self.make_request(
            method='POST', url=url, headers=headers, json=payload
        ))["steps"][0]["items"][0]["data"]

        contract_address = self.client.w3.to_checksum_address(data["to"])
        tx_data = data["data"]
        value = int(data["value"])

        return contract_address, tx_data, value

    @helper
    @gas_checker
    async def bridge(self, amount, to_chain_id):
        amount_in_wei = self.client.to_wei(amount)

        chain_to_name = CHAIN_NAME[to_chain_id]
        contract_address, tx_data, value = await self.get_bridge_info(amount_in_wei, chain_to_name)

        self.logger_msg(
            *self.client.acc_info,
            msg=f'Bridge {amount} from {self.client.network.name} -> {chain_to_name}')

        if await self.client.w3.eth.get_balance(self.client.address) > amount_in_wei:

            transaction = await self.client.prepare_transaction(value=value) | {
                'to': contract_address,
                'data': tx_data
            }

            return await self.client.send_transaction(transaction)

        else:
            raise SoftwareException('Insufficient balance!')
