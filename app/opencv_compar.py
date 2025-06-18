import cv2
import numpy as np


TEMPLATE_CAMINHO = 'uploads\\template.png'
VIDEO_CAMINHO = 'uploads\\video.mp4'

# Carregar o template
template = cv2.imread(TEMPLATE_CAMINHO, cv2.IMREAD_GRAYSCALE)

# Verificar se o template foi carregado
if template is None:
    print(f"Erro: Não foi possível carregar o template em '{TEMPLATE_CAMINHO}'")
    print("Verifique se o arquivo existe e o caminho está correto.")
    exit()

cap = cv2.VideoCapture(VIDEO_CAMINHO)

# Verificar se o vídeo foi aberto corretamente
if not cap.isOpened():
    print(f"Erro: Não foi possível abrir o vídeo em '{VIDEO_CAMINHO}'")
    print("Verifique se o arquivo de vídeo existe, o caminho está correto e se ele não está corrompido.")
    print("Se estiver usando webcam (0), verifique se ela está conectada e disponível.")
    exit()

frame_count = 0

while True:
    
    ret, frame = cap.read()

    if not ret:
        print("Fim do vídeo ou erro ao ler frame.")
        break

    frame_count += 1

    frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(frame_cinza, template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.7

    loc = np.where(res >= threshold)

    num_deteccoes_no_frame = 0

    for pt in zip(*loc[::-1]): # Itera sobre todas as detecções encontradas
        num_deteccoes_no_frame += 1

    if num_deteccoes_no_frame > 0:
        print(f"Template detectado no Frame {frame_count}!")    