#!/bin/bash

GETH_BIN='/opt/geth/geth'
PYTHON='/opt/anaconda3/bin/python'

if [ "${1}" != "" ]; then
    GETH_BIN=${1}
fi

if [ "${2}" != "" ]; then
    PYTHON=${2}
fi

PYTHON_DIR=`dirname "${PYTHON}"`
check_version_web3=` ${PYTHON_DIR}/pip show web3 | egrep 'Version:\s+4\.'`
if [ "${check_version_web3}" == "" ]; then
    echo "Version 4.x of web3.py is needed"
    exit 1
fi

cd ./chain

echo "Test chain is being deployed..."

./start.sh "${GETH_BIN}" silent & 

sleep 2

cd ..

echo "Test chain is almost ready..."

while test ! -S ./chain/data/geth.ipc; do
    sleep 1
done

cd ./tests

echo "Tests running..."

${PYTHON} test.py "${PYTHON}"

echo "Test chain is shuting down..."

ps ax | grep geth | grep "networkid" | grep 47 | grep -v grep | awk '{print $1}' | xargs kill -SIGINT
