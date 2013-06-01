#!/usr/bin/python
from openni import *
import cv2.cv as cv
import array

depth_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 1)
matriz = array.array('B')

ctx = Context()
ctx.init()

depth = DepthGenerator()
depth.create(ctx)
depth.set_resolution_preset(RES_VGA)
depth.fps = 30
ctx.start_generating_all()

def processa_profundidade(imagem):
    matriz.fromstring(imagem)
    cv.SetData(depth_cv, imagem)
    cv.ShowImage('Profundidade', depth_cv)


tecla = -1
while (tecla < 0):
    nRetVal = ctx.wait_one_update_all(depth)
    processa_profundidade(depth.get_raw_depth_map_8())
    tecla = cv.WaitKey(1)

cv.DestroyAllWindows()
