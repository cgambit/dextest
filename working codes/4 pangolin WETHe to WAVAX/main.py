from web3 import Web3
import config as c
import time

# This script will Swap WETH.e to WAVAX in Pangolin

# ------------------------------- INITIALIZE -------------------------------- #

w3 = Web3(Web3.HTTPProvider(c.RPC_URL))

if w3.isConnected():
    print('Connection Successful')
else:
    print('Connection Failed')

# ---------------------------- SWAP TOKENS ----------------------------- #
def swap_token(sell_token, receive_token):
    contract = w3.eth.contract(address=w3.toChecksumAddress(c.PANGOLIN_ROUTER_CONTRACT_ADDRESS), abi=c.AVA_ABI)

    contract_id = w3.toChecksumAddress(sell_token)
    sell_token_contract = w3.eth.contract(contract_id, abi=c.WETHe_ABI)

    balance = sell_token_contract.functions.balanceOf(c.SENDER_ADDRESS).call()  # How many USDT do we have?
    print(balance)

    sell_amt = balance 
    print(sell_amt)

    txn = contract.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        sell_amt,
        0,  # MinAmountOut
        [sell_token, receive_token],  # Path, which token to spend, which to get
        c.SENDER_ADDRESS,  # Our own (metamask) wallet address
        (int(time.time()) + 10000)  # Deadline
    ).buildTransaction({
        'from': c.SENDER_ADDRESS,
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(c.SENDER_ADDRESS),
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=c.PRIVATE_KEY)
    tx_token = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx = w3.toHex(tx_token)
    return tx

# ---------------------------- WAIT FOR RECEIPT ----------------------------- #
def awaitReceipt(tx):
    try:
        return w3.eth.wait_for_transaction_receipt(tx, timeout=30)
    except Exception as ex:
        print('Failed to wait for receipt: ', ex)
        return None


if __name__ == "__main__":
    sell_token = w3.toChecksumAddress(c.WETHe_ADDRESS) 
    receive_token = w3.toChecksumAddress(c.WAVAX_ADDRESS)

    swap_tx = swap_token(sell_token, receive_token)
    print(swap_tx)

    swap_receipt = awaitReceipt(swap_tx) # Wait for transaction to finish

    if swap_receipt.status == 1: # Check if the transaction went through
        print('Swap Successfully!')
    else:
        print('Swap Failed,  Exiting...')
        exit()