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
        # Entradas de dados para adicionar livros
        frame_inputs = ctk.CTkFrame(self)
        frame_inputs.pack(pady=10, padx=10, fill="x")

        self.titulo_input = ctk.CTkEntry(frame_inputs, placeholder_text="Título")
        self.titulo_input.pack(side="left", padx=5, fill="x", expand=True)

        self.autor_input = ctk.CTkEntry(frame_inputs, placeholder_text="Autor")
        self.autor_input.pack(side="left", padx=5, fill="x", expand=True)

        self.lido_check = ctk.CTkCheckBox(frame_inputs, text="Lido")
        self.lido_check.pack(side="left", padx=5)

        self.nota_input = ctk.CTkSlider(frame_inputs, from_=0, to=5, number_of_steps=5)
        self.nota_input.pack(side="left", padx=5)
        self.nota_input.set(0)

        self.tipo_input = ctk.CTkComboBox(frame_inputs, values=["Físico", "Digital"])
        self.tipo_input.pack(side="left", padx=5)
        self.tipo_input.set("Físico")

        self.imagem_button = ctk.CTkButton(frame_inputs, text="Selecionar Imagem", command=self.selecionar_imagem)
        self.imagem_button.pack(side="left", padx=5)

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

        # Botão de adicionar livro
        frame_botoes = ctk.CTkFrame(self)
        frame_botoes.pack(pady=10)

        ctk.CTkButton(frame_botoes, text="Adicionar", command=self.adicionar_livro).pack(side="left", padx=10)
        ctk.CTkButton(frame_botoes, text="Exportar PDF", command=self.exportar_pdf).pack(side="left", padx=10)
        ctk.CTkButton(frame_botoes, text="Exportar Excel", command=self.exportar_excel).pack(side="left", padx=10)
        ctk.CTkButton(frame_botoes, text="Exportar Word", command=self.exportar_word).pack(side="left", padx=10)

    def selecionar_imagem(self):
        caminho_imagem = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if caminho_imagem:
            self.imagem_path = caminho_imagem

    def adicionar_livro(self):
        titulo = self.titulo_input.get()
        autor = self.autor_input.get()
        lido = self.lido_check.get()
        nota = int(self.nota_input.get())
        tipo = self.tipo_input.get()

        if not titulo or not autor:
            messagebox.showwarning("Erro", "Título e autor são obrigatórios.")
            return

        livro = Livro(titulo, autor, lido, nota, tipo, self.imagem_path)
        self.livros.append(livro)
        self.salvar_livros()
        self.atualizar_lista()
        self.limpar_inputs()

    def limpar_inputs(self):
        self.titulo_input.delete(0, "end")
        self.autor_input.delete(0, "end")
        self.lido_check.deselect()
        self.nota_input.set(0)
        self.tipo_input.set("Físico")
        self.imagem_path = None

    def atualizar_lista(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.imagem_refs.clear()

        for idx, livro in enumerate(self.livros):
            frame_item = ctk.CTkFrame(self.scrollable_frame, corner_radius=8)
            frame_item.pack(fill="x", padx=5, pady=5)

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

            label_status = ctk.CTkLabel(texto_frame, text=f"Lido: {'✔️' if livro.lido else '❌'} | Nota: {livro.nota} | Tipo: {livro.tipo}", font=ctk.CTkFont(size=12), anchor="w")
            label_status.pack(fill="x", pady=(4, 0))

            # Botão Editar no canto direito
            btn_editar = ctk.CTkButton(frame_item, text="Editar", width=60, command=lambda i=idx: self.abrir_edicao(i))
            btn_editar.pack(side="right", padx=10, pady=10)

    def abrir_edicao(self, index):
        livro = self.livros[index]

        # Janela de edição
        window = Toplevel(self)
        window.title(f"Editar livro: {livro.titulo}")
        window.geometry("400x400")
        window.grab_set()

        # Entradas para edição
        titulo_input = ctk.CTkEntry(window)
        titulo_input.insert(0, livro.titulo)
        titulo_input.pack(padx=10, pady=5, fill="x")

        autor_input = ctk.CTkEntry(window)
        autor_input.insert(0, livro.autor)
        autor_input.pack(padx=10, pady=5, fill="x")

        lido_var = ctk.BooleanVar(value=livro.lido)
        lido_check = ctk.CTkCheckBox(window, text="Lido", variable=lido_var)
        lido_check.pack(padx=10, pady=5)

        nota_slider = ctk.CTkSlider(window, from_=0, to=5, number_of_steps=5)
        nota_slider.set(livro.nota)
        nota_slider.pack(padx=10, pady=5, fill="x")

        tipo_combo = ctk.CTkComboBox(window, values=["Físico", "Digital"])
        tipo_combo.set(livro.tipo)
        tipo_combo.pack(padx=10, pady=5)

        imagem_path_var = ctk.StringVar(value=livro.imagem_path if livro.imagem_path else "")

        def selecionar_nova_imagem():
            path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
            if path:
                imagem_path_var.set(path)
                label_imagem.config(text=os.path.basename(path))

        ctk.CTkButton(window, text="Selecionar Nova Imagem", command=selecionar_nova_imagem).pack(padx=10, pady=5)
        label_imagem = ctk.CTkLabel(window, text=os.path.basename(imagem_path_var.get()) if imagem_path_var.get() else "Nenhuma imagem selecionada")
        label_imagem.pack(padx=10, pady=5)

        def salvar_modificacoes():
            livro.titulo = titulo_input.get()
            livro.autor = autor_input.get()
            livro.lido = lido_var.get()
            livro.nota = int(nota_slider.get())
            livro.tipo = tipo_combo.get()
            livro.imagem_path = imagem_path_var.get() if imagem_path_var.get() else None
            self.salvar_livros()
            self.atualizar_lista()
            window.destroy()

        btn_salvar = ctk.CTkButton(window, text="Salvar", command=salvar_modificacoes)
        btn_salvar.pack(padx=10, pady=15)

        def excluir_livro():
            resposta = messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente excluir o livro '{livro.titulo}'?")
            if resposta:
                del self.livros[index]
                self.salvar_livros()
                self.atualizar_lista()
                window.destroy()

        btn_excluir = ctk.CTkButton(window, text="Excluir", fg_color="red", hover_color="#cc0000", command=excluir_livro)
        btn_excluir.pack(padx=10, pady=5)


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
