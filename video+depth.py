#!/usr/bin/python
from openni import *
import cv2.cv as cv

depth_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 1)
imagem_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)

ctx = Context()
ctx.init()

video = ImageGenerator()
video.create(ctx)
video.set_resolution_preset(RES_VGA)
video.fps = 30

depth = DepthGenerator()
depth.create(ctx)
depth.set_resolution_preset(RES_VGA)
depth.fps = 30
ctx.start_generating_all()

def processa_video(imagem):
    cv.SetData(imagem_cv, imagem)
    cv.ShowImage('Video', imagem_cv)

def processa_profundidade(imagem):
    cv.SetData(depth_cv, imagem)
    cv.ShowImage('Profundidade', depth_cv)

tecla = -1
while (tecla < 0):
    nRetVal = ctx.wait_one_update_all(video)
    processa_video(video.get_synced_image_map_bgr())
    processa_profundidade(depth.get_raw_depth_map_8())
    tecla = cv.WaitKey(1)

cv.DestroyAllWindows()
