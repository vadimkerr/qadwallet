Original repo: https://github.com/akolotov/qadwallet-testenv

These set of files is intended to perform automatic testing of 'qadwallet' assignement.

The statement of the assignement is available on https://goo.gl/zjpJp6 (Task #1).

1. Put the code of your implementation to `qadwallet.py` of `src` directory.
2. Modify `qadwallet.json` file and manually test your implementatuin carefully.
3. To check that the implementation is compatible with automatic testing system
   use `do_tests` script. It requires path to ethereum-go client (geth)
   and python interpeter with `web3.py` library set up in the environment.
   For example,

On Linux:
```
$ ./do_tests.sh /opt/geth/geth /opt/anaconda3/bin/python
```

On Windows:
```
do_tests.cmd "c:\Program Files\Geth\geth.exe" "c:\Anaconda3\python.exe"
```

4. Look at the passed and failed tests to find how close you to the final solution.

