#!/opt/anaconda3/bin/python

from web3 import Web3
from json import load
from subprocess import check_output, CalledProcessError, TimeoutExpired, STDOUT
import sys, os

with open('qadwallet.json') as file:
    config = load(file)

_IPC_file = config['ipcfile']
web3 = Web3(Web3.IPCProvider(_IPC_file))

python_intrp = ""
if sys.argv[1] != "":
    python_intrp = sys.argv[1]

qadwalletExec = "../src/qadwallet.py"

def runCmd(args):
    executed = False
    out = ""
    ext_args = args[:]
    if python_intrp:
        ext_args.insert(0, python_intrp)
    try:
        tmpout=check_output(ext_args, stderr=STDOUT, timeout=10)
    except CalledProcessError as ret:
        tmpout=ret.stdout
    except TimeoutExpired:
        tmpout=''
    if len(tmpout) > 0:
        executed = True
        out = tmpout.decode().splitlines()
    return (executed, out)

pk_1 = '41358ef24fe86a58d67810e1b3eeeba47473b98e75dcaf9a6c295ff445d6d668'
addr_1 = '2fe6272cfBcd120c5d0Ce59D22162b8AC6fe032e'

pk_2 = 'c96128075e63206192ed8f70484bab090e08feb8ea1caf2e9665d989ab78a3f4'
addr_2 = '74337eee6F1BE7F8d1E0BE46D177a42cf12Ee51e'

pk_3 = '56e02f6e0d151d8a9174557d8b9bf5cd347ef1c3891bd4fedbac252d5aa38b90'
addr_3 = '1AE0eC2abb68764F51e250D930dA0FfaAb58f2B7'

addr_4 = 'd837adae7b3987461f412c41528EF709bbdad8a8'

pk_5 = '61423bbb54c6b8aee380d24954f3c22941020890f67d3305d0957b180f0dc834'
addr_5 = '2c5AD1f8700280ee73261910D1a16dc62c1a7628'

originator = addr_1
originator_pk = pk_1

bad_originator = addr_3
bad_originator_pk = pk_3

recipient = addr_4

Stests = 0
Ftests = 0

def countResult(res):
    global Stests, Ftests
    if res:
        print("PASSED")
        Stests += 1
    else:
        print("FAILED")
        Ftests += 1

def printTotal():
    print('\nTotal tests run: {}\nFailed tests: {}'.format(Stests+Ftests, Ftests))
        
def checkOutput(response, clue):
    cl = clue[:]
    res = False
    if len(response) == len(clue):
        res = True
        for i in range(len(clue)):
            if response[i] != clue[i]:
                res = False
    if not res:
        print('--- ACTUAL RESPONSE:\n{}\n--- EXPECTED RESPONSE:\n{}'.format("\n".join(response), "\n".join(clue)))
    return res

def test_getting_balance(_pk, _addr, _sBalance):
    cmd = [qadwalletExec, '--key', _pk]
    print('EXECUTED:\n{}'.format(" ".join(cmd)))
    ret = runCmd(cmd)
    if ret[0]:
        exp = ['Balance on "{}" is {}'.format(_addr, _sBalance)]
        return checkOutput(ret[1], exp)
    else:
        print("The command executed too long.")
        return False
    
def test_sending_good_transaction():
    new_transaction_filter = web3.eth.filter('pending')
    value = web3.toWei(127.127, 'gwei')
    cmd = [qadwalletExec, '--key', pk_2, '--to', recipient,
           '--value', str(value)]
    print('EXECUTED:\n{}'.format(" ".join(cmd)))
    ret = runCmd(cmd)
    if ret[0]:
        exp = ['Payment of {} to "{}" scheduled'.format('127.127 gwei', recipient)]
        if len(ret[1]) > 1:
            data = new_transaction_filter.get_new_entries()
            web3.eth.uninstallFilter(new_transaction_filter.filter_id)
            if len(data) > 0:
                to_exp = ""
                for i in data:
                    tx = web3.eth.getTransaction(i)
                    if ((tx['value'] == value) and
                        (tx['to'] == '0x'+recipient) and
                        (tx['from'] == '0x'+addr_2)):
                        to_exp = 'Transaction Hash: {}'.format(data[0].hex())
                if len(to_exp) > 0:
                    exp.append(to_exp)
                else:
                    print("ERROR: Cannot find proper transaction")
                    return False
            else:
                print("ERROR: Cannot find any pending transaction")
                return False
        return checkOutput(ret[1], exp)
    else:
        print("ERROR: The command executed too long.")
        return False

def test_sending_good_transaction_with_unknown_nonce():
    new_transaction_filter = web3.eth.filter('pending')
    value = web3.toWei(543.00001, 'finney')
    cmd = [qadwalletExec, '--key', originator_pk, '--to', recipient,
           '--value', str(value)]
    print('EXECUTED:\n{}'.format(" ".join(cmd)))
    ret = runCmd(cmd)
    if ret[0]:
        exp = ['Payment of {} to "{}" scheduled'.format('543.00001 finney', recipient)]
        if len(ret[1]) > 1:
            data = new_transaction_filter.get_new_entries()
            web3.eth.uninstallFilter(new_transaction_filter.filter_id)
            if len(data) > 0:
                to_exp = ""
                for i in data:
                    tx = web3.eth.getTransaction(i)
                    if ((tx['value'] == value) and
                        (tx['to'] == '0x'+recipient) and
                        (tx['from'] == '0x'+originator)):
                        to_exp = 'Transaction Hash: {}'.format(data[0].hex())
                if len(to_exp) > 0:
                    exp.append(to_exp)
                else:
                    print("ERROR: Cannot find proper transaction")
                    return False
            else:
                print("ERROR: Cannot find any pending transaction")
                return False
        return checkOutput(ret[1], exp)
    else:
        print("ERROR: The command executed too long.")
        return False
    
def test_insufficient_funds_error():
    value = web3.toWei(500000, 'ether')
    cmd = [qadwalletExec, '--key', bad_originator_pk, '--to', recipient,
           '--value', str(value)]
    print('EXECUTED:\n{}'.format(" ".join(cmd)))
    ret = runCmd(cmd)
    if ret[0]:
        exp = ['No enough funds for payment']
        return checkOutput(ret[1], exp)
    else:
        print("The command executed too long.")
        return False

def test_validated_transaction():
    txid = '0x4014839bb4efcb79ab0ac062ee9f7239913323134f435cd8272e708810ab7fbd'
    value_formatted = '31.123456 gwei'
    cmd = [qadwalletExec, '--tx', txid]
    print('EXECUTED:\n{}'.format(" ".join(cmd)))
    ret = runCmd(cmd)
    if ret[0]:
        exp = ['Payment of {} to "{}" confirmed'.format(value_formatted, addr_5)]
        return checkOutput(ret[1], exp)
    else:
        print("The command executed too long.")
        return False

def test_pending_transaction():
    txid = '0x98f69c4bdf8f5898ae4419fedaa5d67b55256a271b0277d4127050e78bcccb91'
    value_formatted = '1 szabo'
    cmd = [qadwalletExec, '--tx', txid]
    print('EXECUTED:\n{}'.format(" ".join(cmd)))
    ret = runCmd(cmd)
    if ret[0]:
        exp = ['Delay in payment of {} to "{}"'.format(value_formatted, recipient)]
        return checkOutput(ret[1], exp)
    else:
        print("The command executed too long.")
        return False
    
def test_nonexistent_transaction():
    txid = '0xf0269a31ebacb7b2729bd75eddd4fdbe05ac031c3550f8840bad97db28611bbc'
    cmd = [qadwalletExec, '--tx', txid]
    print('EXECUTED:\n{}'.format(" ".join(cmd)))
    ret = runCmd(cmd)
    if ret[0]:
        exp = ['No such transaction in the local copy of the chain']
        return checkOutput(ret[1], exp)
    else:
        print("The command executed too long.")
        return False
    
print("TEST 001: Getting balance, uno.")
res = test_getting_balance(pk_1, addr_1, '904625697166532841465763557776457343114642500733229858816 ether')
countResult(res)

print("TEST 002: Getting balance, dos.")
res = test_getting_balance(pk_2, addr_2, '2.56 ether')
countResult(res)

print("TEST 003: Getting balance, tres.")
res = test_getting_balance(pk_3, addr_3, '999.999999 finney')
countResult(res)

print("TEST 004: Getting balance, cuatro.")
res = test_getting_balance(pk_5, addr_5, '31.123456 gwei')
countResult(res)

print("TEST 005: Sending transaction.")
res = test_sending_good_transaction()
countResult(res)

print("TEST 006: Test delayed transaction.")
res = test_pending_transaction()
countResult(res)

print("TEST 007: Sending transaction from account already operated.")
res = test_sending_good_transaction_with_unknown_nonce()
countResult(res)

print("TEST 008: Sending transaction when no enough funds.")
res = test_insufficient_funds_error()
countResult(res)

print("TEST 009: Check verified transaction.")
res = test_validated_transaction()
countResult(res)

print("TEST 010: Check nonexistent transaction.")
res = test_nonexistent_transaction()
countResult(res)

printTotal()

if (os.path.basename(sys.argv[0]) != "ipykernel_launcher.py"):
    sys.exit(Ftests)
