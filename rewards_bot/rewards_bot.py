import os
import sys
import logging
import requests

from pathlib import Path
from web3 import HTTPProvider, Web3, WebsocketProvider
from eth_account import Account
from config import *

w3 = Web3(HTTPProvider(RPC_URL))

def get_account():
    private_key = os.environ["PRIVATE_KEY"]
    assert private_key is not None, "You must set a PRIVATE_KEY environment variable"
    assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"
    return Account.from_key(private_key)

def claim_rewards():
    pass

def swap_rewards():
    account = get_account()
    headers = {'Content-Type': 'application/json'}
    params = {
        'chainId': CHAIN_ID,
        'from': FROM_TOKEN,
        'to': TO_TOKEN,
        'amount': '14992500000000000000',
        'receiver': account.address,
        'source': Path(__file__).stem
    }
    logging.info("Swap params: {}".format(params))
    response = requests.get(ROUTER_API, headers=headers, params=params)
    if response.status_code != 200:
        logging.warn("Unexpected code: {} from: {}".format(response.status, ROUTER_API))
        return
    else:
        response = response.json()

    router, data = response['encodedData']['router'], response['encodedData']['data']
    abi = requests.get(FANTOM_API.format(router)).text
    router_contract = w3.eth.contract(Web3.toChecksumAddress(router), abi=abi)

    fn_args = router_contract.decode_function_input(data)[1]
    logging.info("Swap function caller: {}".format(fn_args['caller']))
    logging.info("Swap function tuple: {}".format(fn_args['desc']))
    logging.info("Swap function data: {}".format(fn_args['data']))

    #router_contract.functions.swap(account, fn_args['desc'], fn_args['data']).call()
    #logging.info("Router: {}".format(response['encodedData']['router']))
    #logging.info("Data: {}".format(fn_args))

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)
    swap_rewards()
