from flask import Flask, jsonify, request
import os
from wallet import Wallet

app = Flask(__name__)

app.config.from_envvar('YOUR_ENV_FILE_PATH')

wallet = Wallet()

@app.route('/wallet/create', methods=['POST'])
def create_wallet():
    try:
        wallet_id, private_key = wallet.create_wallet()
        return jsonify({"wallet_id": wallet_id, "private_key": private_key}), 200
    except Exception as e:
        return jsonify({"error": "Unable to create wallet"}), 500

@app.route('/wallet/balance/<string:wallet_id>', methods=['GET'])
def get_wallet_balance(wallet_id):
    try:
        balance = wallet.get_balance(wallet_id)
        return jsonify({"wallet_id": wallet_id, "balance": balance}), 200
    except KeyError:
        return jsonify({"error": "Wallet not found"}), 404

@app.route('/wallet/send', methods=['POST'])
def send_transaction():
    data = request.json
    sender_wallet_id = data.get('sender_wallet_id')
    recipient_wallet_id = data.get('recipient_wallet_id')
    amount = data.get('amount')
    
    if not all([sender_wallet_id, recipient_wallet_id, amount]):
        return jsonify({"error": "Missing data"}), 400

    try:
        transaction_hash = wallet.send_transaction(sender_wallet_id, recipient_wallet_id, amount)
        return jsonify({"transaction": transaction_hash}), 200
    except Exception as e:
        return jsonify({"error": "Transaction failed"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)