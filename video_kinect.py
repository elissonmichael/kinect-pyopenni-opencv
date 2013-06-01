#!/usr/bin/python
from openni import *
import cv2.cv as cv
import array

imagem_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)
matriz = array.array('B')

ctx = Context()
ctx.init()

video = ImageGenerator()
video.create(ctx)
video.set_resolution_preset(RES_VGA)
video.fps = 30

ctx.start_generating_all()

def processa_video(imagem):
    matriz.fromstring(imagem)
    cv.SetData(imagem_cv, imagem)
    cv.ShowImage('Video', imagem_cv)

tecla = -1
while (tecla < 0):
    nRetVal = ctx.wait_one_update_all(video)
    processa_video(video.get_raw_image_map_bgr())
    tecla = cv.WaitKey(1)

cv.DestroyAllWindows()
