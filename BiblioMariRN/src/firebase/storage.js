import storage from '@react-native-firebase/storage';
import { getCurrentUser } from './auth';
import { Platform } from 'react-native';

// Upload de imagem para o Firebase Storage
export const uploadImage = async (uri, path = 'book_covers') => {
  try {
    const user = getCurrentUser();
    if (!user) throw new Error('Usuário não autenticado');

    // Gerar um nome de arquivo único
    const filename = uri.substring(uri.lastIndexOf('/') + 1);
    const fileExtension = filename.split('.').pop();
    const uniqueFilename = `${user.uid}_${Date.now()}.${fileExtension}`;
    
    // Caminho completo no Storage
    const storagePath = `${path}/${user.uid}/${uniqueFilename}`;
    const storageRef = storage().ref(storagePath);

    // Preparar a imagem para upload
    const uploadUri = Platform.OS === 'ios' ? uri.replace('file://', '') : uri;

    // Fazer o upload da imagem
    await storageRef.putFile(uploadUri);

    // Obter a URL de download
    const downloadURL = await storageRef.getDownloadURL();

    return { 
      success: true, 
      url: downloadURL,
      path: storagePath
    };
  } catch (error) {
    console.error('Erro ao fazer upload de imagem:', error);
    return { 
      success: false, 
      error: 'Falha ao fazer upload da imagem. Tente novamente.' 
    };
  }
};

// Excluir imagem do Firebase Storage
export const deleteImage = async (url) => {
  try {
    if (!url) return { success: true };

    // Obter referência do Storage a partir da URL
    const storageRef = storage().refFromURL(url);
    
    // Excluir a imagem
    await storageRef.delete();

    return { success: true };
  } catch (error) {
    console.error('Erro ao excluir imagem:', error);
    return { 
      success: false, 
      error: 'Falha ao excluir imagem. Tente novamente.' 
    };
  }
};
