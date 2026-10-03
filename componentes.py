import os
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

COR_FUNDO = "#EAF2FF"
COR_AZUL = "#1E90FF"
PASTA_OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def criar_botao(parent, texto, comando, estado="normal", amarelo=False, width=None):
    bg, fg, ativo = ("#FFF3B0", "#333333", "#E6D98A") if amarelo else (COR_AZUL, "white", "#1873CC")
    opcoes = dict(text=texto, command=comando, state=estado, bg=bg, fg=fg,
                  activebackground=ativo, relief="flat")
    if width:
        opcoes["width"] = width
    return tk.Button(parent, **opcoes)


def abrir_imagem_cinza():
    """Abre o seletor de arquivo. Retorna (caminho, imagem PIL em cinza) ou (None, None)."""
    caminho = filedialog.askopenfilename(
        filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp")]
    )
    if not caminho:
        return None, None
    try:
        return caminho, Image.open(caminho).convert("L")   # escala de cinza, 0 a 255
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível abrir a imagem: {e}")
        return None, None


def mostrar_imagem(label, pil_image, tamanho):
    copia = pil_image.copy()
    copia.thumbnail(tamanho)                     # só para exibir
    img_tk = ImageTk.PhotoImage(copia)
    label.configure(image=img_tk, text="")
    label.image = img_tk                         # guarda a referência


def limpar_imagem(label, texto):
    label.configure(image="", text=texto)
    label.image = None


def criar_figura_histograma(hist, titulo, largura=4.2, altura=3.4):
    fig = Figure(figsize=(largura, altura), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(range(256), hist, width=1.0, color=COR_AZUL)
    ax.set_title(titulo)
    ax.set_xlabel("Intensidade (0-255)")
    ax.set_ylabel("Nº de pixels")
    ax.set_xlim(0, 255)
    fig.tight_layout()
    return fig


def limpar_figura(parent):
    for widget in parent.winfo_children():
        widget.destroy()


def mostrar_figura(parent, fig):
    limpar_figura(parent)
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill="both")