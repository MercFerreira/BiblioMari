import { ref, uploadBytes, getDownloadURL, deleteObject } from 'firebase/storage';
import { storage } from './config';
import { getCurrentUser } from './auth';
import * as FileSystem from 'expo-file-system';

// Upload de imagem para o Firebase Storage
export const uploadImage = async (uri, path = 'book_covers') => {
  try {
    const user = getCurrentUser();
    if (!user) throw new Error('Usuário não autenticado');

    // Gerar um nome de arquivo único
    const filename = uri.split('/').pop();
    const fileExtension = filename.split('.').pop();
    const uniqueFilename = `${user.uid}_${Date.now()}.${fileExtension}`;
    
    // Caminho completo no Storage
    const storagePath = `${path}/${user.uid}/${uniqueFilename}`;
    const storageRef = ref(storage, storagePath);

    // Converter URI para blob
    const response = await fetch(uri);
    const blob = await response.blob();

    // Fazer o upload da imagem
    await uploadBytes(storageRef, blob);

    // Obter a URL de download
    const downloadURL = await getDownloadURL(storageRef);

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
    const storageRef = ref(storage, url);
    
    // Excluir a imagem
    await deleteObject(storageRef);

    return { success: true };
  } catch (error) {
    console.error('Erro ao excluir imagem:', error);
    return { 
      success: false, 
      error: 'Falha ao excluir imagem. Tente novamente.' 
    };
  }
};

// Baixar imagem temporariamente para compartilhamento
export const downloadImageToTemp = async (url, filename) => {
  try {
    if (!url) throw new Error('URL de imagem não fornecida');
    
    // Caminho temporário para salvar a imagem
    const fileUri = `${FileSystem.cacheDirectory}${filename}`;
    
    // Baixar a imagem
    const downloadResult = await FileSystem.downloadAsync(url, fileUri);
    
    if (downloadResult.status !== 200) {
      throw new Error('Falha ao baixar imagem');
    }
    
    return { success: true, uri: fileUri };
  } catch (error) {
    console.error('Erro ao baixar imagem:', error);
    return { 
      success: false, 
      error: 'Falha ao baixar imagem. Tente novamente.' 
    };
  }
};
