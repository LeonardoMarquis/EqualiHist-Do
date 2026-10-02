import os
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from processamento import calcular_histograma, equalizar

PASTA_OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def criar_figura_histograma(hist, titulo):
    fig = Figure(figsize=(4.2, 3.4), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(range(256), hist, width=1.0, color="#1E90FF")
    ax.set_title(titulo)
    ax.set_xlabel("Intensidade (0-255)")
    ax.set_ylabel("Nº de pixels")
    ax.set_xlim(0, 255)
    fig.tight_layout()
    return fig


class ImageEqualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Equalizador de Imagens em Escala de Cinza")
        self.root.geometry("1150x750")
        self.root.configure(bg="#FFFFFF")

        self.original_path = None
        self.original_image = None
        self.equalized_image = None
        self.hist_original = None
        self.hist_equalized = None

        self.build_screen()

    def build_screen(self):
        # ===== BARRA DE CIMA =====
        top_frame = tk.Frame(self.root, bg="#EAF2FF", pady=10)
        top_frame.pack(fill="x")

        tk.Button(
            top_frame, text="Abrir imagem", command=self.local_search,
            bg="#1E90FF", fg="white", activebackground="#1873CC", relief="flat"
        ).pack(side="left", padx=10)

        self.save_btn = tk.Button(
            top_frame, text="Salvar (pasta output)", command=self.disk_save,
            state="disabled", bg="#FFF3B0", fg="#333333", relief="flat"
        )
        self.save_btn.pack(side="right", padx=10)

        # ===== BARRA DE BAIXO (criada antes para reservar o espaço) =====
        bottom_frame = tk.Frame(self.root, bg="#EAF2FF", pady=10)
        bottom_frame.pack(side="bottom", fill="x")

        self.next_btn = tk.Button(
            bottom_frame, text="Próximo (Passo 3)", command=self.next_step,
            state="disabled", bg="#1E90FF", fg="white",
            activebackground="#1873CC", relief="flat"
        )
        self.next_btn.pack(side="right", padx=10)

        # ===== ÁREA PRINCIPAL =====
        main_frame = tk.Frame(self.root, bg="#FFFFFF")
        main_frame.pack(expand=True, fill="both")

        # ===== BARRA LATERAL =====
        sidebar = tk.Frame(main_frame, width=200, bg="#F5F5F5", padx=10, pady=10)
        sidebar.pack(side="left", fill="y")

        tk.Label(
            sidebar, text="Passos", font=("Arial", 13, "bold"),
            bg="#F5F5F5", fg="#1E90FF"
        ).pack(pady=10)

        self.hist_btn = tk.Button(
            sidebar, text="Gerar histograma", command=self.generate_histogram,
            state="disabled", bg="#1E90FF", fg="white",
            activebackground="#1873CC", relief="flat", width=18
        )
        self.hist_btn.pack(pady=10)

        self.equalize_btn = tk.Button(
            sidebar, text="Equalizar", command=self.equalize,
            state="disabled", bg="#1E90FF", fg="white",
            activebackground="#1873CC", relief="flat", width=18
        )
        self.equalize_btn.pack(pady=10)

        # ===== ÁREA DA IMAGEM + HISTOGRAMA =====
        image_frame = tk.Frame(main_frame, bg="#EAF2FF")
        image_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        # lado esquerdo: imagem
        self.panel_img = tk.Frame(image_frame, bg="#EAF2FF")
        self.panel_img.pack(side="left", expand=True, fill="both")

        self.lbl_titulo = tk.Label(
            self.panel_img, text="", bg="#EAF2FF", fg="#1E90FF",
            font=("Arial", 12, "bold")
        )
        self.lbl_titulo.pack(pady=5)

        self.lbl_imagem = tk.Label(
            self.panel_img, text="Nenhuma imagem carregada",
            bg="#EAF2FF", fg="#1E90FF", font=("Arial", 14)
        )
        self.lbl_imagem.pack(expand=True)

        # lado direito: histograma
        self.panel_hist = tk.Frame(image_frame, bg="#EAF2FF")
        self.panel_hist.pack(side="left", expand=True, fill="both")
        self.clear_histogram_area()

    # ---------- exibição ----------
    def display_on_screen(self, pil_image, titulo):
        img_copy = pil_image.copy()
        img_copy.thumbnail((400, 500))          # só para exibir

        img_tk = ImageTk.PhotoImage(img_copy)
        self.lbl_titulo.configure(text=titulo)
        self.lbl_imagem.configure(image=img_tk, text="")
        self.lbl_imagem.image = img_tk          # guarda a referência

    def clear_histogram_area(self):
        for widget in self.panel_hist.winfo_children():
            widget.destroy()
        tk.Label(
            self.panel_hist, text="O histograma aparece aqui",
            bg="#EAF2FF", fg="#1E90FF", font=("Arial", 12)
        ).pack(expand=True)

    def show_histogram(self, fig):
        for widget in self.panel_hist.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.panel_hist)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

    # ---------- ações ----------
    def local_search(self):
        path = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp")]
        )
        if path:
            self.load_image(path)

    def load_image(self, path):
        try:
            img = Image.open(path).convert("L")     # escala de cinza, 0 a 255
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a imagem: {e}")
            return

        self.original_path = path
        self.original_image = img
        self.equalized_image = None
        self.hist_original = None
        self.hist_equalized = None

        self.display_on_screen(img, "Imagem original")
        self.clear_histogram_area()

        self.hist_btn.config(state="normal")
        self.equalize_btn.config(state="disabled")
        self.save_btn.config(state="disabled")
        self.next_btn.config(state="disabled")

    def generate_histogram(self):
        self.hist_original = calcular_histograma(self.original_image)
        self.show_histogram(
            criar_figura_histograma(self.hist_original, "Histograma original")
        )
        self.hist_btn.config(state="disabled")
        self.equalize_btn.config(state="normal")

    def equalize(self):
        self.equalized_image = equalizar(self.original_image, self.hist_original)
        self.hist_equalized = calcular_histograma(self.equalized_image)

        # a equalizada ocupa o lugar da original
        self.display_on_screen(self.equalized_image, "Imagem equalizada")
        self.show_histogram(
            criar_figura_histograma(self.hist_equalized, "Histograma equalizado")
        )

        self.equalize_btn.config(state="disabled")
        self.save_btn.config(state="normal")
        self.next_btn.config(state="normal")

    def disk_save(self):
        if self.equalized_image is None:
            return

        os.makedirs(PASTA_OUTPUT, exist_ok=True)
        base = os.path.splitext(os.path.basename(self.original_path))[0]

        self.original_image.save(os.path.join(PASTA_OUTPUT, f"{base}_original.png"))
        self.equalized_image.save(os.path.join(PASTA_OUTPUT, f"{base}_equalizada.png"))

        criar_figura_histograma(self.hist_original, "Histograma original").savefig(
            os.path.join(PASTA_OUTPUT, f"{base}_histograma_original.png")
        )
        criar_figura_histograma(self.hist_equalized, "Histograma equalizado").savefig(
            os.path.join(PASTA_OUTPUT, f"{base}_histograma_equalizado.png")
        )

        messagebox.showinfo("Salvo", f"4 arquivos salvos em:\n{PASTA_OUTPUT}")

    def next_step(self):
        # TODO: abrir a tela do passo 3 (especificação do histograma)
        messagebox.showinfo("Passo 3", "Tela do passo 3 ainda não implementada.")