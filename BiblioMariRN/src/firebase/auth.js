import auth from '@react-native-firebase/auth';
import firestore from '@react-native-firebase/firestore';
import { Alert } from 'react-native';

// Registro de novo usuário
export const registerUser = async (email, password, name) => {
  try {
    // Criar usuário com email e senha
    const userCredential = await auth().createUserWithEmailAndPassword(email, password);
    const user = userCredential.user;

    // Atualizar o perfil do usuário com o nome
    await user.updateProfile({
      displayName: name,
    });

    // Criar documento do usuário no Firestore
    await firestore().collection('users').doc(user.uid).set({
      uid: user.uid,
      email: user.email,
      displayName: name,
      createdAt: firestore.FieldValue.serverTimestamp(),
    });

    return { success: true, user };
  } catch (error) {
    console.error('Erro no registro:', error);
    let errorMessage = 'Falha no registro. Tente novamente.';
    
    if (error.code === 'auth/email-already-in-use') {
      errorMessage = 'Este email já está em uso.';
    } else if (error.code === 'auth/invalid-email') {
      errorMessage = 'Email inválido.';
    } else if (error.code === 'auth/weak-password') {
      errorMessage = 'A senha é muito fraca. Use pelo menos 6 caracteres.';
    }
    
    return { success: false, error: errorMessage };
  }
};

// Login de usuário
export const loginUser = async (email, password) => {
  try {
    const userCredential = await auth().signInWithEmailAndPassword(email, password);
    return { success: true, user: userCredential.user };
  } catch (error) {
    console.error('Erro no login:', error);
    let errorMessage = 'Falha no login. Verifique seu email e senha.';
    
    if (error.code === 'auth/user-not-found' || error.code === 'auth/wrong-password') {
      errorMessage = 'Email ou senha incorretos.';
    } else if (error.code === 'auth/invalid-email') {
      errorMessage = 'Email inválido.';
    } else if (error.code === 'auth/user-disabled') {
      errorMessage = 'Esta conta foi desativada.';
    }
    
    return { success: false, error: errorMessage };
  }
};

// Recuperação de senha
export const resetPassword = async (email) => {
  try {
    await auth().sendPasswordResetEmail(email);
    return { success: true };
  } catch (error) {
    console.error('Erro na recuperação de senha:', error);
    let errorMessage = 'Falha ao enviar email de recuperação.';
    
    if (error.code === 'auth/user-not-found') {
      errorMessage = 'Não há usuário registrado com este email.';
    } else if (error.code === 'auth/invalid-email') {
      errorMessage = 'Email inválido.';
    }
    
    return { success: false, error: errorMessage };
  }
};

// Logout de usuário
export const logoutUser = async () => {
  try {
    await auth().signOut();
    return { success: true };
  } catch (error) {
    console.error('Erro no logout:', error);
    return { success: false, error: 'Falha ao fazer logout.' };
  }
};

// Obter usuário atual
export const getCurrentUser = () => {
  return auth().currentUser;
};

// Verificar estado de autenticação
export const onAuthStateChanged = (callback) => {
  return auth().onAuthStateChanged(callback);
};

// Atualizar perfil do usuário
export const updateUserProfile = async (displayName, photoURL = null) => {
  try {
    const user = auth().currentUser;
    if (!user) throw new Error('Usuário não autenticado');
    
    const updateData = {};
    if (displayName) updateData.displayName = displayName;
    if (photoURL) updateData.photoURL = photoURL;
    
    await user.updateProfile(updateData);
    
    // Atualizar também no Firestore
    await firestore().collection('users').doc(user.uid).update({
      displayName: displayName || user.displayName,
      photoURL: photoURL || user.photoURL,
      updatedAt: firestore.FieldValue.serverTimestamp(),
    });
    
    return { success: true };
  } catch (error) {
    console.error('Erro ao atualizar perfil:', error);
    return { success: false, error: 'Falha ao atualizar perfil.' };
  }
};
