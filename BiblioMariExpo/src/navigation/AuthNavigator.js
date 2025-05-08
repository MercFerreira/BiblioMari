import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';

// Importar telas de autenticação
import LoginScreen from '../screens/auth/LoginScreen';
import RegisterScreen from '../screens/auth/RegisterScreen';
import ForgotPasswordScreen from '../screens/auth/ForgotPasswordScreen';

const Stack = createStackNavigator();

const AuthNavigator = ({ isDarkMode, toggleTheme }) => {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
      }}
    >
      <Stack.Screen name="Login">
        {props => <LoginScreen {...props} isDarkMode={isDarkMode} toggleTheme={toggleTheme} />}
      </Stack.Screen>
      <Stack.Screen name="Register">
        {props => <RegisterScreen {...props} isDarkMode={isDarkMode} toggleTheme={toggleTheme} />}
      </Stack.Screen>
      <Stack.Screen name="ForgotPassword">
        {props => <ForgotPasswordScreen {...props} isDarkMode={isDarkMode} toggleTheme={toggleTheme} />}
      </Stack.Screen>
    </Stack.Navigator>
  );
};

export default AuthNavigator;
