#!/usr/bin/python
from openni import *
import cv2.cv as cv

cv.NamedWindow('Video',1)
cv.MoveWindow('Video',0,0)
cv.NamedWindow('Profundidade',1)
cv.MoveWindow('Profundidade',650,0)
fonte_do_texto = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.6, 0.6, 0, 1, 4)

depth_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 1)
imagem_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)
maos = {}

ni = Context()
ni.init()
ni.open_file_recording("BothHands.oni")
video = ni.find_existing_node(NODE_TYPE_IMAGE)
depth = ni.find_existing_node(NODE_TYPE_DEPTH)

gesture_generator = GestureGenerator()
gesture_generator.create(ni)
gesture_generator.add_gesture('Wave')

hands_generator = HandsGenerator()
hands_generator.create(ni)

ni.start_generating_all()

def gesture_detected(src, gesture, id, end_point):
    hands_generator.start_tracking(end_point)

def gesture_progress(src, gesture, point, progress): pass

def create(src, id, pos, time):
    global maos
    ponto = depth.to_projective([pos])
    centro = (int(ponto[0][0]), int(ponto[0][1])) 
    maos[id] = {'real' : pos, 'projecao' : centro}

def update(src, id, pos, time):
    global maos
    ponto = depth.to_projective([pos])
    centro = (int(ponto[0][0]), int(ponto[0][1])) 
    maos[id] = {'real' : pos, 'projecao' : centro}

def destroy(src, id, time):
    global maos
    del maos[id]

gesture_generator.register_gesture_cb(gesture_detected, gesture_progress)
hands_generator.register_hand_cb(create, update, destroy)

def processa_frame(imagem):
    cv.SetData(imagem_cv, imagem)
    if maos:
      for id in maos:
        cv.PutText(imagem_cv, ', '.join(str(int(e)) for e in maos[id]['real']), maos[id]['projecao'] ,fonte_do_texto , cv.CV_RGB(0,0,150))
    else:
        cv.PutText(imagem_cv, 'Acene para ser Rastreado', (10,20) ,fonte_do_texto , cv.CV_RGB(200,0,0))
    cv.ShowImage('Video', imagem_cv)

def processa_profundidade(imagem):
    cv.SetData(depth_cv, imagem)
    cv.ShowImage('Profundidade', depth_cv)

tecla = -1
while (tecla < 0):
    ni.wait_any_update_all()
    imagem = video.get_raw_image_map_bgr()
    depth_frame = depth.get_raw_depth_map_8()
    processa_frame(imagem)
    processa_profundidade(depth_frame)
    tecla = cv.WaitKey(1)
cv.DestroyAllWindows()


