import json
from web3 import Web3, HTTPProvider


class MintCat(object):

    def __init__(self, address, private_key, token_id):
        self.contract_address = "0xe48974CA12AD33b7327332eC444c59E474a58075"
        with open('abi.json', 'r') as f:
            self.abi = json.load(f)
        self.rpc = "https://rpc.mintchain.io"
        self.chain_id = 185
        self.address = address
        self.private_key = private_key
        self.token_id = token_id

    def invite_cat_for_playing(self, invitee):
        w3 = Web3(HTTPProvider(self.rpc))
        contract = w3.eth.contract(address=self.contract_address, abi=self.abi)
        func = contract.functions.inviteCatForPlaying(self.token_id, invitee)
        nonce = w3.eth.get_transaction_count(self.address)

        params = {
            'chainId': 185,
            'nonce': nonce,
            'from': self.address
        }
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(w3.to_hex(txn))

    def accept_play_date(self, invitee):
        w3 = Web3(HTTPProvider(self.rpc))
        contract = w3.eth.contract(address=self.contract_address, abi=self.abi)
        func = contract.functions.acceptPlayDate(self.token_id, invitee)
        nonce = w3.eth.get_transaction_count(self.address)
        params = {
            'chainId': 185,
            'nonce': nonce,
            'from': self.address
        }
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(w3.to_hex(txn))

    def clean_cat(self):
        w3 = Web3(HTTPProvider(self.rpc))
        contract = w3.eth.contract(address=self.contract_address, abi=self.abi)
        func = contract.functions.cleanCat(self.token_id)
        nonce = w3.eth.get_transaction_count(self.address)
        params = {
            'chainId': 185,
            'nonce': nonce,
            'from': self.address
        }
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(w3.to_hex(txn))

    def feed_cat(self):
        w3 = Web3(HTTPProvider(self.rpc))
        contract = w3.eth.contract(address=self.contract_address, abi=self.abi)
        func = contract.functions.feedCat(self.token_id)
        nonce = w3.eth.get_transaction_count(self.address)
        params = {
            'chainId': 185,
            'nonce': nonce,
            'from': self.address
        }
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(w3.to_hex(txn))

    def level_up(self):
        w3 = Web3(HTTPProvider(self.rpc))
        contract = w3.eth.contract(address=self.contract_address, abi=self.abi)
        func = contract.functions.levelUp(self.token_id)
        nonce = w3.eth.get_transaction_count(self.address)
        params = {
            'chainId': 185,
            'nonce': nonce,
            'from': self.address
        }
        tx = func.build_transaction(params)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        txn = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(w3.to_hex(txn))

    def can_clean(self):
        w3 = Web3(HTTPProvider(self.rpc))
        contract = w3.eth.contract(address=self.contract_address, abi=self.abi)
        result = contract.functions.canClean(self.token_id).call({'from': self.address})
        return result

    def can_feed(self):
        w3 = Web3(HTTPProvider(self.rpc))
        contract = w3.eth.contract(address=self.contract_address, abi=self.abi)
        result = contract.functions.canFeed(self.token_id).call({'from': self.address})
        return result

    def can_level_up(self):
        w3 = Web3(HTTPProvider(self.rpc))
        contract = w3.eth.contract(address=self.contract_address, abi=self.abi)
        result = contract.functions.canLevelUp(self.token_id).call({'from': self.address})
        return result

    def can_play(self):
        w3 = Web3(HTTPProvider(self.rpc))
        contract = w3.eth.contract(address=self.contract_address, abi=self.abi)
        result = contract.functions.canPlay(self.token_id).call({'from': self.address})
        return result

    def get_friends_list(self):
        w3 = Web3(HTTPProvider(self.rpc))
        contract = w3.eth.contract(address=self.contract_address, abi=self.abi)
        result = contract.functions.getFriendsList(self.token_id).call({'from': self.address})
        return result

    def get_play_invites_list(self):
        w3 = Web3(HTTPProvider(self.rpc))
        contract = w3.eth.contract(address=self.contract_address, abi=self.abi)
        result = contract.functions.getPlayInvitesList(self.token_id).call({'from': self.address})
        return result
