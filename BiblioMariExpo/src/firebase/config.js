// Importar as funções necessárias do Firebase
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';

// Configuração do Firebase - substitua com suas credenciais
const firebaseConfig = {
  apiKey: "SUBSTITUA_COM_SUA_API_KEY",
  authDomain: "bibliomari.firebaseapp.com",
  projectId: "bibliomari",
  storageBucket: "bibliomari.appspot.com",
  messagingSenderId: "SUBSTITUA_COM_SEU_MESSAGING_ID",
  appId: "SUBSTITUA_COM_SEU_APP_ID"
};

/*
INSTRUÇÕES PARA CONFIGURAR O FIREBASE:

1. Acesse https://console.firebase.google.com/
2. Clique em "Adicionar projeto" e siga as instruções para criar um novo projeto
3. No painel do projeto, clique em "Adicionar app" e selecione o ícone da Web (</>) 
4. Registre seu app e obtenha as credenciais de configuração
5. No console do Firebase, vá para Authentication e habilite o provedor de Email/Senha
6. Vá para Firestore Database e crie um banco de dados em modo de teste
7. Vá para Storage e configure o armazenamento para seu projeto

Depois de configurar, substitua os valores acima com as credenciais do seu projeto.
*/

// Inicializar Firebase
const app = initializeApp(firebaseConfig);

// Exportar serviços do Firebase
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);

export default app;
