@echo off
echo Atualizando para a versão mais recente do Expo Go compatível...
cd "C:\Users\Marcos Ferreira\Documents\ProjetosGIT\BiblioMariExpo"

echo Removendo a versão global do expo-cli (depreciada)...
call npm uninstall -g expo-cli

echo Instalando a versão mais recente do Expo SDK 49 (compatível com expo-router)...
call npm install --save-dev expo@^49.0.0 --legacy-peer-deps

echo Instalando a CLI local do Expo (recomendada)...
call npm install --save-dev @expo/cli --legacy-peer-deps

echo Atualizando o script de inicialização...
echo.

echo Atualização concluída!
echo Para executar o projeto, use o comando: npx expo start --port 8083
pause
