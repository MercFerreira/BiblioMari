@echo off
echo Encerrando processos Metro Bundler anteriores...
taskkill /f /im node.exe
timeout /t 2 /nobreak > nul

echo Limpando cache do Expo...
cd "C:\Users\Marcos Ferreira\Documents\ProjetosGIT\BiblioMariExpo"
rmdir /s /q .expo 2>nul
mkdir .expo 2>nul

echo Iniciando o projeto BiblioMari Expo com cache limpo...
call npx expo start --clear --port 8083
pause
