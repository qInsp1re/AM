import random

from eth_abi import abi
from web3.contract import AsyncContract

from config.constants import HYPERLANE_DATA, NAUTILUS_CONTRACTS, TOKENS_PER_CHAIN
from config.abi import USENEXUS_ABI
from modules import Logger, CosmosClient, Client, SolanaClient
from modules.interfaces import SoftwareExceptionWithoutRetry
from dev_settings import Settings
from utils.tools import helper, gas_checker


class Nautilus(Logger):
    def __init__(self, client: CosmosClient | Client | SolanaClient):
        self.client = client
        Logger.__init__(self)

    @helper
    @gas_checker
    async def bridge(self, bridge_data):
        types_info = {
            'BNB Chain': 0,
            'Nautilus': 0,
            'Solana': 1,
        }

        src_chain_name, dst_chain_name, src_token_name, dsr_token_name, amount, amount_in_wei = bridge_data

        source_chain_type = types_info.get(src_chain_name, 'BAD')
        destination_chain_type = types_info.get(dst_chain_name, 'BAD')

        if source_chain_type == 'BAD' or destination_chain_type == 'BAD':
            raise SoftwareExceptionWithoutRetry('Nautilus bridge support only BNB Chain <-> Nautilus routes')

        bridge_info = f'{amount} {src_token_name} {src_chain_name} -> {dsr_token_name} {dst_chain_name}'
        self.logger_msg(*self.client.acc_info, msg=f'Bridge on Nautilus: {bridge_info}')

        # 0 = EVM ,1 = Solana
        if source_chain_type == 1 and destination_chain_type == 0:
            from solders.compute_budget import set_compute_unit_limit
            from solders.pubkey import Pubkey
            from solders.instruction import AccountMeta
            from solders.keypair import Keypair
            from solders.instruction import Instruction
            from solders.compute_budget import set_compute_unit_price

            unit_price_ix = set_compute_unit_price(random.randint(100000, 150000))
            unit_limit_ix = set_compute_unit_limit(1_000_000)

            src_token_address = TOKENS_PER_CHAIN['Solana'][src_token_name]
            unique_message_account_keypair = Keypair()
            mailbox_program_id = Pubkey.from_string("Ge9atjAc3Ltu91VTbNpJDCjZ9CFxFyck4h3YBcTF9XPq")
            igp_program_id = Pubkey.from_string("HksFWQM1EXJJ5mxo2uZoMfmksXHaNhCunh71NqcQQHZ8")
            token_program = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
            associated_token_program = Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")

            seeds = [
                bytes(self.client.wallet.pubkey()),
                bytes(token_program),
                bytes(Pubkey.from_string(src_token_address)),
            ]

            pda, _ = Pubkey.find_program_address(seeds, associated_token_program)

            dispatched_message_key, _dispatched_message_bump = Pubkey.find_program_address(
                [
                    b"hyperlane",
                    b"-",
                    b"dispatched_message",
                    b"-",
                    bytes(unique_message_account_keypair.pubkey())
                ],
                mailbox_program_id
            )

            # Вычисление программного адреса для gas_payment_pda_key
            gas_payment_pda_key, _ = Pubkey.find_program_address(
                [
                    b"hyperlane_igp",
                    b"-",
                    b"gas_payment",
                    b"-",
                    bytes(unique_message_account_keypair.pubkey())
                ],
                igp_program_id
            )

            accounts = [
                AccountMeta(Pubkey.from_string("11111111111111111111111111111111"), is_writable=False, is_signer=False), # 1
                AccountMeta(Pubkey.from_string("noopb9bkMVfRPU8AsbpTUg8AQkHtKwMYZiFUjNRtMmV"), is_writable=False, is_signer=False), # 2
                AccountMeta(Pubkey.from_string("DmgszocR2orub3FbEPbYfdU1aqWUcT1kLXpAwEU3hgdz"), is_writable=False, is_signer=False), # 3
                AccountMeta(Pubkey.from_string("Ge9atjAc3Ltu91VTbNpJDCjZ9CFxFyck4h3YBcTF9XPq"), is_writable=False, is_signer=False), # 4
                AccountMeta(Pubkey.from_string("GTcS6omUcQLu4coU3ZcweSSpFaViQy5ZJSQm1fRmZvLA"), is_writable=True, is_signer=False), # 5
                AccountMeta(Pubkey.from_string("GSYXBSDaY7Tr6rq6iWnEkbuPc8Tn5kvd42KETDYcHRhJ"), is_writable=False, is_signer=False), # 6
                AccountMeta(self.client.wallet.pubkey(), is_writable=True, is_signer=True), # 7
                AccountMeta(unique_message_account_keypair.pubkey(), is_writable=False, is_signer=True), # 8
                AccountMeta(dispatched_message_key, is_writable=True, is_signer=False), # 9
                AccountMeta(Pubkey.from_string("HksFWQM1EXJJ5mxo2uZoMfmksXHaNhCunh71NqcQQHZ8"), is_writable=False, is_signer=False), # 10
                AccountMeta(Pubkey.from_string("69HWkRJUpW4tpvZU6ASeBJ4bTGe3vr8Km29vawFUaHkw"), is_writable=True, is_signer=False), # 11
                AccountMeta(gas_payment_pda_key, is_writable=True, is_signer=False), # 12
                AccountMeta(Pubkey.from_string("GTj6WzNxLNFydq5zJrV9p13fyqotRoo1MQykNCWuVpbS"), is_writable=False, is_signer=False), # 13
                AccountMeta(Pubkey.from_string("FCNfmLSZLo5x7oNYmkYU8WdPUu7pj636P9CaMxkmaCp7"), is_writable=True, is_signer=False), # 14
                AccountMeta(Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"), is_writable=False, is_signer=False), # 15
                AccountMeta(Pubkey.from_string(src_token_address), is_writable=True, is_signer=False), # 16
                AccountMeta(pda, is_writable=True, is_signer=False), # 17
                AccountMeta(Pubkey.from_string("D7r5ysukjidyoGaUWxdcCyyF9hsoCMfBauuUu2VBCeb1"), is_writable=True, is_signer=False), # 18
            ]

            dest_chain_int = HYPERLANE_DATA['domains'][dst_chain_name]
            dst_address = abi.encode(['address'], [self.client.evm_address])

            program_id = NAUTILUS_CONTRACTS[self.client.network.name][src_token_name]

            destination_domain_bytes = dest_chain_int.to_bytes(4, byteorder='little')
            recipient_bytes = dst_address
            amount_or_id_bytes = amount_in_wei.to_bytes(32, byteorder='little')

            serialized_data = destination_domain_bytes + recipient_bytes + amount_or_id_bytes

            buf = bytearray([1] * 9)
            buf.extend(serialized_data)

            bridge_ix = Instruction(
                program_id=Pubkey.from_string(program_id),
                data=bytes(buf),
                accounts=accounts,
            )

            old_balance_data_on_dst = await self.client.wait_for_receiving(
                chain_to_name=dst_chain_name, token_name=dsr_token_name,
                check_balance_on_dst=True
            )

            await self.client.send_transaction(
                instructions=[unit_price_ix, unit_limit_ix, bridge_ix],
                signers=[self.client.wallet, unique_message_account_keypair],
                raw_mode=True
            )

        else:
            dest_chain_int = HYPERLANE_DATA['domains'][dst_chain_name]
            bridge_contract: AsyncContract = self.client.get_contract(
                NAUTILUS_CONTRACTS[self.client.network.name][src_token_name], USENEXUS_ABI['router']
            )

            srt_token_address = TOKENS_PER_CHAIN[src_chain_name][src_token_name]

            if src_token_name != self.client.network.token:
                await self.client.check_for_approved(srt_token_address, bridge_contract.address, amount_in_wei)

            bridge_gas_fee = await bridge_contract.functions.quoteGasPayment(
                dest_chain_int
            ).call()

            if dst_chain_name != 'Solana':
                dst_address = abi.encode(['address'], [self.client.address])
            else:
                from solders.keypair import Keypair
                sol_address = Keypair.from_base58_string(self.client.solana_private_key).pubkey()
                int_address = self.client.w3.to_int(sol_address.__bytes__())
                dst_address = abi.encode(['uint256'], [int_address])

            value = bridge_gas_fee
            if self.client.network.name == 'Nautilus' and src_token_name == 'ZBC':
                amount_in_wei -= int(round(random.uniform(55, 60), 6) * 10 ** 18)  # fee support
                value += amount_in_wei

            if amount_in_wei < 0:
                raise SoftwareExceptionWithoutRetry('Account balance - bridge fee < 0')

            transaction = await bridge_contract.functions.transferRemote(
                dest_chain_int,
                dst_address,
                amount_in_wei
            ).build_transaction(await self.client.prepare_transaction(value=value))

            old_balance_data_on_dst = await self.client.wait_for_receiving(
                chain_to_name=dst_chain_name, token_name=dsr_token_name,
                check_balance_on_dst=True
            )

            await self.client.send_transaction(transaction)

        if Settings.WAIT_FOR_RECEIPT:

            self.logger_msg(
                *self.client.acc_info, msg=f"Bridge complete. Note: wait a little for receiving funds",
                type_msg='success'
            )

            return await self.client.wait_for_receiving(
                chain_to_name=dst_chain_name, token_name=dsr_token_name,
                old_balance_data=old_balance_data_on_dst,
            )
        else:
            return True
