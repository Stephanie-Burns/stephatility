@echo off
setlocal

:: Parameters are expected in this order:
SET "INTRF=%~1"
SET "IP_ADDR=%~2"
SET "SUBNET=%~3"
SET "GATEWAY=%~4"

:: Apply network settings
netsh interface ipv4 set address name=%INTRF% static %IP_ADDR% %SUBNET% %GATEWAY%

endlocal
