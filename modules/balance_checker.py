import asyncio
import os
import random

import pandas as pd
from pathlib import Path
from termcolor import cprint
from prettytable import PrettyTable
from config.constants import PROXIES
from utils.networks import NetworkRPC

from modules.interfaces import SoftwareException

FIELDS = [
    '#', 'Account Name', 'SOL Balance', 'TIA Balance', 'NTRN Balance', 'INJ Balance'
]

table = PrettyTable()
table.field_names = FIELDS


class TxChecker:
    @staticmethod
    async def get_native_wallet_balance(
            account_name, wallet, client_type: str, rpc: NetworkRPC, token_name: str = None
    ):
        from functions import SolanaClient, CosmosClient

        proxy = random.choice(PROXIES)

        await asyncio.sleep(random.randint(2, 10))

        evm_key = "0x1231231312312312312312312312312312312312312312312312312312312312"

        module_input_data = {
            "account_name": account_name,
            "evm_private_key": evm_key,
            "mnemonic": wallet,
            "solana_private_key": wallet,
            "network": rpc,
            "proxy": proxy,
        }

        try:
            if client_type == 'Solana':
                try:

                    client = SolanaClient(module_input_data)
                except TypeError:
                    return 0
            elif client_type == 'Cosmos':
                client = CosmosClient(module_input_data)
            else:
                raise SoftwareException(f'{client_type} does not exist in tx checker!')
            while True:
                try:
                    _, balance, _ = await client.get_token_balance(token_name)
                    break
                except Exception as error:
                    cprint(
                        f'Got error with check balance, will try again... {error}', color='light_yellow',
                    )

            await client.session.close()

            return balance
        except ValueError:
            cprint(
                '\n⚠️⚠️⚠️Put your proxies into data/accounts_data.xlsx first!⚠️⚠️⚠️\n', color='light_red',
                attrs=["blink"]
            )

    async def fetch_wallet_data(self, account_name, cosmos_mnemonic, solana_private_key, index):
        from functions import SolanaRPC, NeutronRPC, CelestiaRPC, INJ_RPC
        sol_balance = await self.get_native_wallet_balance(account_name, solana_private_key, client_type='Solana',
                                                           rpc=SolanaRPC)
        tia_balance = await self.get_native_wallet_balance(account_name, cosmos_mnemonic, client_type='Cosmos',
                                                           rpc=CelestiaRPC)
        ntrn_balance = await self.get_native_wallet_balance(account_name, cosmos_mnemonic, client_type='Cosmos',
                                                            rpc=NeutronRPC)
        inj_balance = await self.get_native_wallet_balance(account_name, cosmos_mnemonic, client_type='Cosmos',
                                                           rpc=INJ_RPC)

        return {
            '#': index + 1,
            'Account Name': f'{account_name}',
            'SOL Balance': f'{sol_balance:.3f}',
            'TIA Balance': f'{tia_balance:.3f}',
            'NTRN Balance': f'{ntrn_balance:.3f}',
            'INJ Balance': f'{inj_balance:.3f}',
        }


async def main():
    from config.constants import ACCOUNT_NAMES, SOLANA_PRIVATE_KEYS, MNEMONICS

    if not ACCOUNT_NAMES or not SOLANA_PRIVATE_KEYS or not MNEMONICS:
        cprint('\n⚠️⚠️⚠️Put your wallets into data/accounts_data.xlsx first!⚠️⚠️⚠️\n', color='light_red',
               attrs=["blink"])
        return True

    account_datas = []
    for account_name in ACCOUNT_NAMES:
        account_data = {
            'name': account_name,
            'cosmos': MNEMONICS[ACCOUNT_NAMES.index(account_name)],
            'solana': SOLANA_PRIVATE_KEYS[ACCOUNT_NAMES.index(account_name)]
        }
        account_datas.append(account_data)

    tx_checker = TxChecker()

    tasks = [tx_checker.fetch_wallet_data(account['name'], account['cosmos'], account['solana'], index) for
             index, account in enumerate(account_datas, 0)]
    wallet_data = await asyncio.gather(*tasks)

    cprint('✅ Data successfully load to /data/accounts_stats/wallets_stats.xlsx (Excel format)\n',
           'light_yellow', attrs=["blink"])
    await asyncio.sleep(1)

    # Создаем DataFrame с данными
    xlsx_data = pd.DataFrame(wallet_data)

    # Используем pathlib для формирования динамического пути
    current_dir = Path(__file__).parent
    stats_dir = current_dir / 'data' / 'accounts_stats'
    stats_file_path = stats_dir / 'wallets_stats.xlsx'

    # Проверяем наличие директории и создаем её при необходимости
    stats_dir.mkdir(parents=True, exist_ok=True)

    # Сохраняем данные в Excel файл
    xlsx_data.to_excel(stats_file_path, index=False)

    # Добавляем данные в таблицу для вывода
    [table.add_row(data.values()) for data in wallet_data]

    # Выводим таблицу
    print(table)
