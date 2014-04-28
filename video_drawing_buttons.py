#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from openni import *
import cv2.cv as cv

cv.NamedWindow('Video',1)
cv.MoveWindow('Video',0,0)
cv.NamedWindow('Drawing',1)
cv.MoveWindow('Drawing',720,0)

fonte_do_texto = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.6, 0.6, 0, 1, 4)

quadro = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)
cv.Set(quadro, (255.0,255.0,255.0))

imagem_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)
hands = {}
buttons_size = (100, 60)
buttons = {'white': {'color': cv.CV_RGB(255,255,255), 'start': (200, 230), 'end': (200 + buttons_size[0], 230 + buttons_size[1])},
          'black': {'color': cv.CV_RGB(0,0,0), 'start': (400, 230), 'end': (400 + buttons_size[0], 230 + buttons_size[1])}
          }

color = 'Choose a color'

ni = Context()
ni.init()
ni.open_file_recording("paola.oni")
video = ni.find_existing_node(NODE_TYPE_IMAGE)
depth = ni.find_existing_node(NODE_TYPE_DEPTH)

gesture_generator = GestureGenerator()
gesture_generator.create(ni)
gesture_generator.add_gesture('Wave')
gesture_generator.add_gesture('Click')

hands_generator = HandsGenerator()
hands_generator.create(ni)

ni.start_generating_all()

def translate_coordinates(openni_point):
  opencv_point = depth.to_projective([openni_point])
  return (int(opencv_point[0][0]), int(opencv_point[0][1]))

def overlap(point, button):
  pass

def gesture_detected(src, gesture, id, end_point):
    global hands
    hands_generator.start_tracking(end_point)

def gesture_progress(src, gesture, point, progress): pass

def create(src, id, pos, time):
    global hands
    ponto = depth.to_projective([pos])
    centro = (int(ponto[0][0]), int(ponto[0][1])) 
    hands[id] = {'atual': centro, 'posicao': pos, 'color': {'name': 'Choose a Color', 'cv': cv.CV_RGB(255,255,255)}}


def update(src, id, pos, time):
    global hands
    hands[id]['posicao'] =  pos
    hands[id]['anterior'] = hands[id]['atual']
    hands[id]['atual'] = translate_coordinates(pos)

def destroy(src, id, time):
    global hands
    del hands[id]

gesture_generator.register_gesture_cb(gesture_detected, gesture_progress)
hands_generator.register_hand_cb(create, update, destroy)

def processa_frame(imagem):
    cv.SetData(imagem_cv, imagem)
    if hands:
      for id in hands:
        cv.PutText(imagem_cv, hands[id]['color']['name'], hands[id]['atual'] ,fonte_do_texto , cv.CV_RGB(255,255,255))
    else:
      cv.PutText(imagem_cv, 'Wave to Start', (100,100) ,fonte_do_texto , cv.CV_RGB(255,255,255))
    for button in buttons:
      cv.Rectangle(imagem_cv, buttons[button]['start'], buttons[button]['end'] , buttons[button]['color'], -1, cv.CV_AA, 0)
    cv.ShowImage('Video', imagem_cv)

def altera_quadro():
    blink = cv.CloneImage(quadro)
    if hands:
      for id in hands:
        cv.Circle(blink, hands[id]['atual'], 10, hands[id]['color']['cv'], -1, cv.CV_AA, 0)
        if 'anterior' in hands[id]:
          cv.Line(quadro, hands[id]['anterior'], hands[id]['atual'], hands[id]['color']['cv'], 30, cv.CV_AA, 0) 
    cv.ShowImage('Drawing', blink)

tecla = -1
while (tecla < 0):
    ni.wait_any_update_all()
    imagem = video.get_raw_image_map_bgr()
    processa_frame(imagem)
    altera_quadro()

    tecla = cv.WaitKey(1)
cv.DestroyAllWindows()


