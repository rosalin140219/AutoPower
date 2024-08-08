import json
import time

from web3 import Web3, HTTPProvider
from loguru import logger


class SolidViolet(object):

    def __init__(self, address, private_key):
        self.contract_address = "0x06107C39D3Fd57a059Bc4Abae09f3b2b3d75D64E"

        # self.spender_address = "0x06107c39d3fd57a059bc4abae09f3b2b3d75d64e"

        #gnUSD
        self.gnusd_contract_address = "0x5c1409a46cD113b3A667Db6dF0a8D7bE37ed3BB3"

        # USD+
        self.usd_contract_address = "0x4194dddfb5938293621e78dd72e9bb22e59515d0"

        self.chain_id = 161221135
        self.rpc = "https://plume-testnet.rpc.caldera.xyz/http"
        self.scan_url = "https://plume-testnet.explorer.caldera.xyz/"

        # 执行的钱包信息
        self.address = address
        self.private_key = private_key

        with open('abi.json', 'r') as ff:
            self.abi = json.load(ff)

        with open('gnusd_abi.json', 'r') as ff:
            self.gnusd_abi = json.load(ff)

    def approve(self, amount):
        w3 = Web3(HTTPProvider(self.rpc))
        nonce = w3.eth.get_transaction_count(self.address)
        params = {
            'chainId': self.chain_id,
            'nonce': nonce,
            # 'value': amount,
            'from': self.address,
            # 'gas': 400000,
            # 'gasPrice': w3.to_wei(5, 'gwei'),
            # 'maxFeePerGas': w3.to_wei(5, 'gwei'),
            # 'maxPriorityFeePerGas': w3.to_wei(5, 'gwei'),
        }
        contract = w3.eth.contract(address=self.gnusd_contract_address, abi=self.gnusd_abi)
        func = contract.functions.approve(self.contract_address, amount)
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_url = self.scan_url + "tx/" + w3.to_hex(txn)
        logger.info(f"approve gnusd success, tx:{tx_url}")
        return txn

    def execute_swap(self, amount, mint_amount_out):
        w3 = Web3(HTTPProvider(self.rpc))
        nonce = w3.eth.get_transaction_count(self.address)
        params = {
            'chainId': self.chain_id,
            'nonce': nonce,
            # 'value': amount,
            'from': self.address,
            # 'gas': 400000,
            # 'gasPrice': w3.to_wei(5, 'gwei'),
            # 'maxFeePerGas': w3.to_wei(5, 'gwei'),
            # 'maxPriorityFeePerGas': w3.to_wei(5, 'gwei'),
        }
        contract = w3.eth.contract(address=self.contract_address, abi=self.abi)
        # 构造请求参数
        req = (
            (
                self.address, self.contract_address, self.gnusd_contract_address, amount,
                self.usd_contract_address, mint_amount_out, 0,
                [
                    (self.gnusd_contract_address, "", 0),
                    (self.usd_contract_address, "", 0)
                ]
            )
        )
        func = contract.functions.executeSwap(*req)
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_url = self.scan_url + "tx/" + w3.to_hex(txn)
        logger.info(f"execute swap gnusd for usd success, tx:{tx_url}")
        return txn


if __name__ == '__main__':
    with open('../wallet.json', 'r') as f:
        wallets = json.load(f)
    for wallet in wallets:
        try:
            env = wallet['env']
            logger.info(f"正在执行环境:{env}的SolidViolet合约的approve操作")
            address = wallet['address']
            private_key = wallet['private_key']
            solid_violet = SolidViolet(address, private_key)
            # solid_violet.approve(1000000000000000000)
            # time.sleep(10)
            solid_violet.execute_swap(1000000000000000000, 1000000)
        except Exception as e:
            logger.error(f"环境:{wallet['env']}SolidViolet合约的approve操作失败，失败原因:{e}")