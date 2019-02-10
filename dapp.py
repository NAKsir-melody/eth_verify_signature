import os
from web3 import Web3, HTTPProvider
from eth_account.messages import defunct_hash_message
import codecs

#global setting
rpc_url = "http://localhost:8545"
w3 = Web3(HTTPProvider(rpc_url))
keystore_file_path = "./node/keystore/"
con_abi = '''[{"constant":false,"inputs":[{"name":"_message","type":"bytes32"},{"name":"_v","type":"uint8"},{"name":"_r","type":"bytes32"},{"name":"_s","type":"bytes32"}],"name":"get_signer","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"signer","type":"address"}],"name":"ReturnSigner","type":"event"}]'''

#modify here
signer_addr = w3.eth.accounts[0]
signer_pwd = "admin"
keystore_file_path += "UTC--2019-02-10T08-28-05.263719447Z--39b7165b780cce549c49d7c602cff968596b885d"
con_addr = "0x850ff5e165f7699fae600eec684936b87c30cdc1"
'''
def send_transaction():
    transaction = {
        'to' : w3.eth.accounts[1],
            'from' : w3.eth.accounts[0],
            'value' : w3.toWei('3','ether'),
            'gas' : 4000000,
            'gasPrice' : w3.toWei('40','gwei'),
            'chainId':33,
            'nonce': w3.eth.getTransactionCount(w3.eth.accounts[0])
            }

    with open(keystore_file_path) as keyfile:
        encrypted_key = keyfile.read()
        private_key = w3.eth.account.decrypt(encrypted_key,signer_pwd)
        signed_tx = w3.eth.account.signTransaction(transaction, private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(tx_hash)

def unlock_accounts():
    w3.personal.unlockAccount(signer_addr, signer_pwd, 0)
    w3.eth.defaultAccount = signer_addr
'''
        

def init_contract() :
    return w3.eth.contract(address=Web3.toChecksumAddress(con_addr), abi=con_abi)

if __name__ == '__main__':
    w3.eth.enable_unaudited_features()
    contract = init_contract()

    #sender: sign to the msg digest and send {digest + msg}
    with open(keystore_file_path) as keyfile:
        encrypted_key = keyfile.read()
        private_key = w3.eth.account.decrypt(encrypted_key,signer_pwd)

        #message
        msg = 'sigmoid'.encode('utf-8')
        msg_hex = msg.hex()

        #generate message's hash to sign
        msg_hash = defunct_hash_message(hexstr=msg_hex)
        print(msg_hash)

        #sign to the generated hash
        print("signer:" + signer_addr)
        signed_result = w3.eth.account.signHash(msg_hash,private_key=private_key)
        print("signed_result: ")
        print(signed_result)

        #send signed_result + msg & received signed_result + msg 

        #confirm that received data signed by sender
        recovered1_addr = w3.eth.account.recoverHash(signed_result.messageHash, signature=signed_result.signature)
        print("from Web3:" + recovered1_addr)

        recovered2_addr = contract.functions.get_signer(signed_result.messageHash, signed_result.v, signed_result.r.to_bytes(32,'big'), signed_result.s.to_bytes(32,'big')).call()
        print("from local:" + recovered2_addr)

        tx_hash = contract.functions.get_signer(signed_result.messageHash, signed_result.v, signed_result.r.to_bytes(32,'big'), signed_result.s.to_bytes(32,'big')).transact({'from': signer_addr, 'gas': 700000} )
        
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        result = contract.events.ReturnSigner().processReceipt(tx_receipt)

        print("from remote: " + result[0].args.signer)

        #confirm that received data correct
        calc_message_hash = defunct_hash_message(hexstr=msg_hex)

        if signed_result.messageHash == calc_message_hash:
            print("message digest verified")

