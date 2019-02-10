//set your geth binary path
$export GETH='go-ethereum/build/bin/geth'

//init ethereum private network ( db will generated @ ./node folder)
$sh new_node.sh

//run your node
$sh run_node.sh

//refer geth_command.txt
//create account & unlock
//mining start

//deploy verify_signature.so using remix

//in dap.py
//update contract addres
//update keystore file path


//run your dapp
$python3 dapp.py

//dapp flow
1. define message
2. create hash of message(can call it 'digest') to sign
3. sign to the hash with private key
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
assume:
tx: signed_result + plain message
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
4. recover signing address
 4.1 from web3
 4.2 from local contract
 4.3 from remote contract
5. generate hash of plain message
6. compare message hash with new calced hash
7. if 6 is true, the message is
  7.1 sigend by signer
  7.2 message contents preserved.



