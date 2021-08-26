import argparse

# importing web3 stuff takes long, so put parsing arguments in front of that.
arg_parser = argparse.ArgumentParser(description="Test a given contract by deploying and executing it.")
arg_parser.add_argument("contract", help="path to the contracts .abi and .bin.patched file")
mode_group=arg_parser.add_mutually_exclusive_group(required=True)
mode_group.add_argument("-p", "--param", help="deploy the challenge contract with given parameters for the constructor",
						action='store', type=lambda x:eval(str(x))) # use eval and a list to allow arbitrary number/type of parameters
mode_group.add_argument("-a", "--address", help="use already created contract with given address",
						action='store', type=str)
arg_parser.add_argument("-t", "--target", help="set the PoW hash limit for a reward",
						action='store', default="0x2000000000000000000000000000000000000000000000000000000000000000")
arg_parser.add_argument("-i", "--iterations", help="maximum number of different inputs given to offChain",
						action='store', type=int, default=32)
arg_parser.add_argument("-s", "--submit", help="submit inputs on-chain if they will be rewarded (counterexample/hash below target)",
						action='store_true')

args = arg_parser.parse_args()

import os
import json
from web3 import Web3
from eth_account import Account


w3 = Web3(Web3.HTTPProvider(os.environ['WEB3PROVIDER']))
privkey=os.environ['PRIVKEY']
addy=Account.from_key(privkey).address

abi=open(args.contract+".abi").read().strip()
contract=None
if args.address:
	contract=w3.eth.contract(address=args.address,abi=json.loads(abi))
else:
	bytecode=open(args.contract+".bin.patched").read().strip()
	contract=w3.eth.contract(bytecode=bytecode, abi=json.loads(abi))
	signed_txn = w3.eth.account.signTransaction(contract.constructor(*args.param, args.target).buildTransaction(dict(
							nonce=w3.eth.getTransactionCount(addy),
							gas = 3000000,
							value=w3.toWei(0.1,'ether'),
							)),privkey)
	txid=w3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
	print("TX submitted, waiting for confirmation")
	tx=w3.eth.waitForTransactionReceipt(txid)
	print("Contract deployed:", tx["contractAddress"])
	contract=w3.eth.contract(address=tx["contractAddress"], abi=json.loads(abi))

target=contract.functions.target().call().hex()
print("Target:", "0x"+target)
print("Active:", contract.functions.active().call())
print("Start mining:")
for i in range(args.iterations):
	is_counterexample, hash_value = contract.functions.offChain(i).call({'from':addy})
	hash_value=hash_value.hex()
	print(i, is_counterexample, "0x"+hash_value)
	if args.submit and (is_counterexample or int(hash_value, 16) < int(target, 16)):
		txid=w3.eth.sendRawTransaction(w3.eth.account.signTransaction(contract.functions.onChain(i).buildTransaction({
			'nonce':w3.eth.getTransactionCount(addy),
			'gas':300000}),privkey).rawTransaction).hex()
		tx=w3.eth.waitForTransactionReceipt(txid)
		print("Submitted on-chain tx:", tx["transactionHash"].hex())
		if is_counterexample:
			print("Counterexample has been found!")
			break
