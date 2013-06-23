#!/usr/bin/python
# -*- coding: utf-8 -*- 
from openni import *
from cv2 import *
import numpy as np
from scipy import weave

joints = (SKEL_HEAD, SKEL_LEFT_ELBOW, SKEL_LEFT_FOOT, SKEL_LEFT_HAND, SKEL_LEFT_HIP, SKEL_LEFT_KNEE, SKEL_LEFT_SHOULDER, SKEL_NECK, SKEL_RIGHT_ELBOW, SKEL_RIGHT_FOOT, SKEL_RIGHT_HAND, SKEL_RIGHT_HIP, SKEL_RIGHT_KNEE, SKEL_RIGHT_SHOULDER, SKEL_TORSO)
# SKEL_LEFT_ANKLE, SKEL_LEFT_COLLAR, SKEL_LEFT_FINGERTIP, SKEL_LEFT_WRIST, SKEL_RIGHT_ANKLE, SKEL_RIGHT_COLLAR, SKEL_RIGHT_FINGERTIP, SKEL_RIGHT_WRIST, SKEL_WAIST

pose_to_use = 'Psi'

imagem_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)
imagem_binaria = np.zeros((480,640))

fonte_do_texto = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.7, 0.7, 0, 1, 4)

cv.NamedWindow('Video',1)
cv.MoveWindow('Video',0,0)
cv.NamedWindow('Binária',1)
cv.MoveWindow('Binária',720,0)

ctx = Context()
ctx.init()
ctx.open_file_recording("MeuVideo.oni")

video = ctx.find_existing_node(NODE_TYPE_IMAGE)
depth = ctx.find_existing_node(NODE_TYPE_DEPTH)

user = UserGenerator()
user.create(ctx)

skel_cap = user.skeleton_cap
pose_cap = user.pose_detection_cap

def new_user(src, id):
    print "1/4 User {} detected. Looking for pose..." .format(id)
    pose_cap.start_detection(pose_to_use, id)

def pose_detected(src, pose, id):
    print "2/4 Detected pose {} on user {}. Requesting calibration..." .format(pose,id)
    pose_cap.stop_detection(id)
    skel_cap.request_calibration(id, True)

def calibration_start(src, id):
    print "3/4 Calibration started for user {}." .format(id)

def calibration_complete(src, id, status):
    if status == CALIBRATION_STATUS_OK:
        print "4/4 User {} calibrated successfully! Starting to track." .format(id)
        skel_cap.start_tracking(id)
    else:
        print "ERR User {} failed to calibrate. Restarting process." .format(id)
        new_user(user, id)

def lost_user(src, id):
    print "--- User {} lost." .format(id)

# Register them
user.register_user_cb(new_user, lost_user)
pose_cap.register_pose_detected_cb(pose_detected)
skel_cap.register_c_start_cb(calibration_start)
skel_cap.register_c_complete_cb(calibration_complete)

# Set the profile
skel_cap.set_profile(SKEL_PROFILE_ALL)

# Start generating
ctx.start_generating_all()

def c_tuple_to_image(tupla, array):
    assert(type(tupla) == type(()))
    assert(type(array) == type(np.array([])))

    codigo_em_c = """
            int i, j;
            for (i = 0; i < 480; i++){
              for (j = 0; j < 640; j++){
                if (tupla[j + i*640] == 1){
                  array[j + i*640] = 255;
                }
                else{
                  array[j + i*640] = 0;
                }
              }
            }
           """
    return weave.inline(codigo_em_c, ['tupla', 'array'])

tecla = -1
while (tecla < 0):
    ctx.wait_one_update_all(depth)
    imagem = video.get_raw_image_map_bgr()
    cv.SetData(imagem_cv, imagem)

    if user.users != []:
      id = user.users[0]
      contorno = user.get_user_pixels(id)
      c_tuple_to_image(contorno, imagem_binaria)
      #for i in xrange(480):
      #  for j in xrange(640):
      #    if contorno[j + i*640] == 1:
      #      imagem_binaria[i,j] = 255
      #    else:
      #      imagem_binaria[i,j] = 0
      #points = []
      #if skel_cap.is_tracking(id):
      #    for joint in joints:
      #      points.append(skel_cap.get_joint_position(id, joint).point)

      #points = depth.to_projective(points)
      #for point in points:
        #cv.Circle(imagem_cv, (int(point[0]),int(point[1])), 4, cv.CV_RGB(0, 0, 100), -1, cv.CV_AA, 0)

    cv.ShowImage('Video', imagem_cv)

    imshow('Binária',imagem_binaria)
    tecla = cv.WaitKey(1)
cv.DestroyAllWindows()
