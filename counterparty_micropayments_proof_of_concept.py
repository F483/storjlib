

# Proof of concept micropayment channel
# https://en.bitcoin.it/wiki/Contract#Example_7:_Rapidly-adjusted_.28micro.29payments_to_a_pre-determined_party
#
# Needs counterparty lib/api http://counterparty.io/docs/counterparty_lib/
#   ez counterparty server setup http://counterparty.io/docs/federated_node/
#   or use public dev server https://coindaddy.io/public-development-servers


# OP_CHECKLOCKTIMEVERIFY required!!


import json
import requests
import btctxstore
from requests.auth import HTTPBasicAuth


# setup
testnet = True
url = "http://public.coindaddy.io:14000/api/"
headers = {'content-type': 'application/json'}
auth = HTTPBasicAuth('rpc', "1234")
asset = "A14456548018133352000"
quantity = 20

# payer
alice_key = "cTvCnpvQJE3TvNejkWbnFA1z6jLJjB2xXXapFabGsazCz2QNYFQb"  # has funds
alice_address = "n2WQGAvnDS1vf7uXToLou6kLxJXRGFHo2b"

# payee
bob_key = "cQYT6HjZTUrniAb96s5ktjvGGZNBjbhd6SicC7s49RLcBBXmx3cz"  # has funds
bob_address = "mgkr4TjXCGMJSpcoQGi6wDkr72NTtkuMDs"


# channel address
multisig_address = ("2_mgkr4TjXCGMJSpcoQGi6wDkr72NTtkuMDs"
                    "_n2WQGAvnDS1vf7uXToLou6kLxJXRGFHo2b_2")


def rpc_call(payload):
    response = requests.post(url, data=json.dumps(payload),
                             headers=headers, auth=auth)
    return json.loads(response.text)


blockchain = btctxstore.BtcTxStore(testnet=testnet)


# Alice creates and signs secret funding tx to multisig address
funding_tx_hex = rpc_call({
  "method": "create_send",
  "params": {
    "source": alice_address,
    "destination": multisig_address,
    "quantity": quantity,
    'asset': asset,
  },
  "jsonrpc": "2.0",
  "id": 0,
})["result"]
funding_tx_hex = blockchain.sign_tx(funding_tx_hex, [alice_key])
print "Alice's secret funding TX:", funding_tx_hex


# Alice creates and signs initial refund nlocktime tx
unsigned_tx = rpc_call({
    "method": "create_send",
    "params": {
        "source": multisig_address,
        "destination": alice_address,
        "quantity": quantity,
        'asset': asset,
    },
    "jsonrpc": "2.0",
    "id": 0,
})

# TODO Bob signs initial refund transaction

# TODO Alice verifies initial refund transaction

# TODO Alice broadcasts the funding tx

# TODO wait for confirmation, thus locking the funds and opening the channel

# TODO Bob creates and sign new refund tx with small payment to self

# TODO Alice signs new refund tx
