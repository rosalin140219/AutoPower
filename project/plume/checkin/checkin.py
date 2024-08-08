import json
import time
from web3 import Web3, HTTPProvider
import requests
from loguru import logger


class Checkin(object):

    def __init__(self, address, private_key, proxy):
        self.chain_id = 161221135
        self.rpc = "https://plume-testnet.rpc.caldera.xyz/http"
        self.scan_url = "https://plume-testnet.explorer.caldera.xyz/"
        self.checkin_contract_address = "0x8Dc5b3f1CcC75604710d9F464e3C5D2dfCAb60d8"
        self.faucet_contract_address = "0x075e2D02EBcea5dbcE6b7C9F3D203613c0D5B33B"
        self.address = address
        self.private_key = private_key
        self.proxy = proxy

    def check_in(self):
        try:
            w3 = Web3(HTTPProvider("https://plume-testnet.rpc.caldera.xyz/http"))
            with open('checkin_abi.json', 'r') as f:
                abi = json.load(f)
            contract = w3.eth.contract(address=self.checkin_contract_address, abi=abi)
            func = contract.functions.checkIn()
            nonce = w3.eth.get_transaction_count(self.address)
            params = {
                'chainId': self.chain_id,
                'nonce': nonce,
                'from': self.address
            }
            tx = func.build_transaction(params)
            signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
            txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            hash = self.scan_url + "tx/" + w3.to_hex(txn)
            logger.info(f"签到成功，交易hash地址: {hash}")
        except Exception as e:
            logger.error(f"地址:{self.address}签到失败，失败原因:{e}")


if __name__ == '__main__':

    with open('../wallet.json', 'r') as f:
        wallets = json.load(f)

    # 签到
    for wallet in wallets:
        try:
            env = wallet['env']
            logger.info(f"正在执行环境:{env}的签到")
            address = wallet['address']
            private_key = wallet['private_key']
            proxy = wallet['proxy']
            plume = Checkin(address, private_key, proxy)
            plume.check_in()
        except Exception as e:
            logger.error(f"环境:{wallet['env']}签到失败，失败原因:{e}")