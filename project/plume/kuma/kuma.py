import json
import time

import requests
from web3 import Web3, HTTPProvider
from loguru import logger


class Kuma(object):
    def __init__(self, address, private_key):
        # mint合约
        self.mint_contract_address = "0x8504a242d86C7D84Fd11E564e6291f0A20d6C2a2"
        self.contract_name = "KUMAMint"

        # approve合约
        self.bond_token_contract_address = "0x763Ccc2Cb06Eb8932208C5714ff5c010894Ac98d"
        self.bond_token_name = "KUMABondToken"
        self.approve_address_to = "0xa4e9ddad862a1b8b5f8e3d75a3aad4c158e0faab"

        # sell bond合约
        self.sell_bond_contract_address = "0xA4E9ddAD862A1B8b5F8e3d75a3AAd4C158E0faaB"
        self.sell_bond_name = "ERC1967Proxy"

        self.chain_id = 161221135
        self.rpc = "https://plume-testnet.rpc.caldera.xyz/http"
        self.scan_url = "https://plume-testnet.explorer.caldera.xyz/"

        # 执行的钱包信息
        self.address = address
        self.private_key = private_key

        with open('kuma_abi.json', 'r') as ff:
            self.abi = json.load(ff)

        with open('bond_token_abi.json', 'r') as ff:
            self.bond_token_abi = json.load(ff)

        with open('kuma_swap_abi.json', 'r') as ff:
            self.kuma_swap_abi = json.load(ff)

    def mint_aick(self):
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
        contract = w3.eth.contract(address=self.mint_contract_address, abi=self.abi)
        func = contract.functions.mintAICK()
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_url = self.scan_url + "tx/" + w3.to_hex(txn)
        logger.info(f"mint AICK success, tx:{tx_url}")
        return w3.to_hex(txn)

    def approve(self, token_id):
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
            # 'maxPriorityFeePerGas': w3.to_wei(5, 'gwei'),
        }
        contract = w3.eth.contract(address=self.bond_token_contract_address, abi=self.bond_token_abi)
        func = contract.functions.approve(w3.to_checksum_address(self.approve_address_to), token_id)
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_url = self.scan_url + "tx/" + w3.to_hex(txn)
        logger.info(f"approve token:{token_id} success, tx:{tx_url}")
        return txn

    def sell_bond(self, token_id):
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
            # 'maxPriorityFeePerGas': w3.to_wei(5, 'gwei'),
        }
        contract = w3.eth.contract(address=self.sell_bond_contract_address, abi=self.kuma_swap_abi)
        func = contract.functions.sellBond(token_id)
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_url = self.scan_url + "tx/" + w3.to_hex(txn)
        logger.info(f"sell token:{token_id} success, tx:{tx_url}")
        return txn

    def get_all_user_kuma_bond_tokens(self):
        query = "query allUserKumaBondTokens($owner: Bytes!) {\n  kumabondTokens(where: {owner: $owner}) {\n    ...KUMA_BOND_TOKEN_FRAGMENT\n  }\n}\n\nfragment RISK_CATEGORY_FRAGMENT on RiskCategory {\n  issuer\n  currency\n  id\n  term\n}\n\nfragment MINIMAL_KIBT_FRAGMENT on KIBToken {\n  name\n  symbol\n  id\n  address\n  epochLength\n  decimals\n}\n\nfragment KUMA_BOND_TOKEN_FRAGMENT on KUMABondToken {\n  tokenId: id\n  ownerAddress: owner\n  expired\n  redeemed\n  cusip\n  isin\n  issuance\n  maturity\n  coupon\n  principal\n  riskCategory {\n    ...RISK_CATEGORY_FRAGMENT\n    kibToken: KIBToken {\n      ...MINIMAL_KIBT_FRAGMENT\n    }\n  }\n}"
        operationName = "allUserKumaBondTokens"
        variables = {
            "owner": self.address
        }
        query_param = {
            "query": query,
            "variables": variables,
            "operationName": operationName
        }
        url = "https://api.goldsky.com/api/public/project_clyh18uad08wu01uah2zi4h1k/subgraphs/kuma-plume-testnet/0.1.0/gn"

        payload = json.dumps(query_param)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info(f"query all user kuma bond tokens response:{response.text}")
        token_id_list = []
        if response.status_code == 200:
            kuma_bond_tokens = json.loads(response.text)['data']['kumabondTokens']
            if len(kuma_bond_tokens) > 0:

                for kuma_bond_token in kuma_bond_tokens:
                    token_id_list.append(kuma_bond_token['tokenId'])
                return token_id_list
        else:
            return token_id_list


if __name__ == '__main__':
    with open('../wallet.json', 'r') as f:
        wallets = json.load(f)
    for wallet in wallets:
        env = wallet['env']
        logger.info(f"正在执行环境:{env}的Kuma项目交互操作")
        address = wallet['address']
        private_key = wallet['private_key']
        kuma = Kuma(address, private_key)
        try:
            tx = kuma.mint_aick()
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行MintAICK失败，失败原因:{e}")

        time.sleep(60)
        try:
            token_id_list = kuma.get_all_user_kuma_bond_tokens()
            if len(token_id_list) > 0:
                for token_id in token_id_list:
                    time.sleep(30)
                    kuma.approve(int(token_id))
                    time.sleep(30)
                    kuma.sell_bond(int(token_id))
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行SellBond失败，失败原因:{e}")