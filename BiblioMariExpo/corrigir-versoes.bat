@echo off
echo Corrigindo versões incompatíveis das dependências do Expo...
cd "C:\Users\Marcos Ferreira\Documents\ProjetosGIT\BiblioMariExpo"

echo Executando o comando de correção automática do Expo...
call npx expo install --fix

echo Correção concluída!
echo Para executar o projeto, use o script start-expo.bat
pause
