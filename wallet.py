from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

class Wallet:
    def __init__(self, network):
        """Initialize Wallet with a specific network."""
        self.network = network
        self.provider = None
        self.web3 = None
        self.connect_to_network()

    def connect_to_network(self):
        """Establish a connection to the specified blockchain network."""
        networks = {
            'Ethereum': 'ETHEREUM_PROVIDER_URL',
            'BinanceSmartChain': 'BSC_PROVIDER_URL',
        }

        provider_env_var = networks.get(self.network)
        if not provider_env_var:
            raise ValueError("Unsupported network")

        provider_url = os.getenv(provider_env_var)
        self.provider = provider_url

        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        if not self.web3.isConnected():
            raise ConnectionError(f"Failed to connect to {self.network}")

    def create_wallet(self):
        """Create a new wallet with a unique address and private key."""
        account = self.web3.eth.account.create()
        return {'address': account.address, 'private_key': account.privateKey.hex()}

    def fetch_balance(self, address):
        """Retrieve the balance of a given address."""
        balance = self.web3.eth.get_balance(address)
        return self.web3.fromWei(balance, 'ether')

    def send_transaction(self, from_address, private_key, to_address, amount):
        """Send a transaction from one address to another."""
        nonce = self.web.reth.getTransactionCount(from_address)

        transaction = {
            'nonce': nonce,
            'to': to_address,
            'value': self.web3.toWei(amount, 'ether'),
            'gas': 2000000,  # You might want to adjust this based on the network status
            'gasPrice': self.web3.toWei('50', 'gwei'),  # Ditto, consider fetching current gas prices
        }
        signed_transaction = self.web3.eth.account.signTransaction(transaction, private_key)
        transaction_hash = self.web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

        return self.web3.toHex(transaction_hash)

if __name__ == "__main__":
    wallet = Wallet('Etherethm')
    new_wallet = wallet.create_wallet()
    print(f"New Wallet Address: {new_wallet['address']}")
    print(f"Balance: {wallet.fetch_balance(new_wallet['address'])} ETH")