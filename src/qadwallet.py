from web3 import Web3
from web3.account import Account
from json import load
from ethereum.utils import privtoaddr
import argparse

def priv_to_addr(privkey):
	addr = Web3.toHex(privtoaddr(privkey))
	return Web3.toChecksumAddress(addr)

def convert_from_wei(wei):
	if wei / 1e18 >= 1:
		to = 'ether'
	elif wei / 1e15 >= 1:
		to = 'finney'
	elif wei / 1e12 >= 1:
		to = 'szabo'
	elif wei / 1e9 >= 1:
		to = 'gwei'
	elif wei / 1e6 >= 1:
		to = 'mwei'
	elif wei / 1e3 >= 1:
		to = 'kwei'
	else:
		to = 'wei'

	value = round(Web3.fromWei(wei, to), 6)
	value = str(value).rstrip('0').rstrip('.')
	if value == '':
		value = 0
	return str(value)  + ' ' + to

def get_balance(addr):
	return web3.eth.getBalance(addr)

def transfer(privkey, to, value):
	tx_dict = {
		'nonce': web3.eth.getTransactionCount(priv_to_addr(privkey)),
		'to': to,
	    'value': value,
	    'data': b'',
	    'gas': 21000,
	    'gasPrice': int(web3.eth.gasPrice),
	    'chainId': int(web3.net.version)
	}
	raw_tx = Account.signTransaction(tx_dict, privkey)['rawTransaction']
	try:
		tx_hash = web3.eth.sendRawTransaction(raw_tx)
	except:
		return
	
	tx_hash = Web3.toHex(tx_hash)
	return tx_hash


if __name__ == '__main__':
	with open('qadwallet.json') as file:
	    config = load(file)

	_IPC_file = config['ipcfile']
	web3 = Web3(Web3.IPCProvider(_IPC_file))

	parser = argparse.ArgumentParser()
	parser.add_argument('--key')
	parser.add_argument('--to')
	parser.add_argument('--value')
	parser.add_argument('--tx')
	args = parser.parse_args()

	if args.key and args.to and args.value:
		privkey = args.key
		to = args.to
		value = int(args.value)
		tx_hash = transfer(privkey, to, value)
		if tx_hash:
			print('Payment of {} to "{}" scheduled'.format(convert_from_wei(value), to))
			print('Transaction Hash: ' + tx_hash)
		else:
			print('No enough funds for payment')

	elif args.tx:
		tx_hash = args.tx
		
		tx = web3.eth.getTransaction(tx_hash)
		if tx:
			to = tx['to']
			value = int(tx['value'])
			sender = Web3.toChecksumAddress(tx['from'])

			confirmed = True
			for i in web3.txpool.content.pending[sender]:
				if web3.txpool.content.pending[sender][i]['hash'] == tx_hash:
					confirmed = False
					print('Delay in payment of {} to "{}"'.format(convert_from_wei(value), to[2:]))
			if confirmed:
				print('Payment of {} to "{}" confirmed'.format(convert_from_wei(value), to[2:]))
		else:
			print('No such transaction in the local copy of the chain')

	elif args.key:
		privkey = args.key
		addr = priv_to_addr(privkey)
		balance = convert_from_wei(get_balance(addr))

		print('Balance on "{}" is {}'.format(addr[2:], balance))