from web3 import Web3
import config as c
import time

# ------------------------------- INITIALIZE -------------------------------- #

w3 = Web3(Web3.HTTPProvider(c.RPC_URL))
if w3.isConnected():
    print('Connection Successful')
else:
    print('Connection Failed')
spend = w3.toChecksumAddress(c.WAVAX_ADDRESS)
contract = w3.eth.contract(address=w3.toChecksumAddress(c.PANGOLIN_ROUTER_CONTRACT_ADDRESS), abi=c.AVA_ABI)

# ---------------------------- SWAP TOKENS ----------------------------- #
def swap_token(token_address, token_to_spend):
    token_to_buy = w3.toChecksumAddress(token_address)

    txn = contract.functions.swapExactAVAXForTokensSupportingFeeOnTransferTokens(
        0,  # MinAmountOut
        [spend, token_to_buy],  # Path, which token to spend, which to get
        c.SENDER_ADDRESS,  # Our own (metamask) wallet address
        (int(time.time()) + 10000)  # Deadline
    ).buildTransaction({
        'from': c.SENDER_ADDRESS,
        'value': w3.toWei(token_to_spend, 'ether'),
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
    token_address = c.USDT_ADDRESS
    token_to_spend = 0.10 

    buy_tx = swap_token(token_address, token_to_spend)
    print(buy_tx)

    buy_receipt = awaitReceipt(buy_tx) # Wait for transaction to finish

    if buy_receipt.status == 1: # Check if the transaction went through
        print('Bought Successfully!')
    else:
        print('Buy Failed,  Exiting...')
        exit()