import pytest
from web3 import Web3
from web3.providers.eth_tester import EthereumTesterProvider
from web3.test_utils import (
    construct_tester_chain,
    get_open_port,
)
import os
from dotenv import load_dotenv

load_dotenv()

class Wallet:
    def __init__(self, address, provider_uri=os.getenv('WEB3_PROVIDER_URI')):
        self.web3 = Web3(Web3.HTTPProvider(provider_uri))
        self.address = address
    
    def get_balance(self, network='mainnet'):
        if network == 'mainnet':
            return self.web3.eth.get_balance(self.address)
        else:
            raise ValueError('Network not supported')
    
    def send_transaction(self, to_address, amount):
        tx = {
            'from': self.address,
            'to': to_address,
            'value': amount,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
        }
        sign_tx = self.web3.eth.account.sign_transaction(tx, os.getenv('PRIVATE_KEY'))
        return self.web3.eth.send_raw_transaction(sign_tx.rawTransaction)

@pytest.fixture
def web3_instance():
    provider = EthereumTesterProvider()
    web3 = Web3(provider)
    construct_tester_chain(web3, num_blocks=100)
    return web3

@pytest.fixture
def wallet_address(web3_instance):
    return web3_instance.eth.account.create().address

@pytest.fixture
def wallet(web3_instance, wallet, address):
    port = get_open_port()
    provider_uri = f"http://localhost:{port}"
    return Wallet(wallet_address, provider_uri)

def test_create_wallet(wallet_address):
    assert Wallet(wallet_address) is not None, "Failed to create a Wallet instance"

def test_fetch_balance(wallet, web3_instance):
    initial_balance = web3_instance.eth.get_balance(wallet.address)
    assert wallet.get_balance() == initial_balance, "Balance mismatch"

def test_send_transaction(wallet, web3_instance):
    to_address = web3_instance.eth.account.create().address
    initial_balance = web3_instance.eth.get_balance(to_address)
    transaction_amount = 1000000

    wallet.send_transaction(to_address, transaction_amount)
    new_balance = web3_instance.eth.get_balance(to_address)

    assert new_balance - initial_balance == transaction_amount, "Transaction amount does not match"