#!/usr/bin/python
from openni import *
import cv2.cv as cv

depth_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 1)

ctx = Context()
ctx.init()

depth = DepthGenerator()
depth.create(ctx)
depth.set_resolution_preset(RES_VGA)
depth.fps = 30
ctx.start_generating_all()

def processa_profundidade(depth_frame):
    cv.SetData(depth_cv, depth_frame)
    cv.ShowImage('Profundidade', depth_cv)

tecla = -1
while (tecla < 0):
    nRetVal = ctx.wait_one_update_all(depth)
    depth_frame = depth.get_raw_depth_map_8()
    processa_profundidade(depth_frame)
    tecla = cv.WaitKey(1)

cv.DestroyAllWindows()
