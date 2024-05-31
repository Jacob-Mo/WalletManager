from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_address = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'wallet_address': self.wallet_address,
            'balance': self.balance
        }

@app.route('/api/wallet', methods=['POST'])
def create_wallet():
    data = request.get_json()
    new_wallet = Wallet(wallet_address=data['wallet_address'], balance=0)
    db.session.add(new_wallet)
    db.session.commit()
    return jsonify(new_wallet.to_dict()), 201

@app.route('/api/wallet/<wallet_address>', methods=['GET'])
def get_wallet(wallet_address):
    wallet = Wallet.query.filter_by(wallet_address=wallet_address).first()
    if wallet:
        return jsonify(wallet.to_dict()), 200
    else:
        return jsonify({"message": "Wallet not found"}), 404

@app.route('/api/wallet/interact', methods=['POST'])
def interact_with_blockchain():
    data = request.get_json()
    response = {
        "message": "Interacted with blockchain network",
        "data": data
    }
    return jsonify(response), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)