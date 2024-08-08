import json
import time
from web3 import Web3, HTTPProvider
from loguru import logger


class LandShare(object):

    def __init__(self, address, private_key):
        # 用户钱包信息
        self.address = address
        self.private_key = private_key

        # rpc info
        self.chain_id = 161221135
        self.rpc = "https://plume-testnet.rpc.caldera.xyz/http"
        self.scan_url = "https://plume-testnet.explorer.caldera.xyz/"

        #合约信息 land swap
        self.land_swap_contract_address = "0xd2aade12760d5e176f93c8f1c6ae10667c8fca8b"
        self.land_swap_contract_name = "LandshareSwap"
        with open('land_swap_abi.json', 'r') as ff:
            self.land_swap_abi = json.load(ff)

        #合约信息 approve gnUSD
        self.approve_contract_address = "0x5c1409a46cD113b3A667Db6dF0a8D7bE37ed3BB3"
        self.approve_contract_name = "ERC1967Proxy"
        with open('gnusd_abi.json', 'r') as ff:
            self.gnusd_abi = json.load(ff)

        # master chef contract
        self.master_chef_contract_address = "0x5374cf69c5610950526c668a7b540df6686531b4"
        self.master_chef_contract_name = "MasterChef"
        with open('master_chef_abi.json', 'r') as ff:
            self.master_chef_abi = json.load(ff)

        # land share token
        self.land_share_token_contract_address = "0x45934E0253955dE498320D67c0346793be44BEC0"
        self.land_share_token_contract_name = "LandshareToken"
        with open('land_share_token_abi.json', 'r') as ff:
            self.land_share_token_abi = json.load(ff)

    """
    Swap 0.1 gnUSD for 0.1 LAND. LAND is the native utility and governance token of the Landshare ecosystem.
    """
    def approve_gnusd(self):
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
        contract = w3.eth.contract(address=self.approve_contract_address, abi=self.gnusd_abi)
        func = contract.functions.approve(w3.to_checksum_address(self.land_swap_contract_address), 100000000000000000)
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_url = self.scan_url + "tx/" + w3.to_hex(txn)
        logger.info(f"approve gnUSD for the Landshare ecosystem success, tx:{tx_url}")
        return txn

    """
    Swap 0.1 gnUSD for 0.1 LAND. LAND is the native utility and governance token of the Landshare ecosystem.
    """
    def swap(self):
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
        contract = w3.eth.contract(address=w3.to_checksum_address(self.land_swap_contract_address), abi=self.land_swap_abi)
        func = contract.functions.swap()
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_url = self.scan_url + "tx/" + w3.to_hex(txn)
        logger.info(f"Swap 0.1 gnUSD for 0.1 LAND success, tx:{tx_url}")
        return txn

    def approve_land(self):
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
        contract = w3.eth.contract(address=w3.to_checksum_address(self.land_share_token_contract_address), abi=self.land_share_token_abi)
        func = contract.functions.approve(w3.to_checksum_address(self.master_chef_contract_address), 100000000000000000)
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_url = self.scan_url + "tx/" + w3.to_hex(txn)
        logger.info(f"approve land vault success, tx:{tx_url}")
        return txn

    def deposit(self):
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
        contract = w3.eth.contract(address=w3.to_checksum_address(self.master_chef_contract_address), abi=self.master_chef_abi)
        func = contract.functions.deposit(0, 100000000000000000)
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_url = self.scan_url + "tx/" + w3.to_hex(txn)
        logger.info(f"deposit land success, tx:{tx_url}")
        return txn


if __name__ == '__main__':
    with open('../wallet.json', 'r') as f:
        wallets = json.load(f)
    for wallet in wallets:
        env = wallet['env']
        logger.info(f"正在执行环境:{env}的LandShare项目操作")
        address = wallet['address']
        private_key = wallet['private_key']
        land_share = LandShare(address, private_key)
        try:
            land_share.approve_gnusd()
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行LandShare:approve_gnUsd失败，失败原因:{e}")
        time.sleep(10)

        try:
            land_share.swap()
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行LandShare:swapLand失败，失败原因:{e}")
        time.sleep(10)

        try:
            land_share.approve_land()
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行LandShare:approveLand失败，失败原因:{e}")

        time.sleep(10)
        try:
            land_share.deposit()
        except Exception as e:
            logger.error(f"环境:{wallet['env']}执行LandShare:deposit失败，失败原因:{e}")