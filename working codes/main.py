from web3 import Web3
import os

pkey = os.environ.get('carlglibrary')

# connect to the network
node_url = 'https://nd-174-389-806.p2pify.com/579e4bc57a8f733ad2f333fdc2354f3c/ext/bc/C/rpc' #from chainstack C-Chain HTTPS endpoint
w3 = Web3(Web3.HTTPProvider(node_url))

if w3.isConnected():
	print('Connection Successful')
else:
	print('Connection Failed')

# set the addresses
sender = Web3.toChecksumAddress('0xdFf9e2bd6841481D48259789bf303fF0203f7a34') # carlglibrary metamask wallet
receiver = Web3.toChecksumAddress('0x59A0Fc8Db4d4E07bB53F2242AD53FA05F077475e') # CGB1 infinity wallet
private_key = pkey

def transfer_avax():
    balance = w3.eth.get_balance(sender)
    print(type(balance))
    print('AVAX Balance : ', w3.fromWei(balance, 'ether'))
    # avax_to_send = balance - w3.toWei(0.3, 'ether')
    # print('AVAX to Send : ', w3.fromWei(avax_to_send, 'ether'))

    tx = {
        'nonce': w3.eth.getTransactionCount(sender),
        'to': receiver,
        # 'value': w3.fromWei(avax_to_send, 'ether'),
        'value': w3.toWei(0.1, 'ether'),
        'gas': 200000,
        'gasPrice': w3.eth.gas_price
    }
    
    sign_transaction = w3.eth.account.sign_transaction(tx, private_key)
    transaction_hash = w3.eth.sendRawTransaction(sign_transaction.rawTransaction)
    print('AVAX transfer transaction hash : ', w3.toHex(transaction_hash))

if __name__ == "__main__":
    transfer_avax()