@echo off
echo Encerrando processos Metro Bundler anteriores...
taskkill /f /im node.exe
timeout /t 2 /nobreak > nul

echo Iniciando o projeto BiblioMari Expo...
cd "C:\Users\Marcos Ferreira\Documents\ProjetosGIT\BiblioMariExpo"
call npx expo start --port 8083
pause
