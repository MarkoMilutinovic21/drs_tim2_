@echo off
echo Stopping local MySQL service...

net stop MySQL
net stop MySQL80
net stop MySQL57

echo.
echo Local MySQL services stopped.
echo Now you can run start.bat
echo.
pause
