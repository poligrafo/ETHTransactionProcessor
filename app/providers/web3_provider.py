import logging
from web3 import Web3
from web3.middleware import geth_poa_middleware

from app.core.settings import settings

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Connect to Ethereum network via Infura
INFURA_URL = f"https://mainnet.infura.io/v3/{settings.INFURA_API_KEY}"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

if w3.is_connected():
    logger.info("Successfully connected to Infura")
else:
    logger.error("Failed to connect to Infura")

# Apply middleware for compatibility with some networks like Rinkeby
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
