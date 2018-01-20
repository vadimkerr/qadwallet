import os
from json import dump

cwd = os.getcwd()

cwd_splitted = cwd.split('\\')[:-1]
ipcfile = cwd_splitted[:]
ipcfile.extend(['chain', 'data', 'geth.ipc'])

dic = {'ipcfile': '//./pipe/'+'/'.join(ipcfile)}

with open('qadwallet.json', 'w') as file:
    dump(dic, file)