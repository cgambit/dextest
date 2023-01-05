from web3 import Web3
import os

# connect to the network
node_url = 'https://nd-174-389-806.p2pify.com/579e4bc57a8f733ad2f333fdc2354f3c/ext/bc/C/rpc' #from chainstack C-Chain HTTPS endpoint
w3 = Web3(Web3.HTTPProvider(node_url))

if w3.isConnected():
	print('Connection Successful')
else:
	print('Connection Failed')

# set the addresses
# sender = Web3.toChecksumAddress('0xdFf9e2bd6841481D48259789bf303fF0203f7a34') # carlglibrary metamask wallet
# receiver = Web3.toChecksumAddress('0x59A0Fc8Db4d4E07bB53F2242AD53FA05F077475e') # CGB1 infinity wallet

receiver = '0x59A0Fc8Db4d4E07bB53F2242AD53FA05F077475e' # CGB1 infinity wallet

def transfer_avax(acct_sender, pkey):
    sender = acct_sender
    private_key = pkey

    balance = w3.eth.get_balance(sender)
    print(type(balance))
    print('AVAX Balance : ', w3.fromWei(balance, 'ether'))

    # to send AVAX with some AVAX balance in wallet
    avax_to_send = balance - w3.toWei(0.3, 'ether')
    print('AVAX to Send : ', avax_to_send)

    tx = {
        'nonce': w3.eth.getTransactionCount(sender),
        'to': receiver,
        'value': avax_to_send, # to send AVAX with some AVAX balance in wallet
        # 'value': w3.toWei(0.1, 'ether'), # code for sending specific AVAX qty
        'gas': 21000,
        'gasPrice': w3.eth.gas_price,
        'chainId': 43114
    }
    
    sign_transaction = w3.eth.account.sign_transaction(tx, private_key)
    transaction_hash = w3.eth.sendRawTransaction(sign_transaction.rawTransaction)
    tx = w3.toHex(transaction_hash)
    return tx

# ---------------------------- WAIT FOR RECEIPT ----------------------------- #
def awaitReceipt(tx):
    try:
        return w3.eth.wait_for_transaction_receipt(tx, timeout=30)
    except Exception as ex:
        print('Failed to wait for receipt: ', ex)
        return None

if __name__ == "__main__":
    # Transaction for carlglibrary metamask wallet
    acct_sender = '0x16233bbDe3ed87E6a5627e8E2B03Dc5C15320a8D'
    pkey = os.environ.get('hbminerfan') # remember to update value to sync with wallet

    send_tx = transfer_avax(acct_sender, pkey)
    print(send_tx)

    send_receipt = awaitReceipt(send_tx) # Wait for transaction to finish

    if send_receipt.status == 1: # Check if the transaction went through
        print('Transferred Successfully!')
    else:
        print('Transfer Failed,  Exiting...')
        exit()

    
