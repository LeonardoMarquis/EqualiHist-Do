import os
import tkinter as tk
from tkinter import messagebox

from processamento import calcular_histograma, especificar_histograma
from componentes import (COR_DETALHE, COR_DETALHE2, COR_FUNDO, PASTA_OUTPUT, abrir_imagem_cinza, criar_botao,
                         criar_figura_histograma, limpar_figura, limpar_imagem,
                         mostrar_figura, mostrar_imagem)

TAM_IMAGEM = (320, 260)


class FrameEspecificacao(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg="#FFFFFF")
        self.original_image = None
        self.referencia_image = None

        # BARRA DE CIMA
        top_frame = tk.Frame(self, bg=COR_FUNDO, pady=10)
        top_frame.pack(fill="x")

        criar_botao(top_frame, "Abrir imagem original", self.abrir_original).pack(side="left", padx=10)
        criar_botao(top_frame, "Abrir imagem de referência", self.abrir_referencia).pack(side="left", padx=10)


        self.save_btn = criar_botao(top_frame, "Salvar", self.disk_save, estado="disabled", amarelo=True)

        self.save_btn.pack(side="right", padx=10)

        # BARRA DE BAIXO
        bottom_frame = tk.Frame(self, bg=COR_FUNDO, pady=10)
        bottom_frame.pack(side="bottom", fill="x")
        criar_botao(bottom_frame, "Voltar", app.mostrar_equalizar).pack(side="left", padx=10)


        self.btn_especificar = criar_botao(bottom_frame, "Equalização específica", self.especificar, estado="disabled", amarelo=True)

        self.btn_especificar.pack(side="right", padx=10)


        # GRADE: 3 colunas (original, referência, resultado)
        grade = tk.Frame(self, bg=COR_FUNDO)
        grade.pack(expand=True, fill="both", padx=10, pady=10)
        grade.rowconfigure(1, minsize=270)          # evita a tela "pular" quando a imagem carrega
        grade.rowconfigure(2, weight=1)

        titulos = ["Imagem original", "Imagem de referência", "Imagem resultante"]
        self.lbl_imgs = []
        self.pan_hists = []

        for col, titulo in enumerate(titulos):
            grade.columnconfigure(col, weight=1)

            tk.Label(grade, text=titulo, bg=COR_FUNDO, fg=COR_DETALHE2, font=("Arial", 12, "bold")).grid(row=0, column=col, pady=(5, 0))

            lbl = tk.Label(grade, text="Nenhuma imagem", bg=COR_FUNDO, fg=COR_DETALHE2)
            lbl.grid(row=1, column=col)
            self.lbl_imgs.append(lbl)

            painel = tk.Frame(grade, bg=COR_FUNDO)
            painel.grid(row=2, column=col, sticky="nsew")
            self.pan_hists.append(painel)



    # ---------- ações ----------
    def abrir_original(self):
        caminho, img = abrir_imagem_cinza()
        if img is None:
            return
        
        self.original_path = caminho
        self.original_image = img
        mostrar_imagem(self.lbl_imgs[0], img, TAM_IMAGEM)
        self.limpar_resultado()

    def abrir_referencia(self):
        caminho_ref, img = abrir_imagem_cinza()
        if img is None:
            return
        
        self.referencia_path = caminho_ref
        self.referencia_image = img
        mostrar_imagem(self.lbl_imgs[1], img, TAM_IMAGEM)
        self.limpar_resultado()

    def limpar_resultado(self):
        limpar_imagem(self.lbl_imgs[2], "Nenhuma imagem")
        for painel in self.pan_hists:
            limpar_figura(painel)

        pronto = self.original_image is not None and self.referencia_image is not None
        self.btn_especificar.config(state="normal" if pronto else "disabled")

    def especificar(self):
        self.hist_original = calcular_histograma(self.original_image)
        self.hist_referencia = calcular_histograma(self.referencia_image)

        self.equalized_image = especificar_histograma(self.original_image, self.hist_original, self.hist_referencia)
        self.hist_equalized = calcular_histograma(self.equalized_image)

        mostrar_imagem(self.lbl_imgs[2], self.equalized_image, TAM_IMAGEM)

        histogramas = [
            (self.hist_original, "Histograma original"),
            (self.hist_referencia, "Histograma da referência"),
            (self.hist_equalized, "Histograma do resultado"),
        ]
        for painel, (hist, titulo) in zip(self.pan_hists, histogramas):
            mostrar_figura(painel, criar_figura_histograma(hist, titulo, 3.4, 2.5))




        self.save_btn.config(state="normal")

    
    def disk_save(self):
        os.makedirs(PASTA_OUTPUT, exist_ok=True)
        base = os.path.splitext(os.path.basename(self.original_path))[0]

        self.original_image.save(os.path.join(PASTA_OUTPUT, f"{base}_original_eq_es.png"))
        self.referencia_image.save(os.path.join(PASTA_OUTPUT, f"{base}_referencia_eq_es.png"))
        self.equalized_image.save(os.path.join(PASTA_OUTPUT, f"{base}_equalizada_eq_es.png"))


        criar_figura_histograma(self.hist_original, "Histograma original").savefig(
            os.path.join(PASTA_OUTPUT, f"{base}_histograma_original_eq_es.png"))
        criar_figura_histograma(self.hist_referencia, "Histograma da referência").savefig(
            os.path.join(PASTA_OUTPUT, f"{base}_histograma_referencia_eq_es.png"))
        criar_figura_histograma(self.hist_equalized, "Histograma equalizado").savefig(
            os.path.join(PASTA_OUTPUT, f"{base}_histograma_equalizado_eq_es.png"))

        messagebox.showinfo("Salvo", f"6 arquivos salvos em:\n{PASTA_OUTPUT}")