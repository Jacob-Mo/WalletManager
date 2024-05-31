from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = getenv('DEBUG', 'False') == 'True'
    SECRET_KEY = getenv('SECRETKEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URI', 'sqlite:///your_default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ETHEREUM_NODE_URL = getenv('ETHEREUM_NODE_URL', 'default_ethereum_node_url')
    BINANCE_SMART_CHAIN_URL = getenv('BINANCE_SMART_CHAIN_URL', 'default_bsc_node_url')
    OTHER_BLOCKCHAIN_NODE_URL = getenv('OTHER_BLOCKCHAIN_NODE_URL', 'default_other_blockchain_node_url')