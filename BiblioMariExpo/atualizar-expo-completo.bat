@echo off
echo Atualizando o ambiente Expo completo...
cd "C:\Users\Marcos Ferreira\Documents\ProjetosGIT\BiblioMariExpo"

echo Removendo a versão global do expo-cli (depreciada)...
call npm uninstall -g expo-cli

echo Instalando a versão mais recente do Expo compatível com seu projeto...
call npm install --save-dev expo@^49.0.0 --legacy-peer-deps

echo Instalando a CLI local do Expo (recomendada)...
call npm install --save-dev @expo/cli --legacy-peer-deps

echo Atualizando dependências do Metro Bundler...
call npm install --save metro@^0.76.0 metro-resolver@^0.76.0 metro-config@^0.76.0 --legacy-peer-deps

echo Limpando o cache...
call npx expo start --clear --no-dev --non-interactive

echo Atualização concluída!
echo Para executar o projeto, use os scripts start-expo.bat ou restart-expo.bat
pause
