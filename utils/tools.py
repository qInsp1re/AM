import io
import os
import sys
import json
import random
import asyncio
import functools
import traceback
import msoffcrypto
import pandas as pd

from pathlib import Path
from getpass import getpass
from python_socks._protocols.errors import ReplyError
from dev_settings import Settings
from utils.networks import *
from termcolor import cprint
from python_socks import ProxyError, ProxyTimeoutError, ProxyConnectionError
from asyncio.exceptions import TimeoutError
from web3 import AsyncWeb3, AsyncHTTPProvider
from aiohttp import ClientResponseError
from msoffcrypto.exceptions import DecryptionError, InvalidKeyError
from aiohttp.client_exceptions import ClientProxyConnectionError, ClientHttpProxyError, ClientError

from general_settings import (
    SLEEP_TIME_MODULES,
    SLEEP_TIME_RETRY,
    MAXIMUM_RETRY,
    MAXIMUM_GWEI,
    GAS_CONTROL,
    SLEEP_TIME_GAS,
    EXCEL_PASSWORD,
    EXCEL_PAGE_NAME, EXCEL_FILE_PATH, STOP_SOFTWARE
)


async def sleep(self, min_time=SLEEP_TIME_MODULES[0], max_time=SLEEP_TIME_MODULES[1]):
    duration = random.randint(min_time, max_time)
    print()
    self.logger_msg(*self.client.acc_info, msg=f"💤 Sleeping for {duration} seconds")
    await asyncio.sleep(duration)


def get_accounts_data():
    try:
        decrypted_data = io.BytesIO()
        with open(EXCEL_FILE_PATH, 'rb') as file:
            if EXCEL_PASSWORD:
                cprint('⚔️ Enter the password degen', color='light_blue')
                password = getpass()
                office_file = msoffcrypto.OfficeFile(file)

                try:
                    office_file.load_key(password=password)
                except msoffcrypto.exceptions.DecryptionError:
                    cprint('\n⚠️ Incorrect password to decrypt Excel file! ⚠️', color='light_red', attrs=["blink"])
                    raise DecryptionError('Incorrect password')

                try:
                    office_file.decrypt(decrypted_data)
                except msoffcrypto.exceptions.InvalidKeyError:
                    cprint('\n⚠️ Incorrect password to decrypt Excel file! ⚠️', color='light_red', attrs=["blink"])
                    raise InvalidKeyError('Incorrect password')

                except msoffcrypto.exceptions.DecryptionError:
                    cprint('\n⚠️ Set password on your Excel file first! ⚠️', color='light_red', attrs=["blink"])
                    raise DecryptionError('Excel file without password!')

                office_file.decrypt(decrypted_data)

                try:
                    wb = pd.read_excel(decrypted_data, sheet_name=EXCEL_PAGE_NAME)
                except ValueError as error:
                    cprint('\n⚠️ Wrong page name! Please check EXCEL_PAGE_NAME ⚠️', color='light_red', attrs=["blink"])
                    raise ValueError(f"{error}")
            else:
                try:
                    wb = pd.read_excel(file, sheet_name=EXCEL_PAGE_NAME)
                except ValueError as error:
                    cprint('\n⚠️ Wrong page name! Please check EXCEL_PAGE_NAME ⚠️', color='light_red', attrs=["blink"])
                    raise ValueError(f"{error}")

            accounts_data = {}
            for index, row in wb.iterrows():
                account_name = row["Name"]
                private_key = row["Private key"]
                mnemonic = row["Cosmos mnemonic"]
                solana_private_key = row["Solana private key"]
                proxy = row["Proxy"]
                okx_evm_address = row['OKX EVM address']
                bitget_evm_address = row['Bitget EVM address']
                okx_inj_address = row['OKX INJ address']
                bitget_inj_address = row['Bitget INJ address']
                okx_tia_address = row['OKX TIA address']
                bitget_tia_address = row['Bitget TIA address']
                bitget_ntrn_address = row['Bitget NTRN address']

                accounts_data[int(index) + 1] = {
                    "account_number": account_name,
                    "private_key": private_key,
                    "mnemonic": mnemonic,
                    "solana_private_key": solana_private_key,
                    "proxy": proxy,
                    "okx_evm_address": okx_evm_address,
                    "bitget_evm_address": bitget_evm_address,
                    "okx_inj_address": okx_inj_address,
                    "bitget_inj_address": bitget_inj_address,
                    "okx_tia_address": okx_tia_address,
                    "bitget_tia_address": bitget_tia_address,
                    "bitget_ntrn_address": bitget_ntrn_address,
                }

            (acc_names, priv_keys, mnemonics, solana_private_keys, proxies, okx_evm_wallets, bitget_evm_wallets,
             okx_inj_wallets, bitget_tia_wallets, bitget_inj_wallets, okx_tia_wallets,
             bitget_ntrn_wallets) = ([] for _ in range(12))

            for k, v in accounts_data.items():
                acc_names.append(v['account_number'] if isinstance(v['account_number'], (int, str)) else None)
                priv_keys.append(v['private_key'])
                mnemonics.append(v['mnemonic'])
                solana_private_keys.append(v['solana_private_key'])
                proxies.append(v['proxy'] if isinstance(v['proxy'], str) else None)
                okx_evm_wallets.append(v['okx_evm_address'] if isinstance(v['okx_evm_address'], str) else None)
                bitget_evm_wallets.append(v['bitget_evm_address'] if isinstance(v['bitget_evm_address'], str) else None)
                okx_inj_wallets.append(v['okx_inj_address'] if isinstance(v['okx_inj_address'], str) else None)
                bitget_inj_wallets.append(v['bitget_inj_address'] if isinstance(v['bitget_inj_address'], str) else None)
                okx_tia_wallets.append(v['okx_tia_address'] if isinstance(v['okx_tia_address'], str) else None)
                bitget_tia_wallets.append(v['bitget_tia_address'] if isinstance(v['bitget_tia_address'], str) else None)
                bitget_ntrn_wallets.append(
                    v['bitget_ntrn_address'] if isinstance(v['bitget_ntrn_address'], str) else None)

            acc_names = [str(item).strip() for item in acc_names if item is not None]
            proxies = [str(item).strip() for item in proxies if item is not None]
            okx_evm_wallets = [str(item).strip() for item in okx_evm_wallets if item is not None]
            bitget_evm_wallets = [str(item).strip() for item in bitget_evm_wallets if item is not None]
            okx_inj_wallets = [str(item).strip() for item in okx_inj_wallets if item is not None]
            bitget_inj_wallets = [str(item).strip() for item in bitget_inj_wallets if item is not None]
            okx_tia_wallets = [str(item).strip() for item in okx_tia_wallets if item is not None]
            bitget_tia_wallets = [str(item).strip() for item in bitget_tia_wallets if item is not None]
            bitget_ntrn_wallets = [str(item).strip() for item in bitget_ntrn_wallets if item is not None]

            return (
                acc_names, priv_keys, mnemonics, solana_private_keys, proxies, okx_evm_wallets, bitget_evm_wallets,
                okx_inj_wallets, bitget_inj_wallets, okx_tia_wallets, bitget_tia_wallets, bitget_ntrn_wallets
            )

    except (DecryptionError, InvalidKeyError, DecryptionError, ValueError):
        sys.exit()

    except ImportError:
        cprint(f'\nAre you sure about EXCEL_PASSWORD in general_settings.py?', color='light_red')
        sys.exit()

    except Exception as error:
        cprint(f'\nError in <get_accounts_data> function! Error: {error}\n', color='light_red')
        sys.exit()


def clean_progress_file():
    with open(Settings.PROGRESS_FILE_PATH, 'w') as file:
        json.dump({}, file)


def clean_gwei_file():
    # Получаем путь к текущей директории, где находится скрипт
    current_dir = Path(__file__).parent

    # Формируем путь к файлу 'maximum_gwei.json' в папке 'data'
    gwei_file_path = current_dir / 'data' / 'services' / 'maximum_gwei.json'

    # Проверим наличие папки 'services' и создадим её, если она отсутствует
    gwei_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Открываем файл и очищаем его
    with open(gwei_file_path, 'w') as file:
        file.truncate(0)


def progress_file_is_not_empty():
    if not os.path.exists(Settings.PROGRESS_FILE_PATH):
        with open(Settings.PROGRESS_FILE_PATH, 'w') as file:
            json.dump({}, file)
        return False
    else:
        with open(Settings.PROGRESS_FILE_PATH, 'r') as file:
            route_dict = json.load(file)
        if route_dict:
            return True
        else:
            return False


def create_cex_withdrawal_list():
    from config.constants import (
        ACCOUNT_NAMES, OKX_EVM_WALLETS, OKX_INJ_WALLETS, BITGET_TIA_WALLETS, BITGET_EVM_WALLETS,
        BITGET_INJ_WALLETS, OKX_TIA_WALLETS, BITGET_NTRN_WALLETS
    )

    cex_data = {}

    cex_paths = [
        'okx_evm_withdraw_list', 'bitget_evm_withdraw_list', 'okx_inj_withdraw_list',
        'bitget_inj_withdraw_list', 'okx_tia_withdraw_list', 'bitget_tia_withdraw_list',
        'bitget_ntrn_withdraw_list'
    ]

    current_dir = Path(__file__).parent

    for index, cex_addresses in enumerate((
            OKX_EVM_WALLETS, BITGET_EVM_WALLETS, OKX_INJ_WALLETS,
            BITGET_INJ_WALLETS, OKX_TIA_WALLETS, BITGET_TIA_WALLETS, BITGET_NTRN_WALLETS
    ), 0):
        if ACCOUNT_NAMES and cex_addresses:
            # Формируем путь к файлу для записи JSON данных
            cex_file_path = current_dir / 'data' / 'services' / f'{cex_paths[index].lower()}.json'

            # Проверяем наличие директории 'services' и создаём её при необходимости
            cex_file_path.parent.mkdir(parents=True, exist_ok=True)

            # Открываем файл для записи и сохраняем данные
            with open(cex_file_path, 'w') as file:
                for account_name, cex_wallet in zip(ACCOUNT_NAMES, cex_addresses):
                    cex_data[str(account_name)] = str(cex_wallet).strip()
                json.dump(cex_data, file, indent=4)

            # Сообщение об успешном завершении операции
    cprint(f'✅  Successfully added and saved all your CEX deposit wallets ', 'light_blue')
    cprint(f'⚠️ Check all CEX deposit wallets by yourself to avoid problems', 'light_yellow')
    print()


def get_wallet_for_deposit(self, deposit_network, cex_name: str = 'okx'):
    from modules.interfaces import CriticalException

    evm_addresses_path = f'{cex_name.lower()}_evm_withdraw_list'

    file_path = {
        42: f'{cex_name.lower()}_inj_withdraw_list',
        43: f'{cex_name.lower()}_tia_withdraw_list',
        44: f'{cex_name.lower()}_ntrn_withdraw_list',
    }.get(deposit_network, evm_addresses_path)

    try:
        with open(f'./data/services/{file_path}.json') as file:
            from json import load
            cex_withdraw_list = load(file)
            cex_wallet = cex_withdraw_list[self.client.account_name]
        return cex_wallet
    except json.JSONDecodeError:
        raise CriticalException(f"Bad data in {file_path}.json")
    except Exception as error:
        raise CriticalException(f'There is no wallet listed for deposit to CEX: {error}')


def clean_bridge_progress_file(account_name: str):
    # Получаем путь к текущей директории, где находится скрипт
    current_dir = Path(__file__).parent

    # Формируем путь к файлу 'bridge_temp_data.json' в папке 'services'
    file_path = current_dir / 'data' / 'services' / 'bridge_temp_data.json'

    # Проверим наличие директории 'services' и создадим её, если она отсутствует
    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Открываем файл для чтения данных
        with open(file_path, 'r') as file:
            bridges_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл не найден или поврежден, инициализируем пустой словарь
        bridges_data = {}

    # Очищаем или создаем данные для конкретного пользователя
    if bridges_data.get(account_name):
        bridges_data[account_name] = {}
    else:
        bridges_data.setdefault(account_name, {})

    # Записываем обновленные данные обратно в файл
    with open(file_path, 'w') as file:
        json.dump(bridges_data, file, indent=4)


def write_into_bridge_temp_file(account_name: str, bridge_name: str = None, bridge_count_plus: bool = False):
    # Получаем путь к текущей директории, где находится скрипт
    current_dir = Path(__file__).parent

    # Формируем путь к файлу 'bridge_temp_data.json' в папке 'services'
    file_path = current_dir / 'data' / 'services' / 'bridge_temp_data.json'

    # Проверим наличие директории 'services' и создадим её, если она отсутствует
    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Открываем файл для чтения данных
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл не найден или поврежден, инициализируем начальные данные
        data = {
            account_name: {
                bridge_name: 0
            }
        }

    # Обновляем счетчик или добавляем новое значение
    if bridge_count_plus:
        data[account_name][bridge_name] += 1
    else:
        data.setdefault(account_name, {})[bridge_name] = 0

    # Записываем обновленные данные обратно в файл
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def get_current_progress_for_bridge(account_name: str, bridge_name: str = None):
    # Получаем путь к текущей директории, где находится скрипт
    current_dir = Path(__file__).parent

    # Формируем путь к файлу 'bridge_temp_data.json' в папке 'services'
    file_path = current_dir / 'data' / 'services' / 'bridge_temp_data.json'

    # Проверим наличие директории 'services' и создадим её, если она отсутствует
    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Открываем файл и загружаем данные
        with open(file_path, 'r') as file:
            bridge_counts = json.load(file)
        return bridge_counts[account_name][bridge_name]
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        # Если файл не существует, данные повреждены или ключи отсутствуют, создаём новые записи
        write_into_bridge_temp_file(account_name, bridge_name)
        with open(file_path, 'r') as file:
            bridge_counts = json.load(file)
        return bridge_counts[account_name][bridge_name]


def retry_on_error(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        from modules.interfaces import (
            SoftwareExceptionHandled, CriticalException, SoftwareExceptionWithoutRetry, SoftwareException
        )
        attempt = 0
        while attempt < MAXIMUM_RETRY:
            try:
                return await func(self, *args, **kwargs)
            except SoftwareExceptionHandled as error:
                self.logger_msg(*self.client.acc_info, msg=f"{error}", type_msg='warning')
                return True
            except SoftwareExceptionWithoutRetry as error:
                self.logger_msg(*self.client.acc_info, msg=f"{error}", type_msg='warning')
                raise SoftwareException(f"{error}")
            except Exception as error:
                if STOP_SOFTWARE and isinstance(error, CriticalException):
                    raise error
                attempt += 1
                if attempt < MAXIMUM_RETRY:
                    self.logger_msg(
                        None, None,
                        msg=f'{error} | Try[{attempt}/{MAXIMUM_RETRY}]',
                        type_msg='error'
                    )
                    await asyncio.sleep(10)
                else:
                    self.logger_msg(
                        None, None,
                        msg=f"Tries are over\n",
                        type_msg='error'
                    )
        return False

    return wrapper


def network_handler(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):

        k = 0
        client_object = False
        while True:
            try:
                return await func(self, *args, **kwargs)
            except Exception as error:
                from modules import Client
                msg = f'{error}'
                k += 1

                if hasattr(self, 'client') and isinstance(self.client, Client):
                    client_info = self.client.acc_info
                    client_object = True
                else:
                    if isinstance(self, Client):
                        client_info = self.acc_info
                    else:
                        client_info = None, None

                if k % 2 == 0:
                    if client_object:
                        await self.client.change_proxy()
                        await self.client.change_rpc()
                    else:
                        await self.change_proxy()
                        await self.change_rpc()
                    continue

                if isinstance(error, KeyError):
                    self.logger_msg(*client_info, msg=msg, type_msg='error')
                    return False

                elif any(keyword in str(error) for keyword in (
                        'Bad Gateway', '403', 'SSL', 'Invalid proxy', 'rate limit', '429', '407', '503'
                )):
                    self.logger_msg(*client_info, msg=msg, type_msg='warning')
                    if client_object:
                        await self.client.change_proxy()
                    else:
                        await self.change_proxy()
                    continue

                elif 'Error code' in str(error):
                    msg = f'{error}. Will try again...'

                elif 'Server disconnected' in str(error):
                    msg = f'{error}. Will try again...'

                elif 'StatusCode.UNAVAILABLE' in str(error):
                    msg = f'RPC got autism response, will try again...'

                elif '<html lang="en">' in str(error):
                    msg = f'Proxy got non-permanent ban, will try again...'

                elif isinstance(error, (ClientError, asyncio.TimeoutError, ProxyError, ReplyError)):
                    msg = f"Connection to RPC is not stable. Will try again..."

                else:
                    raise error

                self.logger_msg(*client_info, msg=msg, type_msg='warning')
                await asyncio.sleep(10)

        return False

    return wrapper


def helper(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        from modules.interfaces import (
            BlockchainException, SoftwareException, SoftwareExceptionWithoutRetry,
            BlockchainExceptionWithoutRetry, SoftwareExceptionHandled
        )

        attempts = 0
        k = 0

        no_sleep_flag = False
        try:
            while attempts <= MAXIMUM_RETRY:
                try:
                    return await func(self, *args, **kwargs)
                except Exception as error:
                    attempts += 1
                    k += 1
                    msg = f'{error}'
                    # traceback.print_exc()

                    if isinstance(error, KeyError):
                        msg = f"Parameter '{error}' for this module is not exist in software!"
                        self.logger_msg(*self.client.acc_info, msg=msg, type_msg='error')
                        return False

                    elif any(keyword in str(error) for keyword in (
                            'Bad Gateway', '403', 'SSL', 'Invalid proxy', 'rate limit', '429'
                    )):
                        await self.client.change_proxy()

                    elif 'Error code' in str(error):
                        msg = f'{error}. Will try again...'

                    elif 'Server disconnected' in str(error):
                        msg = f'{error}. Will try again...'

                    elif 'StatusCode.UNAVAILABLE' in str(error):
                        msg = f'RPC got autism response, will try again......'

                    elif '<html lang="en">' in str(error):
                        msg = f'Proxy got non-permanent ban, will try again...'

                    elif isinstance(error, SoftwareExceptionHandled):
                        self.logger_msg(*self.client.acc_info, msg=f"{error}", type_msg='warning')
                        return True

                    elif isinstance(error, (SoftwareExceptionWithoutRetry, BlockchainExceptionWithoutRetry)):
                        self.logger_msg(self.client.account_name, None, msg=msg, type_msg='error')
                        return False

                    elif isinstance(error, SoftwareException):
                        msg = f'{error}'

                    elif isinstance(error, BlockchainException):
                        if 'insufficient funds' not in str(error):
                            self.logger_msg(
                                self.client.account_name,
                                None, msg=f'Maybe problem with node: {self.client.rpc}', type_msg='warning'
                            )
                            await self.client.change_rpc()

                    elif isinstance(error, (
                            ClientError, asyncio.TimeoutError, ProxyError, ReplyError, ProxyTimeoutError,
                            ProxyConnectionError
                    )):
                        self.logger_msg(
                            *self.client.acc_info,
                            msg=f"Connection to RPC is not stable. Will try again in 10 seconds...",
                            type_msg='warning'
                        )
                        await asyncio.sleep(10)
                        if k % 2 == 0:
                            await self.client.change_proxy()
                            await self.client.change_rpc()

                        attempts -= 1
                        no_sleep_flag = True

                    else:
                        msg = f'Unknown Error: {error}'
                        traceback.print_exc()

                    self.logger_msg(
                        self.client.account_name, None, msg=f"{msg} | Try[{attempts}/{MAXIMUM_RETRY + 1}]",
                        type_msg='error'
                    )

                    if attempts > MAXIMUM_RETRY:
                        self.logger_msg(
                            self.client.account_name, None,
                            msg=f"Tries are over, software will stop module\n", type_msg='error'
                        )
                        break
                    else:
                        if not no_sleep_flag:
                            await sleep(self, *SLEEP_TIME_RETRY)

        finally:
            await self.client.session.close()
        return False

    return wrapper


def get_addresses_for_cex():
    from config.constants import EVM_PRIVATE_KEYS, MNEMONICS
    from cosmpy.aerial.wallet import LocalWallet
    from cosmpy.crypto.address import Address

    addresses_dict = {}
    addresses_list = []
    zip_data = zip(EVM_PRIVATE_KEYS, MNEMONICS)
    if len(EVM_PRIVATE_KEYS) != len(MNEMONICS):
        cprint('Please make sure that the number of private keys = number of mnemonics\n',
               'light_red', attrs=["blink"])
        return

    for evm_private_key, cosmos_mnemonic in zip_data:
        for address_index in range(4):
            if address_index == 0:
                addresses_dict['EVM'] = AsyncWeb3.to_checksum_address(
                    AsyncWeb3().eth.account.from_key(evm_private_key).address)
            elif address_index == 1:
                wallet = LocalWallet.from_mnemonic(cosmos_mnemonic, 'neutron')
                public_key = wallet.public_key()
                address = Address(public_key, prefix='neutron')
                addresses_dict['NTRN'] = address
            elif address_index == 2:
                wallet = LocalWallet.from_mnemonic(cosmos_mnemonic, 'celestia')
                public_key = wallet.public_key()
                address = Address(public_key, prefix='celestia')
                addresses_dict['TIA'] = address
            elif address_index == 3:
                from utils.inj_derivation import PrivateKey
                cosmos_private_key = PrivateKey.from_mnemonic(cosmos_mnemonic)
                cosmos_public_key = cosmos_private_key.to_public_key()
                cosmos_pre_address = cosmos_public_key.to_address()
                address = Address(cosmos_pre_address.to_acc_bech32(), prefix='inj')
                addresses_dict['INJ'] = address
        addresses_list.append(addresses_dict)
        addresses_dict = {}

    xlsx_data = pd.DataFrame(addresses_list)

    # Используем pathlib для создания динамического пути
    current_dir = Path(__file__).parent
    data_dir = current_dir / 'data'
    file_path = data_dir / 'wallet_addresses_for_cex.xlsx'

    # Проверяем наличие директории 'data' и создаем её при необходимости
    data_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Сохраняем данные в Excel файл
        xlsx_data.to_excel(file_path, index=False)

        cprint(
            f'✅ Data successfully loaded {len(MNEMONICS)} addresses to {file_path} (Excel format)\n',
            'light_yellow', attrs=["blink"])

    except Exception as error:
        if 'Permission denied' in str(error):
            cprint('Please, close Excel file (wallet_addresses_for_cex.xlsx)\n',
                   'light_red', attrs=["blink"])
        else:
            raise error


def gas_checker(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        if GAS_CONTROL:
            await asyncio.sleep(1)
            print()
            counter = 0

            self.logger_msg(self.client.account_name, None, msg=f"Checking for gas price")

            if self.client.network.name != 'Solana':
                w3 = AsyncWeb3(AsyncHTTPProvider(
                    random.choice(EthereumRPC.rpc), request_kwargs=self.client.request_kwargs)
                )
            else:
                return await func(self, *args, **kwargs)
            while True:
                try:
                    gas = round(AsyncWeb3.from_wei(await w3.eth.gas_price, 'gwei'), 3)

                    if gas < float(get_max_gwei_setting()):

                        self.logger_msg(
                            self.client.account_name, None, msg=f"{gas} Gwei | Gas price is good", type_msg='success')
                        return await func(self, *args, **kwargs)

                    else:

                        counter += 1
                        self.logger_msg(
                            self.client.account_name, None,
                            msg=f"{gas} Gwei | Gas is too high. Next check in {SLEEP_TIME_GAS} second",
                            type_msg='warning'
                        )

                        await asyncio.sleep(SLEEP_TIME_GAS)
                except (
                        ClientProxyConnectionError, TimeoutError, ClientHttpProxyError, ProxyError, ClientResponseError
                ):
                    self.logger_msg(
                        *self.client.acc_info,
                        msg=f"Connection to RPC is not stable. Will try again in 1 min...",
                        type_msg='warning'
                    )
                    await asyncio.sleep(60)
                    if counter % 2 == 0:
                        await self.client.change_proxy()
                        await self.client.change_rpc()
        return await func(self, *args, **kwargs)

    return wrapper


def get_max_gwei_setting():
    # Получаем путь к текущей директории, где находится скрипт
    current_dir = Path(__file__).parent

    # Формируем путь к файлу 'maximum_gwei.json' в папке 'services'
    file_path = current_dir / 'data' / 'services' / 'maximum_gwei.json'

    # Проверим наличие директории 'services' и создадим её, если она отсутствует
    file_path.parent.mkdir(parents=True, exist_ok=True)

    data = {}

    try:
        # Открываем файл и загружаем данные
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл не найден или поврежден, используем значение по умолчанию
        data['maximum_gwei'] = MAXIMUM_GWEI

    # Сохраняем данные обратно в файл
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    return data['maximum_gwei']


def create_table(connection) -> bool:
    try:
        with connection.cursor() as cursor:
            query = """CREATE TABLE IF NOT EXISTS logs (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        log_level VARCHAR(255),
                        log_message TEXT
                    );"""
            cursor.execute(query)
            return True
    except Exception as e:
        cprint(f'\nError creating table with logs: {e}\n', color='light_red')
        return False


def insert_log(connection, level, message) -> None:
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO logs (log_level, log_message) VALUES (%s, %s)"
            cursor.execute(query, (level, message))
    except Exception:
        pass
