@echo off
echo Corrigindo incompatibilidades de dependências do Expo...
cd "C:\Users\Marcos Ferreira\Documents\ProjetosGIT\BiblioMariExpo"

echo Instalando versões corretas das dependências...
call npx expo install --fix

echo Correção concluída!
echo Agora você pode executar o projeto sem problemas usando restart-expo.bat
pause
