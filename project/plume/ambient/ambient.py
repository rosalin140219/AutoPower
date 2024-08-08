import json

from web3 import Web3, HTTPProvider
from loguru import logger


class Ambient(object):

    def __init__(self, address, private_key):
        self.contract_address = "0x4c722A53Cf9EB5373c655E1dD2dA95AcC10152D1"
        self.contract_name = "Ambient"

        self.chain_id = 161221135
        self.rpc = "https://plume-testnet.rpc.caldera.xyz/http"
        self.scan_url = "https://plume-testnet.explorer.caldera.xyz/"

        self.gn_usd = "0x5c1409a46cd113b3a667db6df0a8d7be37ed3bb3" # gnUSD代币
        self.goon = "0xba22114ec75f0d55c34a5e5a3cf384484ad9e733"   # GOON代币

        # 执行的钱包信息
        self.address = address
        self.private_key = private_key

        with open('ambient_abi.json', 'r') as ff:
            self.abi = json.load(ff)

    def swap(self):
        w3 = Web3(HTTPProvider(self.rpc))
        nonce = w3.eth.get_transaction_count(w3.to_checksum_address(self.address))
        params = {
            'chainId': self.chain_id,
            'nonce': nonce,
            'from': w3.to_checksum_address(self.address)
        }
        contract = w3.eth.contract(address=self.contract_address, abi=self.abi)
        func = contract.functions.swap(w3.to_checksum_address(self.gn_usd), w3.to_checksum_address(self.goon),
                                       36000, False, False, 1000000000000000000, 0, 65537, 989047015792546300000, 0)
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_url = self.scan_url + "tx/" + w3.to_hex(txn)
        logger.info(f"swap GOON to gnUSD success, tx:{tx_url}")


if __name__ == '__main__':
    with open('../wallet.json', 'r') as f:
        wallets = json.load(f)
    for wallet in wallets:
        try:
            env = wallet['env']
            logger.info(f"正在执行环境:{env}的swap")
            address = wallet['address']
            private_key = wallet['private_key']
            ambient = Ambient(address, private_key)
            ambient.swap()
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行swap失败，失败原因:{e}")
