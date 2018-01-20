@echo off

rmdir data /s /q
robocopy data.orig data /e /np

set miner=0xd837adae7b3987461f412c41528EF709bbdad8a8

set gethbin=%1
if "%~1" == "" set gethbin="c:\Program Files\Geth\geth.exe"

set ipcfile=%cd%\data\geth.ipc

%gethbin% --datadir data --ipcpath "%ipcfile%" --networkid 47 --minerthreads 1 --nodiscover --port 30393 --etherbase %miner% --unlock %miner% --password passwd