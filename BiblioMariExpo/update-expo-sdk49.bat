@echo off
echo Atualizando o Expo para a versão compatível com SDK 49...
cd "C:\Users\Marcos Ferreira\Documents\ProjetosGIT\BiblioMariExpo"

echo Instalando Expo SDK 49 (compatível com expo-router)...
call npm install --save-dev expo@49.0.23 --legacy-peer-deps

echo Atualizando dependências relacionadas...
call npm install --save @expo/config-plugins@~7.2.2 react-native@0.72.10 --legacy-peer-deps

echo Instalando CLI local do Expo...
call npm install --save-dev @expo/cli --legacy-peer-deps

echo Atualização concluída!
echo Para executar o projeto, use os scripts start-expo.bat ou restart-expo.bat
pause
