@echo off
cd %~dp0
call npm install --save @expo/config-plugins@~7.2.2 react-native@0.72.10
echo Dependencies fixed!
pause
