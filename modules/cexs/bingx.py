import asyncio
import hmac
import time

from hashlib import sha256
from modules import CEX, Logger
from modules.interfaces import SoftwareExceptionWithoutRetry, SoftwareException, InsufficientBalanceException
from dev_settings import Settings
from utils.tools import get_wallet_for_deposit, network_handler, helper
from config.constants import CEX_WRAPPED_ID, BINGX_NETWORKS_NAME, TOKENS_PER_CHAIN


class BingX(CEX, Logger):
    def __init__(self, client):
        self.client = client
        Logger.__init__(self)
        CEX.__init__(self, client, 'BingX')

        self.api_url = "https://open-api.bingx.com"
        self.network = self.client.network.name
        self.headers = {
            "Content-Type": "application/json",
            "X-BX-APIKEY": self.api_key,
        }

    @staticmethod
    def parse_params(params: dict | None = None):
        if params:
            sorted_keys = sorted(params)
            params_str = "&".join(["%s=%s" % (x, params[x]) for x in sorted_keys])
        else:
            params_str = ''
        return params_str + "&timestamp=" + str(int(time.time() * 1000))

    def get_sign(self, payload: str = ""):
        try:
            secret_key_bytes = self.api_secret.encode('utf-8')
            signature = hmac.new(secret_key_bytes, payload.encode('utf-8'), sha256).hexdigest()

            return signature
        except Exception as error:
            raise SoftwareExceptionWithoutRetry(f'Bad signature for BingX request: {error}')

    async def get_balance(self, ccy: str):
        path = '/openApi/spot/v1/account/balance'

        params = {
            'timestamp': str(int(time.time() * 1000))
        }

        parse_params = self.parse_params(params)

        url = f"{self.api_url}{path}?{parse_params}&signature={self.get_sign(parse_params)}"
        data = await self.make_request(url=url, headers=self.headers, module_name='Balances Data', content_type=None)
        balance = [item for item in data['balances'] if item['asset'] == ccy]

        if balance:
            return float(balance[0]['free'])
        raise SoftwareExceptionWithoutRetry(f'Your have not enough {ccy} balance on CEX')

    async def get_currencies(self, ccy):
        path = '/openApi/wallets/v1/capital/config/getall'

        params = {
            'timestamp': str(int(time.time() * 1000))
        }

        parse_params = self.parse_params(params)

        url = f"{self.api_url}{path}?{parse_params}&signature={self.get_sign(parse_params)}"
        data = await self.make_request(url=url, headers=self.headers, module_name='Token info')
        return [item for item in data if item['coin'] == ccy]

    async def get_sub_list(self):
        path = "/openApi/subAccount/v1/list"

        params = {
            "page": 1,
            "limit": 100,
        }

        await asyncio.sleep(2)
        parse_params = self.parse_params(params)
        url = f"{self.api_url}{path}?{parse_params}&signature={self.get_sign(parse_params)}"
        return await self.make_request(url=url, headers=self.headers, module_name='Get subAccounts list')

    async def get_sub_balance(self, sub_uid):
        path = '/openApi/subAccount/v1/assets'

        params = {
            "subUid": sub_uid
        }

        await asyncio.sleep(2)
        parse_params = self.parse_params(params)
        url = f"{self.api_url}{path}?{parse_params}&signature={self.get_sign(parse_params)}"
        return await self.make_request(url=url, headers=self.headers, module_name='Get subAccount balance')

    async def get_main_balance(self):
        path = '/openApi/spot/v1/account/balance'

        await asyncio.sleep(2)
        parse_params = self.parse_params()
        url = f"{self.api_url}{path}?{parse_params}&signature={self.get_sign(parse_params)}"
        return await self.make_request(url=url, headers=self.headers, content_type=None,
                                       module_name='Get main account balance')

    async def transfer_from_subaccounts(self, ccy: str = 'ETH', amount: float = None, silent_mode:bool = False):

        if not Settings.COLLECT_FROM_SUB_CEX:
            return True

        if ccy == 'USDC.e':
            ccy = 'USDC'

        if not silent_mode:
            self.logger_msg(*self.client.acc_info, msg=f'Checking subAccounts balance')

        flag = True
        sub_list = (await self.get_sub_list())['result']

        for sub_data in sub_list:
            sub_name = sub_data['subAccountString']
            sub_uid = sub_data['subUid']
            sub_balances = await self.get_sub_balance(sub_uid)

            if sub_balances:

                sub_balance = float(
                    [balance for balance in sub_balances['balances'] if balance['asset'] == ccy][0]['free'])

                amount = amount if amount else sub_balance
                if sub_balance == amount and sub_balance != 0.0:
                    flag = False
                    self.logger_msg(*self.client.acc_info, msg=f'{sub_name} | subAccount balance : {sub_balance} {ccy}')

                    params = {
                        "amount": amount,
                        "coin": ccy,
                        "userAccount": sub_uid,
                        "userAccountType": 1,
                        "walletType": 1
                    }

                    path = "/openApi/wallets/v1/capital/subAccountInnerTransfer/apply"
                    parse_params = self.parse_params(params)

                    url = f"{self.api_url}{path}?{parse_params}&signature={self.get_sign(parse_params)}"
                    await self.make_request(
                        method="POST", url=url, headers=self.headers, module_name='SubAccount transfer')

                    self.logger_msg(
                        *self.client.acc_info,
                        msg=f"Transfer {amount} {ccy} to main account complete", type_msg='success'
                    )
                    if not silent_mode:
                        break
        if flag and not silent_mode:
            self.logger_msg(*self.client.acc_info, msg=f'subAccounts balance: 0 {ccy}', type_msg='warning')
        return True

    async def get_cex_balances(self, ccy: str = 'ETH'):
        while True:
            try:
                if ccy == 'USDC.e':
                    ccy = 'USDC'

                balances = {}

                main_balance = await self.get_main_balance()

                if main_balance:
                    ccy_balance = [balance for balance in main_balance['balances'] if balance['asset'] == ccy]

                    if ccy_balance:
                        balances['Main CEX Account'] = float(ccy_balance[0]['free'])
                    else:
                        balances['Main CEX Account'] = 0
                else:
                    balances['Main CEX Account'] = 0

                sub_list = (await self.get_sub_list())['result']

                for sub_data in sub_list:
                    sub_name = sub_data['subAccountString']
                    sub_uid = sub_data['subUid']
                    sub_balances = await self.get_sub_balance(sub_uid)
                    if sub_balances:
                        ccy_syb_balance = [balance for balance in sub_balances['balances'] if balance['asset'] == ccy]

                        if ccy_syb_balance:
                            balances[sub_name] = float(ccy_syb_balance[0]['free'])
                        else:
                            balances[sub_name] = 0
                    else:
                        balances[sub_name] = 0

                    await asyncio.sleep(3)

                return balances
            except Exception as error:
                if '-1021 Msg: Timestamp for' in str(error):
                    self.logger_msg(
                        *self.client.acc_info,
                        msg=f"Bad timestamp for request. Will try again in 10 second...",
                        type_msg='warning'
                    )
                    await asyncio.sleep(10)
                else:
                    raise error

    @network_handler
    async def wait_deposit_confirmation(
            self, amount: float, old_balances: dict, ccy: str = 'ETH', check_time: int = 45
    ):

        if not Settings.WAIT_FOR_RECEIPT_CEX:
            return True

        if ccy == 'USDC.e':
            ccy = 'USDC'

        self.logger_msg(*self.client.acc_info, msg=f"Start checking CEX balances")

        await asyncio.sleep(10)
        while True:
            new_sub_balances = await self.get_cex_balances(ccy=ccy)
            for acc_name, acc_balance in new_sub_balances.items():
                if acc_name not in old_balances:
                    old_balances[acc_name] = 0
                if acc_balance > old_balances[acc_name]:
                    self.logger_msg(*self.client.acc_info, msg=f"Deposit {amount} {ccy} complete", type_msg='success')
                    return True
                else:
                    continue
            else:
                self.logger_msg(*self.client.acc_info, msg=f"Deposit still in progress...", type_msg='warning')
                await asyncio.sleep(check_time)

    @helper
    async def withdraw(self, withdraw_data:tuple = None, transfer_mode:bool = False):
        path = '/openApi/wallets/v1/capital/withdraw/apply'

        network_id, amount = withdraw_data
        network_raw_name = BINGX_NETWORKS_NAME[network_id]
        split_network_data = network_raw_name.split('-')
        ccy, network_name = split_network_data[0], '-'.join(split_network_data[1:])
        dst_chain_name = CEX_WRAPPED_ID[network_id]

        if isinstance(amount, str):
            amount = self.client.custom_round(await self.get_balance(ccy=ccy) * float(amount), 6)
        elif transfer_mode:
            amount = await self.get_balance(ccy)
        else:
            amount = self.client.custom_round(amount)

        if amount == 0.0:
            raise SoftwareExceptionWithoutRetry('Can`t withdraw zero amount')

        await self.transfer_from_subaccounts(ccy=ccy, silent_mode=True)

        self.logger_msg(*self.client.acc_info, msg=f"Withdraw {amount} {ccy} to {network_name}")

        while True:
            try:
                withdraw_raw_data = (await self.get_currencies(ccy))[0]['networkList']
                network_data = {
                    item['network']: {
                        'withdrawEnable': item['withdrawEnable'],
                        'withdrawFee': item['withdrawFee'],
                        'withdrawMin': item['withdrawMin'],
                        'withdrawMax': item['withdrawMax']
                    } for item in withdraw_raw_data
                }[network_name]

                if network_data['withdrawEnable']:
                    min_wd, max_wd = float(network_data['withdrawMin']), float(network_data['withdrawMax'])

                    if min_wd <= amount <= max_wd:

                        params = {
                            "address": f"{self.client.address}",
                            "amount": amount,
                            "coin": ccy,
                            "network": network_name,
                            "walletType": "1",
                        }

                        ccy = f"{ccy}.e" if network_id in [29, 30] else ccy

                        old_balance_data_on_dst = await self.client.wait_for_receiving(
                            dst_chain_name, token_name=ccy, check_balance_on_dst=True
                        )

                        parse_params = self.parse_params(params)
                        url = f"{self.api_url}{path}?{parse_params}&signature={self.get_sign(parse_params)}"

                        await self.make_request(method='POST', url=url, headers=self.headers, module_name='Withdraw')

                        self.logger_msg(
                            *self.client.acc_info,
                            msg=f"Withdraw complete. Note: wait a little for receiving funds", type_msg='success'
                        )

                        await self.client.wait_for_receiving(
                            dst_chain_name, old_balance_data=old_balance_data_on_dst, token_name=ccy
                        )

                        return True
                    else:
                        raise SoftwareExceptionWithoutRetry(f"Limit range for withdraw: {min_wd:.5f} {ccy} - {max_wd} {ccy}")
                else:
                    self.logger_msg(
                        *self.client.acc_info,
                        msg=f"Withdraw from {network_name} is not active now. Will try again in 1 min...",
                        type_msg='warning'
                    )
                    await asyncio.sleep(60)
            except InsufficientBalanceException:
                continue

    @helper
    async def deposit(self, deposit_data:tuple = None):
        deposit_network, amount = deposit_data
        network_raw_name = BINGX_NETWORKS_NAME[deposit_network]
        ccy, network_name = network_raw_name.split('-')
        ccy = f"{ccy}.e" if deposit_network in [29, 30] else ccy
        cex_wallet = get_wallet_for_deposit(self, deposit_network)
        info = f"{cex_wallet[:10]}....{cex_wallet[-6:]}"

        await self.transfer_from_subaccounts(ccy=ccy, silent_mode=True)

        self.logger_msg(*self.client.acc_info, msg=f"Deposit {amount} {ccy} from {network_name} to BingX wallet: {info}")

        while True:
            try:
                withdraw_data = (await self.get_currencies(ccy))[0]['networkList']
                network_data = {
                    item['network']: {
                        'depositEnable': item['depositEnable']
                    } for item in withdraw_data
                }[network_name]

                if network_data['depositEnable']:

                    cex_balances = await self.get_cex_balances(ccy=ccy)

                    if deposit_network in [42, 43, 44]:
                        result_tx = await self.client.send_tokens(
                            address=cex_wallet, amount=amount, ccy=ccy, without_fee_support=True
                        )
                    else:

                        if ccy != self.client.token:
                            token_contract = self.client.get_contract(TOKENS_PER_CHAIN[self.network][ccy])
                            decimals = await self.client.get_decimals(ccy)
                            amount_in_wei = self.client.to_wei(amount, decimals)

                            transaction = await token_contract.functions.transfer(
                                self.client.w3.to_checksum_address(cex_wallet),
                                amount_in_wei
                            ).build_transaction(await self.client.prepare_transaction())
                        else:
                            amount_in_wei = self.client.to_wei(amount)
                            transaction = (await self.client.prepare_transaction(value=int(amount_in_wei))) | {
                                'to': self.client.w3.to_checksum_address(cex_wallet),
                                'data': '0x'
                            }

                        result_tx = await self.client.send_transaction(transaction)

                    if result_tx:
                        result_confirmation = await self.wait_deposit_confirmation(amount, cex_balances, ccy=ccy)

                        result_transfer = await self.transfer_from_subaccounts(ccy=ccy, amount=amount)

                        return all([result_tx, result_confirmation, result_transfer])
                    else:
                        raise SoftwareException('Transaction not sent, trying again')

                else:
                    self.logger_msg(
                        *self.client.acc_info,
                        msg=f"Deposit to {network_name} is not active now. Will try again in 1 min...",
                        type_msg='warning'
                    )
                    await asyncio.sleep(60)
            except InsufficientBalanceException:
                continue
