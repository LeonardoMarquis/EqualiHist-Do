# necessita pip install pillow numpy matplotlib
# use pip install -r requirements.txt
import tkinter as tk
from equalizar_frame import FrameEqualizar
from comparar_frame import FrameComparar
from especificacao_frame import FrameEspecificacao
import ctypes

myappid = 'dokizax.equalihistdo.tkinter.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class App:
    def __init__(self, root):
        self.root = root
        root.title("Equalizador de Imagens em Escala de Cinza")
        root.geometry("1200x800")
        root.configure(bg="#FFFFFF")

        self.tela_atual = None
        self.tela_equalizar = FrameEqualizar(root, self)
        self.tela_comparar = None
        self.tela_especificacao = None

        self._trocar(self.tela_equalizar)

    def _trocar(self, tela):
        if self.tela_atual is not None:
            self.tela_atual.pack_forget()
        self.tela_atual = tela
        tela.pack(expand=True, fill="both")

    def mostrar_equalizar(self):
        self._trocar(self.tela_equalizar)

    def mostrar_comparar(self, original, equalizada, hist_original, hist_equalizada):
        if self.tela_comparar is not None:
            self.tela_comparar.destroy()
        self.tela_comparar = FrameComparar(self.root, self, original, equalizada,
                                          hist_original, hist_equalizada)
        self._trocar(self.tela_comparar)

    def mostrar_especificacao(self):
        if self.tela_especificacao is None:
            self.tela_especificacao = FrameEspecificacao(self.root, self)
        self._trocar(self.tela_especificacao)


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("assets/grace_s_icon.ico")  
    app = App(root)
    root.mainloop()
    