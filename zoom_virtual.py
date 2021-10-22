# 1. Importar as bibliotecas
import cv2
from cvzone.HandTrackingModule import HandDetector

# 2. Carregar o módulo de detecção
detector = HandDetector(maxHands=2, detectionCon=0.8, minTrackCon=0.8)

# 3. Configurar o tamanho da tela
largura_tela = 1280
altura_tela = 720

# 4. Configurar o ponto inicial da distância entre as mãos, a escala, cx e cy
distancia_inicial = None
escala = 0
cx, cy = 500, 500

# 5. Captura de vídeo
cap = cv2.VideoCapture(0)
cap.set(3, largura_tela)
cap.set(4, altura_tela)


while True:
    # Detectar as mãos
    sucesso, imagem = cap.read()
    maos, imagem = detector.findHands(imagem)
    
    # Extrair as informações das mãos
    if len(maos) == 2:
        # Detectar se os dedos (dedão e indicador) estão levantados
        if detector.fingersUp(maos[0]) == [1, 1, 0, 0, 0] and detector.fingersUp(maos[1]) == [1, 1, 0, 0, 0]:
            centro_mao_1 = maos[0]['center']
            centro_mao_2 = maos[1]['center']
            
            # Usaremos o centro da mão como os pontos de referência
            if distancia_inicial is None:
                comprimento, info, imagem = detector.findDistance(centro_mao_1, centro_mao_2, imagem)
                distancia_inicial = comprimento
                
            comprimento, info, imagem = detector.findDistance(centro_mao_1, centro_mao_2, imagem)
            # Como os valores são grandes, vamos dividí-los por dois
            escala = int((comprimento - distancia_inicial) // 2)
            # Colocar a foto bem no meio da distância entre as mãos
            cx, cy = info[4:]
    else:
        distancia_inicial = None
    
    # Manipular a foto
    foto = cv2.imread('python_logo.jpg')
    altura_foto, largura_foto, _ = foto.shape
    try:
        nova_altura_foto, nova_largura_foto = ((altura_foto + escala)//2)*2, ((largura_foto + escala)//2)*2
        foto = cv2.resize(foto, (nova_altura_foto, nova_largura_foto))
        imagem[cy-nova_altura_foto//2: cy+nova_altura_foto//2,
               cx-nova_largura_foto//2:cx+nova_largura_foto//2] = foto
    except:
        pass

    # Mostrar a imagem na tela
    cv2.imshow('Imagem', imagem)
    
    # Terminar o loop
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

# 6. Fechar a tela de captura
cap.release()
cv2.destroyAllWindows()