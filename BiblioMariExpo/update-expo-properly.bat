@echo off
echo Atualizando o Expo e dependências para a versão mais recente compatível...
cd "C:\Users\Marcos Ferreira\Documents\ProjetosGIT\BiblioMariExpo"

echo Instalando Expo SDK 49 (compatível com seu projeto atual)...
call npm install --save-dev expo@^49.0.0

echo Atualizando dependências relacionadas...
call npm install --save @expo/config-plugins@~7.2.2 react-native@0.72.10

echo Instalando CLI local do Expo...
call npm install --save-dev @expo/cli

echo Atualização concluída!
echo Para executar o projeto, use os scripts start-expo.bat ou restart-expo.bat
pause
