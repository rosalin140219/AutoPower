import random
import requests
import json

from web3 import Web3, HTTPProvider
from loguru import logger


class Cultured(object):

    def __init__(self, address, private_key):
        # 用户钱包信息
        self.address = address
        self.private_key = private_key

        # rpc info
        self.chain_id = 161221135
        self.rpc = "https://plume-testnet.rpc.caldera.xyz/http"
        self.scan_url = "https://plume-testnet.explorer.caldera.xyz/"
        self.http_url = "https://testnet-rpc.plumenetwork.xyz/http"

        # 合约信息
        self.cultured_contract_address = "0x032139f44650481f4d6000c078820B8E734bF253"
        self.cultured_contract_name = "ERC1967Proxy"
        # abi
        with open('oracle_game_abi.json', 'r') as ff:
            self.oracle_game_abi = json.load(ff)

        # 加密货币预测
        self.cryptos = [
            ("ETHUSDT", 0, "0xe940f6a900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"),
            ("BTCUSDT", 2, "0xe940f6a900000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000001"),
            ("ARBUSDT", 4, "0xe940f6a900000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000001"),
            ("SOLUSDT", 6, "0xe940f6a900000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000001"),
            ("TIAUSDT", 8, "0xe940f6a900000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000001"),
            ("MKRUSDT", 10, "0xe940f6a9000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000000000001"),
            ("ONDOUSDT", 12, "0xe940f6a9000000000000000000000000000000000000000000000000000000000000000c0000000000000000000000000000000000000000000000000000000000000001")
        ]

        # Forex 外汇预测
        self.forex = [
            ("EURUSD", 3, "0xe940f6a900000000000000000000000000000000000000000000000000000000000000030000000000000000000000000000000000000000000000000000000000000001"),
            ("USDJPY", 4, "0xe940f6a900000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000"),
            ("GBPUSD", 5, "0xe940f6a900000000000000000000000000000000000000000000000000000000000000050000000000000000000000000000000000000000000000000000000000000000"),
            ("USDVND", 7, "0xe940f6a900000000000000000000000000000000000000000000000000000000000000070000000000000000000000000000000000000000000000000000000000000000"),
            ("USDHKD", 9, "0xe940f6a900000000000000000000000000000000000000000000000000000000000000090000000000000000000000000000000000000000000000000000000000000000"),
            ("USDSGD", 11, "0xe940f6a9000000000000000000000000000000000000000000000000000000000000000b0000000000000000000000000000000000000000000000000000000000000000"),
            ("USDINR", 13, "0xe940f6a9000000000000000000000000000000000000000000000000000000000000000d0000000000000000000000000000000000000000000000000000000000000000")
        ]

    def predict_price_movement(self, predict_tye):
        global item
        w3 = Web3(HTTPProvider(self.rpc))
        nonce = w3.eth.get_transaction_count(self.address)
        params = {
            'chainId': self.chain_id,
            'nonce': nonce,
            # 'value': amount,
            'from': w3.to_checksum_address(self.address),
            # 'gas': 400000,
            # 'gasPrice': w3.to_wei(5, 'gwei'),
            # 'maxFeePerGas': w3.to_wei(5, 'gwei'),
            # 'maxPriorityFeePerGas': w3.to_wei(0.1, 'gwei'),
        }
        contract = w3.eth.contract(address=self.cultured_contract_address, abi=self.oracle_game_abi)
        # 随机取一项
        if predict_tye == 'crypto':
            item = random.choice(self.cryptos)
        elif predict_tye == 'forex':
            item = random.choice(self.forex)
        check = self.check(item[2])
        if check:
            is_long = random.choice([True, False])
            func = contract.functions.predictPriceMovement(item[1], is_long)
            tx = func.build_transaction(params)
            signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
            txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_url = self.scan_url + "tx/" + w3.to_hex(txn)
            logger.info(f"predict crypto:{item[0]} success, tx:{tx_url}")
            return txn
        else:
            logger.error("execution reverted: Wait for cooldown")

    def check(self, sign):
        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": random.randint(0, 10000),
            "method": "eth_call",
            "params": [
                {
                    "data": sign,
                    "from": self.address,
                    "to": self.cultured_contract_address
                },
                "latest"
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", self.http_url, headers=headers, data=payload)
        logger.info(f"check predict price movement status response:{response.text}")
        if 'result' in json.loads(response.text):
            result = json.loads(response.text)['result']
            return result == '0x'
        else:
            return False


if __name__ == '__main__':
    with open('../wallet.json', 'r') as f:
        wallets = json.load(f)
    for wallet in wallets:
        env = wallet['env']
        logger.info(f"正在执行环境:{env}的Cultured项目操作")
        address = wallet['address']
        private_key = wallet['private_key']
        cultured = Cultured(address, private_key)
        cultured.predict_price_movement("forex")
