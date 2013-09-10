import cv2
import numpy as np
camera = cv2.VideoCapture(0)

tecla = -1
while (tecla < 0):
    _,imagem = camera.read()
    cv2.imshow('camera', imagem)
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    cv2.imshow('cinza', cinza)
    tecla = cv2.waitKey(1)
cv2.destroyAllWindows()
