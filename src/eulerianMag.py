from Transformacoes import uint8_2_float,filtro_passabandas_temporal
import es
import os
import cv2
import numpy
print("imports ok")

def cria_piramide_gaussiana_imagem(imagem, num_camadas):
	# gera a piramide gaussiana ate o nivel num_camadas a partir da imagem
	
	camadaAtual = numpy.ndarray(shape=imagem.shape, dtype="float")
	#base da piramide é a imagem original
	camadaAtual[:] = imagem
	piramide_gaussiana_imagem = [camadaAtual]
	
	for pyramid_level in range(1, num_camadas):
		# gera proxima camada da piramide
		camadaAtual = cv2.pyrDown(camadaAtual)
		piramide_gaussiana_imagem.append(camadaAtual)
	
	return piramide_gaussiana_imagem
	
def cria_piramide_laplaciana_imagem(imagem, num_camadas):
	# gera a piramide laplaciana ate o nivel num_camadas a partir da imagem
	
	piramide_gaussiana = cria_piramide_gaussiana_imagem(imagem, num_camadas)
	piramide_laplaciana = []
	for i in range(num_camadas - 1):
		# cada camada é a diferença entre 2 camadas da piramide gaussiana
		camadaAtual = (piramide_gaussiana[i] - cv2.pyrUp(piramide_gaussiana[i + 1]))
		piramide_laplaciana.append(camadaAtual + 0)
	
	piramide_laplaciana.append(piramide_gaussiana[-1])
	return piramide_laplaciana

def cria_piramide_laplaciana_(video, num_camadas):
	# cria uma piramide laplaciana de videos a partir do video
	
	piramide_laplaciana = []
	# frame_count, height, width, colors = video.shape
	for indice_frame, frame in enumerate(video):
		piramide_imagens = cria_piramide_laplaciana_imagem(frame, num_camadas)
	
		for indice_camada, frame_da_camada in enumerate(piramide_imagens):
			if indice_frame == 0:
				piramide_laplaciana.append(
					numpy.zeros((video.shape[0], frame_da_camada.shape[0], frame_da_camada.shape[1], 3),
									dtype="float"))
	
			piramide_laplaciana[indice_camada][indice_frame] = frame_da_camada
	
	return piramide_laplaciana

def colapsa_piramide_laplaciana_imagem(piramide_laplaciana_imagens):
	# recalcula a imagem original a partir da sua piramide laplaciana
    imagem = piramide_laplaciana_imagens.pop()
    while piramide_laplaciana_imagens:
        imagem = cv2.pyrUp(imagem) + (piramide_laplaciana_imagens.pop() - 0)
		
    return imagem


def colapsa_piramide_laplaciana(piramide_laplaciana):
	# recalcula o video original a partir de sua piramide laplaciana
    i = 0
    while True:
        try:
            piramide_laplaciana_imagens = [video[i] for video in piramide_laplaciana]
			# recalculando cada frame do video original em cima da primeira camada
            piramide_laplaciana[0][i] = colapsa_piramide_laplaciana_imagem(piramide_laplaciana_imagens)
            i += 1
        except IndexError:
			# para ir ate a ultima camada da piramide
            break
    return piramide_laplaciana[0]

def magnificacao_euleriana(video_data, fps, freq_min, freq_max, amplificacao, num_camadas=4, skip_levels_at_top=2):

	# cria a piramide laplaciana a partir do video
    piramide_laplaciana = cria_piramide_laplaciana_(video_data, num_camadas=num_camadas)
	
    for i, video in enumerate(piramide_laplaciana):
        if i < skip_levels_at_top or i >= len(piramide_laplaciana) - 1:
			# nao amplifica os niveis mais ao topo (skip_levels_at_top)
			# porque eles geralmente contem muito ruido
			# nem a base da piramide porque ela é o video original
            continue
			
		# aplica filtragem temporal em cada pixel dos videosa de cada uma das camadas da piramide
        bandpassed = filtro_passabandas_temporal(video, fps, freq_min=freq_min, freq_max=freq_max, taxa_de_amplificacao=amplificacao)

        es.play_video_data(bandpassed)

        piramide_laplaciana[i] += bandpassed
        #es.play_vid_data(piramide_laplaciana[i])

    video_data = colapsa_piramide_laplaciana(piramide_laplaciana)
    return video_data
	

#
#--------
# "main":

video, fps = es._carrega_video('face.mp4')
#es.play_video_data(video)
videoEuler = magnificacao_euleriana(video, fps, freq_min=0.5, freq_max=10, amplificacao=5)
#es.play_video_data(videoEuler)
es.salva_video(videoEuler,fps,nome_arquivo='resultado.avi')
print("fim \n fps:" + str(fps))
