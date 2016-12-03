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
    resultado[:] = img*(1./255)
    return resultado

def float_2_uint8(imagem):
    resultado = np.ndarray(shape=imagem.shape,dtype='uint8')
    resultado[:] = imagem * 255
    return resultado

def float_2_int8(imagem):
    resultado = np.ndarray(shape=imagem.shape, dtype='int8')
    resultado[:] = (imagem * 255) - 127
    return resultado

#--------------------------------
#
#
#--------------------------------
def filtro_passabandas_temporal(data,fps,freq_min=0.833,freq_max=1,eixos=0,fator_de_amplificacao=1):
    print("Aplicando uma filtragem temporal que seleciona as frequencias entre "+str(freq_min)+" e "+str(freq_max)+" Hz")
    fft = sp.fftpack.rfft(data,axis=eixos)
    frequencias = sp.fftpack.fftfreq(data.shape[0],d=1.0/fps)
    # Onde d eh o tempo entre um frame e o proximo
    
    # Calcula os limites e inferior reais para a filtragem de sequencias
    limite_inferior = (np.abs(frequencias - freq_min)).argmin()
    limite_superior = (np.abs(frequencias - freq_max)).argmin()
    
    #
    fft[:limite_inferior] = 0
    fft[limite_superior:-limite_superior] = 0
    fft[-limite_inferior:]=0

    resultado = np.ndarray(shape=data.shape, dtype ='float')
    resultado[:] = sp.fftpack.ifft(fft,axis=0)
    resultado *= fator_de_amplificacao

    return resultado
#-----------------------------------