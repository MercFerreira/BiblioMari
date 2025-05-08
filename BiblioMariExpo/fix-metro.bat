@echo off
echo Corrigindo problemas com o Metro Bundler...
cd "C:\Users\Marcos Ferreira\Documents\ProjetosGIT\BiblioMariExpo"

echo Instalando versões compatíveis do Metro...
call npm install --save metro@0.76.8 metro-resolver@0.76.8 metro-config@0.76.8 --legacy-peer-deps

echo Reinstalando o Expo CLI...
call npm install --save-dev @expo/cli@0.10.16 --legacy-peer-deps

echo Limpando cache...
call npx expo start --clear

echo Correção concluída!
echo Para executar o projeto, use os scripts start-expo.bat ou restart-expo.bat
pause
