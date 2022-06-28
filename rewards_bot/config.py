CHAIN_ID = 250
RPC_URL = "https://rpc.ftm.tools/"
ROUTER_API = "https://router.firebird.finance/aggregator/v1/route"
ETHSCAN_API = "http://api.ftmscan.com/api?module=contract&action=getabi&address={}&format=raw&apikey={}"
FROM_TOKEN = "0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83" # DEUS
TO_TOKEN = "0xde12c7959e1a72bbe8a5f7a1dc8f8eef9ab011b3" # USDC
WFTM_TOKEN = "0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83" # WFTM
USDC_TOKEN = "0x04068da6c83afcfa0e13ba15a6696662335d5b75" # USDC
# FROM_TOKEN = "0x# " # WFTM
# TO_TOKEN = "0x" # DEI
REWARD_CONTRACT = "0x67932809213afd6bac5ecd2e4e214fe18209c419"
ROUTER_CONTRACT = "0xe0c38b2a8d09aad53f1c67734b9a95e43d5981c0"
LOG_FORMAT = "%(asctime)s logLevel=%(levelname)s logger=%(name)s - %(message)s"