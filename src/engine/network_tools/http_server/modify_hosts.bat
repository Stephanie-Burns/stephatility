@echo off
setlocal
set friendly_name=%1
echo 127.0.0.1 %friendly_name% >> %SystemRoot%\System32\drivers\etc\hosts
endlocal
