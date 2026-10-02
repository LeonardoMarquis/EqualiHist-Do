import numpy as np
from PIL import Image


def calcular_histograma(img):
    """Recebe imagem PIL em escala de cinza e retorna array com 256 posições."""
    pixels = np.array(img)
    return np.bincount(pixels.flatten(), minlength=256)


def equalizar(img, hist):
    """Equalização: s_k = round(255 * CDF[k]). Retorna uma nova imagem PIL."""
    total = hist.sum()
    cdf = np.cumsum(hist)                           # histograma acumulado
    mapa = np.round(255 * cdf / total).astype(np.uint8)

    pixels = np.array(img)
    novos = mapa[pixels]                            # troca cada pixel pelo valor mapeado
    return Image.fromarray(novos)