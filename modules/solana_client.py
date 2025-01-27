import json
import httpx
import random
import asyncio

from aiohttp_socks import ProxyConnector
from aiohttp import ClientSession, TCPConnector
from web3 import AsyncWeb3
from eth_typing import HexStr
from nacl.encoding import RawEncoder
from nacl.signing import SigningKey
from config.constants import TOKENS_PER_CHAIN
from modules.interfaces import SoftwareException
from modules import Logger, RequestClient
from typing import Optional, Dict, List
from solana.rpc.types import TxOpts
from solana.transaction import Transaction
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solana.rpc.providers.core import DEFAULT_TIMEOUT
from solana.rpc.providers.async_http import AsyncHTTPProvider
from solders.keypair import Keypair
from solders.instruction import Instruction
from solders.message import to_bytes_versioned, MessageV0, MessageAddressTableLookup
from solders.transaction import VersionedTransaction

from utils.tools import network_handler


class CustomAsyncHTTPProvider(AsyncHTTPProvider):
    def __init__(
            self,
            endpoint=None,
            extra_headers=None,
            timeout: float = DEFAULT_TIMEOUT,
            proxies: Optional[Dict[str, str]] = None,
    ):
        super().__init__(endpoint=endpoint, extra_headers=extra_headers)
        self.session = httpx.AsyncClient(timeout=timeout, proxies=proxies)


class CustomAsyncClient(AsyncClient):
    def __init__(
            self,
            endpoint: Optional[str] = None,
            commitment: Optional[Commitment] = None,
            timeout: float = 10,
            extra_headers: Optional[Dict[str, str]] = None,
            proxies: Optional[Dict[str, str]] = None,
    ):
        super().__init__(commitment=commitment)
        self._provider = CustomAsyncHTTPProvider(
            endpoint, timeout=timeout, extra_headers=extra_headers, proxies=proxies
        )


class SolanaClient(Logger, RequestClient):
    def __init__(self, module_input_data: dict):

        self.module_input_data = module_input_data
        account_name, evm_private_key, mnemonic, solana_private_key, network, proxy = self.module_input_data.values()

        Logger.__init__(self)
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
        self.wallet: Keypair = Keypair.from_base58_string(solana_private_key)
        self.solana_client = CustomAsyncClient(endpoint=random.choice(network.rpc), proxies={
            "http://": f"http://{proxy}",
            "https://": f"http://{proxy}"
        } if proxy else None)

        self.address = self.wallet.pubkey()
        self.account_name = str(account_name)
        self.cosmos_mnemonic = mnemonic
        self.solana_private_key = solana_private_key
        self.private_key = evm_private_key
        self.evm_address = AsyncWeb3.to_checksum_address(AsyncWeb3().eth.account.from_key(evm_private_key).address)
        self.acc_info = account_name, self.address, self.network.name

    async def sign_message(self, message: str):
        signing_key = SigningKey(self.wallet.secret())
        signed_message = signing_key.sign(message.encode())
        return f"0x{signed_message.signature.hex()}"

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

    @staticmethod
    async def simulate_transfer(self, **_) -> float:
        return 0

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

    @staticmethod
    def to_wei(number: int | float | str, decimals: int = 9) -> int:
        return int(number * 10 ** decimals)

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

    @network_handler
    async def get_token_balance(
            self, token_name: str = None, check_native: bool = False, **_
    ) -> [int, float, str]:
        if not token_name:
            token_name = self.token

        await asyncio.sleep(3)
        if not check_native:
            if token_name != self.network.token:
                token_address = TOKENS_PER_CHAIN['Solana'][token_name]

                headers = {"accept": "application/json", "content-type": "application/json"}

                payload = {
                    "id": 1,
                    "jsonrpc": "2.0",
                    "method": "getTokenAccountsByOwner",
                    "params": [
                        f"{self.wallet.pubkey()}",
                        {
                            "mint": token_address
                        },
                        {
                            "encoding": "jsonParsed"
                        },
                    ],
                }

                response = (await self.session.post(url=self.network.rpc[0], json=payload, headers=headers))

                json_data = await response.json()

                if json_data['result'].get('value'):
                    data = (await response.json())['result']['value'][0]['account']['data']['parsed']['info']['tokenAmount']
                else:
                    return 0, 0, token_name

                amount_in_wei = int(data['amount'])
                amount = float(data['uiAmount'])

                return amount_in_wei, amount, token_name

        amount_in_wei = (await self.solana_client.get_balance(self.address)).value
        return amount_in_wei, amount_in_wei / 10 ** 9, self.network.token

    def get_contract(self, contract_address):
        pass

    async def new_client(self, chain_name: str):
        from functions import get_rpc_by_chain_name
        from modules import CosmosClient, Client

        self.module_input_data['network'] = get_rpc_by_chain_name(chain_name)

        if chain_name in ['Injective', 'Neutron', 'Celestia']:
            return CosmosClient(self.module_input_data)
        elif chain_name in ['Solana']:
            return SolanaClient(self.module_input_data)
        return Client(self.module_input_data)

    @staticmethod
    async def get_decimals(token_name: str = None, **_) -> int:
        return {
            'SOL': 9,
            'ZBC': 9,
            'USDC': 6,
            'USDT': 6,
        }[token_name]

    async def wait_for_receiving(
            self, chain_to_name: str, old_balance_data: tuple = None, token_name: str = None,
            token_address: str = None, sleep_time: int = 60,
            check_balance_on_dst: bool = False
    ) -> bool | tuple:
        client = await self.new_client(chain_to_name)

        if not token_name:
            token_name = self.token
        try:
            while True:
                try:
                    if check_balance_on_dst:
                        old_balance_in_wei, old_balance, _ = await client.get_token_balance(
                            token_name, token_address, check_symbol=False
                        )

                        return old_balance_in_wei, old_balance

                    old_balance_in_wei, old_balance = old_balance_data

                    client.logger_msg(*client.acc_info, msg=f'Waiting {token_name} to receive')

                    while True:
                        new_balance_in_wei, new_balance, _ = await client.get_token_balance(
                            token_name, token_address, check_symbol=False
                        )

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

    @staticmethod
    async def sign_ed25519(message_data, secret_key):
        signing_key = SigningKey(secret_key[:32], encoder=RawEncoder)
        return signing_key.sign(message_data).signature

    async def sign_transaction(self, tx: Transaction | VersionedTransaction, signers: list[Keypair]) -> bytes:
        blockhash_with_expiry_block_height = await self.solana_client.get_latest_blockhash(
            commitment=Commitment('finalized')
        )

        blockhash = blockhash_with_expiry_block_height.value.blockhash

        tx.recent_blockhash = blockhash
        tx.sign(*signers)

        return tx.serialize(verify_signatures=True)

    async def create_v0_message(self, raw_tx_bytes):
        blockhash_with_expiry_block_height = await self.solana_client.get_latest_blockhash()
        blockhash = blockhash_with_expiry_block_height.value.blockhash

        raw_tx = VersionedTransaction.from_bytes(raw_tx_bytes)
        json_tx = json.loads(raw_tx.to_json())

        message_address_table_lookups = []
        for addressTableLookup in json_tx['message'][1]['addressTableLookups'][1:]:
            message_address_table_lookups.append(
                MessageAddressTableLookup.from_json(json.dumps(addressTableLookup))
            )

        return MessageV0(
            account_keys=raw_tx.message.account_keys,
            recent_blockhash=blockhash,
            instructions=raw_tx.message.instructions,
            header=raw_tx.message.header,
            address_table_lookups=message_address_table_lookups
        )

    async def send_transaction(
            self, message: MessageV0 = None, instructions: list[Instruction] | dict = None,
            signers: list[Keypair] = None, raw_mode: bool = False, gas_limit: int = None,
            funds: str = False, timeout: int = 360,
    ) -> bool | HexStr:

        try:
            if message:
                signature_for_sign = self.wallet.sign_message(to_bytes_versioned(message))
                signed_tx = VersionedTransaction.populate(message, [signature_for_sign])
            else:
                ixs: List[Instruction] = []
                if instructions:
                    for instruction in instructions:
                        ixs.append(instruction)

                unsigned_tx = Transaction(instructions=ixs)
                signed_tx = await self.sign_transaction(tx=unsigned_tx, signers=signers)

            if raw_mode:
                signature_response = await self.solana_client.send_raw_transaction(signed_tx, opts=TxOpts(
                    skip_preflight=False
                ))
            else:
                if signers:
                    signature_response = await self.solana_client.send_transaction(
                        signed_tx, *signers, opts=TxOpts(skip_preflight=False)
                    )
                else:
                    signature_response = await self.solana_client.send_transaction(
                        signed_tx, opts=TxOpts(skip_preflight=False)
                    )
        except Exception as error:
            if 'SendTransactionPreflightFailureMessage' in str(error):
                self.logger_msg(
                    *self.acc_info, msg=f'PreFlight tx is failure, try again', type_msg='warning'
                )
                raise SoftwareException(f'Exception for retry')
            else:
                raise SoftwareException(f'Bad response from RPC:{error}')

        signature = signature_response.value

        try:
            await self.solana_client.confirm_transaction(tx_sig=signature, commitment=Commitment('finalized'))
        except Exception as error:
            if 'Unable to confirm transaction' in str(error):
                self.logger_msg(
                    *self.acc_info, msg=f'Validators do not take your tx', type_msg='warning'
                )
                raise SoftwareException(f'Exception for retry')
            else:
                raise error

        message = f'Transaction was successful: {self.explorer}tx/{signature}'
        self.logger_msg(*self.acc_info, msg=message, type_msg='success')

        return True
