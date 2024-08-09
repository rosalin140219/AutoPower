import json
import time
import requests
from loguru import logger
from web3 import Web3, HTTPProvider


class Faucet(object):
    def __init__(self, address, private_key, proxy):
        self.chain_id = 161221135
        self.rpc = "https://plume-testnet.rpc.caldera.xyz/http"
        self.scan_url = "https://plume-testnet.explorer.caldera.xyz/"
        self.faucet_contract_address = "0x075e2D02EBcea5dbcE6b7C9F3D203613c0D5B33B"
        self.address = address
        self.private_key = private_key
        self.proxy = proxy

    def faucet(self, token):
        with open('./faucet/faucet_abi.json', 'r') as ff:
            abi = json.load(ff)
        sign_res = self.get_sign(token)
        logger.info(f"get faucet token: {token} sign response:{sign_res}")
        w3 = Web3(HTTPProvider(self.rpc))
        nonce = w3.eth.get_transaction_count(self.address)
        params = {
            'chainId': self.chain_id,
            'nonce': nonce,
            'from': self.address
        }
        contract = w3.eth.contract(address=self.faucet_contract_address, abi=abi)
        func = contract.functions.getToken(token, sign_res['salt'], sign_res['signature'])
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_url = self.scan_url + "tx/" + w3.to_hex(txn)
        logger.info(f"get faucet success, tx:{tx_url}")

    def get_sign(self, token):
        headers = {
            "User_Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            'Content-Type': 'application/json'
        }

        proxies = {
            'http': self.proxy,
            'https': self.proxy
        }
        url = "https://faucet.plumenetwork.xyz/api/faucet"
        payload = json.dumps({
            "walletAddress": self.address,
            "token": token
        })
        if self.proxy is not None:
            response = requests.request("POST", url, headers=headers, data=payload, proxies=proxies)
        else:
            response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.text)
