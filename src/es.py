import os 

import cv2
import numpy as np

from Transformacoes import uint8_2_float, float_2_uint8

def carrega_imagem(caminho_imagem):
    imagem = cv2.imread(caminho_imagem)
    return uint8_2_float(imagem)

def pegar_dimensoes_de_captura(captura):
    """Adquire as dimensoes da captura"""
    largura = int(captura.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(captura.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return largura, altura

def _carrega_video(nome_do_arquivo_video):
    """Carrega um video para array de numpy"""
    print("Carregando " + nome_do_arquivo_video)
    if not os.path.isfile(nome_do_arquivo_video):
        raise Exception("Arquivo nao encontrado:%s" % nome_do_arquivo_video)
    captura = cv2.VideoCapture(nome_do_arquivo_video)
    contador_de_frames = int(captura.get(cv2.CAP_PROP_FRAME_COUNT))
    largura, altura = pegar_dimensoes_de_captura(captura)
    fps = int(captura.get(cv2.CAP_PROP_FPS))
    x = 0
    frames_video = np.zeros((contador_de_frames,altura,largura,3),dtype='uint8')
    while captura.isOpened():
        ret,frame = captura.read()
        if not ret:
            break

        frames_video[x] = frame
        x = x+1
    captura.release()

    return frames_video,fps


def carrega_video_float(nome_do_arquivo_video):
    video_data, fps = _load_video(nome_do_arquivo_video)
    return uint8_2_float(video_data), fps