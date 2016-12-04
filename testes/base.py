import cv2

DISPLAY_RESULTADOS = True
TESTE_CAMINHO_VIDEO = r"C:/home/vilmar/EulerianVM/baby.mp4"
TESTE_CAMINHO_IMAGEM = r"C:/home/vilmar/EulerianVM/cameraman.tif"


def display_imagem(imagem,titulo='Imagem',espera=False):
	if DISPLAY_RESULTADOS:
		cv2.imshow(titulo,imagem)
		if espera:
    			cv2.waitKey(0)

def display_imagem_piramide(piramide):
    	if DISPLAY_RESULTADOS:
			for i,imagem in enumerate(piramide):
    				cv2.imshow(str(i),piramide[i])
			cv2.waitKey(0)
