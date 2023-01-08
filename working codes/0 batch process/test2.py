import config as c




start_acct = c.carlglibrary

for item in start_acct:
    for key, value in item.items():
        exec(f"{key} = '{value}'")

#Step 1
sender_address = address1
sender_pk = address1_pk
print('Step 1')
print('sender1 address : ', sender_address)
print('sender1_pk : ', sender_pk)

#Step 2
sender_address = address1
sender_pk = address1_pk
receiver_address = address2
print('Step 2')
print('sender1 address : ', sender_address)
print('sender1_pk : ', sender_pk)
print('Receiver address :', receiver_address)

#Step 3
sender_address = address2
sender_pk = address2_pk
print('Step 3')
print('sender address : ', sender_address)
print('sender_pk : ', sender_pk)

#Step 4
sender_address = address2
sender_pk = address2_pk
print('Step 4')
print('sender address : ', sender_address)
print('sender_pk : ', sender_pk)

#Step 5
sender_address = address2
sender_pk = address2_pk
receiver_address = address3
print('Step 5')
print('sender1 address : ', sender_address)
print('sender1_pk : ', sender_pk)
print('Receiver address :', receiver_address)
