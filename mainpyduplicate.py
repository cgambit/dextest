from web3 import Web3
import os

pkey = os.environ.get('private_key')

# connect to the network
node_url = 'https://nd-174-389-806.p2pify.com/579e4bc57a8f733ad2f333fdc2354f3c/ext/bc/C/rpc' #from chainstack C-Chain HTTPS endpoint
w3 = Web3(Web3.HTTPProvider(node_url))

if w3.isConnected():
	print('Connection Successful')
else:
	print('Connection Failed')

# set the addresses
sender = '0xbA4eD1bE76587e000588fc3499707cAF581E626b'
receiver = '0x16233bbDe3ed87E6a5627e8E2B03Dc5C15320a8D'
private_key = pkey

def transfer_wavax():
    token_address = '0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E'
    token_abi = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]'
    token_contract = w3.eth.contract(token_address, abi=token_abi)

    # token balance
    token_balance = token_contract.functions.balanceOf(sender).call()
    print('Token Balance : ', w3.fromWei(token_balance, 'ether'))

    # erc20 transfer
    nonce = w3.eth.getTransactionCount(sender)
    transaction = token_contract.functions.transfer(
        receiver, 
        w3.toWei(1, 'ether')).buildTransaction({
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': w3.eth.gas_price
    })

    sign_transaction = w3.eth.account.sign_transaction(transaction, private_key)
    transaction_hash = w3.eth.sendRawTransaction(sign_transaction.rawTransaction)
    print('WAVAX transfer transaction hash : ', w3.toHex(transaction_hash))

if __name__ == "__main__":
    transfer_wavax()