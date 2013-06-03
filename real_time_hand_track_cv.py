#!/usr/bin/python
from openni import *
import cv2.cv as cv

cv.NamedWindow('Video',1)
cv.MoveWindow('Video',0,0)
cv.NamedWindow('Profundidade',1)
cv.MoveWindow('Profundidade',650,0)

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

depth.alternative_view_point_cap.set_view_point(video)

gesture_generator = GestureGenerator()
gesture_generator.create(ni)
gesture_generator.add_gesture('Wave')
centro = (0,0)

hands_generator = HandsGenerator()
hands_generator.create(ctx)

ctx.start_generating_all()

def gesture_detected(src, gesture, id, end_point):
    hands_generator.start_tracking(end_point)

def gesture_progress(src, gesture, point, progress): pass

def create(src, id, pos, time):
    return 

def update(src, id, pos, time):
    global centro
    centro = (int(pos[0]), int(pos[1]))

def destroy(src, id, time):
    return

gesture_generator.register_gesture_cb(gesture_detected, gesture_progress)
hands_generator.register_hand_cb(create, update, destroy)

def processa_frame(imagem):
    cv.SetData(imagem_cv, imagem)
    cv.Flip(imagem_cv,imagem_cv,1)
    cv.Circle(imagem_cv, centro, 16, cv.CV_RGB(0, 0, 255), 2, cv.CV_AA, 0)
    cv.ShowImage('Video', imagem_cv)

def processa_profundidade(imagem):
    cv.SetData(depth_cv, imagem)
    cv.Flip(depth_cv,depth_cv,1)
    cv.ShowImage('Profundidade', depth_cv)

tecla = -1
while (tecla < 0):
    nRetVal = ctx.wait_any_update_all
    processa_video(video.get_synced_image_map_bgr())
    processa_profundidade(depth.get_raw_depth_map_8())

    tecla = cv.WaitKey(1)
cv.DestroyAllWindows()


