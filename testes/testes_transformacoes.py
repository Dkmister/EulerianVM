
#from src.base import show_frequencies
from src.es import _load_video, play_video_data, carrega_imagem, carrega_video_float
from src.Transformacoes import uint8_2_float, float_2_uint8
from .base import TESTE_CAMINHO_IMAGEM, TESTE_CAMINHO_VIDEO


def teste_uint8_2_float_e_viceversa():
    imagem = carrega_imagem(TESTE_CAMINHO_IMAGEM)
    img_float = uint8_2_float(imagem)
    img_uint8 = float_2_uint8(img_float)
    img_diff = imagem - img_uint8

    assert img_diff.max() <= 1

teste_uint8_2_float_e_viceversa()