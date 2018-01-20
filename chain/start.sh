#!/bin/bash

GETH_BIN='/opt/geth/geth'

if [ "$1" != "" ]; then
    GETH_BIN=$1
fi

MINER='0xd837adae7b3987461f412c41528EF709bbdad8a8'

/bin/rm -rf data
/bin/cp -R data.orig data

GETH_ARGS="--datadir data --networkid 47 --minerthreads 1 --nodiscover --port 30393 --etherbase ${MINER} --unlock ${MINER} --password passwd"

if [ "$2" == "silent" ]; then
    exec ${GETH_BIN} ${GETH_ARGS} &>/dev/null
else
    exec ${GETH_BIN} ${GETH_ARGS}
fi
