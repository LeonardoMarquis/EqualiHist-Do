import tkinter as tk

from processamento import calcular_histograma, especificar_histograma
from componentes import (COR_AZUL, COR_FUNDO, abrir_imagem_cinza, criar_botao,
                         criar_figura_histograma, limpar_figura, limpar_imagem,
                         mostrar_figura, mostrar_imagem)

TAM_IMAGEM = (320, 260)


class FrameEspecificacao(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg="#FFFFFF")
        self.img_original = None
        self.img_referencia = None

        # ===== BARRA DE CIMA =====
        top_frame = tk.Frame(self, bg=COR_FUNDO, pady=10)
        top_frame.pack(fill="x")

        criar_botao(top_frame, "Abrir imagem original", self.abrir_original).pack(side="left", padx=10)
        criar_botao(top_frame, "Abrir imagem de referência", self.abrir_referencia).pack(side="left", padx=10)

        self.btn_especificar = criar_botao(top_frame, "Equalização específica", self.especificar,
                                           estado="disabled", amarelo=True)
        self.btn_especificar.pack(side="left", padx=10)

        # ===== BARRA DE BAIXO =====
        bottom_frame = tk.Frame(self, bg=COR_FUNDO, pady=10)
        bottom_frame.pack(side="bottom", fill="x")
        criar_botao(bottom_frame, "Voltar", app.mostrar_equalizar).pack(side="left", padx=10)

        # ===== GRADE: 3 colunas (original, referência, resultado) =====
        grade = tk.Frame(self, bg=COR_FUNDO)
        grade.pack(expand=True, fill="both", padx=10, pady=10)
        grade.rowconfigure(1, minsize=270)          # evita a tela "pular" quando a imagem carrega
        grade.rowconfigure(2, weight=1)

        titulos = ["Imagem original", "Imagem de referência", "Imagem resultante"]
        self.lbl_imgs = []
        self.pan_hists = []

        for col, titulo in enumerate(titulos):
            grade.columnconfigure(col, weight=1)

            tk.Label(grade, text=titulo, bg=COR_FUNDO, fg=COR_AZUL,
                     font=("Arial", 12, "bold")).grid(row=0, column=col, pady=(5, 0))

            lbl = tk.Label(grade, text="Nenhuma imagem", bg=COR_FUNDO, fg=COR_AZUL)
            lbl.grid(row=1, column=col)
            self.lbl_imgs.append(lbl)

            painel = tk.Frame(grade, bg=COR_FUNDO)
            painel.grid(row=2, column=col, sticky="nsew")
            self.pan_hists.append(painel)

    # ---------- ações ----------
    def abrir_original(self):
        _, img = abrir_imagem_cinza()
        if img is None:
            return
        self.img_original = img
        mostrar_imagem(self.lbl_imgs[0], img, TAM_IMAGEM)
        self.limpar_resultado()

    def abrir_referencia(self):
        _, img = abrir_imagem_cinza()
        if img is None:
            return
        self.img_referencia = img
        mostrar_imagem(self.lbl_imgs[1], img, TAM_IMAGEM)
        self.limpar_resultado()

    def limpar_resultado(self):
        limpar_imagem(self.lbl_imgs[2], "Nenhuma imagem")
        for painel in self.pan_hists:
            limpar_figura(painel)

        pronto = self.img_original is not None and self.img_referencia is not None
        self.btn_especificar.config(state="normal" if pronto else "disabled")

    def especificar(self):
        hist_original = calcular_histograma(self.img_original)
        hist_referencia = calcular_histograma(self.img_referencia)

        resultado = especificar_histograma(self.img_original, hist_original, hist_referencia)
        hist_resultado = calcular_histograma(resultado)

        mostrar_imagem(self.lbl_imgs[2], resultado, TAM_IMAGEM)

        histogramas = [
            (hist_original, "Histograma original"),
            (hist_referencia, "Histograma da referência"),
            (hist_resultado, "Histograma do resultado"),
        ]
        for painel, (hist, titulo) in zip(self.pan_hists, histogramas):
            mostrar_figura(painel, criar_figura_histograma(hist, titulo, 3.4, 2.5))