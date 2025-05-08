@echo off
echo Corrigindo configuração do app.json para o BiblioMari Expo...

echo 1. Fazendo backup do app.json original...
copy app.json app.json.backup

echo 2. Substituindo app.json com versão corrigida...
copy app.json.fixed app.json

echo 3. Removendo dependência inválida do package.json...
powershell -Command "(Get-Content package.json) -replace '\"undefined\": \"Ferreira\\\\Documents\\\\ProjetosGIT\\\\BiblioMariExpo\",' -replace ',\s*}', '}' | Set-Content package.json"

echo 4. Limpando cache do Expo...
rmdir /s /q node_modules\.cache 2>nul
rmdir /s /q .expo 2>nul

echo Correções aplicadas com sucesso!
echo.
echo Agora você pode iniciar o aplicativo com:
echo npx expo start --clear
echo.
echo Se ainda houver problemas, tente:
echo 1. Fechar completamente o aplicativo Expo Go no celular
echo 2. Reiniciar o servidor Expo
echo 3. Escanear o QR code novamente
