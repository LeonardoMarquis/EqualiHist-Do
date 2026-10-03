import os
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

COR_FUNDO = "#E7EBF1"
COR_DETALHE = "#009797"
COR_DETALHE2 = "#000000"

PASTA_OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")



# alterando a classe botao

class Botao(tk.Button):
    def __init__(self, parent, texto, comando, estado="normal", amarelo=False, width=None):
        if amarelo:
            self._normal = ("#FFF3B0", "#1F1E1E")      # (fundo, texto)
            self._ativo = "#E6D98A"                    # fundo ao clicar
            self._desab = ("#A89B4A", "#2B2B2B")       # desabilitado: mais escuro
        else:
            self._normal = (COR_DETALHE, "white")
            self._ativo = "#007A7A"
            self._desab = ("#005252", "#BDBDBD")

        opcoes = dict(text=texto, command=comando, relief="flat")
        if width:
            opcoes["width"] = width
        super().__init__(parent, **opcoes)
        self._aplicar_estado(estado)

    def _aplicar_estado(self, estado):
        bg, fg = self._desab if estado == "disabled" else self._normal
        tk.Button.configure(self, state=estado, bg=bg, fg=fg,
                            disabledforeground=fg, activebackground=self._ativo)

    def configure(self, cnf=None, **kw):
        estado = kw.pop("state", None)
        resultado = super().configure(cnf, **kw)
        if estado is not None:
            self._aplicar_estado(estado)
        return resultado

    config = configure      # sem isso o .config(state=) nao iria mudar a cor do botao



def criar_botao(parent, texto, comando, estado="normal", amarelo=False, width=None):
    return Botao(parent, texto, comando, estado, amarelo, width)


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
    ax.bar(range(256), hist, width=1.0, color=COR_DETALHE)
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