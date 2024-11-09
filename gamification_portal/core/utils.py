import os

from PIL import Image


def converter_jfif_para_png(diretorio):
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.jfif'):
            caminho_jfif = os.path.join(diretorio, arquivo)
            caminho_png = os.path.join(diretorio, arquivo.replace('.jfif', '.png'))

            # Abrir e converter a imagem
            with Image.open(caminho_jfif) as img:
                img.save(caminho_png, 'PNG')
            print(f'{arquivo} convertido para {caminho_png}')


# Exemplo de uso
converter_jfif_para_png(
    '/home/gustavo/PycharmProjects/Desafio-Desenvolvedor-Python-Django/docker_desafio/mediafiles/banners'
)
