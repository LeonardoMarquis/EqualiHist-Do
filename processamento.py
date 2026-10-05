import numpy as np
from PIL import Image


def calcular_histograma(img):
    """Recebe imagem PIL em escala de cinza e retorna array com 256 posições"""
    pixels = np.array(img)
    return np.bincount(pixels.flatten(), minlength=256)


def equalizar(img, hist):
    """Equalização: s_k = round(255 * CDF[k]). E retorna uma nova imagem PIL"""
    total = hist.sum()
    cdf = np.cumsum(hist)
    mapa = np.round(255 * cdf / total).astype(np.uint8)

    pixels = np.array(img)
    return Image.fromarray(mapa[pixels])


def especificar_histograma(img, hist_img, hist_ref):
    """
    Especificação de histograma: transforma a distribuição de 'img'
    na distribuição da imagem de referência
    Para cada nível r da imagem, procura o menor nível z da referência
    cujo CDF seja >= ao CDF de r
    """
    cdf_img = np.cumsum(hist_img) / hist_img.sum()
    cdf_ref = np.cumsum(hist_ref) / hist_ref.sum()

    mapa = np.searchsorted(cdf_ref, cdf_img, side="left")
    mapa = np.clip(mapa, 0, 255).astype(np.uint8)

    pixels = np.array(img)
    return Image.fromarray(mapa[pixels])
