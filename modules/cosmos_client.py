import asyncio
import math
import random

from aiohttp import ClientSession, TCPConnector
from aiohttp_socks import ProxyConnector
from cosmpy.aerial.contract import LedgerContract
from cosmpy.aerial.exceptions import QueryTimeoutError
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.address import Address
from cosmpy.aerial.client import LedgerClient, Account
from cosmpy.aerial.tx import Transaction, TxState, SigningCfg
from cosmpy.aerial.config import NetworkConfig
from eth_typing import HexStr

from modules.interfaces import SoftwareException
from modules import Logger
from web3 import AsyncWeb3

from utils.tools import network_handler


class CustomTransaction(Transaction):
    def sign(self, signer, chain_id: str, account_number: int, deterministic: bool = False):
        if self.state != TxState.Sealed:
            raise RuntimeError(
                "Transaction is not sealed. It must be sealed before signing is possible."
            )

        from cosmpy.protos.cosmos.tx.v1beta1.tx_pb2 import SignDoc
        sd = SignDoc()
        sd.body_bytes = self._tx.body.SerializeToString()
        sd.auth_info_bytes = self._tx.auth_info.SerializeToString()
        sd.chain_id = chain_id
        sd.account_number = account_number

        data_for_signing = sd.SerializeToString()

        signature = signer.sign(
            data_for_signing,
        )

        self._tx.signatures.extend([signature])
        return self


class CosmosClient(Logger):
    def __init__(self, module_input_data: dict):

        Logger.__init__(self)
        self.module_input_data = module_input_data
        account_name, evm_private_key, mnemonic, solana_private_key, network, proxy = self.module_input_data.values()

        self.network = network
        self.eip1559_support = network.eip1559_support
        self.token = network.token
        self.explorer = network.explorer
        self.chain_id = network.chain_id
        self.network_prefix = network.name.lower()

        self.session = ClientSession(
            connector=ProxyConnector.from_url(f"http://{proxy}", verify_ssl=False)
            if proxy else TCPConnector(verify_ssl=False)
        )

        self.proxy_init = proxy

        self.network_config = NetworkConfig(
            chain_id=f"{self.chain_id}",
            url=f"grpc+{random.choice(network.rpc)}",
            fee_minimum_gas_price=0.01 if self.network.name != 'Injective' else 10 ** 9,
            fee_denomination=network.token,
            staking_denomination=network.token,
        )

        self.request_kwargs = {"proxy": f"http://{proxy}"} if proxy else {}
        self.rpc = random.choice(network.rpc)

        if self.network.name == 'Injective':
            self.network_prefix = 'inj'

            from utils.inj_derivation import PrivateKey

            self.cosmos_private_key = PrivateKey.from_mnemonic(mnemonic)
            cosmos_public_key = self.cosmos_private_key.to_public_key()
            cosmos_pre_address = cosmos_public_key.to_address()
            self.address = Address(cosmos_pre_address.to_acc_bech32(), prefix=self.network_prefix)

            from cosmpy.crypto.keypairs import PrivateKey
            final_private_kep = PrivateKey(bytes.fromhex(self.cosmos_private_key.to_hex()))

            class CustomLocalWallet(LocalWallet):
                def address(self) -> Address:
                    return Address(cosmos_pre_address.to_acc_bech32(), prefix='inj')

            from cosmpy.protos.cosmos.auth.v1beta1.query_pb2 import QueryAccountRequest
            from cosmpy.protos.cosmos.auth.v1beta1.auth_pb2 import BaseAccount

            class CustomLedgerClient(LedgerClient):
                def query_account(self, address: Address) -> Account:
                    """Query account.

                    :param address: address
                    :raises RuntimeError: Unexpected account type returned from query
                    :return: account details
                    """
                    request = QueryAccountRequest(address=str(address))
                    response = self.auth.Account(request)
                    account = BaseAccount()
                    response.account.Unpack(account)

                    return Account(
                        address=address,
                        number=account.account_number,
                        sequence=account.sequence,
                    )

            self.wallet = CustomLocalWallet(final_private_kep, prefix=self.network_prefix)
            self.account = CustomLedgerClient(self.network_config)
        else:
            self.wallet = LocalWallet.from_mnemonic(mnemonic, self.network_prefix)
            self.public_key = self.wallet.public_key()
            self.cosmos_private_key = self.wallet.signer()
            self.address = Address(self.public_key, prefix=self.network_prefix)
            self.account = LedgerClient(self.network_config)

        self.account_name = str(account_name)
        self.cosmos_mnemonic = mnemonic
        self.solana_private_key = solana_private_key
        self.private_key = evm_private_key
        self.evm_address = AsyncWeb3.to_checksum_address(AsyncWeb3().eth.account.from_key(evm_private_key).address)
        self.acc_info = account_name, self.address, self.network.name

    async def get_balance(self):
        print(self.address)

    @staticmethod
    def custom_round(number: int | float | list | tuple, decimals: int = 6) -> float:
        if isinstance(number, (list, tuple)):
            number = random.uniform(*number)
        number = float(number)
        str_number = f"{number:.18f}".split('.')
        if len(str_number) != 2:
            return round(number, 6)
        str_number_to_round = str_number[1]
        rounded_number = str_number_to_round[:decimals]
        final_number = float('.'.join([str_number[0], rounded_number]))
        return final_number

    async def simulate_transfer(self, **_) -> float:
        gas_limit = random.randint(150000, 160000)
        return math.ceil(gas_limit * self.network_config.fee_minimum_gas_price)

    @staticmethod
    def get_normalize_error(error: Exception) -> Exception | str:
        try:
            if isinstance(error.args[0], dict):
                error = error.args[0].get('message', error)
            return error
        except:
            return error

    @staticmethod
    async def change_rpc():
        return True

    async def change_proxy(self, without_logs: bool = False):
        from config.constants import PROXIES
        if not without_logs:
            self.logger_msg(
                self.account_name,
                None, msg=f'Trying to replace old proxy: {self.proxy_init}', type_msg='warning'
            )

        if len(PROXIES) != 0:
            new_proxy = random.choice(PROXIES)

            await self.session.close()
            self.proxy_init = new_proxy
            self.session = ClientSession(
                connector=ProxyConnector.from_url(f"http://{new_proxy}", verify_ssl=False)
                if new_proxy else TCPConnector(verify_ssl=False)
            )
            if not without_logs:
                self.logger_msg(
                    self.account_name, None,
                    msg=f'Proxy successfully replaced. New Proxy: {new_proxy}', type_msg='success'
                )
        else:
            if not without_logs:
                self.logger_msg(
                    self.account_name, None,
                    msg=f'This network has only 1 Proxy, no replacement is possible', type_msg='warning'
                )

    @staticmethod
    def to_wei(number: int | float | str, decimals: int = 18) -> int:

        unit_name = {
            18: 'ether',
            6: 'mwei'
        }[decimals]

        return AsyncWeb3().to_wei(number=number, unit=unit_name)

    async def get_smart_amount(
            self, settings: tuple, need_percent: bool = False, token_name: str = None, fee_support: float = None,
            without_limiter: bool = False
    ) -> float:
        await asyncio.sleep(2)

        if not token_name:
            token_name = self.token

        if isinstance(settings[0], str) or need_percent:
            _, amount, _ = await self.get_token_balance(token_name)
            percent = round(random.uniform(float(settings[0]), float(settings[1])), 6) / 100

            if fee_support:
                amount -= fee_support
            amount = self.custom_round(amount * percent, 6)

        else:
            amount = self.custom_round(settings)

        if token_name == self.token and not without_limiter:
            from dev_settings import Settings

            _, amount_balance, _ = await self.get_token_balance(token_name)

            global_limiter = random.uniform(*Settings.GLOBAL_LIMITER.get(self.network.name, (0, 0)))

            if amount > global_limiter:
                if amount_balance - amount < global_limiter:
                    final_amount = amount_balance - amount
                    hold_amount = global_limiter - final_amount
                    amount = round((amount - hold_amount), 6)

        return amount

    async def stake_tia(self, validator, amount):
        from cosmpy.protos.cosmos.staking.v1beta1.tx_pb2 import MsgDelegate
        from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin

        gas_limit = random.randint(170000, 180000)
        gas_fee = math.ceil(gas_limit * self.network_config.fee_minimum_gas_price)
        amount_in_wei = int(amount * 10 ** await self.get_decimals('TIA'))
        denom = 'utia'

        msg = MsgDelegate(
            delegator_address=str(self.address),
            validator_address=str(validator),
            amount=Coin(amount=str(amount_in_wei), denom=denom)
        )

        return await self.send_transaction(msg=msg, gas_fee=gas_fee, gas_limit=gas_limit)

    async def send_tokens(
            self, address: str = None, amount: float = None, ccy: str = None, without_fee_support: bool = False
    ):
        from cosmpy.protos.cosmos.bank.v1beta1.tx_pb2 import MsgSend
        from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin

        if not ccy:
            ccy = {
                'Celestia': 'TIA',
                'Neutron': 'NTRN',
                'Injective': 'INJ'
            }[self.network.name]

        gas_limit = random.randint(140000, 150000)
        gas_fee = math.ceil(gas_limit * self.network_config.fee_minimum_gas_price)
        decimals = await self.get_decimals(ccy)
        if not without_fee_support:
            amount = round(amount - float(gas_fee / 10 ** decimals), 6)
        amount_in_wei = int(amount * 10 ** await self.get_decimals(ccy))

        token_demon = {
            'TIA': 'utia',
            'NTRN': 'untrn',
            'INJ': 'inj',
        }[ccy]

        msg = MsgSend(
            from_address=str(self.address),
            to_address=str(address),
            amount=[Coin(amount=str(amount_in_wei), denom=token_demon)],
        )

        return await self.send_transaction(msg=msg, gas_fee=gas_fee, gas_limit=gas_limit)

    @network_handler
    async def get_token_balance(
            self, token_name: str = None, denom: str = None, **_
    ) -> [float, int, str]:

        if token_name == self.token or not token_name:
            token_demon = self.token
        else:
            token_demon = {
                'TIA.n': 'utia',
                'TIA': 'utia',
                'NTRN': 'untrn',
                'INJ': 'inj',
            }[token_name]

        token_decimals = {
            'utia': 6,
            'untrn': 6,
            'inj': 18,
        }[token_demon]

        if token_demon == 'utia' and self.network.name == 'Neutron':
            denom = 'ibc/773B4D0A3CD667B2275D5A4A7A2F0909C0BA0F4059C0B9181E680DDF4965DCC7'

        balance_data = None
        balances = self.account.query_bank_all_balances(self.address)

        if balances:
            for token_balance in balances:
                if token_balance.denom == token_demon or denom == token_balance.denom:
                    amount_in_wei = int(token_balance.amount)
                    amount = round(amount_in_wei / 10 ** token_decimals, 6)
                    balance_data = amount_in_wei, amount, token_name

        if balance_data:
            return balance_data
        return 0, 0, token_name

    def get_contract(self, contract_address) -> LedgerContract:
        return LedgerContract(
            path=None, client=self.account, address=contract_address
        )

    async def new_client(self, chain_name: str):
        from functions import get_rpc_by_chain_name
        from modules import SolanaClient, Client

        self.module_input_data['network'] = get_rpc_by_chain_name(chain_name)

        if chain_name in ['Injective', 'Neutron', 'Celestia']:
            return CosmosClient(self.module_input_data)
        elif chain_name in ['Solana']:
            return SolanaClient(self.module_input_data)
        return Client(self.module_input_data)

    @staticmethod
    async def get_decimals(token_name: str = None, **_) -> int:
        return {
            'TIA.n': 6,
            'TIA': 6,
            'NTRN': 6,
            'INJ': 18,
        }[token_name]

    async def wait_for_receiving(
            self, chain_to_name: str, old_balance_data: tuple = None, token_name: str = None,
            sleep_time: int = 60, check_balance_on_dst: bool = False, **_
    ) -> bool | tuple:
        client = await self.new_client(chain_to_name)

        if not token_name:
            token_name = self.token
        try:
            while True:
                try:
                    if check_balance_on_dst:
                        old_balance_in_wei, old_balance, _ = await client.get_token_balance(token_name)

                        return old_balance_in_wei, old_balance

                    old_balance_in_wei, old_balance = old_balance_data

                    client.logger_msg(*client.acc_info, msg=f'Waiting {token_name} to receive')

                    while True:
                        new_balance_in_wei, new_balance, _ = await client.get_token_balance(token_name)

                        if new_balance_in_wei > old_balance_in_wei:
                            received_amount = client.custom_round(new_balance - old_balance, 6)
                            client.logger_msg(
                                *client.acc_info,
                                msg=f'{received_amount} {token_name} was received on {client.network.name}',
                                type_msg='success'
                            )
                            return True
                        else:
                            client.logger_msg(
                                *client.acc_info, msg=f'Still waiting {token_name} to receive...', type_msg='warning'
                            )
                            await asyncio.sleep(sleep_time)

                except Exception as error:
                    import traceback
                    traceback.print_exc()
                    self.logger_msg(
                        *self.acc_info, msg=f'Bad response from RPC, will try again in 1 min. Error: {error}',
                        type_msg='warning'
                    )
                    await asyncio.sleep(60)
                    await client.change_rpc()
        finally:
            if not client.session.closed:
                await client.session.close()

    async def send_transaction(
            self, msg=None, gas_fee: int = None, gas_limit: int = None, timeout: int = 360,
    ) -> bool | HexStr:

        try:
            if self.network.name == 'Injective':
                raw_tx = CustomTransaction()
            else:
                raw_tx = Transaction()

            raw_tx.add_message(msg)

            gas_fee_total = f"{gas_fee}{self.network.token}"

            await asyncio.sleep(5)

            account_info = self.account.query_account(self.address)

            account_number = account_info.number
            account_sequence = account_info.sequence

            while True:
                await asyncio.sleep(5)
                try:
                    signing_cfg = SigningCfg.direct(
                        public_key=self.wallet.public_key(), sequence_num=account_sequence
                    )
                    sealed_tx = raw_tx.seal(signing_cfgs=signing_cfg, fee=gas_fee_total, gas_limit=gas_limit)

                    await asyncio.sleep(5)

                    if self.network.name == 'Injective':
                        sealed_tx._tx.auth_info.signer_infos[
                            0].public_key.type_url = '/injective.crypto.v1beta1.ethsecp256k1.PubKey'
                        sign_tx = sealed_tx.sign(self.cosmos_private_key, self.chain_id, account_number)
                    else:
                        sign_tx = sealed_tx.sign(self.wallet.signer(), self.chain_id, account_number)

                    await asyncio.sleep(5)

                    completed_tx = sign_tx.complete()
                    submitted_tx = self.account.broadcast_tx(completed_tx)
                    break
                except Exception as error:
                    if 'account sequence mismatch' in str(error):
                        account_sequence = int(str(error)[36:-35].replace(',', ''))
                    elif 'signature verification failed' in str(error):
                        account_number = int(str(error)[61:-86].replace(',', ''))
                    elif 'header with status: 429' in str(error) or 'status = StatusCode.UNAVAILABLE' in str(error):
                        message = f'RPC got rate limit, trying again in 1 min...'
                        self.logger_msg(*self.acc_info, msg=message, type_msg='warning')
                        await asyncio.sleep(60)
                    elif 'pool reached max tx capacity' in str(error):
                        message = f'Pool reached max tx capacity, trying again in 1 min...'
                        self.logger_msg(*self.acc_info, msg=message, type_msg='warning')
                        await asyncio.sleep(10)
                    else:
                        raise error

            await asyncio.sleep(10)

            while True:
                try:
                    submitted_tx.wait_to_complete(timeout=timeout, poll_period=5)
                    break
                except QueryTimeoutError:
                    await asyncio.sleep(5)
                    raise SoftwareException('Transaction not in chain after 360 second')

            tx_subdomain = {
                'Celestia': 'tx',
                'Neutron': 'txs',
                'Injective': 'transaction',
            }[self.network.name]

            message = f'Transaction was successful: {self.explorer}{tx_subdomain}/{submitted_tx.tx_hash}'
            self.logger_msg(*self.acc_info, msg=message, type_msg='success')
        except Exception as error:
            if "transaction indexing is disabled" in str(error):
                message = f'Transaction was send, but node get autism response'
                self.logger_msg(*self.acc_info, msg=message, type_msg='warning')
            else:
                raise error

        return True
