#!/usr/bin/python
from openni import *
import cv2.cv as cv

imagem_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)

ni = Context()
ni.init()
ni.open_file_recording("MeuVideo.oni")
ni.start_generating_all()
video = ni.find_existing_node(NODE_TYPE_IMAGE)

tecla = -1
while (tecla < 0):
    ni.wait_one_update_all(video)
    imagem = video.get_raw_image_map_bgr()
    cv.SetData(imagem_cv, imagem)
    cv.ShowImage("video", imagem_cv)

    tecla = cv.WaitKey(1)
cv.DestroyAllWindows()


