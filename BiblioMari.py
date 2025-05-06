import os
import json
import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel
from openpyxl import Workbook
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class Livro:
    def __init__(self, titulo, autor, lido, nota, tipo, imagem_path=None):
        self.titulo = titulo
        self.autor = autor
        self.lido = lido
        self.nota = nota
        self.tipo = tipo
        self.imagem_path = imagem_path

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "lido": self.lido,
            "nota": self.nota,
            "tipo": self.tipo,
            "imagem_path": self.imagem_path
        }


class BibliotecaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Minha Biblioteca")
        self.geometry("700x600")
        self.livros = []
        self.imagem_path = None
        self.imagem_refs = {}  # Para manter referência das imagens exibidas na lista
        self.setup_ui()
        self.load_livros()

    def setup_ui(self):
        # Título da aplicação
        titulo_app = ctk.CTkLabel(self, text="The Bookshelf", font=ctk.CTkFont(size=24, weight="bold"))
        titulo_app.pack(pady=(20, 10))
        
        subtitulo_app = ctk.CTkLabel(self, text="Sua biblioteca pessoal", font=ctk.CTkFont(size=14))
        subtitulo_app.pack(pady=(0, 20))

        # Frame para mostrar lista de livros com scroll
        self.lista_livros_frame = ctk.CTkFrame(self)
        self.lista_livros_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.canvas = ctk.CTkCanvas(self.lista_livros_frame, borderwidth=0, highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(self.lista_livros_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Botões de ação
        frame_botoes = ctk.CTkFrame(self)
        frame_botoes.pack(pady=15, padx=10, fill="x")

        # Botão de adicionar livro com ícone
        btn_adicionar = ctk.CTkButton(
            frame_botoes, 
            text="Adicionar Livro", 
            command=self.abrir_janela_adicionar,
            height=40,
            corner_radius=8
        )
        btn_adicionar.pack(side="left", padx=10, expand=True, fill="x")

        # Botões de exportação
        frame_exportar = ctk.CTkFrame(self)
        frame_exportar.pack(pady=(0, 15), padx=10, fill="x")

        ctk.CTkButton(frame_exportar, text="Exportar PDF", command=self.exportar_pdf).pack(side="left", padx=5, expand=True, fill="x")
        ctk.CTkButton(frame_exportar, text="Exportar Excel", command=self.exportar_excel).pack(side="left", padx=5, expand=True, fill="x")
        ctk.CTkButton(frame_exportar, text="Exportar Word", command=self.exportar_word).pack(side="left", padx=5, expand=True, fill="x")

    def abrir_janela_adicionar(self):
        # Janela para adicionar novo livro
        window = Toplevel(self)
        window.title("Adicionar Novo Livro")
        window.geometry("500x550")
        window.grab_set()
        
        # Estilizar a janela
        frame_principal = ctk.CTkFrame(window)
        frame_principal.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Título da janela
        titulo_janela = ctk.CTkLabel(frame_principal, text="Adicionar Novo Livro", font=ctk.CTkFont(size=20, weight="bold"))
        titulo_janela.pack(pady=(20, 30))
        
        # Campos de entrada
        frame_campos = ctk.CTkFrame(frame_principal)
        frame_campos.pack(padx=20, pady=10, fill="x")
        
        # Título
        ctk.CTkLabel(frame_campos, text="Título:", anchor="w").pack(fill="x", pady=(10, 0))
        titulo_input = ctk.CTkEntry(frame_campos, placeholder_text="Título do livro")
        titulo_input.pack(fill="x", pady=(0, 10))
        
        # Autor
        ctk.CTkLabel(frame_campos, text="Autor:", anchor="w").pack(fill="x", pady=(10, 0))
        autor_input = ctk.CTkEntry(frame_campos, placeholder_text="Nome do autor")
        autor_input.pack(fill="x", pady=(0, 10))
        
        # Tipo
        ctk.CTkLabel(frame_campos, text="Tipo:", anchor="w").pack(fill="x", pady=(10, 0))
        tipo_input = ctk.CTkComboBox(frame_campos, values=["Físico", "Digital", "E-book", "Audiobook"])
        tipo_input.set("Físico")
        tipo_input.pack(fill="x", pady=(0, 10))
        
        # Status de leitura
        frame_lido = ctk.CTkFrame(frame_campos, fg_color="transparent")
        frame_lido.pack(fill="x", pady=10)
        
        ctk.CTkLabel(frame_lido, text="Status de leitura:", anchor="w").pack(side="left")
        lido_var = ctk.BooleanVar(value=False)
        lido_check = ctk.CTkCheckBox(frame_lido, text="Lido", variable=lido_var)
        lido_check.pack(side="left", padx=10)
        
        # Avaliação com estrelas
        ctk.CTkLabel(frame_campos, text="Avaliação:", anchor="w").pack(fill="x", pady=(10, 5))
        
        frame_estrelas = ctk.CTkFrame(frame_campos, fg_color="transparent")
        frame_estrelas.pack(fill="x", pady=(0, 10))
        
        nota_var = ctk.IntVar(value=0)
        
        # Implementaremos a lógica das estrelas em uma função separada
        def selecionar_nota(valor):
            nota_var.set(valor)
            for i in range(1, 6):
                if i <= valor:
                    estrelas_btn[i-1].configure(text="★", font=ctk.CTkFont(size=24))
                else:
                    estrelas_btn[i-1].configure(text="☆", font=ctk.CTkFont(size=24))
        
        estrelas_btn = []
        for i in range(1, 6):
            btn = ctk.CTkButton(
                frame_estrelas, 
                text="☆", 
                width=30, 
                height=30, 
                corner_radius=15,
                font=ctk.CTkFont(size=24),
                command=lambda v=i: selecionar_nota(v),
                fg_color="transparent", 
                hover_color="#e0e0e0",
                text_color="#FFD700"
            )
            btn.pack(side="left", padx=2)
            estrelas_btn.append(btn)
            
        # Seleção de imagem
        ctk.CTkLabel(frame_campos, text="Imagem da capa:", anchor="w").pack(fill="x", pady=(20, 5))
        
        frame_imagem = ctk.CTkFrame(frame_campos)
        frame_imagem.pack(fill="x", pady=(0, 10))
        
        imagem_path_var = ctk.StringVar()
        label_imagem = ctk.CTkLabel(frame_imagem, text="Nenhuma imagem selecionada")
        label_imagem.pack(side="left", padx=10, fill="x", expand=True)
        
        def selecionar_nova_imagem():
            path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
            if path:
                imagem_path_var.set(path)
                label_imagem.configure(text=os.path.basename(path))
        
        btn_imagem = ctk.CTkButton(frame_imagem, text="Selecionar", command=selecionar_nova_imagem)
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
                lido=lido_var.get(),
                nota=nota_var.get(),
                tipo=tipo_input.get(),
                imagem_path=imagem_path_var.get() if imagem_path_var.get() else None
            )
            
            self.livros.append(livro)
            self.salvar_livros()
            self.atualizar_lista()
            window.destroy()
        
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
            command=salvar_livro
        )
        btn_salvar.pack(side="left", padx=20, expand=True, fill="x")

    def abrir_edicao(self, index):
        livro = self.livros[index]

        # Janela de edição
        window = Toplevel(self)
        window.title(f"Editar livro: {livro.titulo}")
        window.geometry("500x550")
        window.grab_set()
        
        # Estilizar a janela
        frame_principal = ctk.CTkFrame(window)
        frame_principal.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Título da janela
        titulo_janela = ctk.CTkLabel(frame_principal, text=f"Editar Livro", font=ctk.CTkFont(size=20, weight="bold"))
        titulo_janela.pack(pady=(20, 30))
        
        # Campos de entrada
        frame_campos = ctk.CTkFrame(frame_principal)
        frame_campos.pack(padx=20, pady=10, fill="x")
        
        # Título
        ctk.CTkLabel(frame_campos, text="Título:", anchor="w").pack(fill="x", pady=(10, 0))
        titulo_input = ctk.CTkEntry(frame_campos, placeholder_text="Título do livro")
        titulo_input.insert(0, livro.titulo)
        titulo_input.pack(fill="x", pady=(0, 10))
        
        # Autor
        ctk.CTkLabel(frame_campos, text="Autor:", anchor="w").pack(fill="x", pady=(10, 0))
        autor_input = ctk.CTkEntry(frame_campos, placeholder_text="Nome do autor")
        autor_input.insert(0, livro.autor)
        autor_input.pack(fill="x", pady=(0, 10))
        
        # Tipo
        ctk.CTkLabel(frame_campos, text="Tipo:", anchor="w").pack(fill="x", pady=(10, 0))
        tipo_input = ctk.CTkComboBox(frame_campos, values=["Físico", "Digital", "E-book", "Audiobook"])
        tipo_input.set(livro.tipo)
        tipo_input.pack(fill="x", pady=(0, 10))
        
        # Status de leitura
        frame_lido = ctk.CTkFrame(frame_campos, fg_color="transparent")
        frame_lido.pack(fill="x", pady=10)
        
        ctk.CTkLabel(frame_lido, text="Status de leitura:", anchor="w").pack(side="left")
        lido_var = ctk.BooleanVar(value=livro.lido)
        lido_check = ctk.CTkCheckBox(frame_lido, text="Lido", variable=lido_var)
        lido_check.pack(side="left", padx=10)
        
        # Avaliação com estrelas
        ctk.CTkLabel(frame_campos, text="Avaliação:", anchor="w").pack(fill="x", pady=(10, 5))
        
        frame_estrelas = ctk.CTkFrame(frame_campos, fg_color="transparent")
        frame_estrelas.pack(fill="x", pady=(0, 10))
        
        nota_var = ctk.IntVar(value=livro.nota)
        
        # Implementaremos a lógica das estrelas em uma função separada
        def selecionar_nota(valor):
            nota_var.set(valor)
            for i in range(1, 6):
                if i <= valor:
                    estrelas_btn[i-1].configure(text="★", font=ctk.CTkFont(size=24))
                else:
                    estrelas_btn[i-1].configure(text="☆", font=ctk.CTkFont(size=24))
        
        estrelas_btn = []
        for i in range(1, 6):
            btn = ctk.CTkButton(
                frame_estrelas, 
                text="☆" if i > livro.nota else "★", 
                width=30, 
                height=30, 
                corner_radius=15,
                font=ctk.CTkFont(size=24),
                command=lambda v=i: selecionar_nota(v),
                fg_color="transparent", 
                hover_color="#e0e0e0",
                text_color="#FFD700"
            )
            btn.pack(side="left", padx=2)
            estrelas_btn.append(btn)
            
        # Seleção de imagem
        ctk.CTkLabel(frame_campos, text="Imagem da capa:", anchor="w").pack(fill="x", pady=(20, 5))
        
        frame_imagem = ctk.CTkFrame(frame_campos)
        frame_imagem.pack(fill="x", pady=(0, 10))
        
        imagem_path_var = ctk.StringVar(value=livro.imagem_path if livro.imagem_path else "")
        label_imagem = ctk.CTkLabel(
            frame_imagem, 
            text=os.path.basename(imagem_path_var.get()) if imagem_path_var.get() else "Nenhuma imagem selecionada"
        )
        label_imagem.pack(side="left", padx=10, fill="x", expand=True)
        
        def selecionar_nova_imagem():
            path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
            if path:
                imagem_path_var.set(path)
                label_imagem.configure(text=os.path.basename(path))
        
        btn_imagem = ctk.CTkButton(frame_imagem, text="Selecionar", command=selecionar_nova_imagem)
        btn_imagem.pack(side="right", padx=10)
        
        # Botões de ação
        frame_acoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_acoes.pack(pady=20, fill="x")
        
        def salvar_modificacoes():
            livro.titulo = titulo_input.get()
            livro.autor = autor_input.get()
            livro.lido = lido_var.get()
            livro.nota = nota_var.get()
            livro.tipo = tipo_input.get()
            livro.imagem_path = imagem_path_var.get() if imagem_path_var.get() else None
            self.salvar_livros()
            self.atualizar_lista()
            window.destroy()
        
        def excluir_livro():
            resposta = messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente excluir o livro '{livro.titulo}'?")
            if resposta:
                del self.livros[index]
                self.salvar_livros()
                self.atualizar_lista()
                window.destroy()
        
        frame_botoes = ctk.CTkFrame(frame_acoes, fg_color="transparent")
        frame_botoes.pack(side="left", expand=True, fill="x")
        
        btn_cancelar = ctk.CTkButton(
            frame_botoes, 
            text="Cancelar", 
            fg_color="#f0f0f0", 
            text_color="black",
            hover_color="#e0e0e0",
            command=window.destroy
        )
        btn_cancelar.pack(side="left", padx=5, expand=True, fill="x")
        
        btn_salvar = ctk.CTkButton(
            frame_botoes, 
            text="Salvar", 
            command=salvar_modificacoes
        )
        btn_salvar.pack(side="left", padx=5, expand=True, fill="x")
        
        # Botão de excluir separado
        btn_excluir = ctk.CTkButton(
            frame_acoes, 
            text="Excluir Livro", 
            fg_color="#FF5555", 
            hover_color="#FF0000",
            command=excluir_livro
        )
        btn_excluir.pack(side="right", padx=20)

    def atualizar_lista(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.imagem_refs.clear()

        if not self.livros:
            # Mensagem quando não há livros
            msg_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
            msg_frame.pack(fill="both", expand=True, padx=20, pady=50)
            
            msg = ctk.CTkLabel(
                msg_frame, 
                text="Sua biblioteca está vazia.\nClique em 'Adicionar Livro' para começar!",
                font=ctk.CTkFont(size=16),
                justify="center"
            )
            msg.pack(pady=50)
            return

        for idx, livro in enumerate(self.livros):
            frame_item = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
            frame_item.pack(fill="x", padx=10, pady=8)

            # Imagem do livro (thumbnail)
            if livro.imagem_path and os.path.exists(livro.imagem_path):
                try:
                    img = Image.open(livro.imagem_path).convert("RGBA")
                    img.thumbnail((80, 120), Image.LANCZOS)
                    photo = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                    self.imagem_refs[idx] = photo
                    label_img = ctk.CTkLabel(frame_item, image=photo, text=None)
                    label_img.pack(side="left", padx=10, pady=10)
                except Exception as e:
                    print(f"Erro ao carregar imagem do livro: {e}")
                    spacer = ctk.CTkLabel(frame_item, width=80)
                    spacer.pack(side="left", padx=10, pady=10)
            else:
                spacer = ctk.CTkLabel(frame_item, width=80)
                spacer.pack(side="left", padx=10, pady=10)

            # Texto do livro (título, autor, status)
            texto_frame = ctk.CTkFrame(frame_item, fg_color="transparent")
            texto_frame.pack(side="left", fill="both", expand=True, padx=5, pady=10)

            label_titulo = ctk.CTkLabel(texto_frame, text=livro.titulo, font=ctk.CTkFont(size=16, weight="bold"), anchor="w")
            label_titulo.pack(fill="x")

            label_autor = ctk.CTkLabel(texto_frame, text=f"Autor: {livro.autor}", font=ctk.CTkFont(size=12), anchor="w")
            label_autor.pack(fill="x", pady=(4, 0))
            
            # Exibir estrelas para a nota
            estrelas_frame = ctk.CTkFrame(texto_frame, fg_color="transparent")
            estrelas_frame.pack(fill="x", pady=(4, 0))
            
            nota_texto = "".join(["★" if i < livro.nota else "☆" for i in range(5)])
            label_estrelas = ctk.CTkLabel(
                estrelas_frame, 
                text=nota_texto, 
                font=ctk.CTkFont(size=14),
                text_color="#FFD700",
                anchor="w"
            )
            label_estrelas.pack(side="left")

            label_status = ctk.CTkLabel(texto_frame, text=f"Lido: {'✔️' if livro.lido else '❌'} | Tipo: {livro.tipo}", font=ctk.CTkFont(size=12), anchor="w")
            label_status.pack(fill="x", pady=(4, 0))

            # Botão Editar no canto direito
            btn_editar = ctk.CTkButton(frame_item, text="Editar", width=60, command=lambda i=idx: self.abrir_edicao(i))
            btn_editar.pack(side="right", padx=10, pady=10)

    def salvar_livros(self):
        with open("biblioteca.json", "w", encoding="utf-8") as f:
            json.dump([livro.to_dict() for livro in self.livros], f, ensure_ascii=False, indent=2)

    def load_livros(self):
        if os.path.exists("biblioteca.json"):
            with open("biblioteca.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                for livro_data in dados:
                    if 'tipo' not in livro_data:
                        livro_data['tipo'] = 'Físico'
                self.livros = [Livro(**d) for d in dados]
                self.atualizar_lista()

    def exportar_pdf(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if path:
            from reportlab.lib.units import inch
            c = canvas.Canvas(path, pagesize=letter)
            width, height = letter
            margin = 50
            y = height - margin

            for livro in self.livros:
                if y < 150:
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
                c.drawString(text_x, text_y, livro.titulo)

                c.setFont("Helvetica", 12)
                c.drawString(text_x, text_y - 20, f"Autor: {livro.autor}")

                c.setFont("Helvetica", 11)
                status_text = f"Lido: {'Sim' if livro.lido else 'Não'} | Nota: {livro.nota} | Tipo: {livro.tipo}"
                c.drawString(text_x, text_y - 40, status_text)

                y -= 140  # Espaço entre livros
    
            c.save()

    def exportar_excel(self):
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if path:
            wb = Workbook()
            sheet = wb.active
            sheet.append(["Título", "Autor", "Lido", "Nota", "Tipo", "Imagem"])
            for livro in self.livros:
                sheet.append([livro.titulo, livro.autor, livro.lido, livro.nota, livro.tipo, livro.imagem_path])
            wb.save(path)

    def exportar_word(self):
        path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Files", "*.docx")])
        if path:
            doc = Document()
            for livro in self.livros:
                doc.add_paragraph(f"Título: {livro.titulo}")
                doc.add_paragraph(f"Autor: {livro.autor}")
                doc.add_paragraph(f"Lido: {'Sim' if livro.lido else 'Não'}")
                doc.add_paragraph(f"Nota: {livro.nota}")
                doc.add_paragraph(f"Tipo: {livro.tipo}")
                if livro.imagem_path:
                    doc.add_paragraph(f"Imagem: {livro.imagem_path}")
                doc.add_paragraph("")
            doc.save(path)


if __name__ == "__main__":
    app = BibliotecaApp()
    app.mainloop()
