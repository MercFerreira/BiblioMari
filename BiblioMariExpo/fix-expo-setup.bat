@echo off
echo Aplicando correções para o projeto BiblioMari Expo...

echo 1. Atualizando configurações do app.json...
copy /Y app.json.new app.json
del app.json.new

echo 2. Atualizando package.json...
copy /Y package.json.new package.json
del package.json.new

echo 3. Criando pastas para imagens...
mkdir src\assets 2>nul

echo 4. Instalando dependências corretas...
call npm install

echo 5. Verificando instalação...
call npx expo doctor

echo Processo concluído! Agora você pode iniciar o aplicativo com:
echo npx expo start
