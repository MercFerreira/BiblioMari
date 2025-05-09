import os
import json
import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel, PhotoImage
from openpyxl import Workbook
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image, ImageTk
import tkinter as tk

# Definindo cores personalizadas em tons de lilás pastel
CORES = {
    "primaria": "#D8BFD8",      # Lilás pastel claro
    "secundaria": "#E6E6FA",    # Lavanda muito claro
    "terciaria": "#C9A0DC",     # Lilás médio
    "texto": "#4B0082",         # Índigo (para texto)
    "botao": "#9370DB",         # Lilás médio para botões
    "botao_hover": "#8A2BE2",   # Violeta para hover
    "estrela": "#9932CC",       # Orquídea escura para estrelas
    "fundo": "#F8F4FF",         # Fundo muito claro com tom lilás
    "destaque": "#BA55D3",      # Orquídea médio para destaques
    "item_hover": "#DCD0FF",    # Lilás muito claro para hover em itens
    "borda": "#B19CD9"          # Lilás médio para bordas
}

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")  # Mantemos o tema base, mas vamos sobrescrever as cores


class Livro:
    def __init__(self, titulo, autor, status_leitura, nota, tipo, imagem_path=None):
        self.titulo = titulo
        self.autor = autor
        self.status_leitura = status_leitura  # "Lido", "Não lido" ou "Lendo"
        self.nota = nota
        self.tipo = tipo
        self.imagem_path = imagem_path

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "status_leitura": self.status_leitura,
            "nota": self.nota,
            "tipo": self.tipo,
            "imagem_path": self.imagem_path
        }


class BibliotecaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("The Bookshelf")
        self.geometry("800x650")
        self.configure(fg_color=CORES["fundo"])  # Cor de fundo personalizada
        self.livros = []
        self.imagem_path = None
        self.imagem_refs = {}  # Para manter referência das imagens exibidas na lista
        self.text_items = []  # Para armazenar os IDs dos textos no canvas
        
        # Configurar ícone da aplicação se disponível
        try:
            self.iconbitmap("bookshelf_icon.ico")
        except:
            pass  # Ignora se o ícone não existir
            
        self.setup_ui()
        self.load_livros()
        
    def load_custom_font(self):
        """Carrega a fonte varsity_regular do diretório de imagens"""
        try:
            # Caminho para o arquivo de fonte
            font_path = r"C:\Users\Marcos Ferreira\Documents\Imagens the bookshelf\varsity_regular.ttf"
            
            # Verificar se o arquivo existe
            if os.path.exists(font_path):
                # Registrar a fonte no sistema
                import tkinter.font as tkFont
                from tkinter import font
                
                # Adicionar a fonte ao Tkinter
                self.font_id = font.Font(family="varsity_regular", size=36)
                return True
            else:
                print(f"Arquivo de fonte não encontrado: {font_path}")
                return False
        except Exception as e:
            print(f"Erro ao carregar fonte personalizada: {e}")
            return False
            
    def on_window_resize(self, event):
        """Atualiza o tamanho da imagem de fundo e a posição do texto quando a janela é redimensionada"""
        # Só atualiza se o evento for da janela principal e não de algum widget interno
        if event.widget == self:
            self.update_header_background()
    
    def update_header_background(self):
        """Atualiza a imagem de fundo e o texto do cabeçalho para se ajustar à largura atual da janela"""
        try:
            # Obter a largura atual da janela
            width = self.winfo_width()
            if width < 10:  # Se a janela ainda não foi renderizada completamente
                width = 800  # Usar valor padrão
                
            # Redimensionar a imagem para a largura atual da janela
            resized_image = self.original_bg_image.resize((width, 150))
            self.bg_photo = ImageTk.PhotoImage(resized_image)
            
            # Limpar o canvas
            self.bg_canvas.delete("all")
            
            # Redesenhar a imagem de fundo
            self.bg_canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
            
            # Redesenhar o título centralizado
            title_id = self.bg_canvas.create_text(
                width // 2,  # Centralizado horizontalmente
                50,   # Posição vertical
                text="The BookShelf",
                font=("varsity_regular", 36),
                fill="#FFFFFF"  # Cor branca para contrastar com o fundo
            )
            
            # Redesenhar o subtítulo centralizado
            subtitle_id = self.bg_canvas.create_text(
                width // 2,  # Centralizado horizontalmente
                90,   # Posição vertical
                text="Sua biblioteca pessoal",
                font=("Arial", 16),
                fill="#FFFFFF"  # Cor branca para contrastar com o fundo
            )
            
            # Armazenar os IDs dos textos para referência futura
            self.text_items = [title_id, subtitle_id]
            
        except Exception as e:
            print(f"Erro ao atualizar imagem de fundo: {e}")


    def setup_ui(self):
        # Carregar a fonte varsity_regular
        self.load_custom_font()
        
        # Cabeçalho com título e subtítulo
        header_frame = ctk.CTkFrame(self, fg_color=CORES["primaria"], corner_radius=0, height=150)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)  # Impede que o frame encolha com o conteúdo
        
        # Criar um canvas para colocar a imagem de fundo
        self.bg_canvas = tk.Canvas(header_frame, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        
        # Carregar a imagem de fundo para o cabeçalho
        try:
            bg_image_path = r"C:\Users\Marcos Ferreira\Documents\Imagens the bookshelf\bgbook.png"
            self.original_bg_image = Image.open(bg_image_path)
            self.update_header_background()
            
            # Vincular evento de redimensionamento da janela
            self.bind("<Configure>", self.on_window_resize)
        except Exception as e:
            print(f"Erro ao carregar imagem de fundo: {e}")
            # Fallback para o cabeçalho original caso a imagem não seja carregada
            titulo_app = ctk.CTkLabel(
                header_frame, 
                text="The Bookshelf", 
                font=ctk.CTkFont(size=28, weight="bold"),
                text_color=CORES["texto"]
            )
            titulo_app.pack(pady=(20, 5))
            
            subtitulo_app = ctk.CTkLabel(
                header_frame, 
                text="Sua biblioteca pessoal", 
                font=ctk.CTkFont(size=16),
                text_color=CORES["texto"]
            )
            subtitulo_app.pack(pady=(0, 20))

        # Área principal com barra lateral e conteúdo
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(padx=15, pady=10, fill="both", expand=True)
        
        # Barra lateral com botões de ação
        sidebar_frame = ctk.CTkFrame(main_frame, fg_color=CORES["secundaria"], width=180)
        sidebar_frame.pack(side="left", fill="y", padx=(0, 15), pady=5)
        sidebar_frame.pack_propagate(False)  # Impede que o frame encolha
        
        # Título da barra lateral
        sidebar_title = ctk.CTkLabel(
            sidebar_frame, 
            text="Ações", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=CORES["texto"]
        )
        sidebar_title.pack(pady=(20, 15))
        
        # Botão de adicionar livro
        btn_adicionar = ctk.CTkButton(
            sidebar_frame, 
            text="Adicionar Livro", 
            command=self.abrir_janela_adicionar,
            height=40,
            corner_radius=8,
            fg_color=CORES["botao"],
            hover_color=CORES["botao_hover"],
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        btn_adicionar.pack(padx=15, pady=10, fill="x")
        
        # Separador
        separator = ctk.CTkFrame(sidebar_frame, height=1, fg_color=CORES["terciaria"])
        separator.pack(fill="x", padx=15, pady=15)
        
        # Título da seção de exportação
        export_title = ctk.CTkLabel(
            sidebar_frame, 
            text="Exportar", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=CORES["texto"]
        )
        export_title.pack(pady=(5, 10))
        
        # Botões de exportação
        ctk.CTkButton(
            sidebar_frame, 
            text="Exportar PDF", 
            command=self.exportar_pdf,
            fg_color=CORES["botao"],
            hover_color=CORES["botao_hover"],
            text_color="white"
        ).pack(padx=15, pady=5, fill="x")
        
        ctk.CTkButton(
            sidebar_frame, 
            text="Exportar Excel", 
            command=self.exportar_excel,
            fg_color=CORES["botao"],
            hover_color=CORES["botao_hover"],
            text_color="white"
        ).pack(padx=15, pady=5, fill="x")
        
        ctk.CTkButton(
            sidebar_frame, 
            text="Exportar Word", 
            command=self.exportar_word,
            fg_color=CORES["botao"],
            hover_color=CORES["botao_hover"],
            text_color="white"
        ).pack(padx=15, pady=5, fill="x")

        # Frame para mostrar lista de livros com scroll
        content_frame = ctk.CTkFrame(main_frame, fg_color=CORES["secundaria"])
        content_frame.pack(side="right", fill="both", expand=True, pady=5)
        
        # Título da lista de livros
        list_title = ctk.CTkLabel(
            content_frame, 
            text="Meus Livros", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=CORES["texto"]
        )
        list_title.pack(pady=(15, 10))
        
        # Frame para a lista com scroll
        self.lista_livros_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.lista_livros_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.canvas = ctk.CTkCanvas(self.lista_livros_frame, borderwidth=0, highlightthickness=0, bg=CORES["secundaria"])
        self.scrollbar = ctk.CTkScrollbar(self.lista_livros_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
    def abrir_janela_adicionar(self):
        # Janela para adicionar novo livro
        window = Toplevel(self)
        window.title("Adicionar Novo Livro")
        window.geometry("700x500")
        window.grab_set()
        
        # Estilizar a janela
        frame_principal = ctk.CTkFrame(window, fg_color=CORES["fundo"])
        frame_principal.pack(padx=0, pady=0, fill="both", expand=True)
        
        # Cabeçalho com título
        header_frame = ctk.CTkFrame(frame_principal, fg_color=CORES["primaria"], corner_radius=0, height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)  # Mantém a altura fixa
        
        # Título da janela
        titulo_janela = ctk.CTkLabel(
            header_frame, 
            text="Adicionar Novo Livro", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=CORES["texto"]
        )
        titulo_janela.pack(pady=25)
        
        # Layout em duas colunas
        frame_conteudo = ctk.CTkFrame(frame_principal, fg_color=CORES["secundaria"], corner_radius=10)
        frame_conteudo.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Coluna esquerda - Informações básicas
        frame_esquerda = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
        frame_esquerda.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        
        # Coluna direita - Avaliação e imagem
        frame_direita = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
        frame_direita.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        
        # === COLUNA ESQUERDA ===
        
        # Título - com label e campo na mesma linha
        frame_titulo = ctk.CTkFrame(frame_esquerda, fg_color="transparent")
        frame_titulo.pack(fill="x", pady=5)
        ctk.CTkLabel(frame_titulo, text="Título:", width=80, anchor="w", text_color=CORES["texto"]).pack(side="left")
        titulo_input = ctk.CTkEntry(frame_titulo, placeholder_text="Título do livro", border_color=CORES["borda"])
        titulo_input.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Autor
        frame_autor = ctk.CTkFrame(frame_esquerda, fg_color="transparent")
        frame_autor.pack(fill="x", pady=5)
        ctk.CTkLabel(frame_autor, text="Autor:", width=80, anchor="w", text_color=CORES["texto"]).pack(side="left")
        autor_input = ctk.CTkEntry(frame_autor, placeholder_text="Nome do autor", border_color=CORES["borda"])
        autor_input.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Tipo
        frame_tipo = ctk.CTkFrame(frame_esquerda, fg_color="transparent")
        frame_tipo.pack(fill="x", pady=5)
        ctk.CTkLabel(frame_tipo, text="Tipo:", width=80, anchor="w", text_color=CORES["texto"]).pack(side="left")
        tipo_input = ctk.CTkComboBox(
            frame_tipo, 
            values=["Físico", "Digital", "E-book", "Audiobook"],
            fg_color="white",
            button_color=CORES["botao"],
            button_hover_color=CORES["botao_hover"],
            border_color=CORES["borda"],
            dropdown_fg_color="white",
            dropdown_hover_color=CORES["item_hover"],
            dropdown_text_color=CORES["texto"]
        )
        tipo_input.set("Físico")
        tipo_input.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Status de leitura
        frame_status = ctk.CTkFrame(frame_esquerda, fg_color="transparent")
        frame_status.pack(fill="x", pady=5)
        ctk.CTkLabel(frame_status, text="Status:", width=80, anchor="w", text_color=CORES["texto"]).pack(side="left")
        status_leitura_input = ctk.CTkComboBox(
            frame_status, 
            values=["Lido", "Não lido", "Lendo"],
            fg_color="white",
            button_color=CORES["botao"],
            button_hover_color=CORES["botao_hover"],
            border_color=CORES["borda"],
            dropdown_fg_color="white",
            dropdown_hover_color=CORES["item_hover"],
            dropdown_text_color=CORES["texto"]
        )
        status_leitura_input.set("Não lido")
        status_leitura_input.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # === COLUNA DIREITA ===
        
        # Avaliação com estrelas
        frame_avaliacao = ctk.CTkFrame(frame_direita, fg_color="transparent")
        frame_avaliacao.pack(fill="x", pady=5)
        ctk.CTkLabel(frame_avaliacao, text="Avaliação:", anchor="w", text_color=CORES["texto"]).pack(fill="x")
        
        frame_estrelas = ctk.CTkFrame(frame_avaliacao, fg_color="transparent")
        frame_estrelas.pack(fill="x", pady=(5, 0))
        
        nota_var = ctk.IntVar(value=0)
        
        def selecionar_nota(valor):
            nota_var.set(valor)
            for i in range(1, 6):
                if i <= valor:
                    estrelas_btn[i-1].configure(text="★", font=ctk.CTkFont(size=20))
                else:
                    estrelas_btn[i-1].configure(text="☆", font=ctk.CTkFont(size=20))
        
        estrelas_btn = []
        for i in range(1, 6):
            btn = ctk.CTkButton(
                frame_estrelas, 
                text="☆", 
                width=30, 
                height=30, 
                corner_radius=15,
                font=ctk.CTkFont(size=20),
                command=lambda v=i: selecionar_nota(v),
                fg_color="transparent", 
                hover_color=CORES["item_hover"],
                text_color=CORES["estrela"]
            )
            btn.pack(side="left", padx=2)
            estrelas_btn.append(btn)
        
        # Seleção de imagem
        frame_imagem_titulo = ctk.CTkFrame(frame_direita, fg_color="transparent")
        frame_imagem_titulo.pack(fill="x", pady=(15, 5))
        ctk.CTkLabel(frame_imagem_titulo, text="Imagem da capa:", anchor="w", text_color=CORES["texto"]).pack(fill="x")
        
        frame_imagem = ctk.CTkFrame(frame_direita, fg_color="white", border_width=1, border_color=CORES["borda"])
        frame_imagem.pack(fill="x")
        
        imagem_path_var = ctk.StringVar()
        label_imagem = ctk.CTkLabel(frame_imagem, text="Nenhuma imagem selecionada", height=60, text_color=CORES["texto"])
        label_imagem.pack(side="left", padx=10, fill="x", expand=True)
        
        def selecionar_nova_imagem():
            path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
            if path:
                imagem_path_var.set(path)
                label_imagem.configure(text=os.path.basename(path))
        
        btn_imagem = ctk.CTkButton(
            frame_imagem, 
            text="Selecionar", 
            command=selecionar_nova_imagem,
            fg_color=CORES["botao"],
            hover_color=CORES["botao_hover"],
            text_color="white"
        )
        btn_imagem.pack(side="right", padx=10)
        
        # Botões de ação
        frame_acoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_acoes.pack(pady=20, fill="x")
        
        def salvar_livro():
            titulo = titulo_input.get()
            autor = autor_input.get()
            
            if not titulo or not autor:
                messagebox.showwarning("Erro", "Título e autor são obrigatórios.")
                return
                
            livro = Livro(
                titulo=titulo,
                autor=autor,
                status_leitura=status_leitura_input.get(),
                nota=nota_var.get(),
                tipo=tipo_input.get(),
                imagem_path=imagem_path_var.get() if imagem_path_var.get() else None
            )
            
            self.livros.append(livro)
            self.salvar_livros()
            self.atualizar_lista()
            window.destroy()
            messagebox.showinfo("Sucesso", f"Livro '{titulo}' adicionado com sucesso!")
        
        btn_cancelar = ctk.CTkButton(
            frame_acoes, 
            text="Cancelar", 
            fg_color="#f0f0f0", 
            text_color="black",
            hover_color="#e0e0e0",
            command=window.destroy
        )
        btn_cancelar.pack(side="left", padx=20, expand=True, fill="x")
        
        btn_salvar = ctk.CTkButton(
            frame_acoes, 
            text="Salvar", 
            command=salvar_livro,
            fg_color=CORES["botao"],
            hover_color=CORES["botao_hover"],
            text_color="white",
            font=ctk.CTkFont(weight="bold")
        )
        btn_salvar.pack(side="left", padx=20, expand=True, fill="x")
        
    def abrir_edicao(self, index):
        livro = self.livros[index]

        # Janela de edição
        window = Toplevel(self)
        window.title(f"Editar livro: {livro.titulo}")
        window.geometry("700x500")
        window.grab_set()
        
        # Estilizar a janela
        frame_principal = ctk.CTkFrame(window, fg_color=CORES["fundo"])
        frame_principal.pack(padx=0, pady=0, fill="both", expand=True)
        
        # Cabeçalho com título
        header_frame = ctk.CTkFrame(frame_principal, fg_color=CORES["primaria"], corner_radius=0, height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)  # Mantém a altura fixa
        
        # Título da janela
        titulo_janela = ctk.CTkLabel(
            header_frame, 
            text=f"Editar Livro", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=CORES["texto"]
        )
        titulo_janela.pack(pady=25)
        
        # Layout em duas colunas
        frame_conteudo = ctk.CTkFrame(frame_principal, fg_color=CORES["secundaria"], corner_radius=10)
        frame_conteudo.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Coluna esquerda - Informações básicas
        frame_esquerda = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
        frame_esquerda.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        
        # Coluna direita - Avaliação e imagem
        frame_direita = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
        frame_direita.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        
        # === COLUNA ESQUERDA ===
        
        # Título - com label e campo na mesma linha
        frame_titulo = ctk.CTkFrame(frame_esquerda, fg_color="transparent")
        frame_titulo.pack(fill="x", pady=5)
        ctk.CTkLabel(frame_titulo, text="Título:", width=80, anchor="w", text_color=CORES["texto"]).pack(side="left")
        titulo_input = ctk.CTkEntry(frame_titulo, placeholder_text="Título do livro", border_color=CORES["borda"])
        titulo_input.insert(0, livro.titulo)
        titulo_input.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Autor
        frame_autor = ctk.CTkFrame(frame_esquerda, fg_color="transparent")
        frame_autor.pack(fill="x", pady=5)
        ctk.CTkLabel(frame_autor, text="Autor:", width=80, anchor="w", text_color=CORES["texto"]).pack(side="left")
        autor_input = ctk.CTkEntry(frame_autor, placeholder_text="Nome do autor", border_color=CORES["borda"])
        autor_input.insert(0, livro.autor)
        autor_input.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Tipo
        frame_tipo = ctk.CTkFrame(frame_esquerda, fg_color="transparent")
        frame_tipo.pack(fill="x", pady=5)
        ctk.CTkLabel(frame_tipo, text="Tipo:", width=80, anchor="w", text_color=CORES["texto"]).pack(side="left")
        tipo_input = ctk.CTkComboBox(
            frame_tipo, 
            values=["Físico", "Digital", "E-book", "Audiobook"],
            fg_color="white",
            button_color=CORES["botao"],
            button_hover_color=CORES["botao_hover"],
            border_color=CORES["borda"],
            dropdown_fg_color="white",
            dropdown_hover_color=CORES["item_hover"],
            dropdown_text_color=CORES["texto"]
        )
        tipo_input.set(livro.tipo)
        tipo_input.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Status de leitura
        frame_status = ctk.CTkFrame(frame_esquerda, fg_color="transparent")
        frame_status.pack(fill="x", pady=5)
        ctk.CTkLabel(frame_status, text="Status:", width=80, anchor="w", text_color=CORES["texto"]).pack(side="left")
        status_leitura_input = ctk.CTkComboBox(
            frame_status, 
            values=["Lido", "Não lido", "Lendo"],
            fg_color="white",
            button_color=CORES["botao"],
            button_hover_color=CORES["botao_hover"],
            border_color=CORES["borda"],
            dropdown_fg_color="white",
            dropdown_hover_color=CORES["item_hover"],
            dropdown_text_color=CORES["texto"]
        )
        status_leitura_input.set(livro.status_leitura if hasattr(livro, 'status_leitura') else "Lido" if getattr(livro, 'lido', False) else "Não lido")
        status_leitura_input.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # === COLUNA DIREITA ===
        
        # Avaliação com estrelas
        frame_avaliacao = ctk.CTkFrame(frame_direita, fg_color="transparent")
        frame_avaliacao.pack(fill="x", pady=5)
        ctk.CTkLabel(frame_avaliacao, text="Avaliação:", anchor="w", text_color=CORES["texto"]).pack(fill="x")
        
        frame_estrelas = ctk.CTkFrame(frame_avaliacao, fg_color="transparent")
        frame_estrelas.pack(fill="x", pady=(5, 0))
        
        nota_var = ctk.IntVar(value=livro.nota)
        
        def selecionar_nota(valor):
            nota_var.set(valor)
            for i in range(1, 6):
                if i <= valor:
                    estrelas_btn[i-1].configure(text="★", font=ctk.CTkFont(size=20))
                else:
                    estrelas_btn[i-1].configure(text="☆", font=ctk.CTkFont(size=20))
        
        estrelas_btn = []
        for i in range(1, 6):
            btn = ctk.CTkButton(
                frame_estrelas, 
                text="★" if i <= livro.nota else "☆", 
                width=30, 
                height=30, 
                corner_radius=15,
                font=ctk.CTkFont(size=20),
                command=lambda v=i: selecionar_nota(v),
                fg_color="transparent", 
                hover_color=CORES["item_hover"],
                text_color=CORES["estrela"]
            )
            btn.pack(side="left", padx=2)
            estrelas_btn.append(btn)
        
        # Seleção de imagem
        frame_imagem_titulo = ctk.CTkFrame(frame_direita, fg_color="transparent")
        frame_imagem_titulo.pack(fill="x", pady=(15, 5))
        ctk.CTkLabel(frame_imagem_titulo, text="Imagem da capa:", anchor="w", text_color=CORES["texto"]).pack(fill="x")
        
        frame_imagem = ctk.CTkFrame(frame_direita, fg_color="white", border_width=1, border_color=CORES["borda"])
        frame_imagem.pack(fill="x")
        
        imagem_path_var = ctk.StringVar(value=livro.imagem_path if livro.imagem_path else "")
        label_imagem = ctk.CTkLabel(
            frame_imagem, 
            text=os.path.basename(imagem_path_var.get()) if imagem_path_var.get() else "Nenhuma imagem selecionada",
            height=60,
            text_color=CORES["texto"]
        )
        label_imagem.pack(side="left", padx=10, fill="x", expand=True)
        
        def selecionar_nova_imagem():
            path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
            if path:
                imagem_path_var.set(path)
                label_imagem.configure(text=os.path.basename(path))
        
        btn_imagem = ctk.CTkButton(
            frame_imagem, 
            text="Selecionar", 
            command=selecionar_nova_imagem,
            fg_color=CORES["botao"],
            hover_color=CORES["botao_hover"],
            text_color="white"
        )
        btn_imagem.pack(side="right", padx=10)
        
        # Botões de ação
        frame_acoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_acoes.pack(pady=20, fill="x")
        
        def salvar_modificacoes():
            livro.titulo = titulo_input.get()
            livro.autor = autor_input.get()
            livro.status_leitura = status_leitura_input.get()
            livro.nota = nota_var.get()
            livro.tipo = tipo_input.get()
            livro.imagem_path = imagem_path_var.get() if imagem_path_var.get() else None
            self.salvar_livros()
            self.atualizar_lista()
            window.destroy()
            messagebox.showinfo("Sucesso", f"Livro '{livro.titulo}' atualizado com sucesso!")
        
        def excluir_livro():
            resposta = messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente excluir o livro '{livro.titulo}'?")
            if resposta:
                del self.livros[index]
                self.salvar_livros()
                self.atualizar_lista()
                window.destroy()
                messagebox.showinfo("Exclusão", f"Livro '{livro.titulo}' excluído com sucesso!")
        
        # Frame para os botões
        frame_botoes = ctk.CTkFrame(frame_acoes, fg_color="transparent")
        frame_botoes.pack(fill="x")
        
        # Botão de excluir
        btn_excluir = ctk.CTkButton(
            frame_botoes, 
            text="Excluir", 
            fg_color="#FF6B6B", 
            hover_color="#FF5252",
            text_color="white",
            command=excluir_livro
        )
        btn_excluir.pack(side="left", padx=10, expand=True, fill="x")
        
        # Botão de cancelar
        btn_cancelar = ctk.CTkButton(
            frame_botoes, 
            text="Cancelar", 
            fg_color="#f0f0f0", 
            text_color="black",
            hover_color="#e0e0e0",
            command=window.destroy
        )
        btn_cancelar.pack(side="left", padx=10, expand=True, fill="x")
        
        # Botão de salvar
        btn_salvar = ctk.CTkButton(
            frame_botoes, 
            text="Salvar", 
            command=salvar_modificacoes,
            fg_color=CORES["botao"],
            hover_color=CORES["botao_hover"],
            text_color="white",
            font=ctk.CTkFont(weight="bold")
        )
        btn_salvar.pack(side="left", padx=10, expand=True, fill="x")
        
    def atualizar_lista(self):
        # Limpar a lista atual
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Limpar referências de imagens
        self.imagem_refs.clear()
        
        if not self.livros:
            # Mensagem quando não há livros
            msg_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
            msg_frame.pack(pady=20, padx=20, fill="x")
            
            ctk.CTkLabel(
                msg_frame, 
                text="Sua biblioteca está vazia. Adicione seu primeiro livro!", 
                font=ctk.CTkFont(size=14),
                text_color=CORES["texto"]
            ).pack(pady=10)
            
            ctk.CTkButton(
                msg_frame, 
                text="Adicionar Livro", 
                command=self.abrir_janela_adicionar,
                fg_color=CORES["botao"],
                hover_color=CORES["botao_hover"],
                text_color="white"
            ).pack(pady=10)
            return
        
        # Adicionar cada livro à lista
        for idx, livro in enumerate(self.livros):
            # Frame para o item do livro com efeito de hover
            frame_item = ctk.CTkFrame(self.scrollable_frame, fg_color=CORES["secundaria"], corner_radius=10)
            frame_item.pack(fill="x", padx=10, pady=5, ipady=5)
            
            # Adicionar evento de hover
            def on_enter(e, frame=frame_item):
                frame.configure(fg_color=CORES["item_hover"])
                
            def on_leave(e, frame=frame_item):
                frame.configure(fg_color=CORES["secundaria"])
                
            frame_item.bind("<Enter>", on_enter)
            frame_item.bind("<Leave>", on_leave)
            
            # Container para imagem e texto
            content_frame = ctk.CTkFrame(frame_item, fg_color="transparent")
            content_frame.pack(fill="x", padx=10, pady=5, expand=True)
            
            # Frame para imagem (lado esquerdo)
            img_frame = ctk.CTkFrame(content_frame, width=80, height=120, fg_color="white")
            img_frame.pack(side="left", padx=(0, 10))
            img_frame.pack_propagate(False)  # Mantém o tamanho fixo
            
            # Carregar e exibir imagem se existir
            if livro.imagem_path and os.path.exists(livro.imagem_path):
                try:
                    img = Image.open(livro.imagem_path)
                    img.thumbnail((80, 120))
                    photo_img = ctk.CTkImage(light_image=img, size=(80, 120))
                    self.imagem_refs[idx] = photo_img  # Manter referência
                    
                    img_label = ctk.CTkLabel(img_frame, image=photo_img, text="")
                    img_label.pack(fill="both", expand=True)
                except Exception as e:
                    print(f"Erro ao carregar imagem: {e}")
                    ctk.CTkLabel(img_frame, text="Imagem", fg_color="#f0f0f0").pack(fill="both", expand=True)
            else:
                # Placeholder para quando não há imagem
                placeholder = ctk.CTkLabel(
                    img_frame, 
                    text="Sem\nImagem", 
                    font=ctk.CTkFont(size=12),
                    fg_color=CORES["secundaria"],
                    text_color=CORES["texto"]
                )
                placeholder.pack(fill="both", expand=True)
            
            # Frame para texto (lado direito)
            texto_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            texto_frame.pack(side="left", fill="both", expand=True)
            
            # Título e autor
            titulo_label = ctk.CTkLabel(
                texto_frame, 
                text=livro.titulo, 
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w",
                text_color=CORES["texto"]
            )
            titulo_label.pack(fill="x", pady=(0, 2))
            
            autor_label = ctk.CTkLabel(
                texto_frame, 
                text=f"por {livro.autor}", 
                font=ctk.CTkFont(size=14),
                anchor="w",
                text_color=CORES["texto"]
            )
            autor_label.pack(fill="x", pady=(0, 5))
            
            # Avaliação com estrelas
            estrelas_frame = ctk.CTkFrame(texto_frame, fg_color="transparent")
            estrelas_frame.pack(fill="x", pady=(0, 5))
            
            # Exibir estrelas de acordo com a nota
            for i in range(5):
                estrela = ctk.CTkLabel(
                    estrelas_frame, 
                    text="★" if i < livro.nota else "☆", 
                    font=ctk.CTkFont(size=16),
                    text_color=CORES["estrela"]
                )
                estrela.pack(side="left", padx=1)
            
            # Status de leitura e tipo
            status_texto = livro.status_leitura if hasattr(livro, 'status_leitura') else "Lido" if getattr(livro, 'lido', False) else "Não lido"
            label_status = ctk.CTkLabel(
                texto_frame, 
                text=f"Status: {status_texto} | Tipo: {livro.tipo}", 
                font=ctk.CTkFont(size=12), 
                anchor="w",
                text_color=CORES["texto"]
            )
            label_status.pack(fill="x", pady=(4, 0))
            
            # Botão Editar no canto direito
            btn_editar = ctk.CTkButton(
                frame_item, 
                text="Editar", 
                width=80,
                command=lambda i=idx: self.abrir_edicao(i),
                fg_color=CORES["botao"],
                hover_color=CORES["botao_hover"],
                text_color="white"
            )
            btn_editar.pack(side="right", padx=10, pady=10)
    
    def salvar_livros(self):
        with open("biblioteca.json", "w", encoding="utf-8") as f:
            json.dump([livro.to_dict() for livro in self.livros], f, ensure_ascii=False, indent=2)
    
    def load_livros(self):
        if os.path.exists("biblioteca.json"):
            with open("biblioteca.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                for livro_data in dados:
                    if 'status_leitura' not in livro_data and 'lido' in livro_data:
                        livro_data['status_leitura'] = "Lido" if livro_data['lido'] else "Não lido"
                    if 'tipo' not in livro_data:
                        livro_data['tipo'] = 'Físico'
                self.livros = []
                for d in dados:
                    # Remover campo 'lido' se existir para evitar duplicação
                    if 'lido' in d and 'status_leitura' in d:
                        d.pop('lido')
                    self.livros.append(Livro(**d))
                self.atualizar_lista()
    
    def exportar_pdf(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if path:
            from reportlab.lib.units import inch
            c = canvas.Canvas(path, pagesize=letter)
            width, height = letter
            margin = 50
            y = height - margin
            
            # Adicionar título ao PDF
            c.setFont("Helvetica-Bold", 18)
            c.setFillColorRGB(0.29, 0.0, 0.51)  # Cor índigo similar ao CORES["texto"]
            c.drawString(margin, y, "The Bookshelf - Minha Biblioteca")
            y -= 30
            
            # Adicionar data
            from datetime import datetime
            c.setFont("Helvetica", 10)
            c.setFillColorRGB(0.29, 0.0, 0.51)  # Cor índigo similar ao CORES["texto"]
            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.drawString(margin, y, f"Exportado em: {data_atual}")
            y -= 40

            for livro in self.livros:
                if y < 150:  # Se não couber mais na página, criar nova página
                    c.showPage()
                    y = height - margin

                # Imagem
                img_x = margin
                img_y = y - 120  # altura da imagem

                if livro.imagem_path and os.path.exists(livro.imagem_path):
                    try:
                        imagem = Image.open(livro.imagem_path)
                        imagem.thumbnail((80, 120), Image.LANCZOS)
                        img_temp_path = "temp_pdf_img.jpg"
                        imagem.save(img_temp_path)
                        c.drawImage(img_temp_path, img_x, img_y, width=80, height=120)
                    except Exception as e:
                        print(f"Erro ao adicionar imagem no PDF: {e}")

                # Texto ao lado da imagem
                text_x = img_x + 100
                text_y = y - 20

                c.setFont("Helvetica-Bold", 14)
                c.setFillColorRGB(0.29, 0.0, 0.51)  # Cor índigo similar ao CORES["texto"]
                c.drawString(text_x, text_y, livro.titulo)

                c.setFont("Helvetica", 12)
                c.setFillColorRGB(0.29, 0.0, 0.51)  # Cor índigo similar ao CORES["texto"]
                c.drawString(text_x, text_y - 20, f"Autor: {livro.autor}")

                c.setFont("Helvetica", 11)
                c.setFillColorRGB(0.29, 0.0, 0.51)  # Cor índigo similar ao CORES["texto"]
                status_texto = livro.status_leitura if hasattr(livro, 'status_leitura') else "Lido" if getattr(livro, 'lido', False) else "Não lido"
                status_text = f"Status: {status_texto} | Nota: {livro.nota} | Tipo: {livro.tipo}"
                c.drawString(text_x, text_y - 40, status_text)
                
                # Desenhar estrelas
                c.setFillColorRGB(0.6, 0.2, 0.8)  # Cor lilás para as estrelas
                for i in range(5):
                    star_x = text_x + i * 15
                    star_y = text_y - 60
                    if i < livro.nota:
                        c.drawString(star_x, star_y, "★")
                    else:
                        c.drawString(star_x, star_y, "☆")

                y -= 140  # Espaço entre livros
        
            c.save()
            messagebox.showinfo("Exportação", f"PDF exportado com sucesso para {path}")
    
    def exportar_excel(self):
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if path:
            wb = Workbook()
            sheet = wb.active
            sheet.title = "Minha Biblioteca"
            
            # Estilizar cabeçalho
            from openpyxl.styles import Font, PatternFill, Alignment
            header_font = Font(name='Arial', size=12, bold=True, color='4B0082')
            header_fill = PatternFill(start_color="D8BFD8", end_color="D8BFD8", fill_type="solid")
            
            # Adicionar cabeçalho
            headers = ["Título", "Autor", "Status", "Nota", "Tipo", "Imagem"]
            for col_num, header in enumerate(headers, 1):
                cell = sheet.cell(row=1, column=col_num, value=header)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal='center')
            
            # Adicionar dados
            for row_num, livro in enumerate(self.livros, 2):
                status = livro.status_leitura if hasattr(livro, 'status_leitura') else "Lido" if getattr(livro, 'lido', False) else "Não lido"
                sheet.cell(row=row_num, column=1, value=livro.titulo)
                sheet.cell(row=row_num, column=2, value=livro.autor)
                sheet.cell(row=row_num, column=3, value=status)
                sheet.cell(row=row_num, column=4, value=livro.nota)
                sheet.cell(row=row_num, column=5, value=livro.tipo)
                sheet.cell(row=row_num, column=6, value=livro.imagem_path)
            
            # Ajustar largura das colunas
            for col in sheet.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                adjusted_width = (max_length + 2)
                sheet.column_dimensions[column].width = adjusted_width
            
            wb.save(path)
            messagebox.showinfo("Exportação", f"Excel exportado com sucesso para {path}")
    
    def exportar_word(self):
        path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Files", "*.docx")])
        if path:
            doc = Document()
            
            # Adicionar título
            doc.add_heading("The Bookshelf - Minha Biblioteca", 0)
            
            # Adicionar data
            from datetime import datetime
            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
            doc.add_paragraph(f"Exportado em: {data_atual}")
            
            # Adicionar livros
            for livro in self.livros:
                doc.add_heading(livro.titulo, level=1)
                
                # Tabela com informações
                table = doc.add_table(rows=5, cols=2)
                table.style = 'Table Grid'
                
                # Autor
                row = table.rows[0]
                row.cells[0].text = "Autor"
                row.cells[1].text = livro.autor
                
                # Status
                row = table.rows[1]
                status = livro.status_leitura if hasattr(livro, 'status_leitura') else "Lido" if getattr(livro, 'lido', False) else "Não lido"
                row.cells[0].text = "Status"
                row.cells[1].text = status
                
                # Nota
                row = table.rows[2]
                row.cells[0].text = "Nota"
                estrelas = "★" * livro.nota + "☆" * (5 - livro.nota)
                row.cells[1].text = f"{livro.nota}/5 {estrelas}"
                
                # Tipo
                row = table.rows[3]
                row.cells[0].text = "Tipo"
                row.cells[1].text = livro.tipo
                
                # Imagem
                row = table.rows[4]
                row.cells[0].text = "Imagem"
                row.cells[1].text = livro.imagem_path if livro.imagem_path else "Nenhuma imagem"
                
                doc.add_paragraph("")
            
            doc.save(path)
            messagebox.showinfo("Exportação", f"Word exportado com sucesso para {path}")


if __name__ == "__main__":
    app = BibliotecaApp()
    app.mainloop()
