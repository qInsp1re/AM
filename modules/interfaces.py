import asyncio

from aiohttp import ClientSession, TCPConnector
from aiohttp_socks import ProxyConnector
from loguru import logger
from sys import stderr
from datetime import datetime
from abc import ABC, abstractmethod
from random import uniform
import json as js
import mysql.connector

from pathlib import Path
from dev_settings import Settings
from utils.tools import create_table, insert_log, network_handler
from config.constants import TOKEN_API_INFO
from termcolor import cprint

from general_settings import (LAYERSWAP_API_KEY, OKX_API_KEY, OKX_API_PASSPHRAS,
                              OKX_API_SECRET, BINGX_API_KEY, BINGX_API_SECRET, BINANCE_API_KEY,
                              BINANCE_API_SECRET, BITGET_API_SECRET, BITGET_API_KEY, MAIN_PROXY,
                              SAVE_LOGS_TO_DATABASE, DB_HOST, DB_NAME, DB_USERNAME, DB_PASSWORD)
from version import VERSION


def get_user_agent():
    random_version = f"{uniform(520, 540):.2f}"
    return (f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random_version} (KHTML, like Gecko)'
            f' Chrome/126.0.0.0 Safari/{random_version} Edg/126.0.0.0')


class PriceImpactException(Exception):
    pass


class BlockchainException(Exception):
    pass


class BlockchainExceptionWithoutRetry(Exception):
    pass


class SoftwareException(Exception):
    pass


class CriticalException(Exception):
    pass


class SoftwareExceptionWithoutRetry(Exception):
    pass


class SoftwareExceptionWithRetries(Exception):
    pass


class SoftwareExceptionHandled(Exception):
    pass


class InsufficientBalanceException(Exception):
    pass


class BridgeExceptionWithoutRetry(Exception):
    pass


class DepositExceptionWithoutRetry(Exception):
    pass


class Logger(ABC):
    def __init__(self):
        self.logger = logger
        self.logger.remove()
        logger_format = "<cyan>{time:HH:mm:ss}</cyan> | <level>" "{level: <8}</level> | <level>{message}</level>"
        self.logger.add(stderr, format=logger_format)

        # Используем pathlib для динамического формирования пути
        current_dir = Path(__file__).parent
        logs_dir = current_dir / 'data' / 'logs'

        # Создаем директорию для логов, если она не существует
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Формируем путь для лог-файла с текущей датой
        date = datetime.today().date()
        log_file_path = logs_dir / f"{date}.log"

        # Добавляем лог-файл
        self.logger.add(log_file_path, rotation="500 MB", level="INFO", format=logger_format)

        # Установка соединения с базой данных
        self.connection = None
        if SAVE_LOGS_TO_DATABASE:
            try:
                self.connection = mysql.connector.connect(
                    host=DB_HOST,
                    database=DB_NAME,
                    user=DB_USERNAME,
                    password=DB_PASSWORD,
                    autocommit=True
                )
            except Exception as ex:
                cprint(f"\nError connecting to db. Logs won't be saved. {ex}\n", color='light_red')
            if self.connection is not None:
                self.table_created = create_table(self.connection)
        else:
            self.table_created = False

    def logger_msg(self, account_name, address, network_name=None, msg=None, type_msg: str = 'info'):
        class_name = self.__class__.__name__
        software_chain = network_name if network_name else 'OmniChain'
        acc_info = '1/1'
        module_info = '1/1'
        if account_name:
            try:
                with open(Settings.PROGRESS_FILE_PATH) as file:
                    wallets_progress_data = js.load(file)
                keys_list = list(wallets_progress_data.keys())
                acc_index = keys_list.index(account_name) + 1
                accs_count = len(wallets_progress_data)
                acc_info = f'{acc_index}/{accs_count}'
                module_index = wallets_progress_data[account_name]['current_step']
                modules_count = len(wallets_progress_data[account_name]['route'])
                module_info = f'{module_index}/{modules_count}'
            except ValueError:
                acc_info = "0/0"
                module_info = "0/0"

        if account_name is None and address is None:
            info = f'[Annihilator] | {software_chain} | {class_name} |'
        elif account_name is not None and address is None:
            info = f'[{acc_info}] | [{account_name}] | [{module_info}] | v{VERSION} | {software_chain} | {class_name} |'
        else:
            info = f'[{acc_info}] | [{account_name}] | [{module_info}] | {address} | {software_chain} | {class_name} |'
        if SAVE_LOGS_TO_DATABASE:
            if type_msg == 'info':
                self.logger.info(f"{info} {msg}")
                insert_log(self.connection, 'INFO', msg)
            elif type_msg == 'error':
                self.logger.error(f"{info} {msg}")
                insert_log(self.connection, 'ERROR', msg)
            elif type_msg == 'success':
                self.logger.success(f"{info} {msg}")
                insert_log(self.connection, 'SUCCESS', msg)
            elif type_msg == 'warning':
                self.logger.warning(f"{info} {msg}")
                insert_log(self.connection, 'WARNING', msg)
        else:
            if type_msg == 'info':
                self.logger.info(f"{info} {msg}")
            elif type_msg == 'error':
                self.logger.error(f"{info} {msg}")
            elif type_msg == 'success':
                self.logger.success(f"{info} {msg}")
            elif type_msg == 'warning':
                self.logger.warning(f"{info} {msg}")


class DEX(ABC):
    @abstractmethod
    async def swap(self):
        pass


class CEX(ABC):
    def __init__(self, client, class_name):
        self.client = client
        self.class_name = class_name
        if class_name == 'OKX':
            self.api_key = OKX_API_KEY
            self.api_secret = OKX_API_SECRET
            self.passphras = OKX_API_PASSPHRAS
        elif class_name == 'BingX':
            self.api_key = BINGX_API_KEY
            self.api_secret = BINGX_API_SECRET
        elif class_name == 'Binance':
            self.api_key = BINANCE_API_KEY
            self.api_secret = BINANCE_API_SECRET
        elif class_name == 'Bitget':
            self.api_key = BITGET_API_KEY
            self.api_secret = BITGET_API_SECRET
        else:
            raise SoftwareException('CEX don`t available now')

    @abstractmethod
    async def deposit(self):
        pass

    @abstractmethod
    async def withdraw(self):
        pass

    async def make_request(self, method: str = 'GET', url: str = None, data: str = None, params: dict = None,
                           headers: dict = None, json: dict = None, module_name: str = 'Request',
                           content_type: str | None = "application/json"):

        insf_balance_code = {
            'BingX': [100437],
            'Binance': [4026],
            'Bitget': [43012, 13004, 13008],
            'OKX': [58350],
        }[self.class_name]

        freeze_balance_code = {
            'BingX': [],
            'Binance': [-9000],
            'Bitget': [47003],
            'OKX': [],
        }.get(self.class_name, False)

        async with ClientSession(
                connector=ProxyConnector.from_url(f"http://{MAIN_PROXY}", ) if MAIN_PROXY != '' else TCPConnector()
        ) as session:
            async with session.request(
                    method=method, url=url, headers=headers, data=data, json=json, params=params
            ) as response:
                data: dict = await response.json(content_type=content_type)

                if self.class_name == 'Binance' and response.status in [200, 201]:
                    return data

                if int(data.get('code')) != 0:
                    message = data.get('msg') or data.get('desc') or 'Unknown error'
                    code = int(data['code'])
                    if code in insf_balance_code:
                        self.client.logger_msg(
                            *self.client.acc_info,
                            msg=f"Your CEX balance < your want transfer amount. Will try again in 5 min...",
                            type_msg='warning'
                        )
                        await asyncio.sleep(300)
                        raise InsufficientBalanceException('Trying request again...')

                    elif freeze_balance_code and code in freeze_balance_code:
                        self.client.logger_msg(
                            *self.client.acc_info,
                            msg=message,
                            type_msg='warning'
                        )
                        await asyncio.sleep(300)
                        raise InsufficientBalanceException('Trying request again...')

                    error = f"Error code: {data['code']} Msg: {message}"
                    raise SoftwareException(f"Bad request to {self.class_name}({module_name}): {error}")

                # self.logger.success(f"{self.info} {module_name}")
                return data['data']


class RequestClient(ABC):
    def __init__(self, client):
        self.client = client

    async def make_request(self, method: str = 'GET', url: str = None, headers: dict = None, params: dict = None,
                           data: str = None, json: dict | list = None, without_response: bool = False):

        headers = (headers or {}) | {'User-Agent': get_user_agent()}

        async with self.client.session.request(
                method=method, url=url, headers=headers, data=data, json=json, params=params
        ) as response:

            if response.status in [200, 201]:
                if without_response:
                    return True
                data = await response.json()
                return data
            raise SoftwareException(
                f"Bad request to {self.__class__.__name__} API. "
                f"Response status: {response.status}. Status: {response.status}. Response: {await response.text()}")

    async def get_token_price_via_gate(self, token_name: str) -> float:

        url = f'https://api.gateio.ws/api/v4/spot/tickers'

        params = {
            'currency_pair': f'{token_name}_USDT'
        }

        async with ClientSession(
                connector=ProxyConnector.from_url(f"http://{MAIN_PROXY}", ssl=False) if MAIN_PROXY else TCPConnector(
                    ssl=False)
        ) as session:
            async with session.request(method='GET', url=url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return float(data[0]['last'])
                elif response.status == 429:
                    self.client.logger_msg(
                        *self.client.acc_info, msg='Gate API got rate limit. Next try in 300 second',
                        type_msg='warning')
                    await asyncio.sleep(300)
                raise SoftwareException(f'Bad request to Gate API: {response.status}')

    async def get_token_price_via_okx(self, token_name: str) -> float:

        url = f'https://www.okx.com/api/v5/market/ticker'

        params = {
            'instId': f'{token_name}-USDT'
        }

        async with ClientSession(
                connector=ProxyConnector.from_url(f"http://{MAIN_PROXY}", ssl=False) if MAIN_PROXY else TCPConnector(
                    ssl=False)
        ) as session:
            async with session.request(method='GET', url=url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return float(data['data'][0]['last'])
                elif response.status == 429:
                    self.client.logger_msg(
                        *self.client.acc_info, msg='OKX API got rate limit. Next try in 300 second',
                        type_msg='warning')
                    await asyncio.sleep(300)
                raise SoftwareException(f'Bad request to OKX API: {response.status}')

    async def get_token_price_via_bybit(self, token_name: str) -> float:

        url = f'https://api.bybit.com/spot/v3/public/quote/ticker/price?symbol={token_name}USDT'

        params = {
            'symbol': f'{token_name}USDT'
        }

        async with ClientSession(
                connector=ProxyConnector.from_url(f"http://{MAIN_PROXY}", ssl=False) if MAIN_PROXY else TCPConnector(
                    ssl=False)
        ) as session:
            async with session.request(method='GET', url=url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return float(data['result']['price'])
                elif response.status == 429:
                    self.client.logger_msg(
                        *self.client.acc_info, msg='Bybit API got rate limit. Next try in 300 second',
                        type_msg='warning')
                    await asyncio.sleep(300)
                raise SoftwareException(f'Bad request to Bybit API: {response.status}')

    async def get_token_price_via_binance(self, token_name: str) -> float:
        if 'ETH' in token_name:
            token_name = 'ETH'
        elif 'MATIC' in token_name:
            token_name = 'POL'
        elif 'POL' in token_name:
            token_name = 'POL'
        elif 'TIA' in token_name:
            token_name = 'TIA'
        elif 'BNB' in token_name:
            token_name = 'BNB'
        elif 'SOL' in token_name:
            token_name = 'BNB'

        url = f'https://api.binance.com/api/v3/ticker/price'

        params = {
            'symbol': f'{token_name}USDT'
        }

        async with ClientSession(
                connector=ProxyConnector.from_url(f"http://{MAIN_PROXY}", ssl=False) if MAIN_PROXY else TCPConnector(
                    ssl=False)
        ) as session:
            async with session.request(method='GET', url=url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return float(data['price'])
                elif response.status == 429:
                    self.client.logger_msg(
                        *self.client.acc_info, msg='Binance API got rate limit. Next try in 300 second',
                        type_msg='warning')
                    await asyncio.sleep(300)
                raise SoftwareException(f'Bad request to Binance API: {response.status}')

    @network_handler
    async def get_token_price(self, token_name: str, vs_currency: str = 'usd') -> float:

        if token_name in TOKEN_API_INFO['stables']:
            return 1.0

        if token_name not in TOKEN_API_INFO['coingecko']:
            if token_name in TOKEN_API_INFO['binance']:
                return await self.get_token_price_via_binance(token_name)
            elif token_name in TOKEN_API_INFO['gate']:
                return await self.get_token_price_via_gate(token_name)
            else:
                raise SoftwareExceptionWithoutRetry(
                    f"CEX on which the rate for {token_name} will be calculated hasn't been determined"
                )
        else:
            await asyncio.sleep(10)
            url = 'https://api.coingecko.com/api/v3/simple/price'

            token_name = TOKEN_API_INFO['coingecko'][token_name]

            params = {
                'ids': f'{token_name}',
                'vs_currencies': f'{vs_currency}'
            }

            async with ClientSession(
                    connector=ProxyConnector.from_url(f"http://{MAIN_PROXY}",
                                                      ssl=False) if MAIN_PROXY else TCPConnector(ssl=False)
            ) as session:
                async with session.request(method='GET', url=url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return float(data[token_name][vs_currency])
                    elif response.status == 429:
                        self.client.logger_msg(
                            *self.client.acc_info, msg='CoinGecko API got rate limit. Next try in 300 second',
                            type_msg='warning')
                        await asyncio.sleep(300)
                    raise SoftwareException(f'Bad request to CoinGecko API: {response.status}')


class Bridge(ABC):
    def __init__(self, client):
        self.client = client

        if self.__class__.__name__ == 'LayerSwap':
            self.headers = {
                'X-LS-APIKEY': f'{LAYERSWAP_API_KEY}',
                'Content-Type': 'application/json'
            }
        elif self.__class__.__name__ == 'Rhino':
            self.headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        elif self.__class__.__name__ == 'Bungee':
            self.headers = {
                "Api-Key": "1b2fd225-062f-41aa-8c63-d1fef19945e7",
            }

    @abstractmethod
    async def bridge(self, *args, **kwargs):
        pass

    async def make_request(self, method: str = 'GET', url: str = None, headers: dict = None, params: dict = None,
                           data: str = None, json: dict = None, without_response: bool = False, cookies: dict = None):

        headers = (headers or {}) | {'User-Agent': get_user_agent()}
        async with self.client.session.request(method=method, url=url, headers=headers, data=data, json=json,
                                               params=params, cookies=cookies) as response:
            if response.status in [200, 201]:
                if without_response:
                    return True
                data = await response.json()
                return data
            raise SoftwareException(
                f"Bad request to {self.__class__.__name__} API. "
                f"Response status: {response.status}. Status: {response.status}. Response: {await response.text()}")


class Refuel(ABC):
    @abstractmethod
    async def refuel(self, *args, **kwargs):
        pass


class Messenger(ABC):
    @abstractmethod
    async def send_message(self):
        pass


class Landing(ABC):
    @abstractmethod
    async def deposit(self):
        pass

    @abstractmethod
    async def withdraw(self):
        pass


class Minter(ABC):
    @abstractmethod
    async def mint(self, *args, **kwargs):
        pass


class Creator(ABC):
    @abstractmethod
    async def create(self):
        pass


class Blockchain(ABC):
    def __init__(self, client):
        self.client = client

    async def make_request(self, method: str = 'GET', url: str = None, headers: dict = None, params: dict = None,
                           data: str = None, json: dict = None):
        headers = (headers or {}) | {'User-Agent': get_user_agent()}
        async with self.client.session.request(method=method, url=url, headers=headers, data=data,
                                               params=params, json=json) as response:
            data = await response.json()
            if response.status == 200:
                return data
            raise SoftwareException(
                f"Bad request to {self.__class__.__name__} API. "
                f"Response status: {response.status}. Status: {response.status}. Response: {await response.text()}")