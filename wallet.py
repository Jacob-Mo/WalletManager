from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

class NetworkConfig:
    networks = {
        'Ethereum': os.getenv('ETHEREUM_PROVIDER_URL'),
        'BinanceSmartChain': os.getenv('BSC_PROVIDER_URL'),
    }

class Wallet:
    def __init__(self, network):
        self.network = network
        self.connect_to_network()

    def connect_to_network(self):
        provider_url = NetworkConfig.networks.get(self.network)
        if not provider_url:
            raise ValueError("Unsupported network")

        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        if not self.web3.isConnected():
            raise ConnectionError(f"Failed to connect to {self.network}")

    def create_wallet(self):
        account = self.web3.eth.account.create()
        return {'address': account.address, 'private_key': account.privateKey.hex()}

    def fetch_balance(self, address):
        balance = self.web3.eth.get_balance(address)
        return self.web3.fromWei(balance, 'ether')

    def send_transaction(self, from_address, private_key, to_address, amount):
        nonce = self.web3.eth.getTransactionCount(from_address)

        transaction = {
            'nonce': nonce,
            'to': to_address,
            'value': self.web3.toWei(amount, 'ether'),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
        }
        signed_transaction = self.web3.eth.account.signTransaction(transaction, private_key)
        transaction_hash = self.web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

        return self.web3.toHex(transaction_hash)

if __name__ == "__main__":
    wallet = Wallet('Ethereum')
    new_wallet = wallet.create_wallet()
    print(f"New Wallet Address: {new_wallet['address']}")
    print(f"Balance: {wallet.fetch_balance(new_wallet['address'])} ETH")