import json
import time

from web3 import Web3, HTTPProvider
from loguru import logger


class NestStaking(object):
    def __init__(self, address, private_key):
        self.contract_address = "0xA34420e04DE6B34F8680EE87740B379103DC69f6"
        self.contract_name = "NestStaking"

        self.chain_id = 161221135
        self.rpc = "https://plume-testnet.rpc.caldera.xyz/http"
        self.scan_url = "https://plume-testnet.explorer.caldera.xyz/"

        self.gn_usd = "0x5c1409a46cd113b3a667db6df0a8d7be37ed3bb3"

        # 执行的钱包信息
        self.address = address
        self.private_key = private_key

        with open('neststaking_abi.json', 'r') as ff:
            self.abi = json.load(ff)

        with open('gnusd_abi.json', 'r') as ff:
            self.gnusd_abi = json.load(ff)

    def approve_gnusd(self, amount):
        w3 = Web3(HTTPProvider(self.rpc))
        nonce = w3.eth.get_transaction_count(self.address)
        params = {
            'chainId': self.chain_id,
            'nonce': nonce,
            # 'value': amount,
            'from': w3.to_checksum_address(self.address),
            'gas': 400000
        }
        contract = w3.eth.contract(address=w3.to_checksum_address(self.gn_usd), abi=self.gnusd_abi)
        func = contract.functions.approve(w3.to_checksum_address(self.contract_address), amount)
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_url = self.scan_url + "tx/" + w3.to_hex(txn)
        logger.info(f"approve gnUSD to NestStaking success, tx:{tx_url}")

    def stake(self, amount):
        w3 = Web3(HTTPProvider(self.rpc))
        nonce = w3.eth.get_transaction_count(self.address)
        params = {
            'chainId': self.chain_id,
            'nonce': nonce,
            # 'value': amount,
            'from': w3.to_checksum_address(self.address),
            'gas': 400000
        }
        contract = w3.eth.contract(address=self.contract_address, abi=self.abi)
        func = contract.functions.stake(amount)
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_url = self.scan_url + "tx/" + w3.to_hex(txn)
        logger.info(f"stake gnUSD success, tx:{tx_url}")

    def claim(self):
        w3 = Web3(HTTPProvider(self.rpc))
        nonce = w3.eth.get_transaction_count(self.address)
        params = {
            'chainId': self.chain_id,
            'nonce': nonce,
            # 'value': amount,
            'from': w3.to_checksum_address(self.address),
            # 'gas': 400000,
            # 'gasPrice': w3.to_wei(0.1, 'gwei'),
            # 'maxFeePerGas': w3.to_wei(2, 'gwei'),
            # 'maxPriorityFeePerGas': w3.to_wei(2, 'gwei'),
        }
        contract = w3.eth.contract(address=self.contract_address, abi=self.abi)
        func = contract.functions.claim()
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_url = self.scan_url + "tx/" + w3.to_hex(txn)
        logger.info(f"claim all rewards success, tx:{tx_url}")


if __name__ == '__main__':
    with open('../wallet.json', 'r') as f:
        wallets = json.load(f)
    for wallet in wallets:
        env = wallet['env']
        logger.info(f"正在执行环境:{env}的staking操作")
        address = wallet['address']
        private_key = wallet['private_key']
        nest = NestStaking(address, private_key)
        try:
            nest.approve_gnusd(100000000000000000000)
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行staking:approve失败，失败原因:{e}")
        time.sleep(10)

        try:
            nest.stake(100000000000000000000)
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行staking:stake失败，失败原因:{e}")