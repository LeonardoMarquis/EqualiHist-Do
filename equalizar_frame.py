import os
import tkinter as tk
from tkinter import messagebox

from processamento import calcular_histograma, equalizar
from componentes import (COR_AZUL, COR_FUNDO, PASTA_OUTPUT, abrir_imagem_cinza,
                         criar_botao, criar_figura_histograma, limpar_figura,
                         mostrar_figura, mostrar_imagem)

TAM_IMAGEM = (400, 500)


class FrameEqualizar(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg="#FFFFFF")
        self.app = app

        self.original_path = None
        self.original_image = None
        self.equalized_image = None
        self.hist_original = None
        self.hist_equalized = None

        self.build_screen()

    def build_screen(self):
        # ===== BARRA DE CIMA =====
        top_frame = tk.Frame(self, bg=COR_FUNDO, pady=10)
        top_frame.pack(fill="x")

        criar_botao(top_frame, "Abrir imagem", self.local_search).pack(side="left", padx=10)

        self.save_btn = criar_botao(top_frame, "Salvar (pasta output)", self.disk_save,
                                    estado="disabled", amarelo=True)
        self.save_btn.pack(side="right", padx=10)

        # ===== BARRA DE BAIXO (criada antes para reservar o espaço) =====
        bottom_frame = tk.Frame(self, bg=COR_FUNDO, pady=10)
        bottom_frame.pack(side="bottom", fill="x")

        self.next_btn = criar_botao(bottom_frame, "Equalização Específica", self.app.mostrar_especificacao)
        self.next_btn.pack(side="right", padx=10)

        self.compare_btn = criar_botao(bottom_frame, "Comparar", self.comparar,
                                       estado="disabled", amarelo=True)
        self.compare_btn.pack(side="right", padx=10)

        # ===== ÁREA PRINCIPAL =====
        main_frame = tk.Frame(self, bg="#FFFFFF")
        main_frame.pack(expand=True, fill="both")

        # ===== BARRA LATERAL =====
        sidebar = tk.Frame(main_frame, width=200, bg="#F5F5F5", padx=10, pady=10)
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar, text="Passos", font=("Arial", 13, "bold"),
                 bg="#F5F5F5", fg=COR_AZUL).pack(pady=10)

        self.hist_btn = criar_botao(sidebar, "Gerar histograma", self.generate_histogram,
                                    estado="disabled", width=18)
        self.hist_btn.pack(pady=10)

        self.equalize_btn = criar_botao(sidebar, "Equalizar", self.equalize,
                                        estado="disabled", width=18)
        self.equalize_btn.pack(pady=10)

        # ===== IMAGEM + HISTOGRAMA =====
        image_frame = tk.Frame(main_frame, bg=COR_FUNDO)
        image_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        panel_img = tk.Frame(image_frame, bg=COR_FUNDO)
        panel_img.pack(side="left", expand=True, fill="both")

        self.lbl_titulo = tk.Label(panel_img, text="", bg=COR_FUNDO, fg=COR_AZUL,
                                   font=("Arial", 12, "bold"))
        self.lbl_titulo.pack(pady=5)

        self.lbl_imagem = tk.Label(panel_img, text="Nenhuma imagem carregada",
                                   bg=COR_FUNDO, fg=COR_AZUL, font=("Arial", 14))
        self.lbl_imagem.pack(expand=True)

        self.panel_hist = tk.Frame(image_frame, bg=COR_FUNDO)
        self.panel_hist.pack(side="left", expand=True, fill="both")
        self.clear_histogram_area()

    def clear_histogram_area(self):
        limpar_figura(self.panel_hist)
        tk.Label(self.panel_hist, text="O histograma aparece aqui", bg=COR_FUNDO,
                 fg=COR_AZUL, font=("Arial", 12)).pack(expand=True)

    # ---------- ações ----------
    def local_search(self):
        caminho, img = abrir_imagem_cinza()
        if img is None:
            return

        self.original_path = caminho
        self.original_image = img
        self.equalized_image = None
        self.hist_original = None
        self.hist_equalized = None

        self.lbl_titulo.configure(text="Imagem original")
        mostrar_imagem(self.lbl_imagem, img, TAM_IMAGEM)
        self.clear_histogram_area()

        self.hist_btn.config(state="normal")
        self.equalize_btn.config(state="disabled")
        self.save_btn.config(state="disabled")
        self.compare_btn.config(state="disabled")


    def generate_histogram(self):
        self.hist_original = calcular_histograma(self.original_image)
        mostrar_figura(self.panel_hist,
                       criar_figura_histograma(self.hist_original, "Histograma original"))
        self.hist_btn.config(state="disabled")
        self.equalize_btn.config(state="normal")

    def equalize(self):
        self.equalized_image = equalizar(self.original_image, self.hist_original)
        self.hist_equalized = calcular_histograma(self.equalized_image)

        # a equalizada ocupa o lugar da original
        self.lbl_titulo.configure(text="Imagem equalizada")
        mostrar_imagem(self.lbl_imagem, self.equalized_image, TAM_IMAGEM)
        mostrar_figura(self.panel_hist,
                       criar_figura_histograma(self.hist_equalized, "Histograma equalizado"))

        self.equalize_btn.config(state="disabled")
        self.save_btn.config(state="normal")
        self.compare_btn.config(state="normal")


    def comparar(self):
        self.app.mostrar_comparar(self.original_image, self.equalized_image,
                                  self.hist_original, self.hist_equalized)

    def disk_save(self):
        os.makedirs(PASTA_OUTPUT, exist_ok=True)
        base = os.path.splitext(os.path.basename(self.original_path))[0]

        self.original_image.save(os.path.join(PASTA_OUTPUT, f"{base}_original.png"))
        self.equalized_image.save(os.path.join(PASTA_OUTPUT, f"{base}_equalizada.png"))

        criar_figura_histograma(self.hist_original, "Histograma original").savefig(
            os.path.join(PASTA_OUTPUT, f"{base}_histograma_original.png"))
        criar_figura_histograma(self.hist_equalized, "Histograma equalizado").savefig(
            os.path.join(PASTA_OUTPUT, f"{base}_histograma_equalizado.png"))

        messagebox.showinfo("Salvo", f"4 arquivos salvos em:\n{PASTA_OUTPUT}")