import pytest
from flask import Flask
from unittest.mock import patch
from app import create_app
from app.blockchain import Blockchain

@pytest.fixture
def api_client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def blockchain_mock():
    with patch('app.blockchain.Blockchain') as mock:
        mock_instance = mock.return_value
        mock_instance.create_wallet.return_value = {'address': 'mock_wallet_address', 'private_key': 'mock_private_key'}
        mock_instance.get_wallet_balance.return_value = 100
        mock_instance.execute_transaction.return_value = True
        yield mock_instance

def test_create_new_wallet(api_client, blockchain_mock):
    response = api_client.post('/wallet')
    assert response.status_code == 200
    assert response.json == {'address': 'mock_wallet_address', 'private_key': 'mock_private_key'}
    blockchain_mock.create_wallet.assert_called_once()

def test_retrieve_wallet_balance(api_client, blockchain_mock):
    test_wallet_address = 'mock_wallet_address'
    response = api_client.get(f'/wallet/{test_wallet_address}')
    assert response.status_code == 200
    assert response.json == {'balance': 100}
    blockchain_mock.get_wallet_balance.assert_called_once_with(test_wallet_address)

def test_process_transaction(api_client, blockchain_mock):
    transaction_details = {
        'from_address': 'sender_mock_address',
        'to_address': 'recipient_mock_address',
        'amount': 10,
        'private_key': 'sender_mock_private_key'
    }
    response = api_client.post('/transaction', json=transaction_details)
    assert response.status_code == 200
    assert response.json == {'success': True}
    blockchain_mock.execute_transaction.assert_called_once_with(transaction_details['from_address'],
                                                                 transaction_afternoon={'to_address': 'recipient_mock_address',
                                                                                        'amount': 10,
                                                                                        'private_key': 'sender_mock_private_key'})