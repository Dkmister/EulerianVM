import numpy as np
import scipy as sp
#-------------------------------
# Arquivo de transformacoes:
#-------------------------------
# uint8_2_float(imagem)=> imagem
# float_2_uint8(imagem)=> imagem
# float_2_int8(imagem) => imagem
#------------------------------
# imagem uint8 => imagem float
# imagem float => imagem uint8
# imagem float => imagem int8
#-------------------------------
def uint8_2_float(imagem):
    resultado = np.ndarray(shape=imagem.shape,dtype='float')
    resultado = img*(1./255)
    return resultado

def float_2_uint8(imagem):
    resultado = np.ndarray(shape=imagem.shape,dtype='uint8')
    resultado[:] = imagem * 255
    return resultado

def float_2_int8(imagem):
    resultado = np.ndarray(shape=imagem.shape, dtype='int8')
    resultado[:] = (img * 255) - 127
    return resultado
