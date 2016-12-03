import os 

import cv2
import numpy as np

from Transformacoes import uint8_2_float, float_2_uint8

def carrega_imagem(imagem_path):
    imagem = cv2.imread(imagem_path)
    return uint8_2_float(imagem)

def pegar_dimensoes_da_imagem(imagem):
    """Adquire as dimensoes da imagem"""
    largura = int(imagem.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(imagem.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return largura, altura

def _carrega_video(nome_do_arquivo_de_video):
    """Carrega um video para um array de numpy"""
    print("Carregando " + nome_do_arquivo_de_video)
    if not os.path.isfile(nome_do_arquivo_de_video):
        raise Exception("Arquivo nao encontrado:%s" % nome_do_arquivo_de_video)
    captura = cv2.VideoCapture(nome_do_arquivo_de_video)
    contador_de_frames = int(captura.get(cv2.CAP_PROP_FRAME_COUNT))
    largura, altura = pegar_dimensoes_da_imagem(captura)
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


def carrega_video_float(nome_do_arquivo_de_video):
	video_data, fps = _load_video(nome_do_arquivo_de_video)
	return uint8_2_float(video_data), fps

def play_video(nome_do_arquivo_de_video):
		video_data, fps = carrega_video_float(nome_do_arquivo_de_video)
		play_video_data(video_data)

def play_piramide(piramide):
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
		
def play_video_data(frames):
	play_piramide([frames])
	

def salva_video(video,fps,nome_arquivo='resultados/resultado.avi'):
	
	print (nome_arquivo)
	video = float_2_uint8(video)
	fourcc = cv2.VideoWriter_fourcc(*'MJPG')
	writer = cv2.VideoWriter(nome_arquivo,fourcc,fps,(video.shape[2],video.shape[1]),1)
	for i in range(0,video.shape[0]):
		res = cv2.convertScaleAbs(video[i])
		writer.write(res)
