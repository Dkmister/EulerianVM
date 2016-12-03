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

def toca_video(nome_do_arquivo_video):
    video_orig, fps = carrega_video_float(nome_do_arquivo_video)
    toca_video_data(video_orig)

def toca_piramide(piramide):
    i = 0
    while True:
        try:
            for nivel, vid in enumerate(piramide):
                cv2.imshow('Nivel %i' % nivel, vid[i])
            i = i + 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except IndexError:
            break

def toca_video_data(frames):
    toca_piramide([frames])


def salva_video(video,fps,save_nome_arquivo='media/output.avi')

    print (save_nome_arquivo)
    video = float_2_uint8(video)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    escritor = cv2.VideoWriter(save_nome_arquivo,fourcc,fps,(video.shape[2],video.shape[1]),1)
    for i in range(0,video.shape[0]):
        res = cv2.convertScaleAbs(video[i])
        escritor.write(res)