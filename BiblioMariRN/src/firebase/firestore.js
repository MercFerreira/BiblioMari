import firestore from '@react-native-firebase/firestore';
import storage from '@react-native-firebase/storage';
import { getCurrentUser } from './auth';

// Coleções do Firestore
const USERS_COLLECTION = 'users';
const BOOKS_COLLECTION = 'books';

// Adicionar um novo livro
export const addBook = async (bookData) => {
  try {
    const user = getCurrentUser();
    if (!user) throw new Error('Usuário não autenticado');

    // Referência para a subcoleção de livros do usuário
    const bookRef = firestore()
      .collection(USERS_COLLECTION)
      .doc(user.uid)
      .collection(BOOKS_COLLECTION);

    // Adicionar timestamp de criação
    const bookWithTimestamp = {
      ...bookData,
      createdAt: firestore.FieldValue.serverTimestamp(),
      updatedAt: firestore.FieldValue.serverTimestamp(),
      userId: user.uid,
    };

    // Adicionar o livro ao Firestore
    const docRef = await bookRef.add(bookWithTimestamp);
    
    return { 
      success: true, 
      bookId: docRef.id,
      book: { id: docRef.id, ...bookWithTimestamp }
    };
  } catch (error) {
    console.error('Erro ao adicionar livro:', error);
    return { 
      success: false, 
      error: 'Falha ao adicionar livro. Tente novamente.' 
    };
  }
};

// Atualizar um livro existente
export const updateBook = async (bookId, bookData) => {
  try {
    const user = getCurrentUser();
    if (!user) throw new Error('Usuário não autenticado');

    // Referência para o documento do livro
    const bookRef = firestore()
      .collection(USERS_COLLECTION)
      .doc(user.uid)
      .collection(BOOKS_COLLECTION)
      .doc(bookId);

    // Adicionar timestamp de atualização
    const bookWithTimestamp = {
      ...bookData,
      updatedAt: firestore.FieldValue.serverTimestamp(),
    };

    // Atualizar o livro no Firestore
    await bookRef.update(bookWithTimestamp);
    
    return { 
      success: true, 
      book: { id: bookId, ...bookWithTimestamp }
    };
  } catch (error) {
    console.error('Erro ao atualizar livro:', error);
    return { 
      success: false, 
      error: 'Falha ao atualizar livro. Tente novamente.' 
    };
  }
};

// Excluir um livro
export const deleteBook = async (bookId, imagePath = null) => {
  try {
    const user = getCurrentUser();
    if (!user) throw new Error('Usuário não autenticado');

    // Se houver uma imagem associada, excluí-la do Storage
    if (imagePath) {
      try {
        // Extrair o caminho do Storage da URL completa
        const storageRef = storage().refFromURL(imagePath);
        await storageRef.delete();
      } catch (imageError) {
        console.warn('Erro ao excluir imagem:', imageError);
        // Continuar mesmo se a exclusão da imagem falhar
      }
    }

    // Excluir o documento do livro
    await firestore()
      .collection(USERS_COLLECTION)
      .doc(user.uid)
      .collection(BOOKS_COLLECTION)
      .doc(bookId)
      .delete();
    
    return { success: true };
  } catch (error) {
    console.error('Erro ao excluir livro:', error);
    return { 
      success: false, 
      error: 'Falha ao excluir livro. Tente novamente.' 
    };
  }
};

// Obter todos os livros do usuário
export const getUserBooks = async (sortBy = 'createdAt', sortOrder = 'desc') => {
  try {
    const user = getCurrentUser();
    if (!user) throw new Error('Usuário não autenticado');

    // Consultar a subcoleção de livros do usuário
    const booksSnapshot = await firestore()
      .collection(USERS_COLLECTION)
      .doc(user.uid)
      .collection(BOOKS_COLLECTION)
      .orderBy(sortBy, sortOrder)
      .get();

    // Mapear os documentos para um array de objetos
    const books = booksSnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
    
    return { success: true, books };
  } catch (error) {
    console.error('Erro ao obter livros:', error);
    return { 
      success: false, 
      error: 'Falha ao carregar livros. Tente novamente.',
      books: [] 
    };
  }
};

// Obter um livro específico
export const getBookById = async (bookId) => {
  try {
    const user = getCurrentUser();
    if (!user) throw new Error('Usuário não autenticado');

    // Obter o documento do livro
    const bookDoc = await firestore()
      .collection(USERS_COLLECTION)
      .doc(user.uid)
      .collection(BOOKS_COLLECTION)
      .doc(bookId)
      .get();

    if (!bookDoc.exists) {
      return { 
        success: false, 
        error: 'Livro não encontrado.' 
      };
    }

    return { 
      success: true, 
      book: { id: bookDoc.id, ...bookDoc.data() }
    };
  } catch (error) {
    console.error('Erro ao obter livro:', error);
    return { 
      success: false, 
      error: 'Falha ao carregar livro. Tente novamente.' 
    };
  }
};

// Pesquisar livros por título ou autor
export const searchBooks = async (searchTerm) => {
  try {
    const user = getCurrentUser();
    if (!user) throw new Error('Usuário não autenticado');

    // Firestore não suporta pesquisa de texto completo, então precisamos fazer múltiplas consultas
    const titleSnapshot = await firestore()
      .collection(USERS_COLLECTION)
      .doc(user.uid)
      .collection(BOOKS_COLLECTION)
      .orderBy('titulo')
      .startAt(searchTerm)
      .endAt(searchTerm + '\uf8ff')
      .get();

    const authorSnapshot = await firestore()
      .collection(USERS_COLLECTION)
      .doc(user.uid)
      .collection(BOOKS_COLLECTION)
      .orderBy('autor')
      .startAt(searchTerm)
      .endAt(searchTerm + '\uf8ff')
      .get();

    // Combinar resultados e remover duplicatas
    const titleResults = titleSnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));

    const authorResults = authorSnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));

    // Remover duplicatas (livros que aparecem em ambas as consultas)
    const allResults = [...titleResults];
    authorResults.forEach(authorBook => {
      if (!allResults.some(book => book.id === authorBook.id)) {
        allResults.push(authorBook);
      }
    });

    return { success: true, books: allResults };
  } catch (error) {
    console.error('Erro ao pesquisar livros:', error);
    return { 
      success: false, 
      error: 'Falha ao pesquisar livros. Tente novamente.',
      books: [] 
    };
  }
};

// Filtrar livros por status de leitura
export const filterBooksByReadStatus = async (isRead) => {
  try {
    const user = getCurrentUser();
    if (!user) throw new Error('Usuário não autenticado');

    const booksSnapshot = await firestore()
      .collection(USERS_COLLECTION)
      .doc(user.uid)
      .collection(BOOKS_COLLECTION)
      .where('lido', '==', isRead)
      .orderBy('createdAt', 'desc')
      .get();

    const books = booksSnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));

    return { success: true, books };
  } catch (error) {
    console.error('Erro ao filtrar livros:', error);
    return { 
      success: false, 
      error: 'Falha ao filtrar livros. Tente novamente.',
      books: [] 
    };
  }
};
