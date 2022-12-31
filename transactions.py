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
# build transactions
# sign

sender = ''
receiver = ''
privateKey = pkey
print(privateKey)