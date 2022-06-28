import os
import sys
import logging
import requests

from web3 import HTTPProvider, Web3, WebsocketProvider
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
    logging.info("Found account: {}".format(account.address))


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)
    swap_rewards()
