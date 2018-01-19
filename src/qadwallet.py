#!/opt/anaconda3/bin/python

from web3 import Web3
#install web3 >=4.0.0 by `pip install --upgrade 'web3==4.0.0b5'`

from json import load

with open('qadwallet.json') as file:
    config = load(file)

_IPC_file = config['ipcfile']
web3 = Web3(Web3.IPCProvider(_IPC_file))
