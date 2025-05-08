@echo off
echo Corrigindo problemas de compatibilidade do Metro Bundler...
cd "C:\Users\Marcos Ferreira\Documents\ProjetosGIT\BiblioMariExpo"

echo Instalando versões específicas e compatíveis...
call npm install --save metro@0.76.8 metro-config@0.76.8 metro-core@0.76.8 metro-resolver@0.76.8 metro-runtime@0.76.8 --legacy-peer-deps

echo Instalando @expo/metro-config compatível...
call npm install --save @expo/metro-config@0.10.0 --legacy-peer-deps

echo Limpando node_modules e reinstalando dependências...
call rmdir /s /q node_modules
call del package-lock.json
call npm install --legacy-peer-deps

echo Correção concluída!
echo Para executar o projeto, use os scripts start-expo.bat ou restart-expo.bat
pause
