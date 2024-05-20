@echo off
setlocal

set new_name=%1
set old_name=%2
set hosts_file=%SystemRoot%\System32\drivers\etc\hosts

if not "%old_name%"=="" (
    findstr /v /c:"%old_name%.local" %hosts_file% > %hosts_file%.tmp
    move /y %hosts_file%.tmp %hosts_file%
)

echo 127.0.0.1 %new_name%.local >> %hosts_file%

endlocal
