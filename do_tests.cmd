@echo off

set gethbin=%1
if "%~1" == "" set gethbin="c:\Program Files\Geth\geth.exe"

set pythonbin=%2
if "%~2" == "" set pythonbin="c:\Anaconda3\python.exe"

%pythonbin% -c "import web3; import sys ; sys.exit(1) if web3.__version__[0] != '4' else sys.exit(0)"

echo Checking version of web3.py python library...
if errorlevel 1 exit /b 1

cd chain

echo Test chain is being deployed...

start "TESTBEDGETH" start.cmd

rem **** HACK - wait for 5 seconds o_O ****
ping 127.0.0.1 -n 6 -w 1000 > NUL

cd ..\tests

echo Tests running...

%pythonbin% gen_json_win.py

%pythonbin% test.py %gethbin% %pythonbin%

echo Test chain is shuting down...

taskkill.exe /fi "WINDOWTITLE eq TESTBEDGETH*" > NUL