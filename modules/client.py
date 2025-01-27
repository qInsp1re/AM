import asyncio
import random

from asyncio import sleep

from aiohttp import ClientSession, TCPConnector
from aiohttp_socks import ProxyConnector
from eth_account.messages import encode_defunct
from eth_typing import HexStr
from web3.contract import AsyncContract
from web3.exceptions import TransactionNotFound
from modules import Logger, RequestClient
from config.constants import CHAIN_IDS, TOKENS_PER_CHAIN, TOKENS_FOR_SWAPS
from config.abi import ERC20_ABI
from web3 import AsyncHTTPProvider, AsyncWeb3
from config.constants import RHINO_CHAIN_INFO, ORBITER_CHAINS_INFO, LAYERSWAP_CHAIN_NAME
from general_settings import (
    GAS_LIMIT_MULTIPLIER,
    GAS_PRICE_MULTIPLIER, UNLIMITED_APPROVE, SLIPPAGE,
)
from modules.interfaces import PriceImpactException, BlockchainException, SoftwareException

from dev_settings import Settings
from utils.tools import network_handler


class Client(Logger, RequestClient):
    def __init__(self, module_input_data: dict):
        Logger.__init__(self)

        self.module_input_data = module_input_data
        account_name, evm_private_key, mnemonic, solana_private_key, network, proxy = self.module_input_data.values()

        self.network = network
        self.eip1559_support = network.eip1559_support
        self.token = network.token
        self.explorer = network.explorer
        self.chain_id = network.chain_id

        self.proxy_init = proxy
        self.session = ClientSession(
            connector=ProxyConnector.from_url(f"http://{proxy}", ssl=False)
            if proxy else TCPConnector(ssl=False)
        )
        self.request_kwargs = {"proxy": f"http://{proxy}", "verify_ssl": False} if proxy else {"verify_ssl": False}
        self.rpc = random.choice(network.rpc)
        self.w3 = AsyncWeb3(AsyncHTTPProvider(self.rpc, request_kwargs=self.request_kwargs))
        self.account_name = str(account_name)
        self.private_key = evm_private_key
        self.cosmos_mnemonic = mnemonic
        self.solana_private_key = solana_private_key
        self.address = AsyncWeb3.to_checksum_address(self.w3.eth.account.from_key(evm_private_key).address)
        self.acc_info = account_name, self.address, self.network.name

    async def handling_rpc_errors(self, error):
        if 'insufficient funds' in str(error) or 'gas required exceeds' in str(error):
            self.logger_msg(
                *self.acc_info, msg=f'Not enough native for send tx, will stop module',
                type_msg='warning'
            )
            return True
        else:
            raise BlockchainException(error)

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
    def get_normalize_error(error: Exception) -> Exception | str:
        try:
            if isinstance(error.args[0], dict):
                error = error.args[0].get('message', error)
            return error
        except:
            return error

    async def change_rpc(self, without_logs: bool = False):
        if not without_logs:
            self.logger_msg(
                self.account_name, None, msg=f'Trying to replace RPC', type_msg='warning'
            )

        if len(self.network.rpc) != 1:
            rpcs_list = [rpc for rpc in self.network.rpc if rpc != self.rpc]
            new_rpc = random.choice(rpcs_list)
            self.rpc = new_rpc
            self.w3 = AsyncWeb3(AsyncHTTPProvider(new_rpc, request_kwargs=self.request_kwargs))
            if not without_logs:
                self.logger_msg(
                    self.account_name, None,
                    msg=f'RPC successfully replaced. New RPC: {new_rpc}', type_msg='success'
                )
        else:
            if not without_logs:
                self.logger_msg(
                    self.account_name, None,
                    msg=f'This network has only 1 RPC, no replacement is possible', type_msg='warning'
                )

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
            self.request_kwargs = {
                "proxy": f"http://{new_proxy}", "verify_ssl": False
            } if new_proxy else {"verify_ssl": False}

            self.w3 = AsyncWeb3(AsyncHTTPProvider(self.rpc, request_kwargs=self.request_kwargs))

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

    def to_wei(self, number: int | float | str, decimals: int = 18) -> int:

        unit_name = {
            18: 'ether',
            9: 'gwei',
            6: 'mwei'
        }[decimals]

        return self.w3.to_wei(number=number, unit=unit_name)

    async def simulate_transfer(self, token_name: str) -> float:
        if token_name != self.token:
            token_contract = self.get_contract(TOKENS_PER_CHAIN[self.network.name][token_name])

            transaction = await token_contract.functions.transfer(
                self.address,
                1
            ).build_transaction(await self.prepare_transaction())
        else:
            transaction = (await self.prepare_transaction(value=1)) | {
                'to': self.address,
                'data': '0x'
            }
        gas_price = await self.w3.eth.gas_price

        return float((await self.w3.eth.estimate_gas(transaction)) * GAS_LIMIT_MULTIPLIER * gas_price / 10 ** 18 * 1.2)

    async def get_decimals(self, token_name: str = None, token_address: str = None) -> int:
        if token_name != self.token:
            contract_address = token_address if token_address else TOKENS_PER_CHAIN[self.network.name][token_name]
            contract = self.get_contract(contract_address)
            return await contract.functions.decimals().call()
        return 18

    async def get_normalize_amount(self, token_name: str, amount_in_wei: int) -> float:
        decimals = await self.get_decimals(token_name)
        return float(amount_in_wei / 10 ** decimals)

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

    async def price_impact_defender(
            self, from_token_name: str, from_token_amount: float, to_token_name: str, to_token_amount_in_wei: int
    ):

        to_token_amount_in_wei = int(to_token_amount_in_wei * (1 + SLIPPAGE / 100))
        to_token_amount = await self.get_normalize_amount(to_token_name, to_token_amount_in_wei)

        amount1_in_usd = (await self.get_token_price(from_token_name)) * from_token_amount
        amount2_in_usd = (await self.get_token_price(to_token_name)) * to_token_amount
        dex_slippage = 100 - (amount2_in_usd / amount1_in_usd) * 100

        if dex_slippage > SLIPPAGE:
            raise PriceImpactException(
                f'DEX slippage > your wanted slippage | DEX slippage: {dex_slippage:.3}% > 5%'
            )

    async def get_bridge_data(self, chain_from_name: int, dapp_id: int, settings_id: int):
        bridge_config = {
            1: CHAIN_IDS,
            2: CHAIN_IDS,
            3: LAYERSWAP_CHAIN_NAME,
            4: CHAIN_IDS,
            5: ORBITER_CHAINS_INFO,
            6: CHAIN_IDS,
            7: CHAIN_IDS,
            8: RHINO_CHAIN_INFO,
            9: CHAIN_IDS,
            10: CHAIN_IDS,
            11: CHAIN_IDS,
        }[dapp_id]

        chain_to_names, bridge_setting, bridge_token = {
            1: (Settings.ACROSS_CHAIN_TO_NAMES, Settings.ACROSS_BRIDGE_AMOUNT, Settings.ACROSS_TOKEN_NAME),
            2: (Settings.BUNGEE_CHAIN_TO_NAMES, Settings.BUNGEE_BRIDGE_AMOUNT, Settings.BUNGEE_TOKEN_NAME),
            3: (Settings.LAYERSWAP_CHAIN_TO_NAMES, Settings.LAYERSWAP_BRIDGE_AMOUNT, Settings.LAYERSWAP_TOKEN_NAME),
            4: (Settings.NITRO_CHAIN_TO_NAMES, Settings.NITRO_BRIDGE_AMOUNT, Settings.NITRO_TOKEN_NAME),
            5: (Settings.ORBITER_CHAIN_TO_NAMES, Settings.ORBITER_BRIDGE_AMOUNT, Settings.ORBITER_TOKEN_NAME),
            6: (Settings.OWLTO_CHAIN_TO_NAMES, Settings.OWLTO_BRIDGE_AMOUNT, Settings.OWLTO_TOKEN_NAME),
            7: (Settings.RELAY_CHAIN_TO_NAMES, Settings.RELAY_BRIDGE_AMOUNT, Settings.RELAY_TOKEN_NAME),
            8: (Settings.RHINO_CHAIN_TO_NAMES, Settings.RHINO_BRIDGE_AMOUNT, Settings.RHINO_TOKEN_NAME),
            9: (Settings.NATIVE_CHAIN_TO_NAMES, Settings.NATIVE_BRIDGE_AMOUNT, Settings.NATIVE_TOKEN_NAME),
            10: (Settings.RANGO_CHAIN_TO_NAMES, Settings.RANGO_BRIDGE_AMOUNT, Settings.RANGO_TOKEN_NAME),
            11: (Settings.XYFINANCE_CHAIN_TO_NAMES, Settings.XYFINANCE_BRIDGE_AMOUNT, Settings.XYFINANCE_TOKEN_NAME),
        }[settings_id]

        bridge_cfg_from_name = bridge_config[chain_from_name]
        chain_to_name = random.choice([chain for chain in chain_to_names if chain != chain_from_name])
        bridge_cfg_to_name = bridge_config[chain_to_name]
        if isinstance(bridge_token, tuple):
            bridge_token = bridge_token[0]

        amount = await self.get_smart_amount(bridge_setting, token_name=bridge_token)
        return bridge_cfg_from_name, bridge_cfg_to_name, amount, chain_to_name

    async def sign_message(self, message):
        text_hex = "0x" + message.encode('utf-8').hex()
        text_encoded = encode_defunct(hexstr=text_hex)
        return self.w3.to_hex(self.w3.eth.account.sign_message(
            text_encoded, private_key=self.private_key
        ).signature)

    async def new_client(self, chain_name: str):
        from modules import CosmosClient, SolanaClient
        from functions import get_rpc_by_chain_name

        self.module_input_data['network'] = get_rpc_by_chain_name(chain_name)

        if chain_name in ['Injective', 'Neutron', 'Celestia']:
            return CosmosClient(self.module_input_data)
        elif chain_name in ['Solana']:
            return SolanaClient(self.module_input_data)
        return Client(self.module_input_data)

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
                    await client.change_rpc()
                    await client.change_proxy()
                    await asyncio.sleep(60)
        finally:
            if not client.session.closed:
                await client.session.close()

    @network_handler
    async def get_token_balance(
            self, token_name: str = None, token_address: str = None, check_symbol: bool = True,
            check_native: bool = False, without_error: bool = False, only_address: bool = False,
            swapcheck: bool = False
    ) -> [int, float, str]:
        if not token_name and not only_address:
            token_name = self.token

        if without_error and token_name not in TOKENS_PER_CHAIN[self.network.name].keys():
            return 0, 0, ''

        if not check_native:
            if token_name != self.network.token:
                if token_address:
                    contract = self.get_contract(token_address)
                elif swapcheck:
                    contract = self.get_contract(TOKENS_FOR_SWAPS[self.network.name][token_name])
                else:
                    contract = self.get_contract(TOKENS_PER_CHAIN[self.network.name][token_name])

                amount_in_wei = await contract.functions.balanceOf(self.address).call()
                decimals = await contract.functions.decimals().call()

                if check_symbol:
                    symbol = await contract.functions.symbol().call()
                    return amount_in_wei, amount_in_wei / 10 ** decimals, symbol
                return amount_in_wei, amount_in_wei / 10 ** decimals, ''

        amount_in_wei = await self.w3.eth.get_balance(self.address)
        return amount_in_wei, amount_in_wei / 10 ** 18, self.network.token

    def get_contract(self, contract_address: str, abi: dict = ERC20_ABI) -> AsyncContract:
        return self.w3.eth.contract(
            address=AsyncWeb3.to_checksum_address(contract_address),
            abi=abi
        )

    async def get_allowance(self, token_address: str, spender_address: str) -> int:
        return await self.get_contract(token_address).functions.allowance(
            self.address,
            spender_address
        ).call()

    async def get_priotiry_fee(self) -> int:
        fee_history = await self.w3.eth.fee_history(5, 'latest', [20.0])
        non_empty_block_priority_fees = [fee[0] for fee in fee_history["reward"] if fee[0] != 0]

        divisor_priority = max(len(non_empty_block_priority_fees), 1)

        priority_fee = int(round(sum(non_empty_block_priority_fees) / divisor_priority))

        return priority_fee

    async def prepare_transaction(self, value: int = 0) -> dict:
        try:
            tx_params = {
                'chainId': self.network.chain_id,
                'from': self.w3.to_checksum_address(self.address),
                'nonce': await self.w3.eth.get_transaction_count(self.address),
                'value': value,
            }

            if self.network.eip1559_support:

                base_fee = await self.w3.eth.gas_price
                max_priority_fee_per_gas = await self.get_priotiry_fee()
                max_fee_per_gas = int(base_fee * 2 + max_priority_fee_per_gas * 1.5 * GAS_PRICE_MULTIPLIER)

                if max_priority_fee_per_gas > max_fee_per_gas:
                    max_priority_fee_per_gas = int(max_fee_per_gas * 0.95)

                if self.network.name in ['Scroll']:
                    max_fee_per_gas = int(max_fee_per_gas * random.uniform(2, 2.2))
                    max_priority_fee_per_gas = int(max_fee_per_gas * random.uniform(0.8, 0.9))

                tx_params['maxPriorityFeePerGas'] = max_priority_fee_per_gas
                tx_params['maxFeePerGas'] = max_fee_per_gas
                tx_params['type'] = '0x2'
            else:
                if self.network.name == 'BNB Chain':
                    tx_params['gasPrice'] = self.w3.to_wei(round(random.uniform(1.4, 1.5), 1), 'gwei')
                else:
                    gas_price = await self.w3.eth.gas_price
                    if self.network.name in ['Nautilus', 'Scroll']:
                        gas_price = int(gas_price * 3)

                    tx_params['gasPrice'] = int(gas_price * 1.25 * GAS_PRICE_MULTIPLIER)

            return tx_params
        except Exception as error:
            raise BlockchainException(f'{self.get_normalize_error(error)}')

    async def make_approve(
            self, token_address: str, spender_address: str, amount_in_wei: int, unlimited_approve: bool
    ) -> bool:
        transaction = await self.get_contract(token_address).functions.approve(
            spender_address,
            amount=2 ** 256 - 1 if unlimited_approve else amount_in_wei
        ).build_transaction(await self.prepare_transaction())

        return await self.send_transaction(transaction)

    async def check_for_approved(
            self, token_address: str, spender_address: str, amount_in_wei: int, without_bal_check: bool = False,
            unlimited_approve: bool = UNLIMITED_APPROVE
    ) -> bool:
        try:
            contract = self.get_contract(token_address)

            balance_in_wei = await contract.functions.balanceOf(self.address).call()
            symbol = await contract.functions.symbol().call()

            self.logger_msg(*self.acc_info, msg=f'Check for approval {symbol}')

            if not without_bal_check and balance_in_wei <= 0:
                raise SoftwareException(f'Zero {symbol} balance')

            approved_amount_in_wei = await self.get_allowance(
                token_address=token_address,
                spender_address=spender_address
            )

            if amount_in_wei <= approved_amount_in_wei:
                self.logger_msg(*self.acc_info, msg=f'Already approved')
                return False

            result = await self.make_approve(token_address, spender_address, amount_in_wei, unlimited_approve)

            await sleep(random.randint(5, 9))
            return result
        except Exception as error:
            raise BlockchainException(f'{self.get_normalize_error(error)}')

    async def send_transaction(
            self, transaction=None, need_hash: bool = False, without_gas: bool = False, poll_latency: int = 10,
            timeout: int = 360, tx_hash=None, send_mode: bool = False, signed_tx=None
    ) -> bool | HexStr:

        if self.network.name == 'Nautilus':
            timeout = 720
        elif self.network.name == 'Scroll':
            timeout = 30

        try:
            if not without_gas and not tx_hash and not send_mode:
                transaction['gas'] = int((await self.w3.eth.estimate_gas(transaction)) * GAS_LIMIT_MULTIPLIER)
        except Exception as error:
            raise BlockchainException(f'{self.get_normalize_error(error)}')

        if not tx_hash:
            try:
                if not send_mode:
                    signed_tx = self.w3.eth.account.sign_transaction(transaction, self.private_key).raw_transaction
                tx_hash = self.w3.to_hex(await self.w3.eth.send_raw_transaction(signed_tx))
            except Exception as error:
                if isinstance(error, asyncio.TimeoutError) or 'replacement transaction underpriced' in str(error):
                    self.logger_msg(
                        *self.acc_info,
                        msg='RPC got network error, but tx maybe was send, will sleep 10 min and continue route',
                        type_msg='warning'
                    )
                    await asyncio.sleep(600)
                    return True
                if self.get_normalize_error(error) == 'already known':
                    self.logger_msg(*self.acc_info, msg='RPC got error, but tx was send', type_msg='warning')
                    return True
                else:
                    raise BlockchainException(f'{self.get_normalize_error(error)}')

        total_time = 0
        while True:
            try:
                receipts = await self.w3.eth.get_transaction_receipt(tx_hash)
                status = receipts.get("status")
                if status == 1:
                    message = f'Transaction was successful: {self.explorer}tx/{tx_hash}'
                    self.logger_msg(*self.acc_info, msg=message, type_msg='success')
                    if need_hash:
                        return tx_hash
                    return True
                elif status is None:
                    await asyncio.sleep(poll_latency)
                else:
                    raise BlockchainException(f'Transaction failed: {self.explorer}tx/{tx_hash}')
            except TransactionNotFound:
                if total_time >= timeout:
                    if self.network.name == 'Nautilus':
                        message = f'Blockchain got autism, will wait 10 min to try again...'
                        self.logger_msg(*self.acc_info, msg=message, type_msg='success')
                        await asyncio.sleep(600)
                    raise BlockchainException(f"Transaction is not in the chain after {timeout} seconds")
                total_time += poll_latency
                await asyncio.sleep(poll_latency)

            except Exception as error:
                if 'Transaction failed' in str(error):
                    raise BlockchainException(f'Transaction failed: {self.explorer}tx/{tx_hash}')
                self.logger_msg(*self.acc_info, msg=f'RPC got autims response. Error: {error}', type_msg='warning')
                total_time += poll_latency
                await asyncio.sleep(poll_latency)

    async def wait_for_l0_received(self, tx_hash: HexStr, need_wait: bool = False) -> bool:
        if not Settings.WAIT_FOR_RECEIPT_L0 and not need_wait:
            return True

        await asyncio.sleep(10)
        url = f"https://api-mainnet.layerzero-scan.com/tx/{tx_hash}"

        while True:
            try:
                async with self.session.get(url=url) as response:
                    result = await response.json()

                    if (len(result["messages"]) > 0 and "dstTxHash" in result["messages"][0]
                            and "status" in result["messages"][0] and result["messages"][0]["status"] == "DELIVERED"):
                        self.logger_msg(
                            *self.acc_info, msg=f'Funds were received on destination chain', type_msg='success'
                        )
                        return True
                    elif result["messages"][0]["status"] == "BLOCKED":
                        self.logger_msg(
                            *self.acc_info, msg=f'Your tx were blocked by LayerZero Relayer', type_msg='warning')
                        return False

                self.logger_msg(
                    *self.acc_info, msg=f'Waiting for funds on destination chain...', type_msg='warning')
                await asyncio.sleep(30)

            except Exception as error:
                self.logger_msg(
                    *self.acc_info, msg=f'Can`t get info about LayerZero transaction. Error: {error}',
                    type_msg='warning'
                )
                await asyncio.sleep(10)
