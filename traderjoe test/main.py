from web3 import Web3
import config as c
import time

# This script will Swap USDC to WETH.e in TraderJoe

# ------------------------------- INITIALIZE -------------------------------- #

w3 = Web3(Web3.HTTPProvider(c.RPC_URL))

if w3.isConnected():
    print('Connection Successful')
else:
    print('Connection Failed')

# ---------------------------- APPROVE TOKEN ----------------------------- #
def approve(sell_token):
    contract_id = w3.toChecksumAddress(sell_token)
    sellTokenContract = w3.eth.contract(contract_id, abi=c.WAVAX_ABI)
    approve = sellTokenContract.functions.approve(w3.toChecksumAddress(c.TRADERJOE_ROUTER_ADDRESS), 1000).buildTransaction({
        'from': w3.toChecksumAddress(c.SENDER_ADDRESS),
        'nonce': w3.eth.get_transaction_count(c.SENDER_ADDRESS),
    })
    signed_txn = w3.eth.account.sign_transaction(approve, private_key=c.PRIVATE_KEY)
    tx_token = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx = w3.toHex(tx_token)
    return tx

# ---------------------------- SWAP TOKENS ----------------------------- #
def swap_token(sell_token, receive_token):
    contract = w3.eth.contract(address=w3.toChecksumAddress(c.TRADERJOE_ROUTER_ADDRESS), abi=c.AVA_ABI)

    contract_id = w3.toChecksumAddress(sell_token)
    sell_token_contract = w3.eth.contract(contract_id, abi=c.WAVAX_ABI)

    balance = sell_token_contract.functions.balanceOf(c.SENDER_ADDRESS).call()  # How many USDC do we have?

    sell_amt = balance # Cannot use toWei or fromWei functions since USDC only has 6 decimals
    print('WAVAX Balance to Sell : ', sell_amt)

    txn = contract.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        sell_amt,
        0,  # MinAmountOut
        [sell_token, receive_token],  # Path, which token to spend, which to get
        c.SENDER_ADDRESS,  # Our own (metamask) wallet address
        (int(time.time()) + 10000)  # Deadline
    ).buildTransaction({
        'from': c.SENDER_ADDRESS,
        'gas': 300000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(c.SENDER_ADDRESS),
        'chainId': 43114
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=c.PRIVATE_KEY)
    tx_token = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx = w3.toHex(tx_token)
    return tx

# ---------------------------- WAIT FOR RECEIPT ----------------------------- #
def awaitReceipt(tx):
    try:
        return w3.eth.wait_for_transaction_receipt(tx, timeout=60)
    except Exception as ex:
        print('Failed to wait for receipt: ', ex)
        return None


if __name__ == "__main__":
    sell_token = w3.toChecksumAddress(c.WAVAX_ADDRESS) 
    receive_token = w3.toChecksumAddress(c.USDC_ADDRESS)

    # -------------APPROVE TOKENS-----------------------------------------#
    # Approve the token, must be done once before selling
    approve_tx = approve(sell_token)
    print(approve_tx)
    approve_receipt = awaitReceipt(approve_tx)
    print(approve_receipt)

    # # -------------SWAP TOKENS-----------------------------------------#
    # swap_tx = swap_token(sell_token, receive_token)
    # print(swap_tx)

    # swap_receipt = awaitReceipt(swap_tx) # Wait for transaction to finish

    # if swap_receipt.status == 1: # Check if the transaction went through
    #     print('Swap Successfully!')
    # else:
    #     print('Swap Failed,  Exiting...')
    #     exit()