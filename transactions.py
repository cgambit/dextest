from web3 import Web3
import os

pkey = os.environ.get('private_key')

# connect to the network

node_url = 'https://nd-174-389-806.p2pify.com/579e4bc57a8f733ad2f333fdc2354f3c/ext/bc/C/rpc' #from chainstack C-Chain HTTPS endpoint
web3 = Web3(Web3.HTTPProvider(node_url))

if web3.isConnected():
	print('Connection Successful')
else:
	print('Connection Failed')

# set the addresses
sender = '0xbA4eD1bE76587e000588fc3499707cAF581E626b'
receiver = '0x16233bbDe3ed87E6a5627e8E2B03Dc5C15320a8D'
private_key = pkey

nonce = web3.eth.getTransactionCount(sender)

# build the transaction
tx = {
	'nonce': nonce,
	'to': receiver,
	'value': web3.toWei(0.5, 'ether'),
	'gas': 200000,
	'gasPrice': web3.toWei(100, 'gwei')
}

# sign tx
signed_tx = web3.eth.account.signTransaction(tx, private_key)

# send transaction
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
print('Transaction Hash:', web3.toHex(tx_hash))