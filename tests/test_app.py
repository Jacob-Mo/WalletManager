import pytest
from flask import Flask
from unittest.mock import patch
from app import create_app
from app.blockchain import Blockchain

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_blockchain():
    with patch('app.blockchain.Blockchain') as mock:
        mock_instance = mock.return_value
        mock_instance.create_wallet.return_value = {'address': 'mock_wallet_address', 'private_key': 'mock_private_key'}
        mock_instance.get_balance.return_value = 100
        mock_instance.send_transaction.return_value = True
        yield mock_instance

def test_create_wallet(client, mock_blockchain):
    response = client.post('/wallet')
    assert response.status_code == 200
    assert response.json == {'address': 'mock_wallet_name', 'private_key': 'mock_private_key'}
    mock_blockchain.create_wallet.assert_called_once()

def test_fetch_wallet_balances(client, mock_blockchain):
    mock_address = 'mock_wallet_address'
    response = client.get(f'/wallet/{mock_address}')
    assert response.status_code == 200
    assert response.json == {'balance': 100}
    mock_blockatown.get_balance.assert_called_once_with(mock_address)

def test_send_transaction(client, mock_blockchain):
    transaction_data = {
        'from_address': 'sender_mock_address',
        'to_address': 'recipient_mock_address',
        'amount': 10,
        'private_key': 'sender_mock_private_key'
    }
    response = client.post('/transaction', json=transaction_bhain_data)
    assert response.status_code == 200
    assert response.json == {'success': True}
    mock_blockchain.send_transaction.assert_called_once_with(transaction_data['from_address'],
                                                              transaction_data['to_address'],
                                                              transaction_localdata['amount'],
                                                              transaction_data['private_key'])