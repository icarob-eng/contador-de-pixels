import cv2
import numpy as np
from matplotlib import pyplot as plt

from itertools import product

ARQ = 'amostras-mes{}/{}.jpg'
BASES = [
         '{}',
         'AL{}',
         'AS{}',
         'M{}',
         'S{}',
         'REF{}'
         ]


def contar(path: str) -> int:
    """ Conta os píxeis de um determinado arquivo """
    imgarr = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    _, binarie = cv2.threshold(src=imgarr, thresh=0, maxval=255, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    contours, _, = cv2.findContours(image=binarie, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

    cnt = max(contours, key=cv2.contourArea)
    # encontra a borda de maior área usando a função `cv2.contourArea()`
    return cv2.contourArea(cnt)


def remover(base: str, mes: int):
    """ Remove um trio de caminhos de arquivo de acordo com especificado """
    for n in range(1, 3 + 1):
        results.pop(ARQ.format(mes, base.format(n)))


def ap_mes(n: int):
    mes = refs_area[n-1]
    aps = [mes[k] / results[ARQ.format(n, k)] for k in mes]

    return np.mean(aps), np.std(aps)


if __name__ == "__main__":
    n_meses = 5
    results = {ARQ.format(mes, base.format(n)): 0 for mes, base, n in
               product(range(1, n_meses + 1), BASES, range(1, 3 + 1))}
    # cria um dicionário cujas chaves são preenchidas para cada mes num intervalo de 1 a n_meses, para todas
    # as bases de nome listadas anteriormente, para todos os valores de 1 a 3 (S1, S2, S3)

    remover(BASES[5], 1)  # remove REF
    remover(BASES[0], 2)  # remove {}
    remover(BASES[0], 3)
    remover(BASES[0], 4)
    remover(BASES[0], 5)

    for key in results:
        results[key] = contar(key)

    refs_REF = {
        BASES[5].format(1): 3 ** 2,  # REF1
        BASES[5].format(2): 3 ** 2,  # REF2
        BASES[5].format(3): 3 ** 2  # REF3
    }
    refs_area = [
        {
            BASES[0].format(1): 2.6 * 2.6,
            BASES[0].format(2): 2.6 * 2.595,
            BASES[0].format(3): 2.6 * 2.6
        },
        refs_REF,  # utilizou-se a mesma referência
        refs_REF,
        refs_REF,
        refs_REF
    ]

    areas = {}
    for k in results:
        if k.split('/')[1].split('.')[0][:-1] != BASES[5][:-2]:  # garante que ref não será considerado
            m = int(k.split('/')[0][-1])  # descobre o número do mês
            areas[k] = results[k] * ap_mes(m)[0]
