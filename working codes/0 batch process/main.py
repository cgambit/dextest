from web3 import Web3
import config as c
import time

# This script will batch processes for swapping & transferring tokens to multiple accts in Pangolin

# ------------------------------- INITIALIZE -------------------------------- #

w3 = Web3(Web3.HTTPProvider(c.RPC_URL))

if w3.isConnected():
    print('Connection Successful')
else:
    print('Connection Failed')

# ---------------------------- SWAP TOKENS ----------------------------- #
def swap_token(sell_token, receive_token, abi_sell, sender_address, sender_pk):
    contract = w3.eth.contract(address=w3.toChecksumAddress(c.PANGOLIN_ROUTER_CONTRACT_ADDRESS), abi=c.AVA_ABI)

    contract_id = w3.toChecksumAddress(sell_token)
    sell_token_contract = w3.eth.contract(contract_id, abi=abi_sell)

    balance = sell_token_contract.functions.balanceOf(sender_address).call()  # How many tokens do we have?
    print('Token Balance to Swap : ', balance)

    sell_amt = balance 

    txn = contract.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        sell_amt,
        0,  # MinAmountOut
        [sell_token, receive_token],  # Path, which token to spend, which to get
        sender_address,  # Our own (metamask) wallet address
        (int(time.time()) + 10000)  # Deadline
    ).buildTransaction({
        'from': sender_address,
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(sender_address),
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=sender_pk)
    tx_token = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx = w3.toHex(tx_token)
    return tx

# ---------------------------- TRANSFER TOKENS ----------------------------- #
def transfer_token(sender_address, sender_pk, receiver_address, token_address, token_abi):
    token_contract = w3.eth.contract(token_address, abi=token_abi)

    # Get Token Balance which will be used as amount to transfer
    token_balance = token_contract.functions.balanceOf(sender_address).call()
    print('Token Balance to Transfer: ', token_balance)

    # Build Transfer Transaction
    nonce = w3.eth.getTransactionCount(sender_address)
    txn = token_contract.functions.transfer(
        receiver_address, 
        token_balance).buildTransaction({
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': w3.eth.gas_price
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=sender_pk)
    tx_token = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx = w3.toHex(tx_token)
    return tx

# ---------------------------- WAIT FOR RECEIPT ----------------------------- #
def awaitReceipt(tx):
    try:
        return w3.eth.wait_for_transaction_receipt(tx, timeout=30)
    except Exception as ex:
        print('Failed to wait for receipt: ', ex)
        return None

def swap_receipt_status():
    if swap_receipt.status == 1: # Check if the transaction went through
        print('Transaction Successful!')
    else:
        print('Transcation Failed,  Exiting...')
        exit()

if __name__ == "__main__":

    # ------------------Initial Step: Acct Setup------------------------ #
    # Select which acct to start with
    start_acct = c.CARLGLIBRARY

    for item in start_acct:
        for key, value in item.items():
            exec(f"{key} = '{value}'")
        
    # ------------------Step 1: Swap WAVAX to WETH.e------------------------ # 
    # Variables to change in config.py => Acct Batch processing
    sender_address = w3.toChecksumAddress(address1)
    sender_pk = address1_pk
    # Fixed variables
    sell_token = w3.toChecksumAddress(c.WAVAX_ADDRESS) 
    receive_token = w3.toChecksumAddress(c.WETHE_ADDRESS)
    abi_sell = c.WAVAX_ABI

    print('-----Starting Step 1: Swap WAVAX to WETH.e-----')
    swap_tx = swap_token(sell_token, receive_token, abi_sell, sender_address, sender_pk)
    print('Transaction Record : ', swap_tx)

    swap_receipt = awaitReceipt(swap_tx) # Wait for transaction to finish

    swap_receipt_status()
    print('Step 1 Completed!')
    time.sleep(15) # Wait for 2 minutes to make sure transaction is cleared

    # ------------------Step 2: Transfer WETH.e----------------------------- #
    # Variables to change in config.py => Acct Batch processing
    sender_address = w3.toChecksumAddress(address1)
    sender_pk = address1_pk
    receiver_address = w3.toChecksumAddress(address2)
    # Fixed variables
    token_address = w3.toChecksumAddress(c.WETHE_ADDRESS)
    token_abi = c.WETHE_ABI

    print('-----Starting Step 2: Transfer WETH.e-----')
    transfer_tx = transfer_token(sender_address, sender_pk, receiver_address, token_address, token_abi)
    print(transfer_tx)

    transfer_receipt = awaitReceipt(transfer_tx) # Wait for transaction to finish

    swap_receipt_status()
    print('Step 2 Completed!')
    time.sleep(15) # Wait for 2 minutes to make sure transaction is cleared

    # ------------------Step 3: Swap WETH.e to WAVAX------------------------ #
    # Variables to change in config.py => Acct Batch processing
    sender_address = w3.toChecksumAddress(address2)
    sender_pk = address2_pk
    # Fixed variables
    sell_token = w3.toChecksumAddress(c.WETHE_ADDRESS) 
    receive_token = w3.toChecksumAddress(c.WAVAX_ADDRESS)
    abi_sell = c.WETHE_ABI

    print('-----Starting Step 3: Swap WETH.e to WAVAX-----')
    swap_tx = swap_token(sell_token, receive_token, abi_sell, sender_address, sender_pk)
    print(swap_tx)

    swap_receipt = awaitReceipt(swap_tx) # Wait for transaction to finish

    swap_receipt_status()
    print('Step 3 Completed!')
    time.sleep(15) # Wait for 2 minutes to make sure transaction is cleared

    # ------------------Step 4: Swap WAVAX to USDT------------------------ #
    # Variables to change in config.py => Acct Batch processing
    sender_address = w3.toChecksumAddress(address2)
    sender_pk = address2_pk
    # Fixed variables
    sell_token = w3.toChecksumAddress(c.WAVAX_ADDRESS) 
    receive_token = w3.toChecksumAddress(c.USDT_ADDRESS)
    abi_sell = c.WAVAX_ABI

    print('-----Starting Step 4: Swap WAVAX to USDT-----')
    swap_tx = swap_token(sell_token, receive_token, abi_sell, sender_address, sender_pk)
    print(swap_tx)

    swap_receipt = awaitReceipt(swap_tx) # Wait for transaction to finish

    swap_receipt_status()
    print('Step 4 Completed!')
    time.sleep(15) # Wait for 2 minutes to make sure transaction is cleared

    # ------------------Step 5: Transfer USDT----------------------------- #
    # Variables to change
    sender_address = w3.toChecksumAddress(address2)
    sender_pk = address2_pk
    receiver_address = w3.toChecksumAddress(address3)
    # Fixed variables
    token_address = w3.toChecksumAddress(c.USDT_ADDRESS)
    token_abi = c.USDT_ABI

    print('-----Starting Step 5: Transfer USDT-----')
    transfer_tx = transfer_token(sender_address, sender_pk, receiver_address, token_address, token_abi)
    print(transfer_tx)

    transfer_receipt = awaitReceipt(transfer_tx) # Wait for transaction to finish

    swap_receipt_status()
    print('Step 5 Completed!')
    print('-----Congrats! All steps are done!-----')