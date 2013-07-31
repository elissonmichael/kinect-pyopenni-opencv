#!/usr/bin/python
import pygame
from openni import *
import cv2
import numpy

def new_user(src, id):
  pose_cap.start_detection(pose_to_use, id)

def pose_detected(src, pose, id):
  pose_cap.stop_detection(id)
  skel_cap.request_calibration(id, True)

def calibration_start(src, id):
  pass

def calibration_complete(src, id, status):
  if status == CALIBRATION_STATUS_OK:
      skel_cap.start_tracking(id)
  else:
      new_user(user, id)

def lost_user(src, id):
  pass

def openni_to_pygame(imagem):
  imagem_cv = numpy.fromstring(imagem, dtype=numpy.uint8).reshape(480, 640, 3)
  cores_corrigidas = cv2.cvtColor(imagem_cv, cv2.cv.CV_BGR2RGB)
  return pygame.image.fromstring(cores_corrigidas.tostring(), (640,480), 'RGB', False)

def exibir(surface):
  screen.blit(surface, (0,0))

def imprimir_camisa(ponto):
  screen.blit(camisa, ponto)

ni = Context()
ni.init()
ni.open_file_recording("MeuVideo.oni")
depth = ni.find_existing_node(NODE_TYPE_DEPTH)
video = ni.find_existing_node(NODE_TYPE_IMAGE)
pose_to_use = 'Psi'
user = UserGenerator()
user.create(ni)
skel_cap = user.skeleton_cap
pose_cap = user.pose_detection_cap
user.register_user_cb(new_user, lost_user)
pose_cap.register_pose_detected_cb(pose_detected)
skel_cap.register_c_start_cb(calibration_start)
skel_cap.register_c_complete_cb(calibration_complete)
skel_cap.set_profile(SKEL_PROFILE_ALL)
ni.start_generating_all()

pygame.init()
screen = pygame.display.set_mode([640,480])
pygame.display.set_caption('Testando Overlay')

camisa = pygame.image.load('camisa.png').convert_alpha()
camisa = pygame.transform.scale(camisa, (100,100))

while True:
  ni.wait_one_update_all(depth)
  imagem = video.get_raw_image_map_bgr()
  exibir(openni_to_pygame(imagem))
  if user.users != []:
    id = user.users[0]
    if skel_cap.is_tracking(id):
      p = skel_cap.get_joint_position(id, SKEL_TORSO).point
      p = depth.to_projective([p])
      ponto = (p[0][0], p[0][1])
      imprimir_camisa(ponto)
  pygame.display.update()

#ni.stop_generating_all()
