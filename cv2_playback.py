#!/usr/bin/python
from openni import *
import cv2
import numpy

ni = Context()
ni.init()
ni.open_file_recording("MeuVideo.oni")
ni.start_generating_all()
video = ni.find_existing_node(NODE_TYPE_IMAGE)

tecla = -1
while (tecla < 0):
    ni.wait_one_update_all(video)
    imagem = video.get_raw_image_map_bgr()
    imagem_cv = numpy.fromstring(imagem, dtype=numpy.uint8).reshape(480, 640, 3)
    cv2.imshow("video", imagem_cv)

    tecla = cv2.waitKey(1)
cv.DestroyAllWindows()


