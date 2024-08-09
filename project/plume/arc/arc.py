import json
import random

from web3 import Web3, HTTPProvider
from loguru import logger


class PlumeArc(object):
    def __init__(self, address, private_key):
        # 用户钱包信息
        self.address = address
        self.private_key = private_key

        # rpc info
        self.chain_id = 161221135
        self.rpc = "https://plume-testnet.rpc.caldera.xyz/http"
        self.scan_url = "https://plume-testnet.explorer.caldera.xyz/"

        #合约信息
        self.arc_contract_address = "0x485D972889Ee8fd0512403E32eE94dE5c7a5DC7b"
        self.arc_contract_name = "ERC1967Proxy"
        with open('./arc/arc_abi.json', 'r') as ff:
            self.arc_abi = json.load(ff)

        # token项目列表: 名称-图片
        self.items = [
            (0, "Museum Grade Art", "https://miles.plumenetwork.xyz/images/arc/art.webp"),
            (1, "Rare Pokemon Cards", "https://miles.plumenetwork.xyz/images/arc/collectible-cards.webp"),
            (2, "Soy Beans", "https://miles.plumenetwork.xyz/images/arc/farming.webp"),
            (3, "Rare Scotch", "https://miles.plumenetwork.xyz/images/arc/investment-alcohol.webp"),
            (4, "Limited Edition Cuban Cigars", "https://miles.plumenetwork.xyz/images/arc/investment-cigars.webp"),
            (5, "Luxury Watches", "https://miles.plumenetwork.xyz/images/arc/investment-watch.webp"),
            (6, "1/1 Jordan's", "https://miles.plumenetwork.xyz/images/arc/rare-sneakers.webp"),
            (7, "NYC Commercial Real Estate", "https://miles.plumenetwork.xyz/images/arc/real-estate.webp"),
            (8, "Solar Farms", "https://miles.plumenetwork.xyz/images/arc/solar-energy.webp"),
            (9, "GPUs for AI", "https://miles.plumenetwork.xyz/images/arc/tokenized-gpus.webp")
        ]

    def create_token(self):
        w3 = Web3(HTTPProvider(self.rpc))
        nonce = w3.eth.get_transaction_count(self.address)
        params = {
            'chainId': self.chain_id,
            'nonce': nonce,
            # 'value': amount,
            'from': w3.to_checksum_address(self.address),
            # 'gas': 400000,
            # 'gasPrice': w3.to_wei(5, 'gwei'),
            # 'maxFeePerGas': w3.to_wei(1, 'gwei'),
            # 'maxPriorityFeePerGas': w3.to_wei(0.1, 'gwei'),
        }
        contract = w3.eth.contract(address=self.arc_contract_address, abi=self.arc_abi)
        # 随机取一项
        item = random.choice(self.items)
        func = contract.functions.createToken(item[1], "ITEM", item[1], item[0], item[2])
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_url = self.scan_url + "tx/" + w3.to_hex(txn)
        logger.info(f"create item in Plume Arc success, tx:{tx_url}")
        return txn
