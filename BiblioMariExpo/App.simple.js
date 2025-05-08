import React, { useState, useEffect } from 'react';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { NavigationContainer } from '@react-navigation/native';
import { Provider as PaperProvider } from 'react-native-paper';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Temas e navegação
import { lightTheme, darkTheme } from './src/theme/theme';
import AppNavigator from './src/navigation/AppNavigator';
import AuthNavigator from './src/navigation/AuthNavigator';

// Contexto de autenticação
import { AuthProvider, useAuth } from './src/hooks/useAuth';

// Componente principal que decide qual navegador mostrar com base no estado de autenticação
const RootNavigator = () => {
  const { user, isLoading } = useAuth();
  const [theme, setTheme] = useState(lightTheme);
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Carregar preferência de tema
  useEffect(() => {
    const loadThemePreference = async () => {
      try {
        const savedTheme = await AsyncStorage.getItem('theme');
        if (savedTheme === 'dark') {
          setTheme(darkTheme);
          setIsDarkMode(true);
        }
      } catch (error) {
        console.log('Erro ao carregar tema:', error);
      }
    };

    loadThemePreference();
  }, []);

  // Função para alternar entre temas claro e escuro
  const toggleTheme = async () => {
    const newIsDarkMode = !isDarkMode;
    setIsDarkMode(newIsDarkMode);
    setTheme(newIsDarkMode ? darkTheme : lightTheme);
    
    try {
      await AsyncStorage.setItem('theme', newIsDarkMode ? 'dark' : 'light');
    } catch (error) {
      console.log('Erro ao salvar tema:', error);
    }
  };

  // Mostrar tela de carregamento enquanto verifica autenticação
  if (isLoading) {
    return null; // Ou um componente de loading
  }

  return (
    <PaperProvider theme={theme}>
      <NavigationContainer theme={theme}>
        <StatusBar style={isDarkMode ? 'light' : 'dark'} />
        {user ? (
          <AppNavigator toggleTheme={toggleTheme} isDarkMode={isDarkMode} />
        ) : (
          <AuthNavigator toggleTheme={toggleTheme} isDarkMode={isDarkMode} />
        )}
      </NavigationContainer>
    </PaperProvider>
  );
};

// Componente principal da aplicação
export default function App() {
  return (
    <SafeAreaProvider>
      <AuthProvider>
        <RootNavigator />
      </AuthProvider>
    </SafeAreaProvider>
  );
}
