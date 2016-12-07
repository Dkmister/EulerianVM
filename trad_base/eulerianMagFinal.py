import cv2
import os
import sys

import numpy
from matplotlib import pyplot
import scipy.signal
import scipy.fftpack


def magnificacao_euleriana(video_filename, tipo_da_piramide='gaussiana', freq_min=0.833, freq_max=1, amplificacao=50, num_camada=4):

    path_to_video = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), video_filename)
    video_original, fps = carrega_video(path_to_video)
    if tipo_da_piramide == 'gaussiana':
        akhnaten = camada_piramide_gaussiana(video_original, num_camada)
    elif tipo_da_piramide == 'laplaciana':
        akhnaten = camada_piramide_laplaciana(video_original, num_camada)
    akhnaten = temporal_bandpass_filter(akhnaten, fps, freq_min=freq_min, freq_max=freq_max)
    print("...amplificando o sinal por " + str(amplificacao) + "...")
	#amplifica a variacao
    akhnaten *= amplificacao
    file_name = os.path.splitext(path_to_video)[0]
    file_name = file_name + "_min"+str(freq_min)+"_max"+str(freq_max)+"_amp"+str(amplificacao)+'_'+tipo_da_piramide
    recombina_piramide_e_salva(akhnaten, video_original, num_camada, fps, save_filename=file_name + '_magnified.avi')


def mostra_frequencias(video_filename):

    original_video, fps = carrega_video(video_filename)
    print(fps)
    medias = []
	
    for x in range(1, original_video.shape[0] - 1):
        medias.append(original_video[x, :, :, : ].sum())

    charts_x = 1
    charts_y = 2
    pyplot.figure(figsize=(charts_y, charts_x))
    pyplot.subplots_adjust(hspace=.7)

    pyplot.subplot(charts_y, charts_x, 1)
    pyplot.title("Média dos Pixels")
    pyplot.plot(medias)

    frequencias = scipy.fftpack.fftfreq(len(medias), d=1.0 / fps)

    pyplot.subplot(charts_y, charts_x, 2)
    pyplot.title("Espectro da Transformada de Fourier")
    pyplot.axis([0, 15, -2000000, 5000000])
    pyplot.plot(frequencias, scipy.fftpack.fft(medias))

    pyplot.show()


def temporal_bandpass_filter(sinal, fps, freq_min=0.833, freq_max=1, axis=0):
    # aplica uma filtragem temporal que seleciona as frequencias entre freq_min e freq_max
    # e entao retorna esse sinal amplificado pela taxa_de_amplificacao
    print("Filtrando frequencias entre " + str(freq_min) + " e " + str(freq_max) + " Hz")
    fft = scipy.fftpack.fft(sinal, axis=axis)
    frequencias = scipy.fftpack.fftfreq(sinal.shape[0], d=1.0 / fps)
	
	# Calcula os limites e inferior reais para a filtragem de sequencias
    limite_inferior  = (numpy.abs(frequencias - freq_min)).argmin()
    limite_superior  = (numpy.abs(frequencias - freq_max)).argmin()
	
	# zera todas as frequencias mais baixas que o limite inferior
	# e tambem suas frequencias conjugadas
    fft[:limite_inferior ] = 0
    fft[-limite_inferior :] = 0
	# zera todas as frequencias mais altas que o limite superior
	# e tambem suas frequencias conjugadas
    fft[limite_superior :-limite_superior ] = 0

    return scipy.fftpack.ifft(fft, axis=0)


def carrega_video(video_filename):
    # carrega um video e converte para um array numpy 
    print("Loading " + video_filename)
    video = cv2.VideoCapture(video_filename)
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width, height = get_capture_dimensions(video)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    x = 0
    np_video = numpy.zeros((num_frames, height, width, 3), dtype='uint8')
    while True:
        _, frame = video.read()

        if frame == None or x >= num_frames:
            break
        np_video[x] = frame
        x += 1
    video.release()

    return np_video, fps





def camada_piramide_gaussiana(video, num_camada):
    #devolve a camada de numero num_camada da piramide gaussiana do video
    camadaVideo = None
    for x in range(0, video.shape[0]):
        frame = video[x]
        camadaAtual = numpy.ndarray(shape=frame.shape, dtype="float")
        camadaAtual[:] = frame
        for i in range(num_camada):
            camadaAtual = cv2.pyrDown(camadaAtual)

        if x == 0:
            camadaVideo = numpy.zeros((video.shape[0], camadaAtual.shape[0], camadaAtual.shape[1], 3))
        camadaVideo[x] = camadaAtual
    return camadaVideo


def camada_piramide_laplaciana(video, num_camada):
    #devolve a camada de numero num_camada da piramide laplaciana do video
    camadaVideo = None
    for x in range(0, video.shape[0]):
        frame = video[x]
        camadaAtual = numpy.ndarray(shape=frame.shape, dtype="float")
        camadaAtual[:] = frame

        for i in range(num_camada):
            camadaAnterior = camadaAtual[:]
            camadaAtual = cv2.pyrDown(camadaAtual)

        laplacian = camadaAnterior - cv2.pyrUp(camadaAtual)

        if x == 0:
            camadaVideo = numpy.zeros((video.shape[0], laplacian.shape[0], laplacian.shape[1], 3))
        camadaVideo[x] = laplacian
    return camadaVideo


def recombina_piramide_e_salva(camadaPiramide, video_original, num_camada, fps, save_filename='resultado.avi'):
    #recombina a camada da pirâmide de sinal amplificado 
    # com o video original e salva
    width, height = get_frame_dimensions(video_original[0])
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    print("Outputting to %s" % save_filename)
    writer = cv2.VideoWriter(save_filename, fourcc, fps, (width, height), 1)
    for x in range(0, camadaPiramide.shape[0]):
        img = numpy.ndarray(shape=camadaPiramide[x].shape, dtype='float')
        img[:] = camadaPiramide[x]
        for i in range(num_camada):
            img = cv2.pyrUp(img)

        img[:height, :width] = img[:height, :width] + video_original[x]
        res = cv2.convertScaleAbs(img[:height, :width])
        writer.write(res)


def get_capture_dimensions(capture):
    # pega as dimensoes de um capture
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return width, height


def get_frame_dimensions(frame):
    # pega as dimensoes de um frame
    height, width = frame.shape[:2]
    return width, height






# "main"
#--------------------------------------------------
# sys.argv[1] => nome do arquivo
# sys.argv[2] => tipo de piramide: gaussiana ou laplacina
# sys.argv[3] => frequencia minima, em float
# sys.argv[4] => frequencia maxima, em float
# sys.argv[5] => fator amplificacao, em inteiro
# sys.argv[6] => numero da camada da pirâmide a ser amplificada, em inteiro
#---------------------------------------------------
# Exemplo de uso:
#---------------------------------------------------
# python3 emBR.py face.mp4 laplaciana 0.83 1 25 4
# python emBR.py face.mp4 laplaciana 0.83 1 25 4
#---------------------------------------------------
# Opcao de visualizacao de frequencias:
# ---------------------------------------------------
# python3 emBR.py freq face.mp4
# python emBR.py freq face.mp4
#---------------------------------------------------
if(len(sys.argv) == 7):
	nome_arq = sys.argv[1]
	tip_piramide = sys.argv[2]
	freq_min = sys.argv[3]
	freq_max = sys.argv[4]
	amp = sys.argv[5]
	num_camada = sys.argv[6]
	
	freq_min = float(freq_min)
	freq_max = float(freq_max)
	amp = int(amp)
	num_camada = int(num_camada)
	magnificacao_euleriana(nome_arq,tip_piramide, freq_min, freq_max, amp, num_camada)
elif( (len(sys.argv)==3) and (sys.argv[1]=='freq') ):
	nome_arq = sys.argv[2]
	mostra_frequencias(nome_arq)
else:
	print("parametros invalidos")
		


