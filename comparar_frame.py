import tkinter as tk

from componentes import (COR_AZUL, COR_FUNDO, criar_botao, criar_figura_histograma,
                         mostrar_figura, mostrar_imagem)

TAM_IMAGEM = (460, 300)


class FrameComparar(tk.Frame):
    def __init__(self, master, app, original, equalizada, hist_original, hist_equalizada):
        super().__init__(master, bg="#FFFFFF")

        # barra de baixo
        bottom_frame = tk.Frame(self, bg=COR_FUNDO, pady=10)
        bottom_frame.pack(side="bottom", fill="x")
        criar_botao(bottom_frame, "Voltar", app.mostrar_equalizar).pack(side="left", padx=10)

        # grade 2 colunas: [imagem + histograma] da original e da equalizada
        grade = tk.Frame(self, bg=COR_FUNDO)
        grade.pack(expand=True, fill="both", padx=10, pady=10)
        grade.columnconfigure(0, weight=1)
        grade.columnconfigure(1, weight=1)

        itens = [
            ("Imagem original", original, "Histograma original", hist_original),
            ("Imagem equalizada", equalizada, "Histograma equalizado", hist_equalizada),
        ]

        for col, (titulo_img, img, titulo_hist, hist) in enumerate(itens):
            coluna = tk.Frame(grade, bg=COR_FUNDO)
            coluna.grid(row=0, column=col, sticky="nsew")

            tk.Label(coluna, text=titulo_img, bg=COR_FUNDO, fg=COR_AZUL,
                     font=("Arial", 12, "bold")).pack(pady=5)

            lbl = tk.Label(coluna, bg=COR_FUNDO)
            lbl.pack()
            mostrar_imagem(lbl, img, TAM_IMAGEM)

            painel = tk.Frame(coluna, bg=COR_FUNDO)
            painel.pack(expand=True, fill="both")
            mostrar_figura(painel, criar_figura_histograma(hist, titulo_hist, 4.6, 2.8))