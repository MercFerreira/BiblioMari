import { DefaultTheme, DarkTheme } from '@react-navigation/native';
import { configureFonts, MD3LightTheme, MD3DarkTheme } from 'react-native-paper';

// Configuração de fontes personalizada
const fontConfig = {
  displayLarge: {
    fontFamily: 'System',
    fontSize: 28,
    fontWeight: '700',
    letterSpacing: 0,
  },
  displayMedium: {
    fontFamily: 'System',
    fontSize: 24,
    fontWeight: '700',
    letterSpacing: 0,
  },
  displaySmall: {
    fontFamily: 'System',
    fontSize: 20,
    fontWeight: '700',
    letterSpacing: 0,
  },
  headlineLarge: {
    fontFamily: 'System',
    fontSize: 24,
    fontWeight: '600',
    letterSpacing: 0,
  },
  headlineMedium: {
    fontFamily: 'System',
    fontSize: 20,
    fontWeight: '600',
    letterSpacing: 0,
  },
  headlineSmall: {
    fontFamily: 'System',
    fontSize: 18,
    fontWeight: '600',
    letterSpacing: 0,
  },
  titleLarge: {
    fontFamily: 'System',
    fontSize: 20,
    fontWeight: '600',
    letterSpacing: 0,
  },
  titleMedium: {
    fontFamily: 'System',
    fontSize: 16,
    fontWeight: '600',
    letterSpacing: 0.15,
  },
  titleSmall: {
    fontFamily: 'System',
    fontSize: 14,
    fontWeight: '500',
    letterSpacing: 0.1,
  },
  bodyLarge: {
    fontFamily: 'System',
    fontSize: 16,
    fontWeight: '400',
    letterSpacing: 0.15,
  },
  bodyMedium: {
    fontFamily: 'System',
    fontSize: 14,
    fontWeight: '400',
    letterSpacing: 0.25,
  },
  bodySmall: {
    fontFamily: 'System',
    fontSize: 12,
    fontWeight: '400',
    letterSpacing: 0.4,
  },
  labelLarge: {
    fontFamily: 'System',
    fontSize: 14,
    fontWeight: '500',
    letterSpacing: 0.1,
  },
  labelMedium: {
    fontFamily: 'System',
    fontSize: 12,
    fontWeight: '500',
    letterSpacing: 0.5,
  },
  labelSmall: {
    fontFamily: 'System',
    fontSize: 11,
    fontWeight: '500',
    letterSpacing: 0.5,
  },
};

// Cores do tema claro
const lightColors = {
  primary: '#3B82F6', // Azul
  onPrimary: '#FFFFFF',
  primaryContainer: '#D1E0FF',
  onPrimaryContainer: '#001A41',
  secondary: '#7C5800',
  onSecondary: '#FFFFFF',
  secondaryContainer: '#FFE08C',
  onSecondaryContainer: '#271900',
  tertiary: '#006874',
  onTertiary: '#FFFFFF',
  tertiaryContainer: '#95F0FF',
  onTertiaryContainer: '#001F24',
  error: '#BA1A1A',
  onError: '#FFFFFF',
  errorContainer: '#FFDAD6',
  onErrorContainer: '#410002',
  background: '#F8FAFC',
  onBackground: '#1A1C1E',
  surface: '#FFFFFF',
  onSurface: '#1A1C1E',
  surfaceVariant: '#E7E0EC',
  onSurfaceVariant: '#49454F',
  outline: '#79747E',
  outlineVariant: '#CAC4D0',
  shadow: '#000000',
  scrim: '#000000',
  inverseSurface: '#2F3033',
  inverseOnSurface: '#F2F0F4',
  inversePrimary: '#ADC6FF',
  elevation: {
    level0: 'transparent',
    level1: '#F5F5F5',
    level2: '#EEEEEE',
    level3: '#E0E0E0',
    level4: '#D6D6D6',
    level5: '#C2C2C2',
  },
  surfaceDisabled: '#1A1C1E1F',
  onSurfaceDisabled: '#1A1C1E61',
  backdrop: '#1A1C1E80',
};

// Cores do tema escuro
const darkColors = {
  primary: '#ADC6FF', // Azul mais claro para tema escuro
  onPrimary: '#002E6A',
  primaryContainer: '#0A4494',
  onPrimaryContainer: '#D8E2FF',
  secondary: '#EAC248',
  onSecondary: '#3F2D00',
  secondaryContainer: '#5C4300',
  onSecondaryContainer: '#FFE08C',
  tertiary: '#4FD8EB',
  onTertiary: '#00363D',
  tertiaryContainer: '#004F58',
  onTertiaryContainer: '#97F0FF',
  error: '#FFB4AB',
  onError: '#690005',
  errorContainer: '#93000A',
  onErrorContainer: '#FFDAD6',
  background: '#1A1C1E',
  onBackground: '#E3E2E6',
  surface: '#121212',
  onSurface: '#E3E2E6',
  surfaceVariant: '#49454F',
  onSurfaceVariant: '#CAC4D0',
  outline: '#938F99',
  outlineVariant: '#49454F',
  shadow: '#000000',
  scrim: '#000000',
  inverseSurface: '#E3E2E6',
  inverseOnSurface: '#1A1C1E',
  inversePrimary: '#0A53C1',
  elevation: {
    level0: 'transparent',
    level1: '#1E1E1E',
    level2: '#232323',
    level3: '#252525',
    level4: '#272727',
    level5: '#2C2C2C',
  },
  surfaceDisabled: '#E3E2E61F',
  onSurfaceDisabled: '#E3E2E661',
  backdrop: '#000000',
};

// Tema claro personalizado
export const lightTheme = {
  ...DefaultTheme,
  ...MD3LightTheme,
  colors: {
    ...DefaultTheme.colors,
    ...MD3LightTheme.colors,
    ...lightColors,
  },
  fonts: configureFonts({ config: fontConfig }),
  roundness: 8,
};

// Tema escuro personalizado
export const darkTheme = {
  ...DarkTheme,
  ...MD3DarkTheme,
  colors: {
    ...DarkTheme.colors,
    ...MD3DarkTheme.colors,
    ...darkColors,
  },
  fonts: configureFonts({ config: fontConfig }),
  roundness: 8,
};
