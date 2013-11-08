#!/usr/bin/python
from openni import *
import cv2
import numpy

ni = Context()
ni.init()
ni.open_file_recording("MeuVideo.oni")
ni.start_generating_all()
depth = ni.find_existing_node(NODE_TYPE_DEPTH)

while True:
    ni.wait_one_update_all(depth)
    imagem = depth.get_raw_depth_map_8()
    imagem_cv = numpy.fromstring(imagem, dtype=numpy.uint8).reshape(480, 640, 1)
    cv2.imshow("Profundidade", imagem_cv)

    cv2.waitKey(1)
cv.DestroyAllWindows()


