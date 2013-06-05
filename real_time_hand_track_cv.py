#!/usr/bin/python
from openni import *
import cv2.cv as cv

cv.NamedWindow('Video',1)
cv.MoveWindow('Video',0,0)
cv.NamedWindow('Profundidade',1)
cv.MoveWindow('Profundidade',650,0)
fonte_do_texto = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.7, 0.7, 0, 2, 8)

depth_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 1)
imagem_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)

ctx = Context()
ctx.init()

video = ImageGenerator()
video.create(ctx)
video.set_resolution_preset(RES_VGA)
video.fps = 30

depth = DepthGenerator()
depth.create(ctx)
depth.set_resolution_preset(RES_VGA)
depth.fps = 30

#depth.alternative_view_point_cap.set_view_point(video)

gesture_generator = GestureGenerator()
gesture_generator.create(ctx)
gesture_generator.add_gesture('Wave')
centro = (0,0)
coordenada_real = ''
coordenada_projecao = ''
gesto = False

hands_generator = HandsGenerator()
hands_generator.create(ctx)

ctx.start_generating_all()

def gesture_detected(src, gesture, id, end_point):
    global gesto
    gesto = True
    hands_generator.start_tracking(end_point)

def gesture_progress(src, gesture, point, progress): pass

def create(src, id, pos, time):
    return 

def update(src, id, pos, time):
    global centro, coordenada_real, coordenada_projecao
    coordenada_real = ''
    coordenada_projecao = ''
    ponto = depth.to_projective([pos])
    centro = (int(ponto[0][0]), int(ponto[0][1])) 
    coordenada_real = ', '.join(str(int(e)) for e in pos)
    coordenada_projecao = ', '.join(str(e) for e in centro)

def destroy(src, id, time):
    global gesto
    gesto = False

gesture_generator.register_gesture_cb(gesture_detected, gesture_progress)
hands_generator.register_hand_cb(create, update, destroy)

def processa_frame(imagem):
    cv.SetData(imagem_cv, imagem)
    if gesto == False:
      cv.PutText(imagem_cv, 'Acene para ser Rastreado!', (80,50) ,fonte_do_texto , cv.CV_RGB(0,0,0))
    cv.Circle(imagem_cv, centro, 16, cv.CV_RGB(0, 0, 255), 2, cv.CV_AA, 0)
    cv.PutText(imagem_cv, 'Real(mm): '+coordenada_real, (80,435) ,fonte_do_texto , cv.CV_RGB(255,255,255))
    cv.PutText(imagem_cv, 'Convertido(px): '+coordenada_projecao, (80,465) ,fonte_do_texto , cv.CV_RGB(255,255,255))
    cv.ShowImage('Video', imagem_cv)

def processa_profundidade(imagem):
    cv.SetData(depth_cv, imagem)
    #cv.Flip(depth_cv,depth_cv,1)
    cv.ShowImage('Profundidade', depth_cv)

tecla = -1
while (tecla < 0):
    nRetVal = ctx.wait_one_update_all(depth)
    processa_frame(video.get_synced_image_map_bgr())
    processa_profundidade(depth.get_raw_depth_map_8())

    tecla = cv.WaitKey(1)
cv.DestroyAllWindows()


