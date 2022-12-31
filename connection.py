from web3 import Web3

# connect to the network

node_url = 'https://nd-174-389-806.p2pify.com/579e4bc57a8f733ad2f333fdc2354f3c/ext/bc/C/rpc' #from chainstack C-Chain HTTPS endpoint
web3 = Web3(Web3.HTTPProvider(node_url))

if web3.isConnected():
	print('Connection Successful')
else:
	print('Connection Failed')


#balance
balance = web3.eth.get_balance('0xa225Fdef8F8Daf001AfaD2597314093fEBa28B6A')
normal_number = web3.fromWei(balance, 'ether')
print(normal_number)