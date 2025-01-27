import math
import random

from eth_abi import abi

from modules import DEX, Logger, Client, RequestClient
from modules.interfaces import SoftwareExceptionHandled
from dev_settings import Settings
from utils.qnumbers import QNumber
from utils.tools import gas_checker, helper
from general_settings import SLIPPAGE
from config.constants import (
    AMBIENT_CONTRACT,
    TOKENS_PER_CHAIN, ZERO_ADDRESS
)
from config.abi import AMBIENT_ABI


class Ambient(DEX, Logger, RequestClient):
    def __init__(self, client: Client):
        self.client = client
        Logger.__init__(self)
        RequestClient.__init__(self, client)
        self.network = self.client.network.name
        self.router_contract = self.client.get_contract(AMBIENT_CONTRACT[self.network]['router'], AMBIENT_ABI['router'])
        self.quoter_contract = self.client.get_contract(AMBIENT_CONTRACT[self.network]['quoter'], AMBIENT_ABI['quoter'])

    async def get_lp_balance(self):
        url = "https://ambindexer.net/scroll-gcgo/user_positions"

        headers = {
            "accept": "*/*",
            "accept-language": "ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "referrer": "https://ambient.finance/",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "body": "null",
            "method": "GET",
            "mode": "cors",
            "credentials": "omit"
        }

        params = {
            "user": self.client.address,
            "chainId": self.client.w3.to_hex(self.client.chain_id),
            "ensResolution": "true",
            "annotate": "true",
            "omitKnockout": "true",
            "addValue": "true",
        }

        response = await self.make_request(url=url, params=params, headers=headers)

        if response['data']:
            for pos in response['data']:
                if pos['concLiq']:
                    return pos['bidTick'], pos['askTick'], pos['concLiq']

        raise SoftwareExceptionHandled('You have not any position on Ambient!')

    async def get_min_amount_out(self, from_token_name, to_token_name, from_token_amount):

        amount_in_usd = (await self.get_token_price(from_token_name)) * from_token_amount
        min_amount_out = (amount_in_usd / await self.get_token_price(to_token_name))

        decimals = 18 if to_token_name == 'ETH' else await self.client.get_decimals(to_token_name)

        min_amount_out_in_wei = self.client.to_wei(min_amount_out, decimals)

        return int(min_amount_out_in_wei - (min_amount_out_in_wei / 100 * SLIPPAGE))

    @staticmethod
    def tick_to_price(tick):
        """
        Преобразует тик в цену.
        """
        return 1.0001 ** tick

    @staticmethod
    def price_to_tick(price):
        """
        Преобразует цену в тикет.
        """
        tick = round(math.log(price) / math.log(1.0001))
        return tick

    @helper
    @gas_checker
    async def swap(self, swap_data: tuple):
        from_token_name, to_token_name, amount, amount_in_wei = swap_data

        self.logger_msg(*self.client.acc_info, msg=f'Swap on Ambient: {amount} {from_token_name} -> {to_token_name}')

        tokens_data = TOKENS_PER_CHAIN[self.network]

        from_token_address = tokens_data[from_token_name]
        to_token_address = tokens_data[to_token_name]
        max_sqrt_price = 21267430153580247136652501917186561137
        min_sqrt_price = 65537
        pool_idx = 420
        reserve_flags = 0
        tip = 0

        min_amount_out = await self.get_min_amount_out(from_token_name, to_token_name, amount)

        if from_token_name != 'ETH':
            await self.client.check_for_approved(
                from_token_address, AMBIENT_CONTRACT[self.network]['router'], amount_in_wei
            )

        tx_params = await self.client.prepare_transaction(value=amount_in_wei if from_token_name == 'ETH' else 0)

        await self.client.price_impact_defender(from_token_name, amount, to_token_name, min_amount_out)

        encode_data = abi.encode(
            ['address', 'address', 'uint16', 'bool', 'bool', 'uint256', 'uint8', 'uint256', 'uint256', 'uint8'], [
                ZERO_ADDRESS,
                to_token_address if from_token_name == 'ETH' else from_token_address,
                pool_idx,
                True if from_token_name == 'ETH' else False,
                True if from_token_name == 'ETH' else False,
                amount_in_wei,
                tip,
                max_sqrt_price if from_token_name == 'ETH' else min_sqrt_price,
                min_amount_out,
                reserve_flags
            ]
        )

        transaction = await self.router_contract.functions.userCmd(
            1,
            encode_data
        ).build_transaction(tx_params)

        return await self.client.send_transaction(transaction)

    @staticmethod
    def get_encode_data(data_to_encode, with_fix: bool = False, withdraw_mode: bool = False):
        (token_address_a, token_address_b, pool_idx, min_tick, max_tick, amount_in_wei_a, sqrt_limit_lower,
         sqrt_limit_upper, tip, reserve_flags) = data_to_encode

        salt = [-3, -2, -1, 0, 1, 2, 3]

        salt_min_tick = random.choices(salt)
        salt_max_tick = random.choices(salt)

        if with_fix:
            min_tick += salt_min_tick[0]
            max_tick += salt_max_tick[0]

        encode_data = abi.encode(
            [
                "uint16",
                'address',
                'address',
                'uint128',
                'int256',
                'int256',
                'uint256',
                'uint256',
                'uint256',
                'uint8',
                'uint8'
            ], [
                11 if not withdraw_mode else 2,  # add liquidity
                token_address_a,
                token_address_b,
                pool_idx,
                min_tick,
                max_tick,
                amount_in_wei_a,
                sqrt_limit_lower,
                sqrt_limit_upper,
                tip,
                reserve_flags
            ]
        )

        return encode_data

    @helper
    @gas_checker
    async def add_liquidity_wrseth(self, amount):

        tokens_data = TOKENS_PER_CHAIN[self.network]

        token_address_a = ZERO_ADDRESS
        token_address_b = tokens_data['wrsETH']
        pool_idx = 420
        reserve_flags = 0
        tip = 0

        current_tick = await self.quoter_contract.functions.queryCurveTick(
            token_address_a,
            token_address_b,
            pool_idx
        ).call()

        wanted_range = float(random.choice(Settings.AMBIENT_PERCENT_RANGE))

        current_pool_price = self.tick_to_price(current_tick)
        min_price = current_pool_price * (1 - wanted_range / 100)
        max_price = current_pool_price * (1 + wanted_range / 100)

        min_tick = self.price_to_tick(min_price)
        max_tick = self.price_to_tick(max_price)

        amount_in_wei_a = self.client.to_wei(amount)

        self.logger_msg(
            *self.client.acc_info,
            msg=f'Adding liquidity into wrsETH/ETH Pool on Ambient. You adding {amount} ETH'
        )

        sqrt_price = math.sqrt(1.0001 ** current_tick)
        sqrt_limit_lower = QNumber.from_float(sqrt_price * 0.98, 64, 64).value
        sqrt_limit_upper = QNumber.from_float(sqrt_price * 1.02, 64, 64).value

        log_info = f"you wanted range {wanted_range}%: {min_price:.5f}(min)/{max_price:.5f}(max)"
        self.logger_msg(
            *self.client.acc_info,
            msg=f'Current Pool price: {current_pool_price:.5f}, {log_info}'
        )

        await self.client.check_for_approved(
            token_address_b, AMBIENT_CONTRACT[self.network]['router'], int(amount_in_wei_a * 2)
        )

        data_to_encode = [
            token_address_a,
            token_address_b,
            pool_idx,
            min_tick,
            max_tick,
            amount_in_wei_a,
            sqrt_limit_lower,
            sqrt_limit_upper,
            tip,
            reserve_flags
        ]

        try:
            encoded_data = self.get_encode_data(data_to_encode)

            transaction = await self.router_contract.functions.userCmd(
                128,
                encoded_data
            ).build_transaction(await self.client.prepare_transaction(value=amount_in_wei_a))

            return await self.client.send_transaction(transaction)
        except Exception as error:
            if 'execution reverted: D' in str(error):

                while True:
                    try:
                        encoded_data = self.get_encode_data(data_to_encode, with_fix=True)

                        transaction = await self.router_contract.functions.userCmd(
                            128,
                            encoded_data
                        ).build_transaction(await self.client.prepare_transaction(value=amount_in_wei_a))

                        return await self.client.send_transaction(transaction)

                    except Exception as error:
                        if 'execution reverted: D' in str(error):
                            continue
                        else:
                            raise error
            else:
                raise error

    @helper
    @gas_checker
    async def remove_liquidity_wrseth(self):

        tokens_data = TOKENS_PER_CHAIN[self.network]

        token_address_a = ZERO_ADDRESS
        token_address_b = tokens_data['wrsETH']
        pool_idx = 420
        reserve_flags = 0
        tip = 0

        current_tick = await self.quoter_contract.functions.queryCurveTick(
            token_address_a,
            token_address_b,
            pool_idx
        ).call()

        lower_tick, max_tick, amount_in_wei_a = await self.get_lp_balance()

        self.logger_msg(*self.client.acc_info, msg=f'Removing all liquidity from wrsETH/ETH Pool on Ambient')

        sqrt_price = math.sqrt(1.0001 ** current_tick)
        sqrt_limit_lower = QNumber.from_float(sqrt_price * 0.98, 64, 64).value
        sqrt_limit_upper = QNumber.from_float(sqrt_price * 1.02, 64, 64).value

        data_to_encode = [
            token_address_a,
            token_address_b,
            pool_idx,
            lower_tick,
            max_tick,
            amount_in_wei_a,
            sqrt_limit_lower,
            sqrt_limit_upper,
            tip,
            reserve_flags
        ]

        encoded_data = self.get_encode_data(data_to_encode, withdraw_mode=True)

        transaction = await self.router_contract.functions.userCmd(
            128,
            encoded_data
        ).build_transaction(await self.client.prepare_transaction())

        return await self.client.send_transaction(transaction)
