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

def get_balance(account, token):
    token_abi = requests.get(ETHSCAN_API.format(token, os.environ["ETHSCAN_API_KEY"])).text
    token_contract = w3.eth.contract(Web3.toChecksumAddress(USDC_TOKEN), abi=token_abi)
    balance = \
        token_contract.functions.balanceOf(Web3.toChecksumAddress(account.address)).call()
    return balance

def claim_rewards():
    account = get_account()
    reward_abi = requests.get(ETHSCAN_API.format(REWARD_CONTRACT_ADDRESS,  os.environ["ETHSCAN_API_KEY"])).text
    reward_contract = w3.eth.contract(Web3.toChecksumAddress(REWARD_CONTRACT_ADDRESS), abi=reward_abi)
    logging.info(reward_contract.all_functions())
    #logging.info(reward_contract.functions.userNftDeposits(Web3.toChecksumAddress(account.address)).call())

def swap_rewards():
    account = get_account()
    balance = get_balance(account, USDC_TOKEN)
    logging.info("Account: {}, USDC: {}".format(account.address, balance))
    if (balance == 0):
        logging.info("Zero balance - nothingto swap")
        return
    headers = {"Content-Type": "application/json"}
    params = {
        "chainId": CHAIN_ID,
        "from": USDC_TOKEN,
        "to": DEI_TOKEN,
        "amount": str(balance),
        "receiver": account.address,
        "source": Path(__file__).stem
    }
    logging.info("Swap params: {}".format(params))
    response = requests.get(ROUTER_API, headers=headers, params=params)
    if response.status_code != 200:
        logging.warn("Unexpected code: {} from: {}".format(response.status, ROUTER_API))
        return
    else:
        response = response.json()

    router, data = response["encodedData"]["router"], response["encodedData"]["data"]
    abi = requests.get(ETHSCAN_API.format(router,  os.environ["ETHSCAN_API_KEY"])).text
    router_contract = w3.eth.contract(Web3.toChecksumAddress(router), abi=abi)
    fn_args = router_contract.decode_function_input(data)[1]

    nonce = w3.eth.get_transaction_count(Web3.toChecksumAddress(account.address))
    tx = router_contract.functions.swap(
        Web3.toChecksumAddress(fn_args["caller"]),
        fn_args["desc"],
        fn_args["data"]
    ).buildTransaction({
        'chainId': CHAIN_ID,
        'gas': 850000,
        'maxFeePerGas': w3.toWei('10', 'gwei'),
        'maxPriorityFeePerGas': w3.toWei('8.5', 'gwei'),
        'nonce': nonce,
    })
    logging.info("Swapping...")
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=os.environ["PRIVATE_KEY"])
    result = w3.eth.send_raw_transaction(signed_tx.rawTransaction)  
    receipt = w3.eth.wait_for_transaction_receipt(result)
    logging.info("Swap completed, result: {}".format(receipt["status"]))

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)
    try:
        os.environ["ETHSCAN_API_KEY"]
    except KeyError as e:
        logging.exception('Missing required environment variable ETHSCAN_API_KEY')
        sys.exit(1)
    claim_rewards()
    sys.exit(0)
    swap_rewards()
