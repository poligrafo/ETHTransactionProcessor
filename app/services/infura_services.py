import os
import requests
import json


class InfuraService:
    def __init__(self):
        self.infura_url = f'https://mainnet.infura.io/v3/{os.getenv("INFURA_API_KEY")}'

    def get_latest_block_number(self):
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_blockNumber",
            "params": [],
            "id": 1
        }
        headers = {'content-type': 'application/json'}
        response = requests.post(self.infura_url, data=json.dumps(payload), headers=headers).json()
        return response['result']

    def get_block_by_number(self, block_number):
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBlockByNumber",
            "params": [block_number, True],
            "id": 1
        }
        headers = {'content-type': 'application/json'}
        response = requests.post(self.infura_url, data=json.dumps(payload), headers=headers).json()
        return response['result']
