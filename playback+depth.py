#!/usr/bin/python
from openni import *
import cv2.cv as cv

cv.NamedWindow('Video',1)
cv.MoveWindow('Video',0,0)
cv.NamedWindow('Profundidade',1)
cv.MoveWindow('Profundidade',650,0)

depth_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 1)
imagem_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)

ni = Context()
ni.init()
ni.open_file_recording("MeuVideo.oni")
ni.start_generating_all()
video = ni.find_existing_node(NODE_TYPE_IMAGE)
depth = ni.find_existing_node(NODE_TYPE_DEPTH)

def processa_frame(imagem):
    cv.SetData(imagem_cv, imagem)
    cv.ShowImage('Video', imagem_cv)

def processa_profundidade(imagem):
    cv.SetData(depth_cv, imagem)
    cv.ShowImage('Profundidade', depth_cv)

tecla = -1
while (tecla < 0):
    ni.wait_one_update_all(video)
    imagem = video.get_raw_image_map_bgr()
    depth_frame = depth.get_raw_depth_map_8()

    processa_frame(imagem)
    processa_profundidade(depth_frame)

    tecla = cv.WaitKey(1)
cv.DestroyAllWindows()


