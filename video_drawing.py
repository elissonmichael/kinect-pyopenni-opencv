#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from openni import *
import cv2.cv as cv

cv.NamedWindow('Video',1)
cv.MoveWindow('Video',0,0)
cv.NamedWindow('Quadro',1)
cv.MoveWindow('Quadro',720,0)

fonte_do_texto = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.6, 0.6, 0, 1, 4)

quadro = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 1)
cv.Set(quadro, 255.0)
imagem_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)
maos = {}
traduz = {'Wave' : 'Apagador', 'Click' : 'Caneta'}
efeito = 'Nenhum'

ni = Context()
ni.init()
ni.open_file_recording("BothGestures.oni")
video = ni.find_existing_node(NODE_TYPE_IMAGE)
depth = ni.find_existing_node(NODE_TYPE_DEPTH)

gesture_generator = GestureGenerator()
gesture_generator.create(ni)
gesture_generator.add_gesture('Wave')
gesture_generator.add_gesture('Click')


hands_generator = HandsGenerator()
hands_generator.create(ni)

ni.start_generating_all()

def gesture_detected(src, gesture, id, end_point):
    global efeito
    if efeito != 'Nenhum' and gesture == 'Click':
      efeito = 'Nenhum'
    else:
      efeito = traduz[gesture]
    hands_generator.start_tracking(end_point)

def gesture_progress(src, gesture, point, progress): pass

def create(src, id, pos, time):
    global maos
    ponto = depth.to_projective([pos])
    centro = (int(ponto[0][0]), int(ponto[0][1])) 
    maos[id] = {'atual' : centro, 'posicao' : pos}

def update(src, id, pos, time):
    global maos
    maos[id]['posicao'] =  pos
    maos[id]['anterior'] = maos[id]['atual']
    ponto = depth.to_projective([pos])
    centro = (int(ponto[0][0]), int(ponto[0][1])) 
    maos[id]['atual'] =  centro

def destroy(src, id, time):
    global maos
    del maos[id]

gesture_generator.register_gesture_cb(gesture_detected, gesture_progress)
hands_generator.register_hand_cb(create, update, destroy)

def processa_frame(imagem):
    cv.SetData(imagem_cv, imagem)
    if maos:
      for id in maos:
        cv.PutText(imagem_cv, efeito, maos[id]['atual'] ,fonte_do_texto , cv.CV_RGB(0,0,150))
    cv.PutText(imagem_cv, 'Efeito: '+efeito, (10,20) ,fonte_do_texto , cv.CV_RGB(200,0,0))
    cv.ShowImage('Video', imagem_cv)

def altera_quadro():
    if maos:
      for id in maos:
        if 'anterior' in maos[id]:
          if efeito == 'Caneta':
            cv.Line(quadro, maos[id]['anterior'], maos[id]['atual'], cv.CV_RGB(0,0,0), 1, cv.CV_AA, 0) 
          elif efeito == 'Apagador':
            cv.Line(quadro, maos[id]['anterior'], maos[id]['atual'], cv.CV_RGB(255,255,255), 30, cv.CV_AA, 0) 
    cv.ShowImage('Quadro', quadro)

tecla = -1
while (tecla < 0):
    ni.wait_any_update_all()
    imagem = video.get_raw_image_map_bgr()
    processa_frame(imagem)
    altera_quadro()

    tecla = cv.WaitKey(1)
cv.DestroyAllWindows()


