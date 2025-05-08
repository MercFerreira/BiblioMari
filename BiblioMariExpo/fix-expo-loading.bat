@echo off
echo ===== CORRIGINDO PROBLEMAS DE CARREGAMENTO DO EXPO =====
echo.

echo 1. Limpando cache do Metro Bundler e do Expo...
echo.
rmdir /s /q node_modules\.cache 2>nul
rmdir /s /q .expo 2>nul

echo 2. Corrigindo o package.json...
echo.
echo Removendo dependência inválida 'undefined'...
powershell -Command "(Get-Content package.json) -replace '\"undefined\": \"Ferreira\\\\Documents\\\\ProjetosGIT\\\\BiblioMariExpo\",' -replace ',\s*}', '}' | Set-Content package.json"

echo 3. Corrigindo o App.js...
echo.
echo Verificando se App.js existe e está correto...
if not exist App.js (
  echo Criando App.js básico...
  echo import React from 'react'; > App.js
  echo import { Text, View, StyleSheet } from 'react-native'; >> App.js
  echo. >> App.js
  echo export default function App() { >> App.js
  echo   return ( >> App.js
  echo     ^<View style={styles.container}^> >> App.js
  echo       ^<Text style={styles.text}^>BiblioMari^</Text^> >> App.js
  echo       ^<Text^>Carregando...^</Text^> >> App.js
  echo     ^</View^> >> App.js
  echo   ); >> App.js
  echo } >> App.js
  echo. >> App.js
  echo const styles = StyleSheet.create({ >> App.js
  echo   container: { >> App.js
  echo     flex: 1, >> App.js
  echo     backgroundColor: '#fff', >> App.js
  echo     alignItems: 'center', >> App.js
  echo     justifyContent: 'center', >> App.js
  echo   }, >> App.js
  echo   text: { >> App.js
  echo     fontSize: 24, >> App.js
  echo     fontWeight: 'bold', >> App.js
  echo     marginBottom: 20, >> App.js
  echo   }, >> App.js
  echo }); >> App.js
)

echo 4. Reinstalando dependências...
echo.
call npm install

echo 5. Instalando expo-cli globalmente...
echo.
call npm install -g expo-cli

echo 6. Verificando se o Expo está instalado corretamente...
echo.
call npx expo --version

echo.
echo ===== CORREÇÕES APLICADAS =====
echo.
echo Para iniciar o aplicativo, execute os seguintes comandos:
echo.
echo 1. Feche completamente o aplicativo Expo Go no seu celular
echo 2. Execute: npx expo start --clear
echo 3. Escaneie o QR code novamente com o aplicativo Expo Go
echo.
echo Se o problema persistir, tente:
echo - Verificar se seu celular e computador estão na mesma rede Wi-Fi
echo - Desativar temporariamente o firewall do Windows
echo - Reiniciar o celular e o computador
echo.
