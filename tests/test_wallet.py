import pytest
from web3 import Web3
from web3.providers.eth_tester import EthereumTesterProvider
from web3.middleware import geth_poa_middleware
from web3.exceptions import TransactionNotFound, BlockNotFound
from hexbytes import HexBytes
import os
from dotenv import load_dotenv

load_dotenv()

class Wallet:
    def __init__(self, address, provider_uri=os.getenv('WEB3_PROVIDER_URI')):
        self.web3 = Web3(Web3.HTTPProvider(provider_uri))
        if not self.web3.isConnected():
            raise ConnectionError("Failed to connect to Web3 provider.")
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.address = address
        # Assuming this wallet will always use the same account for transactions:
        self.nonce = self.web3.eth.getTransactionCount(address)
    
    def get_balance(self, network='mainnet'):
        try:
            if network == 'mainnet':
                return self.web3.eth.get_balance(self.address)
            else:
                raise ValueError('Network not supported')
        except ValueError as e:
            raise e
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            raise
    
    def send_transaction(self, to_address, amount):
        try:
            tx = {
                'nonce': self.nonce,
                'from': self.address,
                'to': to_address,
                'value': amount,
                'gas': 2000000,
                'gasPrice': self.web3.toWei('50', 'gwei'),
            }
            self.nonce += 1  # Increment nonce for the next transaction
            sign_tx = self.web3.eth.account.sign_transaction(tx, os.getenv('PRIVATE_KEY'))
            tx_hash = self.web3.eth.send_raw_transaction(sign_tx.rawTransaction)
            self.web3.eth.wait_for_transaction_receipt(tx_hash)  # Wait for the transaction to be included in a block.
            return tx_hash
        except Exception as e:
            raise TransactionError(f"Failed to send transaction: {str(e)}")

class TransactionError(Exception):
    pass

@pytest.fixture
def web3_instance():
    provider = EthereumTesterProvider()
    web3 = Web3(provider)
    web3.eth.generate_blocks(100)
    return web3

@pytest.fixture
def wallet_address(web3_instance):
    return web3_instance.eth.account.create().address

@pytest.fixture
def wallet(web3_instance, wallet_address):
    port = 8545
    provider_uri = f"http://localhost:{port}"
    return Wallet(wallet_address, provider_uri)

def test_create_wallet(wallet_address):
    assert Wallet(wallet_address) is not None, "Failed to create a Wallet instance"

def test_fetch_balance(wallet, web3_instance):
    try:
        initial_balance = web3_instance.eth.get_balance(wallet.address)
    except BlockNotFound:
        pytest.fail("Block for fetching balance not found.")
    assert wallet.get_balance() == initial_balance, "Balance mismatch"

def test_send_transaction(wallet, web3_instance):
    to_address = web3_instance.eth.account.create().address
    try:
        initial_balance = web3_instance.eth.get_balance(to_address)
    except BlockNotFound:
        pytest.fail("Block for pre-transaction balance fetch not found.")
    
    transaction_amount = 1000000

    try:
        tx_hash = wallet.send_transaction(to_address, transaction_amount)
        tx_receipt = web3_instance.eth.wait_for_transaction_receipt(tx_hash)
    except TransactionError as e:
        pytest.fail(str(e))
    except Exception as e:
        pytest.fail(f"Unexpected error during transaction: {str(e)}")

    try:
        new_balance = web3_instance.eth.get_balance(to_address)
    except BlockNotFound:
        pytest.fail("Block for post-transaction balance check not found.")
    
    assert new_balance - initial_balance == transaction_amount, "Transaction amount does not match"