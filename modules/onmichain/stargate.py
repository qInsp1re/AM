import time

from eth_abi import abi

from config.constants import (
    STARGATE_CONTRACTS, STARGATE_POOLS_ID, TOKENS_PER_CHAIN, ZERO_ADDRESS,
    STARGATE_STG_CONFIG_CHECKERS, VESTG_ADDRESS, STARGATE_ENDPOINTS_ID, OMNICHAIN_NETWORKS_DATA,
)
from config.abi import L0_ENDPOINT_ABI, STARGATE_ABI, USDV_ABI, MAV_ABI, STG_ABI, VESTG_ABI
from modules import Logger, Client
from modules.interfaces import SoftwareExceptionWithoutRetry
from utils.tools import helper, gas_checker


class Stargate(Logger):
    def __init__(self, client: Client):
        self.client = client
        Logger.__init__(self)
        self.network = self.client.network.name
        # factory_contract = self.client.get_contract(contracts['factory'], STARGATE_ABI['factory'])

    @helper
    @gas_checker
    async def bridge(self, bridge_data: tuple):

        src_chain_name, dst_chain_name, from_token_name, to_token_name, amount, amount_in_wei = bridge_data

        self.logger_msg(
            *self.client.acc_info,
            msg=f'Bridge {amount} {from_token_name} from {src_chain_name} to {to_token_name} {dst_chain_name}')

        contracts = STARGATE_CONTRACTS[self.network]
        min_amount_out = int(amount_in_wei * 0.995)
        dst_chain_id, _ = OMNICHAIN_NETWORKS_DATA[dst_chain_name]
        dst_endpoint_id = STARGATE_ENDPOINTS_ID[dst_chain_name]
        dst_gas_for_call, dst_native_amount, dst_native_addr = 0, 0, '0x0000000000000000000000000000000000000001'

        if from_token_name == 'STG':
            stg_contract = self.client.get_contract(TOKENS_PER_CHAIN[self.network]['STG'], STG_ABI)
            config_checker = self.client.get_contract(
                STARGATE_STG_CONFIG_CHECKERS[self.network], STARGATE_ABI['configer'])

            _, base_gas, _ = await config_checker.functions.dstConfigLookup(
                dst_chain_id,
                1
            ).call()

            if not base_gas:
                base_gas = 250000

            endpoint_address = await stg_contract.functions.endpoint().call()
            endpoint_contract = self.client.get_contract(endpoint_address, L0_ENDPOINT_ABI)

            adapter_params = abi.encode(["uint16", "uint64"], [1, base_gas])
            adapter_params = self.client.w3.to_hex(adapter_params[30:])

            estimate_fee = (await endpoint_contract.functions.estimateFees(
                dst_chain_id,
                self.client.address,
                adapter_params,
                False,
                "0x"
            ).call())[0]

            transaction = await stg_contract.functions.sendTokens(
                dst_chain_id,
                self.client.address,
                amount_in_wei,
                ZERO_ADDRESS,
                adapter_params
            ).build_transaction(await self.client.prepare_transaction(value=int(estimate_fee * 1.05)))

        elif from_token_name == 'MAV':
            contracts = STARGATE_CONTRACTS[self.network]
            otf_wrapper_contract = self.client.get_contract(contracts['otf_wrapper'], STARGATE_ABI['MAV'])
            mav_contact = self.client.get_contract(TOKENS_PER_CHAIN[self.network]['MAV'], MAV_ABI)

            await self.client.check_for_approved(mav_contact.address, otf_wrapper_contract.address, amount_in_wei)

            min_gas_limit = await mav_contact.functions.minDstGasLookup(
                dst_chain_id,
                0
            ).call()

            if not min_gas_limit:
                min_gas_limit = 250000

            adapter_params = abi.encode(["uint16", "uint64"], [1, min_gas_limit])
            adapter_params = self.client.w3.to_hex(adapter_params[30:])
            try:
                estimate_fee = (await otf_wrapper_contract.functions.estimateSendFee(
                    mav_contact.address,
                    dst_chain_id,
                    dst_native_addr,
                    0,
                    False,
                    adapter_params,
                    (
                        dst_native_amount,
                        ZERO_ADDRESS,
                        '0x0000'
                    )
                ).call())[0]

                transaction = await otf_wrapper_contract.functions.sendOFT(
                    mav_contact.address,
                    dst_chain_id,
                    self.client.address,
                    amount_in_wei,
                    min_amount_out,
                    self.client.address,
                    ZERO_ADDRESS,
                    adapter_params,
                    (
                        dst_native_amount,
                        ZERO_ADDRESS,
                        '0x0000'
                    )
                ).build_transaction(await self.client.prepare_transaction(value=int(estimate_fee * 1.05)))
            except Exception as error:
                if '0xf4d678b8' in str(error):
                    raise SoftwareExceptionWithoutRetry('Insufficient balance in this chain!')
                else:
                    raise error
        elif from_token_name == 'USDV':
            router_contract = self.client.get_contract(TOKENS_PER_CHAIN[self.network]['USDV'], USDV_ABI)
            msg_contract_address = await router_contract.functions.getRole(3).call()
            msg_contract = self.client.get_contract(msg_contract_address, STARGATE_ABI['messagingV1'])

            min_gas_limit = await msg_contract.functions.minDstGasLookup(
                dst_chain_id,
                1
            ).call()

            if not min_gas_limit:
                min_gas_limit = 250000

            encode_address = abi.encode(["address"], [self.client.address])
            adapter_params = abi.encode(["uint16", "uint64"], [1, min_gas_limit])
            adapter_params = self.client.w3.to_hex(adapter_params[30:])

            try:
                estimate_fee = (await router_contract.functions.quoteSendFee(
                    [
                        encode_address,
                        amount_in_wei,
                        min_amount_out,
                        dst_chain_id
                    ],
                    adapter_params,
                    False,
                    "0x"
                ).call())[0]

                transaction = await router_contract.functions.send(
                    [
                        encode_address,
                        amount_in_wei,
                        min_amount_out,
                        dst_chain_id
                    ],
                    adapter_params,
                    [
                        dst_gas_for_call,
                        dst_native_amount,
                    ],
                    self.client.address,
                    '0x'
                ).build_transaction(await self.client.prepare_transaction(value=int(estimate_fee * 1.05)))
            except Exception as error:
                if '0xf4d678b8' in str(error):
                    raise SoftwareExceptionWithoutRetry('Insufficient balance in this chain!')
                else:
                    raise error
        elif from_token_name == 'ETH':
            router_eth_contract = self.client.get_contract(contracts['router_eth'], STARGATE_ABI['router_eth'])
            params_tuple = [
                dst_endpoint_id,
                abi.encode(['address'], [self.client.address]),
                amount_in_wei,
                min_amount_out,
                '0x',
                '0x',
                '0x'
            ]

            estimate_fee = int((await router_eth_contract.functions.quoteSend(
                params_tuple,
                False
            ).call())[0] * 1.05)

            transaction = await router_eth_contract.functions.send(
                params_tuple,
                [
                    estimate_fee,
                    0
                ],
                self.client.address
            ).build_transaction(await self.client.prepare_transaction(value=estimate_fee + amount_in_wei))
        elif from_token_name == 'USDC':
            router_usdc_contract = self.client.get_contract(contracts['router_usdc'], STARGATE_ABI['router_usdc'])
            params_tuple = [
                dst_endpoint_id,
                abi.encode(['address'], [self.client.address]),
                amount_in_wei,
                min_amount_out,
                '0x',
                '0x',
                '0x'
            ]
            estimate_fee = int((await router_usdc_contract.functions.quoteSend(
                params_tuple,
                False
            ).call())[0] * 1.05)

            token_address = TOKENS_PER_CHAIN[self.network][from_token_name]
            await self.client.check_for_approved(token_address, contracts['router_usdc'], amount_in_wei)

            transaction = await router_usdc_contract.functions.send(
                params_tuple,
                [
                    estimate_fee,
                    0
                ],
                self.client.address
            ).build_transaction(await self.client.prepare_transaction(value=estimate_fee))
        elif from_token_name == 'USDT':
            router_usdt_contract = self.client.get_contract(contracts['router_usdt'], STARGATE_ABI['router_usdt'])
            params_tuple = [
                dst_endpoint_id,
                abi.encode(['address'], [self.client.address]),
                amount_in_wei,
                min_amount_out,
                '0x',
                '0x',
                '0x'
            ]
            estimate_fee = int((await router_usdt_contract.functions.quoteSend(
                params_tuple,
                False
            ).call())[0] * 1.05)

            token_address = TOKENS_PER_CHAIN[self.network][from_token_name]
            await self.client.check_for_approved(token_address, contracts['router_usdt'], amount_in_wei)

            transaction = await router_usdt_contract.functions.send(
                params_tuple,
                [
                    estimate_fee,
                    0
                ],
                self.client.address
            ).build_transaction(await self.client.prepare_transaction(value=estimate_fee))
        else:
            router_contract = self.client.get_contract(contracts['router'], STARGATE_ABI['router'])
            scr_pool_id = STARGATE_POOLS_ID[self.network][from_token_name]
            dst_pool_id = STARGATE_POOLS_ID[dst_chain_name][to_token_name]
            function_type = 1

            estimate_fee = int((await router_contract.functions.quoteLayerZeroFee(
                dst_chain_id,
                function_type,
                STARGATE_CONTRACTS[dst_chain_name][to_token_name],
                "0x",
                (
                    dst_gas_for_call,
                    dst_native_amount,
                    dst_native_addr
                )
            ).call())[0] * 1.05)
            token_address = TOKENS_PER_CHAIN[self.network][from_token_name]

            await self.client.check_for_approved(token_address, contracts['router'], amount_in_wei)

            transaction = await router_contract.functions.swap(
                dst_chain_id,
                scr_pool_id,
                dst_pool_id,
                self.client.address,
                amount_in_wei,
                min_amount_out,
                [
                    dst_gas_for_call,
                    dst_native_amount,
                    dst_native_addr,
                ],
                self.client.address,
                '0x'
            ).build_transaction(await self.client.prepare_transaction(value=estimate_fee))

        tx_hash = await self.client.send_transaction(transaction, need_hash=True)

        return await self.client.wait_for_l0_received(tx_hash, need_wait=True)

    async def stake_stg(self, stakedata:tuple):
        stake_amount, stake_amount_in_wei, lock_time = stakedata

        self.logger_msg(
            *self.client.acc_info, msg=f'Stake {stake_amount} STG on {self.client.network.name} for {lock_time} days')

        stg_contract_address = TOKENS_PER_CHAIN[self.network]['STG']
        vestg_contract_address = VESTG_ADDRESS[self.network]
        vestg_contract = self.client.get_contract(vestg_contract_address, VESTG_ABI)
        deadline = int(int(time.time()) + (lock_time * 24 * 60 * 60))

        await self.client.check_for_approved(
            stg_contract_address, vestg_contract_address, stake_amount_in_wei, unlimited_approve=True
        )

        transaction = await vestg_contract.functions.create_lock(
            stake_amount_in_wei,
            deadline
        ).build_transaction(await self.client.prepare_transaction())

        return await self.client.send_transaction(transaction)
