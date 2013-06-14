import cv2
import numpy as np
camera = cv2.VideoCapture(0)

tecla = -1
while (tecla < 0):
    _,imagem = camera.read()
    cv2.imshow('camera',imagem)
    tecla = cv2.waitKey(1)
cv2.destroyAllWindows()
