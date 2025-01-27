import asyncio
import copy
import random
import traceback

from modules import Logger, RequestClient, Client, CosmosClient, SolanaClient
from modules.interfaces import (
    SoftwareException, SoftwareExceptionWithoutRetry, SoftwareExceptionHandled
)
from utils.tools import helper, gas_checker, sleep, network_handler
from config.constants import (
    TOKENS_PER_CHAIN, OKX_NETWORKS_NAME, BINGX_NETWORKS_NAME,
    BINANCE_NETWORKS_NAME, CEX_WRAPPED_ID, BITGET_NETWORKS_NAME, CELESTIA_VALIDATORS, TOKENS_FOR_SWAPS
)
from dev_settings import Settings


class Custom(Logger, RequestClient):
    def __init__(self, client: Client):
        self.client = client
        Logger.__init__(self)
        RequestClient.__init__(self, client)

    async def wraps_abuser(self):
        chains = copy.deepcopy(Settings.SEARCH_CHAINS)

        current_client, index, balance, balance_in_wei, balances_in_usd = await self.balance_searcher(
            chains, native_check=True
        )

        return await Custom(current_client).wraps_abuser_util()

    @helper
    async def wraps_abuser_util(self):
        from functions import swap_1inch, swap_xyfinance

        func = {
            'Arbitrum': [swap_1inch],
            'Optimism': [swap_1inch],
            'Polygon': [swap_1inch],
            'BNB Chain': [swap_1inch],
            'Base': [swap_1inch],
            'Linea': [swap_xyfinance],
            'Scroll': [swap_xyfinance],
            'zkSync': [swap_1inch]
        }[self.client.network.name]

        current_tokens = list(TOKENS_PER_CHAIN[self.client.network.name].items())[:2]

        if not all(isinstance(amount, str) for amount in Settings.SWAP_AMOUNT):
            raise SoftwareExceptionWithoutRetry('SWAP_AMOUNT must use with % setting')

        wrapper_counter = 0
        for _ in range(2):
            wallet_balance = {k: await self.client.get_token_balance(k) for k, v in current_tokens}
            valid_wallet_balance = {k: v[1] for k, v in wallet_balance.items() if v[0] != 0}
            eth_price = await self.get_token_price('ETH')

            if 'ETH' in valid_wallet_balance:
                valid_wallet_balance['ETH'] = valid_wallet_balance['ETH'] * eth_price
            if 'WETH' in valid_wallet_balance:
                valid_wallet_balance['WETH'] = valid_wallet_balance['WETH'] * eth_price

            max_token = max(valid_wallet_balance, key=lambda x: valid_wallet_balance[x])

            if max_token == 'ETH' and wrapper_counter == 1:
                continue
            elif max_token == 'WETH' and wrapper_counter == 1:
                self.logger_msg(*self.client.acc_info, msg=f"Current balance in WETH, running unwrap")

            amounts = [int(i) for i in copy.deepcopy(Settings.SWAP_AMOUNT)]
            percent = round(random.uniform(*amounts), 9) / 100 if max_token == 'ETH' else 1
            amount_in_wei = int(wallet_balance[max_token][0] * percent)
            amount = self.client.custom_round(amount_in_wei / 10 ** 18, 6)

            if max_token == 'ETH':
                msg = f'Wrap {amount:.6f} ETH'
                from_token_name, to_token_name = 'ETH', 'WETH'
            else:
                msg = f'Unwrap {amount:.6f} WETH'
                from_token_name, to_token_name = 'WETH', 'ETH'

            self.logger_msg(*self.client.acc_info, msg=msg)

            if (max_token == 'ETH' and valid_wallet_balance[max_token] > 1
                    or max_token == 'WETH' and valid_wallet_balance[max_token] != 0):
                data = from_token_name, to_token_name, amount, amount_in_wei
                counter = 0
                result = False
                while True:
                    module_func = random.choice(func)
                    try:
                        result = await module_func(self.client, swap_data=data)
                        wrapper_counter += 1
                    except:
                        pass
                    if result or counter == 3:
                        break

            else:
                self.logger_msg(*self.client.acc_info, msg=f"{from_token_name} balance is too low (lower 1$)")

        return True

    async def custom_sleep(self, sleep_type):
        from dev_settings import Settings

        sleep_time = {
            1: Settings.CUSTOM_SLEEP_1,
            2: Settings.CUSTOM_SLEEP_2,
            3: Settings.CUSTOM_SLEEP_3,
        }[sleep_type]

        duration = random.randint(*sleep_time)
        self.logger_msg(*self.client.acc_info, msg=f"💤 Sleeping for {duration} seconds\n")
        await asyncio.sleep(duration)
        return True

    @helper
    async def smart_factory(
            self, func, chains, native_check: bool = True, wrapped_tokens: bool = False,
            raise_handle: bool = True, wrap_mode: bool = False, transfer_mode: bool = False, tokens: list = None
    ):

        converted_chains = copy.deepcopy(chains)
        if any([isinstance(item, tuple) for item in chains]):
            new_chains = []
            for item in chains:
                if isinstance(item, tuple):
                    new_chains.extend(item)
                else:
                    new_chains.append(item)
            converted_chains = new_chains

        client, index, balance, _, _ = await self.balance_searcher(
            converted_chains, tokens, native_check=native_check, raise_handle=raise_handle,
            wrapped_tokens=wrapped_tokens
        )

        if wrap_mode:
            if wrapped_tokens:
                return await func(client)
            amount = await client.get_smart_amount(Settings.WRAPS_AMOUNT)
            return await func(client, amount=amount)
        elif transfer_mode:
            amount = await client.get_smart_amount(Settings.TRANSFER_AMOUNT)
            return await func(client, amount=amount)

        return await func(client)

    @helper
    async def smart_wrap(self):
        from functions import wrap_eth

        chains = copy.deepcopy(Settings.SEARCH_CHAINS)

        return await self.smart_factory(wrap_eth, chains, wrap_mode=True)

    @helper
    async def smart_unwrap(self):
        from functions import unwrap_eth

        chains = copy.deepcopy(Settings.SEARCH_CHAINS)

        return await self.smart_factory(unwrap_eth, chains, native_check=False, wrapped_tokens=True)

    @helper
    async def smart_rubyscore(self):
        from functions import vote_rubyscore

        chains = [chain for chain in Settings.SEARCH_CHAINS if chain not in ["Arbitrum", "BNB Chain", "Optimism"]]

        return await self.smart_factory(vote_rubyscore, chains)

    @helper
    async def smart_check_in(self):
        from functions import check_in_owlto

        chains = [chain for chain in Settings.SEARCH_CHAINS if chain in [
            "BNB Chain", "Base", "Linea", "Manta", "Scroll", "zkSync"
        ]]

        return await self.smart_factory(check_in_owlto, chains)

    @helper
    async def smart_mintfun(self):
        from functions import mint_mintfun

        chains = [chain for chain in Settings.SEARCH_CHAINS if chain in ["Base", "Optimism", "Zora"]]

        return await self.smart_factory(mint_mintfun, chains)

    @helper
    async def smart_dmail(self):
        from functions import send_message_dmail

        chains = [chain for chain in Settings.SEARCH_CHAINS if chain in [
            "Base", "Linea", "Manta", "Optimism", "Scroll", "zkSync"
        ]]

        return await self.smart_factory(send_message_dmail, chains)

    @helper
    async def smart_transfer(self, random_address: bool = False):
        from functions import transfer_eth, transfer_eth_to_myself

        chains = copy.deepcopy(Settings.SEARCH_CHAINS)

        if random_address:
            return await self.smart_factory(transfer_eth, chains, transfer_mode=True)
        return await self.smart_factory(transfer_eth_to_myself, chains, transfer_mode=True)

    @helper
    async def smart_transfer_cosmos(self, random_address: bool = False):
        from functions import transfer_cosmos, transfer_cosmos_to_cex

        tokens = copy.deepcopy(['TIA', "NTRN", "INJ"])
        chains = copy.deepcopy(["Celestia", "Neutron", "Injective"])

        if random_address:
            return await self.smart_factory(
                transfer_cosmos, chains, tokens=tokens, native_check=False, transfer_mode=True
            )
        return await self.smart_factory(
            transfer_cosmos_to_cex, chains, tokens=tokens, native_check=False, transfer_mode=True
        )

    @helper
    async def stake_celestia(self):
        chains = ["Celestia"]
        tokens = ['TIA']

        validator_addresses = random.choice(CELESTIA_VALIDATORS)

        client, index, balance, _, _ = await self.balance_searcher(
            chains, tokens
        )

        amount = await client.get_smart_amount(Settings.STAKE_AMOUNT)

        client.logger_msg(
            *client.acc_info,
            msg=f"Staking {amount} TIA to Validator: {validator_addresses[:10]}...",
        )

        result = await client.stake_tia(validator=validator_addresses, amount=amount)

        await client.session.close()

        return result

    @helper
    async def smart_organic_swaps(self):
        from functions import (
            swap_izumi, swap_syncswap, swap_1inch, swap_pancake, swap_uniswap, swap_sushiswap, swap_ambient,
            swap_woofi, swap_spacefi, swap_jupiter, swap_dackieswap, swap_bebop
        )

        possible_tokens = copy.deepcopy(Settings.POSSIBLE_TOKENS)
        possible_chains = copy.deepcopy(Settings.SEARCH_CHAINS)

        new_tokens = []
        new_converted_chains = []
        for chain in possible_chains:
            for token in possible_tokens:
                if chain in ["Base", "Linea"] and token == 'USDT':
                    continue
                if (chain == "Solana" and token != 'SOL') or (chain != 55 and token == 'SOL'):
                    continue
                if (chain != "InEVM" and token == 'INJ') or (chain == 45 and token != 'INJ'):
                    continue
                new_tokens.append(token)
                new_converted_chains.append(chain)

        # current_client_copy = await self.client.new_client(OMNICHAIN_WRAPED_NETWORKS[45])
        # swap_data = 'USDC', 'INJ', 11.3312, int(11.3312 * 10 ** 6)
        # await swap_dackieswap(current_client_copy, swap_data=swap_data)
        #
        # return

        current_client, index, balance, balance_in_wei, balances_data = await self.balance_searcher(
            new_converted_chains, new_tokens, need_token_name=True, without_error=True
        )

        if balances_data[0] <= Settings.MINIMUM_ORGANIC_SWAP_AMOUNT:
            await current_client.session.close()
            return True

        modules = {
            'Arbitrum': [swap_1inch, swap_uniswap],
            'Base': [swap_1inch, swap_uniswap],
            'Linea': [swap_izumi, swap_syncswap, swap_pancake],
            'Scroll': [swap_izumi, swap_syncswap, swap_ambient, swap_sushiswap, swap_spacefi],
            'zkSync': [swap_izumi, swap_syncswap, swap_pancake, swap_woofi],
            'Optimism': [swap_1inch, swap_woofi],
            'Solana': [swap_jupiter],
            'inEVM': [swap_dackieswap],
            # 'Polygon ZKEVM': [swap_xyfinance],
            'BNB Chain': [swap_1inch],
            # 'Manta': [swap_xyfinance],
            #'Polygon': [swap_1inch],
            # 'Zora': [swap_oneinch],
            'Taiko': [swap_bebop]
        }[current_client.network.name]

        current_client_copy = await self.client.new_client(new_converted_chains[index])

        network_tokens = TOKENS_PER_CHAIN[current_client.network.name].keys()
        to_possible_tokens = []
        _, _, from_token_name = balances_data

        if from_token_name == 'USDbC':
            from_token_name = 'USDC.e'

        if 'USDT' in network_tokens:
            to_possible_tokens.append("USDT")
        if 'USDC' in network_tokens:
            if current_client.network.name == 'Base':
                to_possible_tokens.append("USDC.e")
            else:
                to_possible_tokens.append("USDC")

        if from_token_name != current_client.token:
            to_possible_tokens = [current_client.token]

        to_token_name = random.choice(to_possible_tokens)
        result_list = []

        for swap_count in range(2):
            if swap_count == 0 and result_list and result_list[0] is False:
                return True
            swap_module = random.choice(modules)

            if swap_count:
                amounts = ('100', '100')
                from_token_name, to_token_name = to_token_name, from_token_name
                current_client = current_client_copy
            else:
                if current_client.network.name == 'inEVM':
                    amounts = copy.deepcopy(Settings.DACKIESWAP_AMOUNT)
                else:
                    amounts = copy.deepcopy(Settings.SWAP_AMOUNT)

            while True:
                try:

                    fee_support = 0

                    if current_client.network.name == 'Solana':
                        decimals = await current_client.get_decimals(from_token_name)
                        if from_token_name == current_client.token:
                            fee_support = round(random.uniform(0.003, 0.004), 6)
                    elif from_token_name != current_client.token:
                        contract = current_client.get_contract(
                            TOKENS_PER_CHAIN[current_client.network.name][from_token_name])
                        decimals = await contract.functions.decimals().call()
                    else:
                        decimals = 18
                        fee_support = round(random.uniform(0.0003, 0.0004), 6)

                    if swap_count and from_token_name == current_client.token:
                        if current_client.network == 'BNB Chain':
                            fee_support += round(random.uniform(0.001, 0.001), 6)
                        elif current_client.network == 'Polygon':
                            fee_support += round(random.uniform(1, 1.1), 6)
                        elif current_client.network == 'Avalanche':
                            fee_support += round(random.uniform(0.006, 0.007), 6)
                        else:
                            fee_support += round(random.uniform(0.0003, 0.004), 6)

                    amount = await current_client.get_smart_amount(
                        settings=amounts, token_name=from_token_name, fee_support=fee_support
                    )

                    amount_in_wei = current_client.to_wei(amount, decimals)
                    swap_data = from_token_name, to_token_name, amount, amount_in_wei

                    result_list.append(await swap_module(current_client, swap_data=swap_data))

                    if swap_count == 0:
                        await sleep(self)

                    break

                except (SoftwareException, SoftwareExceptionWithoutRetry) as error:
                    raise error
                except Exception as error:
                    traceback.print_exc()
                    current_client.logger_msg(
                        *current_client.acc_info,
                        msg=f"Error during the route. Will try again in 1 min... Error: {error}", type_msg='warning'
                    )
                    await asyncio.sleep(60)

        if current_client_copy.session:
            await current_client_copy.session.close()

        if current_client.session:
            await current_client.session.close()

        return result_list

    @helper
    async def smart_organic_landings(self):
        from functions import Aave, Basilisk, EraLend, Keom, LayerBank, Moonwell, Seamless, ZeroLend

        possible_chains = copy.deepcopy(Settings.SEARCH_CHAINS)

        current_client, index, balance, balance_in_wei, balances_data = await self.balance_searcher(
            possible_chains, native_check=True
        )

        classes = {
            'Arbitrum': [Aave],
            'Base': [Aave, Moonwell, Seamless],
            'Linea': [LayerBank],
            'Scroll': [Aave, LayerBank],
            'zkSync': [Basilisk, EraLend, ZeroLend],
            'Optimism': [Aave],
            'Polygon ZKEVM': [Keom],
            'BNB Chain': [Aave],
            # 'Manta': [swap_xyfinance],
            # 'Polygon': [swap_1inch],
            # 'Zora': [swap_oneinch],
        }[current_client.network.name]

        result_list = []

        landing_class = random.choice(classes)
        for module_count in range(2):

            while True:
                try:

                    if not module_count:
                        amounts = copy.deepcopy(Settings.LANDINGS_AMOUNT)
                        fee_support = round(random.uniform(0.0004, 0.0005), 6)

                        amount = await current_client.get_smart_amount(settings=amounts, fee_support=fee_support)
                        amount_in_wei = current_client.to_wei(amount)

                        result_list.append(
                            await landing_class(current_client).deposit(amount=amount, amount_in_wei=amount_in_wei)
                        )
                    else:
                        result_list.append(await landing_class(current_client).withdraw())

                    if module_count == 0:
                        await sleep(self)

                    break

                except (SoftwareException, SoftwareExceptionWithoutRetry) as error:
                    raise error
                except Exception as error:
                    traceback.print_exc()
                    current_client.logger_msg(
                        *current_client.acc_info,
                        msg=f"Error during the route. Will try again in 1 min... Error: {error}", type_msg='warning'
                    )
                    await asyncio.sleep(60)

        if not current_client.session.closed:
            await current_client.session.close()

        return result_list

    @helper
    @gas_checker
    async def custom_swap(self, custom_type):
        from functions import swap_odos, swap_1inch, swap_xyfinance

        custom_swap_data = {
            1: Settings.FULL_CUSTOM_SWAP_DATA1,
            2: Settings.FULL_CUSTOM_SWAP_DATA2,
            3: Settings.FULL_CUSTOM_SWAP_DATA3,
        }[custom_type]

        tokens, swap_amounts, network = custom_swap_data

        current_client = await self.client.new_client(network)

        funcs = {
            'Base': [swap_1inch],
            'Ethereum': [swap_1inch],
            'Optimism': [swap_1inch],
            'Arbitrum': [swap_1inch],
            'Polygon': [swap_1inch],
            'BNB Chain': [swap_1inch],
            'Linea': [swap_odos],
            'zkSync': [swap_1inch],
            'Scroll': [swap_odos],
            'Taiko': [swap_xyfinance],
        }[current_client.network.name]

        swap_module = random.choice(funcs)

        from_token_address, to_token_address = tokens

        if isinstance(swap_amounts[0], str):
            if '0x' in from_token_address:
                amount_in_wei, amount, _ = await current_client.get_token_balance(
                    token_address=from_token_address, only_address=True
                )
            else:
                amount_in_wei, amount, _ = await current_client.get_token_balance(
                    token_name=from_token_address
                )

            swap_amounts = [float(number) for number in swap_amounts]
            percent = round(random.uniform(*swap_amounts), 9) / 100
            amount = round(amount * percent, 6)
        else:
            amount = round(random.uniform(*swap_amounts), 6)

        if from_token_address != current_client.token:
            decimals = await current_client.get_decimals(token_address=from_token_address)
        else:
            decimals = 18

        amount_in_wei = current_client.to_wei(amount, decimals)

        data = from_token_address, to_token_address, amount, amount_in_wei

        return await swap_module(current_client, swap_data=data)

    @helper
    @gas_checker
    async def custom_swaps(self):
        from functions import (
            swap_1inch, swap_izumi, swap_syncswap, swap_uniswap, swap_pancake, swap_ambient, swap_sushiswap,
            swap_spacefi, swap_maverick, swap_woofi, swap_jupiter, swap_dackieswap, swap_quickswap, swap_odos,
            swap_bebop
        )

        swap_amounts, single_dapp, double_swap, want_dapps = Settings.CUSTOM_SWAP_DATA[self.client.network.name]

        dapp_by_key = {
            1: swap_1inch,
            2: swap_odos,
            3: swap_syncswap,
            4: swap_izumi,
            5: swap_uniswap,
            6: swap_maverick,
            7: swap_pancake,
            8: swap_woofi,
            9: swap_ambient,
            10: swap_jupiter,
            11: swap_dackieswap,
            12: swap_quickswap,
            13: swap_sushiswap,
            14: swap_spacefi,
            15: swap_bebop
        }

        possible_modules = {
            'Ethereum': [1, 2],
            'Arbitrum': [1, 2, 5],
            'Base': [1, 2, 5, 6],
            'Linea': [2, 3, 4, 7],
            'Scroll': [2, 3, 4, 9, 13, 14],
            'zkSync': [2, 3, 4, 6, 7, 8],
            'Optimism': [1, 2, 8],
            'Solana': [10],
            'inEVM': [11],
            'Polygon ZKEVM': [12],
            'BNB Chain': [1, 2],
            # 'Manta': [swap_xyfinance],
            'Polygon': [1, 2],
            # 'Zora': [swap_oneinch],
            'Taiko': [4, 15],
        }[self.client.network.name]

        total_modules = []
        for module_number in want_dapps:
            if module_number in possible_modules:
                total_modules.append(dapp_by_key[module_number])

        if total_modules:
            swap_module = random.choice(total_modules)
        else:
            self.logger_msg(
                *self.client.acc_info,
                msg=f'{self.client.network.name} support only: {possible_modules} keys of modules',
                type_msg='warning'
            )
            return False

        token_per_chain = copy.deepcopy(TOKENS_FOR_SWAPS[self.client.network.name])
        del token_per_chain[f"W{self.client.token}"]

        wallet_balance = {
            k: await self.client.get_token_balance(token_name=k, swapcheck=True) for k, v in
            token_per_chain.items()
        }

        valid_wallet_balance = {
            token_name: token_balance[1] for token_name, token_balance in wallet_balance.items() if token_balance[0] != 0
        }

        for token_name in valid_wallet_balance.keys():
            token_price = await self.get_token_price(token_name)
            token_amount_usd = valid_wallet_balance[token_name] * token_price
            valid_wallet_balance[token_name] = self.client.custom_round(token_amount_usd, 6)

        if sum(valid_wallet_balance.values()) < 1:
            self.logger_msg(*self.client.acc_info, msg=f'Account balance < 1$', type_msg='warning')
            return False

        from_token_name = max(valid_wallet_balance, key=lambda x: valid_wallet_balance[x])

        amount_on_balance = wallet_balance[from_token_name][1]

        token_names_list = list(filter(
            lambda token_name: token_name != from_token_name, token_per_chain.keys()
        ))

        if from_token_name == 'ETH':
            if isinstance(swap_amounts[0], str):
                swap_amounts = [float(number) for number in swap_amounts]
            percent = round(random.uniform(*swap_amounts), 9) / 100
        else:
            percent = 1

        amount = self.client.custom_round(amount_on_balance * percent, 6)
        decimals = await self.client.get_decimals(token_name=from_token_name)
        amount_in_wei = self.client.to_wei(amount, decimals)

        for swap_time in range(double_swap + 1):
            counter = 0
            while True:
                result = False
                if not single_dapp:
                    swap_module = random.choice(total_modules)

                if from_token_name == self.client.token:
                    to_token_name = random.choice(token_names_list)
                else:
                    to_token_name = self.client.token

                swap_data = from_token_name, to_token_name, amount, amount_in_wei

                try:
                    self.logger_msg(*self.client.acc_info, msg=f'Launching swap module in {self.client.network.name}')

                    result = await swap_module(self.client, swap_data=swap_data)

                    if double_swap:
                        await sleep(self)

                    if not result:
                        counter += 1

                except Exception as error:
                    self.logger_msg(*self.client.acc_info, msg=f'{error}', type_msg='warning')
                    counter += 1

                if result or counter == 3:
                    break

        return True

    @helper
    async def collect_eth_util(self):
        from functions import (
            swap_1inch, swap_syncswap, unwrap_eth, swap_odos
        )

        self.logger_msg(
            *self.client.acc_info,
            msg=f"Started collecting tokens to {self.client.token} in {self.client.network.name}"
        )

        func = {
            'Base': [swap_1inch],
            'Ethereum': [swap_1inch],
            'Optimism': [swap_1inch],
            'Arbitrum': [swap_1inch],
            'Polygon': [swap_1inch],
            'BNB Chain': [swap_1inch],
            'Linea': [swap_syncswap],
            'zkSync': [swap_syncswap],
            'Scroll': [swap_syncswap],
        }.get(self.client.network.name, swap_1inch)

        chain_tokens_data = copy.deepcopy(Settings.COLLECTOR_DATA[self.client.network.name])

        wallet_balance = {}
        for token_name, token_address in chain_tokens_data.items():
            wallet_balance[token_name] = await self.client.get_token_balance(
                token_address=token_address, only_address=True
            )

        valid_wallet_balance = {k: v[1] for k, v in wallet_balance.items() if v[0] != 0}

        odos_flag = False
        if len(valid_wallet_balance.values()) >= 1:
            try:
                for token_name, token_balance in valid_wallet_balance.items():
                    if token_name != self.client.token:
                        amount_in_wei = wallet_balance[token_name][0]
                        amount = round(wallet_balance[token_name][1] * 0.999999, 6)
                        self.logger_msg(
                            *self.client.acc_info,
                            msg=f'Found {amount} {token_name} in {self.client.network.name}', type_msg='success'
                        )
                        if amount > Settings.COLLECTOR_MIN_AMOUNTS.get(token_name, 1):
                            from_token_name, to_token_name = token_name, self.client.token
                            if from_token_name not in list(TOKENS_PER_CHAIN[self.client.network.name].keys()):
                                odos_flag = True
                                data = chain_tokens_data[from_token_name], to_token_name, amount, amount_in_wei
                            else:
                                data = from_token_name, to_token_name, amount, amount_in_wei
                            counter = 0

                            swap_client = await self.client.new_client(self.client.network.name)

                            while True:
                                result = False
                                if from_token_name == f'W{self.client.token}':
                                    module_func = unwrap_eth
                                    data = amount
                                elif odos_flag:
                                    module_func = swap_odos
                                else:
                                    module_func = random.choice(func)

                                try:
                                    self.logger_msg(
                                        *self.client.acc_info, msg=f'Launching swap module', type_msg='warning'
                                    )
                                    if from_token_name == f'W{self.client.token}':
                                        result = await module_func(swap_client, amount=data)
                                    else:
                                        result = await module_func(swap_client, swap_data=data)
                                    await sleep(self, 10, 50)

                                    if not result:
                                        counter += 1
                                except Exception as error:
                                    self.logger_msg(
                                        *self.client.acc_info, msg=f'Error in collector: {error}', type_msg='warning'
                                    )
                                    counter += 1
                                    pass
                                if result or counter == 3:
                                    break

                            if not swap_client.session.closed:
                                await swap_client.session.close()

                        else:
                            self.logger_msg(*self.client.acc_info, msg=f"{token_name} balance < 1$")
            except Exception as error:
                self.logger_msg(*self.client.acc_info, msg=f"Error in collector route. Error: {error}")
        else:
            self.logger_msg(*self.client.acc_info, msg=f"Account balance already in ETH!", type_msg='warning')

        return True

    @helper
    async def collector_eth(self):
        from utils.networks import (
            ArbitrumRPC, OptimismRPC, BaseRPC, LineaRPC, zkSyncEraRPC, ScrollRPC, EthereumRPC, PolygonRPC, BSC_RPC
        )
        from functions import collect_eth_util

        for network in list(Settings.COLLECTOR_DATA.keys()):
            network_rpc = {
                'Arbitrum': ArbitrumRPC,
                'Optimism': OptimismRPC,
                "Base": BaseRPC,
                "Linea": LineaRPC,
                "zkSync": zkSyncEraRPC,
                "Scroll": ScrollRPC,
                "Polygon": PolygonRPC,
                "BNB Chain": BSC_RPC,
                "Ethereum": EthereumRPC
            }[network]

            try:
                self.client.module_input_data['network'] = network_rpc
                await collect_eth_util(self.client.module_input_data)
            except Exception as error:
                self.logger_msg(
                    *self.client.acc_info, msg=f"Collector in {network_rpc.name} was crashed: {error}", type_msg='error'
                )
        return True

    @helper
    async def balance_average(self):
        from functions import okx_withdraw_util, bingx_withdraw_util, binance_withdraw_util, bitget_withdraw_util

        self.logger_msg(*self.client.acc_info, msg=f"Start checking all balances to make it average")

        balancer_data_copy = copy.deepcopy(Settings.CEX_BALANCER_CONFIG)

        count = 0
        client = None
        for data in balancer_data_copy:
            while True:
                try:
                    cex_network, wanted_balance, cex_wanted = data
                    if isinstance(cex_network, (tuple, list)):
                        cex_wanted = random.choice(cex_wanted)

                    func, cex_config = {
                        1: (okx_withdraw_util, OKX_NETWORKS_NAME),
                        2: (bingx_withdraw_util, BINGX_NETWORKS_NAME),
                        3: (binance_withdraw_util, BINGX_NETWORKS_NAME),
                        4: (bitget_withdraw_util, BITGET_NETWORKS_NAME),
                    }[cex_wanted]

                    dapp_tokens = [f"{cex_config[cex_network].split('-')[0]}{'.e' if cex_network in [29, 30] else ''}"]
                    dapp_chains = [CEX_WRAPPED_ID[cex_network]]

                    client, index, balance, balance_in_wei, balance_data = await self.balance_searcher(
                        chains=dapp_chains, tokens=dapp_tokens, silent_mode=True, balancer_mode=True
                    )

                    dep_token = dapp_tokens[index]
                    balance_in_usd, token_price = balance_data
                    wanted_amount_in_usd = float(f'{wanted_balance * token_price:.2f}')

                    if wanted_amount_in_usd > balance_in_usd:
                        need_to_withdraw = float(f"{(wanted_amount_in_usd - balance_in_usd) / token_price:.6f}")

                        if need_to_withdraw * token_price < 1:
                            self.logger_msg(
                                *self.client.acc_info,
                                msg=f"Amount lower than 1$, will set 1$ to withdraw", type_msg='warning'
                            )
                            need_to_withdraw = round(random.uniform(1.0, 1.1) / token_price, 6)
                        else:
                            self.logger_msg(
                                *self.client.acc_info,
                                msg=f"Not enough balance on account in {client.network.name}, launch CEX withdraw module"
                            )

                        await func(client, withdraw_data=(cex_network, (need_to_withdraw, need_to_withdraw)))
                    else:
                        self.logger_msg(
                            *self.client.acc_info,
                            msg=f"Account have enough {dep_token} balance in {client.network.name}", type_msg='success'
                        )
                    await asyncio.sleep(10)
                    break
                except Exception as error:
                    count += 1
                    if count == 3:
                        raise SoftwareException(f"Exception: {error}")
                    self.logger_msg(*self.client.acc_info, msg=f"Exception: {error}", type_msg='error')
                finally:
                    if client:
                        await client.session.close()
        return True

    async def smart_swap_for_bridging(self, reverse: bool = False):
        if not reverse:
            tokens = ['ETH', 'BNB', 'ETH']
        else:
            tokens = ['TIA.n', 'ZBC', 'TIA.n']

        chains = ["Abitrum", "BNB Chain", "Manta"]

        current_client, index, balance, balance_in_wei, balances_in_usd = await self.balance_searcher(
            chains, tokens
        )

        if current_client.network.name == 'Arbitrum':
            return await Custom(current_client).swap_tia_arb(reverse=reverse)
        elif current_client.network.name == 'Manta':
            return await Custom(current_client).swap_tia_manta(reverse=reverse)
        elif current_client.network.name == 'BNB Chain':
            return await Custom(current_client).swap_zbc_bsc(reverse=reverse)
        else:
            raise SoftwareExceptionWithoutRetry(f'Uncorrected network: {current_client.network.name}!')

    @helper
    async def swap_tia_arb(self, reverse: bool = False):
        from functions import swap_jumper_custom

        if not reverse:
            from_token_name = 'ETH'
            to_token_name = 'TIA.n'
            amount = await self.client.get_smart_amount(Settings.ARBITRUM_TIA_SWAP_AMOUNT)
            amount = round(amount - 0.0005, 6)
            amount_in_wei = self.client.to_wei(amount)
        else:
            from_token_name = 'TIA.n'
            to_token_name = 'ETH'
            _, amount, _ = await self.client.get_token_balance(from_token_name)
            amount = round(amount, 6)
            amount_in_wei = self.client.to_wei(amount, 6)

        bridge_data = 'Arbitrum', 'Arbitrum', from_token_name, to_token_name, amount, amount_in_wei

        return await swap_jumper_custom(self.client, bridge_data=bridge_data, swap_mode=True)

    @helper
    async def ambient_wrseth_scroll(self, reverse: bool = False):
        from functions import Ambient

        liquidity_client = await self.client.new_client('Scroll')

        if not reverse:
            from_token_name = 'ETH'
            to_token_name = 'wrsETH'
            amount = await self.client.get_smart_amount(Settings.AMBIENT_WRSETH_AMOUNT)
            amount = self.client.custom_round(amount + 0.0005, 6)
            amount_in_wei = self.client.to_wei(amount)
        else:
            await Ambient(liquidity_client).remove_liquidity_wrseth()
            from_token_name = 'wrsETH'
            to_token_name = 'ETH'
            _, amount, _ = await self.client.get_token_balance(from_token_name)
            amount = self.client.custom_round(amount, 6)
            amount_in_wei = self.client.to_wei(amount, 18)
            
        swap_data = from_token_name, to_token_name, amount, amount_in_wei

        if reverse:
            await asyncio.sleep(random.randint(10, 20))
            return await Ambient(self.client).swap(swap_data=swap_data)
        else:
            await Ambient(self.client).swap(swap_data=swap_data)
            await asyncio.sleep(random.randint(10, 20))
            return await Ambient(liquidity_client).add_liquidity_wrseth(amount - 0.0005)

    @helper
    async def swap_ezeth(self, reverse: bool = False):
        from functions import swap_1inch

        if not reverse:
            tokens = ['ETH' for _ in range(len(Settings.RENZO_CHAINS))]
        else:
            tokens = ['ezETH' for _ in range(len(Settings.RENZO_CHAINS))]

        chains = copy.deepcopy(Settings.RENZO_CHAINS)

        current_client, index, balance, balance_in_wei, balances_in_usd = await self.balance_searcher(
            chains, tokens
        )

        if not reverse:
            from_token_name = 'ETH'
            to_token_name = 'ezETH'
            amount = await current_client.get_smart_amount(Settings.RENZO_EZETH_SWAP_AMOUNT)
            amount = self.client.custom_round(amount - 0.0005, 6)
            amount_in_wei = current_client.to_wei(amount)
        else:
            from_token_name = 'ezETH'
            to_token_name = 'ETH'
            _, amount, _ = await current_client.get_token_balance(from_token_name)
            amount = self.client.custom_round(amount, 6)
            amount_in_wei = current_client.to_wei(amount, 18)

        swap_data = from_token_name, to_token_name, amount, amount_in_wei

        return await swap_1inch(current_client, swap_data=swap_data)

    @helper
    async def swap_zbc_bsc(self, reverse: bool = False):
        from functions import swap_1inch

        if not reverse:
            from_token_name = 'BNB'
            to_token_name = 'ZBC'
            amount = await self.client.get_smart_amount(Settings.ONEINCH_SWAP_AMOUNT)
            amount = round(amount - 0.001, 6)

            amount_in_wei = self.client.to_wei(amount)
        else:
            from_token_name = 'ZBC'
            to_token_name = 'BNB'
            _, amount, _ = await self.client.get_token_balance(from_token_name)
            amount_in_wei = self.client.to_wei(amount, 9)

        swap_data = from_token_name, to_token_name, amount, amount_in_wei

        return await swap_1inch(self.client, swap_data=swap_data)

    @helper
    async def swap_tia_manta(self, reverse: bool = False):
        from functions import swap_openocean

        if not reverse:
            from_token_name = 'ETH'
            to_token_name = 'TIA.n'
            amount = await self.client.get_smart_amount(Settings.MANTA_TIA_SWAP_AMOUNT)
            amount = round(amount - 0.0005, 6)
            amount_in_wei = self.client.to_wei(amount)
        else:
            from_token_name = 'TIA.n'
            to_token_name = 'ETH'
            _, amount, _ = await self.client.get_token_balance(from_token_name)
            amount_in_wei = self.client.to_wei(amount, 6)

        swap_data = from_token_name, to_token_name, amount, amount_in_wei

        return await swap_openocean(self.client, swap_data=swap_data)

    async def refuel_nautilus(self):
        from functions import Nautilus
        class_name = Nautilus
        tokens = ['ZBC', 'ZBC']
        chains = ["BNB Chain", "Nautilus"]
        amounts = Settings.REFUEL_NAUTILUS_AMOUNT
        module_bridge_count = 1
        run_times = 1

        custom_data = class_name, run_times, tokens, chains, amounts, module_bridge_count

        return await self.smart_bridge_omnichain(dapp_id=4, custom_data=custom_data)

    @helper
    @gas_checker
    async def smart_random_approve(self, custom_rpc: bool = False):
        amount = random.uniform(1, 1000)
        while True:
            client = None
            try:
                from config.constants import (
                    IZUMI_CONTRACTS, RANGO_CONTRACTS, ODOS_CONTRACTS, ONEINCH_CONTRACTS,
                    OPENOCEAN_CONTRACTS, XYFINANCE_CONTRACTS, TOKENS_PER_CHAIN
                )

                all_contracts = {
                    "Rango.Exchange": RANGO_CONTRACTS,
                    "iZumi": IZUMI_CONTRACTS,
                    "ODOS": ODOS_CONTRACTS,
                    "1inch": ONEINCH_CONTRACTS,
                    "OpenOcean": OPENOCEAN_CONTRACTS,
                    "XYfinance": XYFINANCE_CONTRACTS,
                }

                if not custom_rpc:
                    chains = Settings.SEARCH_CHAINS

                    converted_chains = copy.deepcopy(chains)
                    if any([isinstance(item, tuple) for item in chains]):
                        new_chains = []
                        for item in chains:
                            if isinstance(item, tuple):
                                new_chains.extend(item)
                            else:
                                new_chains.append(item)
                        converted_chains = new_chains

                    client, index, _, _, _ = await self.balance_searcher(
                        converted_chains, native_check=True, random_mode=True
                    )

                    network_name = client.network.name
                else:
                    network_name = self.client.network.name
                    client = self.client

                all_network_contracts = {
                    name: contracts[network_name]['router']
                    for name, contracts in all_contracts.items()
                    if contracts.get(network_name)
                }

                approve_contracts = [(k, v) for k, v in all_network_contracts.items()]
                contract_name, approve_contract = random.choice(approve_contracts)
                native = [client.network.token, f"W{client.network.token}"]
                token_contract = random.choice(
                    [i for i in list(TOKENS_PER_CHAIN[network_name].items()) if i[0] not in native]
                )
                amount *= 1.1
                amount_in_wei = self.client.to_wei(amount, await client.get_decimals(token_contract[0]))

                message = f"Approve {amount:.4f} {token_contract[0]} for {contract_name}"
                self.logger_msg(*client.acc_info, msg=message)

                result = await client.check_for_approved(
                    token_contract[1], approve_contract, amount_in_wei, without_bal_check=True
                )

                if not result:
                    raise SoftwareException('Bad approve, trying again with higher amount...')
                return result
            finally:
                if client:
                    await client.session.close()

    @helper
    async def get_fee_support_for_arb(self):
        return await self.get_fee_support_for_txs(custom_fee_support_data={
            2: (0.0011, 0.0012)
        })

    @helper
    async def get_fee_support_for_base(self):
        return await self.get_fee_support_for_txs(custom_fee_support_data={
            6: (0.00204, 0.0021)
        })

    @helper
    async def get_fee_support_for_txs(self, custom_fee_support_data: dict = None):
        """
        2 - ETH-Arbitrum One
        3 - ETH-Optimism
        4 - ETH-zkSync Era
        5 - ETH-Linea
        6 - ETH-Base
        """

        from functions import okx_withdraw_util, bingx_withdraw_util, binance_withdraw_util, bitget_withdraw_util

        self.logger_msg(*self.client.acc_info, msg=f"Start checking all balances to withdraw fee support")

        if custom_fee_support_data:
            fee_support_data = custom_fee_support_data
        else:
            fee_support_data = copy.deepcopy(Settings.FEE_SUPPORT_DATA)

        cex_wanted = random.choice(Settings.FEE_SUPPORT_CEXS)
        cex_networks = list(fee_support_data.keys())

        count = 0
        client = None
        try:
            if isinstance(cex_wanted, (tuple, list)):
                cex_wanted = random.choice(cex_wanted)

            func, cex_config = {
                1: (okx_withdraw_util, OKX_NETWORKS_NAME),
                2: (bingx_withdraw_util, BINGX_NETWORKS_NAME),
                3: (binance_withdraw_util, BINGX_NETWORKS_NAME),
                4: (bitget_withdraw_util, BITGET_NETWORKS_NAME),
            }[cex_wanted]

            dapp_tokens = [cex_config[cex_network].split('-')[0] for cex_network in cex_networks]
            dapp_chains = [CEX_WRAPPED_ID[cex_network] for cex_network in cex_networks]

            client, index, balance, balance_in_wei, balance_data = await self.balance_searcher(
                chains=dapp_chains, tokens=dapp_tokens, silent_mode=True, balancer_mode=True
            )

            current_cex_network = cex_networks[index]
            wanted_balance = fee_support_data[current_cex_network]

            dep_token = dapp_tokens[index]
            balance_in_usd, token_price = balance_data
            wanted_amount_in_usd = float(f'{random.uniform(*wanted_balance) * token_price:.2f}')

            if wanted_amount_in_usd > balance_in_usd:
                need_to_withdraw = float(f"{wanted_amount_in_usd:.6f}")

                min_fee_support = round(random.uniform(*copy.deepcopy(Settings.FEE_SUPPORT_MIN_WITHDRAW)), 4)

                if need_to_withdraw > min_fee_support:
                    self.logger_msg(
                        *self.client.acc_info,
                        msg=f"Need to withdraw: {need_to_withdraw:.2f}$ > min fee support {min_fee_support:.2f}$,"
                            f" launch CEX withdraw module"
                    )

                    need_to_withdraw = round(need_to_withdraw / token_price, 6)

                    return await func(client, withdraw_data=(current_cex_network, (need_to_withdraw, need_to_withdraw)))
                else:
                    self.logger_msg(
                        *self.client.acc_info,
                        msg=f"Need to withdraw: {need_to_withdraw:.2f}$ < min fee support {min_fee_support:.2f}$,"
                            f" will skil module", type_msg='warning'
                    )

            else:
                self.logger_msg(
                    *self.client.acc_info,
                    msg=f"Account have enough {balance_in_usd:.2f}($) {dep_token} balance in {client.network.name}",
                    type_msg='success'
                )
            await asyncio.sleep(10)

        except Exception as error:
            count += 1
            if count == 3:
                raise SoftwareException(f"{error}")
            self.logger_msg(*self.client.acc_info, msg=f"{error}", type_msg='error')
            traceback.print_exc()
        finally:
            if client:
                await client.session.close()

        return True

    @helper
    async def smart_bridge_omnichain(self, dapp_id: int = None, custom_data: tuple = None):
        from functions import UseNexus, Merkly, InEVM, Nautilus, Stargate, DeBridge, Jumper, SquidRouter, Rango, RenzoBridge
        from utils.tools import get_current_progress_for_bridge, write_into_bridge_temp_file

        class_name, run_times, tokens, chains, amounts, module_bridge_count, limiter = {
            1: (UseNexus, Settings.USENEXUS_RUN_TIMES, Settings.USENEXUS_TOKENS, Settings.USENEXUS_CHAINS, Settings.USENEXUS_AMOUNT, Settings.USENEXUS_BRIDGE_COUNT, Settings.USENEXUS_AMOUNT_LIMITER),
            2: (Merkly, Settings.MERKLY_RUN_TIMES, Settings.MERKLY_TOKENS, Settings.MERKLY_CHAINS, Settings.MERKLY_AMOUNT, Settings.MERKLY_BRIDGE_COUNT, Settings.MERKLY_AMOUNT_LIMITER),
            3: (InEVM, Settings.INEVM_RUN_TIMES, Settings.INEVM_TOKENS, Settings.INEVM_CHAINS, Settings.INEVM_AMOUNT, Settings.INEVM_BRIDGE_COUNT, Settings.INEVM_AMOUNT_LIMITER),
            4: (Nautilus, Settings.NAUTILUS_RUN_TIMES, Settings.NAUTILUS_TOKENS, Settings.NAUTILUS_CHAINS, Settings.NAUTILUS_AMOUNT, Settings.NAUTILUS_BRIDGE_COUNT, Settings.NAUTILUS_AMOUNT_LIMITER),
            5: (Stargate, Settings.STARGATE_RUN_TIMES, Settings.STARGATE_TOKENS, Settings.STARGATE_CHAINS, Settings.STARGATE_AMOUNT, Settings.STARGATE_BRIDGE_COUNT, Settings.STARGATE_AMOUNT_LIMITER),
            6: (DeBridge, Settings.DEBRIDGE_RUN_TIMES, Settings.DEBRIDGE_TOKENS, Settings.DEBRIDGE_CHAINS, Settings.DEBRIDGE_AMOUNT, Settings.DEBRIDGE_BRIDGE_COUNT, Settings.DEBRIDGE_AMOUNT_LIMITER),
            7: (Jumper, Settings.JUMPER_RUN_TIMES, Settings.JUMPER_TOKENS, Settings.JUMPER_CHAINS, Settings.JUMPER_AMOUNT, Settings.JUMPER_BRIDGE_COUNT, Settings.JUMPER_AMOUNT_LIMITER),
            8: (SquidRouter, Settings.SQUIDROUTER_RUN_TIMES, Settings.SQUIDROUTER_TOKENS, Settings.SQUIDROUTER_CHAINS, Settings.SQUIDROUTER_AMOUNT, Settings.SQUIDROUTER_BRIDGE_COUNT, Settings.SQUIDROUTER_AMOUNT_LIMITER),
            9: (Rango, Settings.RANGO_RUN_TIMES, Settings.RANGO_TOKENS, Settings.RANGO_CHAINS, Settings.RANGO_AMOUNT, Settings.RANGO_BRIDGE_COUNT, Settings.RANGO_AMOUNT_LIMITER2),
            10: (RenzoBridge, Settings.RENZO_RUN_TIMES, Settings.RENZO_TOKENS, Settings.RENZO_CHAINS, Settings.RENZO_AMOUNT, Settings.RENZO_BRIDGE_COUNT, Settings.RENZO_AMOUNT_LIMITER),
        }[dapp_id]

        if custom_data:
            class_name, run_times, tokens, chains, amounts, module_bridge_count = custom_data

        converted_chains = copy.deepcopy(chains)
        if any([isinstance(item, (tuple, list)) for item in chains]):
            new_chains = []
            for item in chains:
                if isinstance(item, (tuple, list)):
                    new_chains.extend(item)
                else:
                    new_chains.append(item)
            converted_chains = new_chains

        start_chain = None
        used_chains = []
        result_list = []
        count_copy = copy.deepcopy(module_bridge_count)
        total_bridge_count = random.choice(count_copy) if isinstance(count_copy, list) else count_copy

        for bridge_count in range(run_times):
            temp_bridge_count = get_current_progress_for_bridge(
                account_name=self.client.account_name, bridge_name=class_name.__name__
            )
            while True:
                try:
                    current_client, index, balance, balance_in_wei, balances_data = await self.balance_searcher(
                        converted_chains, tokens
                    )

                    if balance_in_wei == 0:
                        raise SoftwareExceptionWithoutRetry(f'Software can`t bridge 0 {tokens[index]}')

                    from_token_name = tokens[index]

                    if dapp_id in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:

                        try:
                            if any([isinstance(path, tuple) for path in chains]) and not isinstance(chains, tuple):
                                tuple_chains = chains[-1]
                                if not isinstance(tuple_chains, tuple) and not all(
                                        isinstance(chain, int) for chain in chains[0: -1]
                                ) and len(chains) != 2:
                                    setting_format = '[chain, chain, ..., (chain, chain, ...)]'
                                    raise SoftwareExceptionWithoutRetry(
                                        f'This mode on Omni-Chain Bridges support only {setting_format} format'
                                    )

                                if temp_bridge_count + 1 == total_bridge_count:
                                    final_chains = [chain for chain in chains if isinstance(chain, int)]
                                    available_chains = [chain for chain in final_chains if chain != converted_chains[index]]
                                    dst_chain_name = random.choice(available_chains)
                                elif temp_bridge_count + 1 == 1:
                                    try:
                                        dst_chain_name = tuple_chains[0]
                                    except TypeError:
                                        dst_chain_name = tuple_chains
                                else:
                                    available_tuple_chains = [
                                        chain for chain in tuple_chains if chain != converted_chains[index]
                                    ]
                                    dst_chain_name = random.choice(available_tuple_chains)
                            elif isinstance(chains[0], list) and isinstance(chains[1], list):
                                dst_chain_name = random.choice(chains[-1])
                            elif isinstance(chains, tuple):
                                try:
                                    if isinstance(chains[temp_bridge_count + 1], tuple):
                                        dst_chain_name = random.choice(chains[temp_bridge_count + 1])
                                    else:
                                        dst_chain_name = chains[temp_bridge_count + 1]
                                except IndexError:
                                    self.logger_msg(
                                        *self.client.acc_info, msg=f'Module got maximum bridges with your settings!',
                                        type_msg='warning'
                                    )
                                    return True
                            else:
                                if not start_chain:
                                    start_chain = converted_chains[index]
                                used_chains.append(start_chain)

                                if len(used_chains) >= len(chains):
                                    dst_chain_name = random.choice(
                                        [chain for chain in converted_chains if chain != converted_chains[index]])
                                else:
                                    available_chains = [chain for chain in converted_chains if chain not in used_chains]
                                    dst_chain_name = random.choice(available_chains)

                                used_chains.append(dst_chain_name)
                        except IndexError:
                            self.logger_msg(
                                *self.client.acc_info, msg=f'Can`t get dst network, will skip module',
                                type_msg='warning'
                            )
                            traceback.print_exc()
                            return True
                    else:
                        raise SoftwareExceptionWithoutRetry(f'Incorrect module "{dapp_id}" in Software')

                    src_chain_name = current_client.network.name
                    to_token_name = tokens[converted_chains.index(dst_chain_name)]

                    if src_chain_name == dst_chain_name:
                        raise SoftwareException(
                            f'Can`t bridge into same network: SRC Chain:{src_chain_name}, DST Chain:{dst_chain_name}'
                        )

                    if from_token_name != current_client.token:
                        if isinstance(current_client, CosmosClient):
                            decimals = {
                                'TIA.n': 6,
                                'TIA': 6,
                                'NTRN': 6,
                                'INJ': 18,
                            }[from_token_name]
                        elif isinstance(current_client, SolanaClient):
                            decimals = {
                                'ZBC': 9,
                                'SOL': 9,
                                'USDC': 6,
                            }[from_token_name]
                        else:
                            contract = current_client.get_contract(
                                TOKENS_PER_CHAIN[current_client.network.name][from_token_name])
                            decimals = await contract.functions.decimals().call()
                    else:
                        decimals = 18

                    amount_in_wei = self.client.to_wei((
                        await current_client.get_smart_amount(amounts, token_name=tokens[index])
                    ), decimals)

                    amount = f"{amount_in_wei / 10 ** decimals:.4f}"

                    balance_in_usd, token_price = balances_data
                    limit_amount, wanted_to_hold_amount = limiter
                    min_wanted_amount, max_wanted_amount = min(wanted_to_hold_amount), max(wanted_to_hold_amount)

                    if balance_in_usd >= limit_amount:
                        min_hold_balance = random.uniform(min_wanted_amount, max_wanted_amount) / token_price
                        if balance - min_hold_balance > 0:
                            if balance < float(amount) and from_token_name == current_client.token:
                                bridge_amount = self.client.custom_round(float(amount), 6)
                            else:
                                bridge_amount = float(amount)

                            if balance - bridge_amount < min_hold_balance:
                                need_to_freeze_amount = min_hold_balance - (balance - bridge_amount)
                                bridge_amount = self.client.custom_round(bridge_amount - need_to_freeze_amount, 6)

                            if bridge_amount < 0:
                                raise SoftwareExceptionHandled(
                                    f'Set LIMITER[2 value] lower than {wanted_to_hold_amount}. '
                                    f'Current amount = {bridge_amount} {from_token_name}')

                            bridge_amount_in_usd = bridge_amount * token_price
                            if balance_in_usd >= bridge_amount_in_usd:
                                pass
                            else:
                                info = f"{balance_in_usd:.2f}$ < {bridge_amount_in_usd:.2f}$"
                                raise SoftwareExceptionHandled(
                                    f'Account {from_token_name} balance < wanted bridge amount: {info}')
                        else:
                            full_need_amount = self.client.custom_round(min_hold_balance, 6)
                            info = f"{balance:.2f} {from_token_name} < {full_need_amount:.2f} {from_token_name}"
                            raise SoftwareExceptionHandled(f'Account {from_token_name} balance < hold amount: {info}')
                    else:
                        info = f"{balance_in_usd:.2f}$ < {limit_amount:.2f}$"
                        raise SoftwareExceptionHandled(
                            f'Account {from_token_name} balance < wanted limit amount: {info}'
                        )

                    bridge_amount_in_wei = current_client.to_wei(bridge_amount, decimals)

                    if bridge_amount_in_wei == 0:
                        raise SoftwareExceptionWithoutRetry('You can`t bridge Zero amount')

                    bridge_data = (
                        src_chain_name, dst_chain_name, from_token_name, to_token_name,
                        bridge_amount, bridge_amount_in_wei
                    )

                    if dapp_id in [2, 10]:
                        result_list.append(await class_name(current_client).bridge_token(bridge_data=bridge_data))
                    else:
                        result_list.append(await class_name(current_client).bridge(bridge_data=bridge_data))

                    if not custom_data:
                        write_into_bridge_temp_file(
                            account_name=current_client.account_name, bridge_name=class_name.__name__, bridge_count_plus=True
                        )

                    if current_client:
                        await current_client.session.close()

                    if bridge_count < run_times != 1:
                        await sleep(self)

                    break
                except asyncio.TimeoutError:
                    self.logger_msg(
                        *self.client.acc_info,
                        msg=f"Bad connection with RPC. Will try again in 1 min...", type_msg='warning'
                    )
                except (SoftwareException, SoftwareExceptionWithoutRetry) as error:
                    raise error
                except Exception as error:
                    if 'No router enrolled for domain' in str(error):
                        raise SoftwareException(f"Module {class_name.__name__} do not support your route!")
                    traceback.print_exc()
                    self.logger_msg(
                        *self.client.acc_info,
                        msg=f"Error during the route. Will try again in 1 min... Error: {error}", type_msg='warning'
                    )
                    await asyncio.sleep(60)

        if total_bridge_count != 1:
            return all(result_list)
        return any(result_list)

    @helper
    async def smart_swaps(self, dapp_id: int = None):
        from functions import Jumper, DeBridge, SquidRouter

        class_name, tokens, chains, amounts, module_bridge_count, limiter, swap_tokens = {
            1: (Jumper, Settings.JUMPER_TOKENS, Settings.JUMPER_CHAINS, Settings.JUMPER_AMOUNT, Settings.JUMPER_BRIDGE_COUNT, Settings.JUMPER_AMOUNT_LIMITER, Settings.JUMPER_SWAP_TOKENS),
            2: (DeBridge, Settings.DEBRIDGE_TOKENS, Settings.DEBRIDGE_CHAINS, Settings.DEBRIDGE_AMOUNT, Settings.DEBRIDGE_BRIDGE_COUNT, Settings.DEBRIDGE_AMOUNT_LIMITER, Settings.DEBRIDGE_SWAP_TOKENS),
            3: (SquidRouter, Settings.SQUIDROUTER_TOKENS, Settings.SQUIDROUTER_CHAINS, Settings.SQUIDROUTER_AMOUNT, Settings.SQUIDROUTER_BRIDGE_COUNT, Settings.SQUIDROUTER_AMOUNT_LIMITER, Settings.SQUIDROUTER_SWAP_TOKENS),
        }[dapp_id]

        result_list = []
        converted_chains = copy.deepcopy(chains)

        if any([isinstance(item, tuple) for item in chains]):
            new_chains = []
            for item in chains:
                if isinstance(item, tuple):
                    new_chains.extend(item)
                else:
                    new_chains.append(item)
            converted_chains = new_chains

        for swap_count in range(2):
            while True:
                try:
                    possible_tokens = copy.deepcopy(swap_tokens)

                    if swap_count == 1:
                        tokens = []
                        new_converted_chains = []
                        for chain in converted_chains:
                            for token in possible_tokens:
                                if token == 'fUSDC' and chain != 1:
                                    pass
                                else:
                                    tokens.append(token)
                                    new_converted_chains.append(chain)
                    else:
                        new_converted_chains = list(converted_chains)

                    current_client, index, balance, balance_in_wei, balances_data = await self.balance_searcher(
                        new_converted_chains, tokens, need_token_name=True
                    )

                    _, _, from_token_name = balances_data

                    src_chain_name = current_client.network.name
                    dst_chain_name = current_client.network.name

                    if src_chain_name == 'Base' and from_token_name == 'USDbC':
                        from_token_name = 'USDC.e'

                    if from_token_name != self.client.token:
                        to_token_name = self.client.token
                    else:
                        to_token_name = random.choice(possible_tokens)

                    if from_token_name != current_client.token:
                        contract = current_client.get_contract(
                            TOKENS_PER_CHAIN[current_client.network.name][from_token_name])
                        decimals = await contract.functions.decimals().call()
                    else:
                        decimals = 18

                    amount_in_wei = self.client.to_wei((
                        await current_client.get_smart_amount(amounts, token_name=tokens[index])
                    ), decimals)

                    amount = round(amount_in_wei / 10 ** decimals, 6)

                    bridge_data = (
                        src_chain_name, dst_chain_name, from_token_name, to_token_name,
                        amount, amount_in_wei
                    )

                    result_list.append(await class_name(current_client).bridge(bridge_data=bridge_data, swap_mode=True))

                    if current_client:
                        await current_client.session.close()

                    if swap_count == 0:
                        await sleep(self)

                    break

                except (SoftwareException, SoftwareExceptionWithoutRetry) as error:
                    raise error
                except Exception as error:
                    if 'No router enrolled for domain' in str(error):
                        raise SoftwareException(f"Module {class_name.__name__} do not support your route!")
                    traceback.print_exc()
                    self.logger_msg(
                        *self.client.acc_info,
                        msg=f"Error during the route. Will try again in 1 min... Error: {error}", type_msg='warning'
                    )
                    await asyncio.sleep(60)

        return result_list

    @network_handler
    async def balance_searcher(
            self, chains, tokens=None, native_check: bool = False, silent_mode: bool = False,
            balancer_mode: bool = False, random_mode: bool = False, wrapped_tokens: bool = False,
            need_token_name: bool = False, raise_handle: bool = False, without_error: bool = False
    ):
        index = 0
        clients = [await self.client.new_client(chain) for chain in chains]
        try:
            if native_check:
                tokens = [client.token for client in clients]
            elif wrapped_tokens:
                tokens = [f'W{client.token}' for client in clients]

            balances = []
            for client, token in zip(clients, tokens):
                balances.append(await client.get_token_balance(
                    token_name=token,
                    without_error=without_error
                ) if token in TOKENS_PER_CHAIN[client.network.name] or token in [f'W{client.token}', client.token] else (0, 0, ''))

            flag = all(balance_in_wei == 0 for balance_in_wei, _, _ in balances)

            if raise_handle and flag:
                raise SoftwareExceptionHandled('Insufficient balances in all networks!')

            if flag and not balancer_mode:
                raise SoftwareException('Insufficient balances in all networks!')

            balances_in_usd = []
            token_prices = {}
            for balance_in_wei, balance, token_name in balances:
                token_price = 1
                if 'USD' != token_name:
                    if token_name not in token_prices:
                        if token_name != '':
                            token_price = await self.get_token_price(token_name)
                        else:
                            token_price = 0
                        token_prices[token_name] = token_price
                    else:
                        token_price = token_prices[token_name]
                balance_in_usd = balance * token_price

                if need_token_name:
                    balances_in_usd.append([balance_in_usd, token_price, token_name])
                else:
                    balances_in_usd.append([balance_in_usd, token_price])

            if not random_mode:
                index = balances_in_usd.index(max(balances_in_usd, key=lambda x: x[0]))
            else:
                try:
                    index = balances_in_usd.index(random.choice(
                        [balance for balance in balances_in_usd if balance[0] > 0.2]
                    ))
                except Exception as error:
                    if 'list index out of range' in str(error):
                        raise SoftwareExceptionWithoutRetry('All networks have lower 0.2$ of native')

            for index_client, client in enumerate(clients):
                if index_client != index:
                    await client.session.close()

            if not silent_mode:
                clients[index].logger_msg(
                    *clients[index].acc_info,
                    msg=f"Detected {round(balances[index][1], 5)} {tokens[index]} in {clients[index].network.name}",
                    type_msg='success'
                )

            return clients[index], index, balances[index][1], balances[index][0], balances_in_usd[index]
        except Exception as error:
            if 'Insufficient balances in all networks!' in str(error):
                for client in clients:
                    await client.session.close()
            raise error
        finally:
            for index_client, client in enumerate(clients):
                if index_client != index:
                    await client.session.close()

    @helper
    async def smart_bridge_superform(self):
        from functions import Superform

        from_token_name, to_token_name = copy.deepcopy(Settings.SUPERFORM_TOKEN_NAME)
        from_chains = copy.deepcopy(Settings.SUPERFORM_CHAIN_FROM)
        tokens = [from_token_name for _ in from_chains]
        vaults_data = copy.deepcopy(Settings.SUPERFORM_VAULTS_TO)

        converted_chains = copy.deepcopy(from_chains)
        if any([isinstance(item, tuple) for item in from_chains]):
            new_chains = []
            for item in from_chains:
                if isinstance(item, tuple):
                    new_chains.extend(item)
                else:
                    new_chains.append(item)
            converted_chains = new_chains

        current_client, index, _, _, _ = await self.balance_searcher(
            converted_chains, tokens
        )

        dst_chain_name = random.choice(
            [chain for chain in vaults_data.keys()]
        )

        vault_ids = random.choice(list(vaults_data.values()))
        amount = await current_client.get_smart_amount(Settings.SUPERFORM_AMOUNT)
        src_chain_name = current_client.network.name

        bridge_data = src_chain_name, dst_chain_name, vault_ids, from_token_name, to_token_name, amount

        return await Superform(current_client).bridge(bridge_data)

    @helper
    @gas_checker
    async def smart_layerzero_util(self, dapp_id: int = None, dapp_mode: int = None):
        from functions import omnichain_util

        class_id, src_chain_names, dst_tuple_data = {
            1: (1, Settings.SRC_CHAIN_L2PASS, (Settings.DST_CHAIN_L2PASS_REFUEL, Settings.DST_CHAIN_L2PASS_NFT)),
            2: (2, Settings.SRC_CHAIN_NOGEM, (Settings.DST_CHAIN_NOGEM_REFUEL, Settings.DST_CHAIN_NOGEM_NFT)),
            3: (3, Settings.SRC_CHAIN_MERKLY, (Settings.DST_CHAIN_MERKLY_REFUEL, Settings.DST_CHAIN_MERKLY_NFT)),
            4: (4, Settings.SRC_CHAIN_WHALE, (Settings.DST_CHAIN_WHALE_REFUEL, Settings.DST_CHAIN_WHALE_NFT)),
            5: (5, Settings.SRC_CHAIN_ZERIUS, (Settings.DST_CHAIN_ZERIUS_REFUEL, Settings.DST_CHAIN_ZERIUS_NFT)),
            8: (8, Settings.SRC_CHAIN_BUNGEE, (Settings.DST_CHAIN_BUNGEE_REFUEL, 0)),
        }[dapp_id]

        dst_datas, module_name = {
            1: (list(dst_tuple_data[0].items()), 'refuel'),
            2: (dst_tuple_data[1], 'bridge NFT')
        }[dapp_mode]

        random.shuffle(src_chain_names)
        random.shuffle(dst_datas)

        result = False
        action_flag = False
        for dst_data in dst_datas:
            chain_name_to = dst_data if dapp_mode == 2 else dst_data[0]
            for src_chain_name in src_chain_names:
                try:
                    input_data = {
                        dst_data[0]: dst_data[1]
                    } if dapp_mode == 1 else dst_data

                    if dapp_mode == 1:
                        if src_chain_name == dst_data[0]:
                            continue

                    elif dapp_mode == 2:
                        input_data = dst_data

                        if src_chain_name == input_data:
                            continue

                    action_flag = await omnichain_util(
                        self.client.module_input_data, chain_from_name=src_chain_name,
                        dapp_id=class_id, dapp_mode=dapp_mode, input_data=input_data, need_check=True
                    )

                    if action_flag:
                        self.logger_msg(
                            *self.client.acc_info,
                            msg=f"Detected funds to {module_name} into {chain_name_to} from {src_chain_name}",
                            type_msg='success')

                        result = await omnichain_util(
                            self.client.module_input_data, chain_from_name=src_chain_name,
                            dapp_id=class_id, dapp_mode=dapp_mode, input_data=input_data
                        )

                        if not Settings.ALL_DST_CHAINS:
                            if result:
                                return True
                            raise SoftwareException(f'Software do not complete {module_name}. Will try again...')

                        if Settings.ALL_DST_CHAINS:
                            random.shuffle(src_chain_names)
                            if result:
                                break

                        await sleep(self)
                    else:
                        await asyncio.sleep(5)
                except SoftwareException as error:
                    raise error
                except Exception as error:
                    traceback.print_exc()
                    self.logger_msg(*self.client.acc_info, msg=f"{error}", type_msg='warning')
                    return True

            if not result:
                self.logger_msg(
                    *self.client.acc_info,
                    msg=f"Can`t {module_name} into {chain_name_to} from those SRC networks\n",
                    type_msg='warning'
                )

        if action_flag is False:
            self.logger_msg(
                *self.client.acc_info, msg=f"Can`t detect funds in all networks!", type_msg='warning')

        return True

    @helper
    @gas_checker
    async def merkly_omnichain_util(self, dapp_id: int, dapp_function: int):
        from functions import omnichain_util

        module_name, src_chain_names, dst_chains, token_amounts, refuel_data = {
            1: ('Hyperlane', Settings.SRC_CHAIN_WOMEX_HYPERLANE, Settings.DST_CHAIN_WOMEX_HYPERLANE, (0, 0), 0),
            2: ('Hyperlane', Settings.SRC_CHAIN_GETMINT_HYPERLANE, Settings.DST_CHAIN_GETMINT_HYPERLANE, (0, 0), 0),
            3: ('Hyperlane', Settings.SRC_CHAIN_MERKLY_HYPERLANE, Settings.DST_CHAIN_MERKLY_HYPERLANE, Settings.MERKLY_HYP_TOKENS_AMOUNTS, 0),
            4: ('Hyperlane', Settings.SRC_CHAIN_NOGEM_HYPERLANE, Settings.DST_CHAIN_NOGEM_HYPERLANE, Settings.NOGEM_HYP_TOKENS_AMOUNTS, 0),
        }[dapp_id]

        dst_datas, module_func_name = {
            2: (dst_chains, 'bridge NFT'),
            3: (dst_chains, 'bridge Token')
        }[dapp_function]

        random.shuffle(src_chain_names)
        random.shuffle(dst_datas)
        func_mode = f"{module_func_name} {module_name}"

        dapp_id = {
            3: 3,
            2: 6,
            1: 7,
            4: 2,
        }[dapp_id]

        result = False
        action_flag = False
        for dst_data in dst_datas:
            chain_name_to = dst_data if dapp_function != 1 else dst_data[0]
            for src_chain_name in src_chain_names:
                try:
                    if dapp_function == 1:
                        input_data = {
                            dst_data[0]: dst_data[1]
                        }
                        if src_chain_name == dst_data[0]:
                            continue

                    elif dapp_function == 2:
                        input_data = dst_data

                        if src_chain_name == dst_data:
                            continue
                    else:
                        tokens_amount_mint, tokens_amount_bridge = token_amounts

                        if isinstance(tokens_amount_bridge, (tuple, list)):
                            tokens_amount_bridge = random.choice(tokens_amount_bridge)
                        if isinstance(tokens_amount_mint, (tuple, list)):
                            tokens_amount_mint = random.choice(tokens_amount_mint)

                        input_data = tokens_amount_mint, tokens_amount_bridge, dst_data

                    action_flag = await omnichain_util(
                        self.client.module_input_data, chain_from_name=src_chain_name,
                        dapp_id=dapp_id, dapp_mode=func_mode, input_data=input_data, need_check=True
                    )

                    if action_flag:
                        self.logger_msg(
                            *self.client.acc_info,
                            msg=f"Detected funds to {module_func_name} into {chain_name_to} from {src_chain_name}",
                            type_msg='success')

                        result = await omnichain_util(
                            self.client.module_input_data, chain_from_name=src_chain_name,
                            dapp_id=dapp_id, dapp_mode=func_mode, input_data=input_data
                        )

                        if not Settings.ALL_DST_CHAINS:
                            if result:
                                return True
                            raise SoftwareExceptionWithoutRetry(f'Software do not complete {module_name}. Will try again')

                        if Settings.ALL_DST_CHAINS:
                            random.shuffle(src_chain_names)
                            if result:
                                break

                        await sleep(self)
                    else:
                        await asyncio.sleep(5)
                except SoftwareException as error:
                    raise error
                except Exception as error:
                    self.logger_msg(*self.client.acc_info, msg=f"{error}", type_msg='warning')
                    return True

            if not result and Settings.ALL_DST_CHAINS:
                self.logger_msg(
                    *self.client.acc_info,
                    msg=f"Can`t {module_func_name} into {chain_name_to} from those SRC networks\n",
                    type_msg='warning'
                )

        if action_flag is False:
            self.logger_msg(
                *self.client.acc_info, msg=f"Can`t detect funds in all networks!", type_msg='warning')

        return True

    async def okx_custom_withdraw_1(self):
        withdraw_data = copy.deepcopy(Settings.OKX_CUSTOM_WITHDRAW_1)

        return await self.smart_cex_withdraw(dapp_id=1, custom_withdraw_data=withdraw_data)

    async def okx_custom_withdraw_2(self):
        withdraw_data = copy.deepcopy(Settings.OKX_CUSTOM_WITHDRAW_2)

        return await self.smart_cex_withdraw(dapp_id=1, custom_withdraw_data=withdraw_data)

    async def okx_custom_withdraw_3(self):
        withdraw_data = copy.deepcopy(Settings.OKX_CUSTOM_WITHDRAW_3)

        return await self.smart_cex_withdraw(dapp_id=1, custom_withdraw_data=withdraw_data)

    async def okx_custom_withdraw_4(self):
        withdraw_data = copy.deepcopy(Settings.OKX_CUSTOM_WITHDRAW_4)

        return await self.smart_cex_withdraw(dapp_id=1, custom_withdraw_data=withdraw_data)

    async def bitget_custom_withdraw_1(self):
        withdraw_data = copy.deepcopy(Settings.BITGET_CUSTOM_WITHDRAW_1)

        return await self.smart_cex_withdraw(dapp_id=4, custom_withdraw_data=withdraw_data)

    async def bitget_custom_withdraw_2(self):
        withdraw_data = copy.deepcopy(Settings.BITGET_CUSTOM_WITHDRAW_2)

        return await self.smart_cex_withdraw(dapp_id=4, custom_withdraw_data=withdraw_data)

    async def bitget_custom_withdraw_3(self):
        withdraw_data = copy.deepcopy(Settings.BITGET_CUSTOM_WITHDRAW_3)

        return await self.smart_cex_withdraw(dapp_id=4, custom_withdraw_data=withdraw_data)

    async def bitget_custom_withdraw_4(self):
        withdraw_data = copy.deepcopy(Settings.BITGET_CUSTOM_WITHDRAW_4)

        return await self.smart_cex_withdraw(dapp_id=4, custom_withdraw_data=withdraw_data)

    async def binance_custom_withdraw_1(self):
        withdraw_data = copy.deepcopy(Settings.BINANCE_CUSTOM_WITHDRAW_1)

        return await self.smart_cex_withdraw(dapp_id=3, custom_withdraw_data=withdraw_data)

    async def binance_custom_withdraw_2(self):
        withdraw_data = copy.deepcopy(Settings.BINANCE_CUSTOM_WITHDRAW_2)

        return await self.smart_cex_withdraw(dapp_id=3, custom_withdraw_data=withdraw_data)

    async def binance_custom_withdraw_3(self):
        withdraw_data = copy.deepcopy(Settings.BINANCE_CUSTOM_WITHDRAW_3)

        return await self.smart_cex_withdraw(dapp_id=3, custom_withdraw_data=withdraw_data)

    async def binance_custom_withdraw_4(self):
        withdraw_data = copy.deepcopy(Settings.BINANCE_CUSTOM_WITHDRAW_4)

        return await self.smart_cex_withdraw(dapp_id=3, custom_withdraw_data=withdraw_data)

    @helper
    async def smart_cex_withdraw(self, dapp_id: int, custom_withdraw_data: list = None):
        while True:
            try:
                from functions import (
                    okx_withdraw_util, bingx_withdraw_util, binance_withdraw_util, bitget_withdraw_util,
                    get_rpc_by_chain_name
                )

                func, withdraw_data = {
                    1: (okx_withdraw_util, Settings.OKX_WITHDRAW_DATA),
                    2: (bingx_withdraw_util, Settings.BINGX_WITHDRAW_DATA),
                    3: (binance_withdraw_util, Settings.BINANCE_WITHDRAW_DATA),
                    4: (bitget_withdraw_util, Settings.BITGET_WITHDRAW_DATA)
                }[dapp_id]

                if custom_withdraw_data:
                    withdraw_data = custom_withdraw_data

                withdraw_data_copy = copy.deepcopy(withdraw_data)

                random.shuffle(withdraw_data_copy)
                result_list = []

                for index, data in enumerate(withdraw_data_copy, 1):
                    current_data = data
                    if isinstance(data[0], list):
                        current_data = random.choice(data)
                        if not current_data:
                            continue

                    network, amount = current_data

                    if network in [42, 43, 44]:
                        self.client.module_input_data["network"] = get_rpc_by_chain_name(CEX_WRAPPED_ID[network])
                        current_client = CosmosClient(self.client.module_input_data)
                    elif network == 47:
                        self.client.module_input_data["network"] = get_rpc_by_chain_name(CEX_WRAPPED_ID[network])
                        current_client = SolanaClient(self.client.module_input_data)
                    else:
                        current_client = self.client
                    try:
                        if isinstance(amount[0], str):
                            amount = f"{self.client.custom_round(random.uniform(float(amount[0]), float(amount[1])), 6) / 100}"

                        result_list.append(await func(current_client, withdraw_data=(network, amount)))

                        if index != len(withdraw_data_copy):
                            await sleep(self)
                    finally:
                        if current_client:
                            await current_client.session.close()

                return all(result_list)
            except Exception as error:
                self.logger_msg(self.client.account_name, None, msg=f'{error}', type_msg='error')
                msg = f"Software cannot continue, awaiting operator's action. Will try again in 1 min..."
                self.logger_msg(self.client.account_name, None, msg=msg, type_msg='warning')
                await asyncio.sleep(60)

    @helper
    @gas_checker
    async def smart_cex_deposit(self, dapp_id: int):
        from functions import cex_deposit_util

        class_id, deposit_data, cex_config = {
            1: (1, Settings.OKX_DEPOSIT_DATA, OKX_NETWORKS_NAME),
            2: (2, Settings.BINGX_DEPOSIT_DATA, BINGX_NETWORKS_NAME),
            3: (3, Settings.BINANCE_DEPOSIT_DATA, BINANCE_NETWORKS_NAME),
            4: (4, Settings.BITGET_DEPOSIT_DATA, BITGET_NETWORKS_NAME),
            5: (1, Settings.OKX_CUSTOM_DEPOSIT_1, OKX_NETWORKS_NAME),
        }[dapp_id]

        deposit_data_copy = copy.deepcopy(deposit_data)

        client = None
        result_list = []
        for data in deposit_data_copy:
            while True:
                try:
                    current_data = data
                    if isinstance(data[0], list):
                        current_data = random.choice(data)
                        if not current_data:
                            continue

                    networks, amount, limit_amount, wanted_to_hold_amount = current_data
                    if (not isinstance(networks, (int, tuple)) or not isinstance(amount, tuple)
                            or not isinstance(limit_amount, (int, float)) or not isinstance(wanted_to_hold_amount, tuple)):
                        raise SoftwareExceptionWithoutRetry(
                            'Software only support [1, (1, 1), 0, (1, 1)] deposit format. See CEX CONTROL'
                        )

                    if isinstance(networks, tuple):
                        dapp_tokens = [f"{cex_config[network].split('-')[0]}{'.e' if network in [29, 30] else ''}"
                                       for network in networks]
                        dapp_chains = [CEX_WRAPPED_ID[chain] for chain in networks]
                    else:
                        dapp_tokens = [f"{cex_config[networks].split('-')[0]}{'.e' if networks in [29, 30] else ''}"]
                        dapp_chains = [CEX_WRAPPED_ID[networks]]

                    try:
                        client, chain_index, balance, _, balance_data = await self.balance_searcher(
                            chains=dapp_chains, tokens=dapp_tokens
                        )
                    except Exception as error:
                        if 'Insufficient balances in all networks!' in str(error):
                            self.logger_msg(
                                *self.client.acc_info,
                                msg=f'Insufficient {dapp_tokens[0]} balance in {dapp_chains[0]}!',
                                type_msg='warning'
                            )
                            break
                        else:
                            raise error

                    balance_in_usd, token_price = balance_data

                    if balance_in_usd == 0:
                        self.logger_msg(*self.client.acc_info, msg=f'Can`t deposit ZERO amount', type_msg='warning')
                        break

                    dep_token = dapp_tokens[chain_index]

                    dep_network = networks if isinstance(networks, int) else networks[chain_index]
                    min_wanted_amount, max_wanted_amount = min(wanted_to_hold_amount), max(wanted_to_hold_amount)

                    if balance_in_usd >= limit_amount:

                        dep_amount = await client.get_smart_amount(amount, token_name=dep_token)
                        deposit_fee = int(await client.simulate_transfer(token_name=dep_token) * 2)
                        min_hold_balance = random.uniform(min_wanted_amount, max_wanted_amount) / token_price

                        if dep_token == client.token and balance < dep_amount + deposit_fee:
                            dep_amount = dep_amount - deposit_fee

                        if balance - dep_amount < 0:
                            self.logger_msg(
                                *self.client.acc_info,
                                msg=f'Account balance {balance:.6f} - deposit fee {dep_amount} < 0',
                                type_msg='warning'
                            )
                            break

                        if balance - dep_amount < min_hold_balance:
                            need_to_freeze_amount = min_hold_balance - (balance - dep_amount)
                            dep_amount = dep_amount - need_to_freeze_amount

                        if dep_amount < 0:
                            self.logger_msg(
                                *self.client.acc_info,
                                msg=f'Set CEX_DEPOSIT_LIMITER[2 value] lower than {wanted_to_hold_amount}. '
                                    f'Current amount = {dep_amount:.4f} {dep_token}',
                                type_msg='warning'
                            )
                            break

                        dep_amount_in_usd = dep_amount * token_price * 0.99

                        if balance_in_usd >= dep_amount_in_usd:

                            deposit_data = dep_network, self.client.custom_round(dep_amount, 6)

                            if len(deposit_data_copy) == 1:
                                return await cex_deposit_util(client, dapp_id=class_id, deposit_data=deposit_data)
                            else:
                                result_list.append(
                                    await cex_deposit_util(client, dapp_id=class_id, deposit_data=deposit_data)
                                )
                                break

                        info = f"{balance_in_usd:.2f}$ < {dep_amount_in_usd:.2f}$"
                        self.logger_msg(
                            *self.client.acc_info,
                            msg=f'Account {dep_token} balance < wanted deposit amount: {info}',
                            type_msg='warning'
                        )
                        break

                    info = f"{balance_in_usd:.2f}$ < {limit_amount:.2f}$"
                    self.logger_msg(
                        *self.client.acc_info,
                        msg=f'Account {dep_token} balance < wanted limit amount: {info}', type_msg='warning'
                    )
                    break

                except Exception as error:
                    raise error
                finally:
                    if client and not client.session.closed:
                        await client.session.close()

        return all(result_list)

    @helper
    @gas_checker
    async def smart_bridge(self, dapp_id: int = None):
        client = None
        fee_client = None
        while True:
            try:
                from functions import bridge_utils

                dapp_chains, dapp_tokens, limiter = {
                    1: (Settings.ACROSS_CHAIN_FROM_NAMES, Settings.ACROSS_TOKEN_NAME, Settings.ACROSS_AMOUNT_LIMITER),
                    2: (Settings.BUNGEE_CHAIN_FROM_NAMES, Settings.BUNGEE_TOKEN_NAME, Settings.BUNGEE_AMOUNT_LIMITER),
                    3: (Settings.LAYERSWAP_CHAIN_FROM_NAMES, Settings.LAYERSWAP_TOKEN_NAME, Settings.LAYERSWAP_AMOUNT_LIMITER),
                    4: (Settings.NITRO_CHAIN_FROM_NAMES, Settings.NITRO_TOKEN_NAME, Settings.NITRO_AMOUNT_LIMITER),
                    5: (Settings.ORBITER_CHAIN_FROM_NAMES, Settings.ORBITER_TOKEN_NAME, Settings.ORBITER_AMOUNT_LIMITER),
                    6: (Settings.OWLTO_CHAIN_FROM_NAMES, Settings.OWLTO_TOKEN_NAME, Settings.OWLTO_AMOUNT_LIMITER),
                    7: (Settings.RELAY_CHAIN_FROM_NAMES, Settings.RELAY_TOKEN_NAME, Settings.RELAY_AMOUNT_LIMITER),
                    8: (Settings.RHINO_CHAIN_FROM_NAMES, Settings.RHINO_TOKEN_NAME, Settings.RHINO_AMOUNT_LIMITER),
                    9: (Settings.NATIVE_CHAIN_FROM_NAMES, Settings.NATIVE_TOKEN_NAME, Settings.NATIVE_AMOUNT_LIMITER),
                    10: (Settings.RANGO_CHAIN_FROM_NAMES, Settings.RANGO_TOKEN_NAME, Settings.RANGO_AMOUNT_LIMITER),
                    11: (Settings.XYFINANCE_CHAIN_FROM_NAMES, Settings.XYFINANCE_TOKEN_NAME, Settings.XYFINANCE_AMOUNT_LIMITER),
                }[dapp_id]

                if len(dapp_tokens) == 2:
                    from_token_name, to_token_name = dapp_tokens
                else:
                    from_token_name, to_token_name = dapp_tokens, dapp_tokens

                dapp_tokens = [from_token_name for _ in dapp_chains]

                client, chain_index, balance, _, balance_data = await self.balance_searcher(
                    chains=dapp_chains, tokens=dapp_tokens, raise_handle=True
                )

                fee_client = await client.new_client(dapp_chains[chain_index])
                chain_from_name, token_name = dapp_chains[chain_index], from_token_name

                switch_id = Settings.BRIDGE_SWITCH_CONTROL.get(dapp_id, dapp_id)

                bridge_cfg_from_name, bridge_cfg_to_name, amount, chain_to_name = await client.get_bridge_data(
                    chain_from_name=chain_from_name, dapp_id=switch_id, settings_id=dapp_id
                )

                await asyncio.sleep(3)

                from_token_addr = TOKENS_PER_CHAIN[client.network.name][from_token_name]

                if to_token_name == 'USDC':
                    to_token_addr = TOKENS_PER_CHAIN[chain_to_name].get('USDC.e')
                    if not to_token_addr:
                        to_token_addr = TOKENS_PER_CHAIN[chain_to_name]['USDC']
                else:
                    to_token_addr = TOKENS_PER_CHAIN[chain_to_name][to_token_name]

                balance_in_usd, token_price = balance_data
                limit_amount, wanted_to_hold_amount = limiter
                min_wanted_amount, max_wanted_amount = min(wanted_to_hold_amount), max(wanted_to_hold_amount)
                fee_bridge_data = (
                    bridge_cfg_from_name, bridge_cfg_to_name, amount, from_token_name,
                    to_token_name, from_token_addr, to_token_addr, chain_to_name
                )

                if balance_in_usd >= limit_amount:
                    bridge_fee = await bridge_utils(
                        fee_client, switch_id, fee_bridge_data, need_fee=True)
                    min_hold_balance = random.uniform(min_wanted_amount, max_wanted_amount) / token_price

                    if balance - bridge_fee - min_hold_balance > 0:
                        if balance < amount + bridge_fee:
                            bridge_amount = self.client.custom_round(amount - bridge_fee, 6)
                        else:
                            bridge_amount = amount
                        if balance - bridge_amount < min_hold_balance:
                            need_to_freeze_amount = min_hold_balance - (balance - bridge_amount)
                            bridge_amount = self.client.custom_round(bridge_amount - need_to_freeze_amount, 6)

                        if bridge_amount < 0:
                            raise SoftwareExceptionWithoutRetry(
                                f'Set BRIDGE_AMOUNT_LIMITER[2 value] lower than {wanted_to_hold_amount}. '
                                f'Current amount = {bridge_amount} {from_token_name}')

                        bridge_amount_in_usd = bridge_amount * token_price

                        bridge_data = (
                            bridge_cfg_from_name, bridge_cfg_to_name, bridge_amount, from_token_name,
                            to_token_name, from_token_addr, to_token_addr, chain_to_name
                        )

                        if balance_in_usd >= bridge_amount_in_usd:
                            return await bridge_utils(client, switch_id, bridge_data)

                        info = f"{balance_in_usd:.2f}$ < {bridge_amount_in_usd:.2f}$"
                        raise SoftwareExceptionHandled(f'Account {token_name} balance < wanted bridge amount: {info}')

                    full_need_amount = self.client.custom_round(bridge_fee + min_hold_balance, 6)
                    info = f"{balance:.2f} {token_name} < {full_need_amount:.2f} {token_name}"
                    raise SoftwareExceptionHandled(f'Account {token_name} balance < bridge fee + hold amount: {info}')

                info = f"{balance_in_usd:.2f}$ < {limit_amount:.2f}$"
                raise SoftwareExceptionHandled(f'Account {token_name} balance < wanted limit amount: {info}')

            except Exception as error:
                raise error
            finally:
                if client:
                    await client.session.close()
                if fee_client:
                    await fee_client.session.close()
