# BiblioMari - Aplicativo de Biblioteca Pessoal

BiblioMari é um aplicativo de gerenciamento de biblioteca pessoal desenvolvido com Expo/React Native e Firebase.

## Configuração e Instalação

### Pré-requisitos

- Node.js (versão 14 ou superior)
- npm ou yarn
- Expo CLI (`npm install -g expo-cli`)
- Conta no Firebase

### Instalação

1. Clone o repositório ou baixe os arquivos
2. Navegue até a pasta do projeto:
   ```
   cd BiblioMariExpo
   ```
3. Instale as dependências:
   ```
   npm install
   ```

### Configuração do Firebase

1. Crie um projeto no [Firebase Console](https://console.firebase.google.com/)
2. Ative a Autenticação com Email/Senha
3. Configure o Firestore Database
4. Configure o Storage
5. Obtenha as credenciais do projeto e atualize o arquivo `src/firebase/config.js`

## Executando o Aplicativo

### Com SDK 49 (Padrão)

```
npm start
```

### Com SDK 53

```
npm run start:sdk53
```

## Funcionalidades

- Autenticação de usuários (login, registro, recuperação de senha)
- Gerenciamento de livros (adicionar, editar, excluir)
- Upload de imagens de capa
- Avaliação com sistema de estrelas
- Filtros e pesquisa
- Exportação de dados
- Tema claro e escuro

## Estrutura do Projeto

- `/src/assets` - Imagens e recursos
- `/src/components` - Componentes reutilizáveis
- `/src/firebase` - Configuração e serviços do Firebase
- `/src/hooks` - Hooks personalizados
- `/src/navigation` - Configuração de navegação
- `/src/screens` - Telas do aplicativo
- `/src/theme` - Configuração de temas
- `/src/utils` - Funções utilitárias

## Suporte a Múltiplos SDKs

Este projeto está configurado para suportar tanto o SDK 49 quanto o SDK 53 do Expo, permitindo maior flexibilidade e compatibilidade.
