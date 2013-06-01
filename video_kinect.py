#!/usr/bin/python
from openni import *
import cv2.cv as cv

imagem_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)

ctx = Context()
ctx.init()

video = ImageGenerator()
video.create(ctx)
video.set_resolution_preset(RES_VGA)
video.fps = 30

ctx.start_generating_all()

def processa_frame(frame):
    cv.SetData(imagem_cv, frame)
    cv.ShowImage('Video', imagem_cv)

tecla = -1
while (tecla < 0):
    nRetVal = ctx.wait_one_update_all(video)
    frame = video.get_raw_image_map_bgr()
    processa_frame(frame)
    tecla = cv.WaitKey(1)

cv.DestroyAllWindows()
