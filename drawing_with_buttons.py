#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from openni import *
import cv2.cv as cv

#Create and move the windows that will show the RGB camera and the Drawing
cv.NamedWindow('Video',1)
cv.MoveWindow('Video',0,0)
cv.NamedWindow('Drawing',1)
cv.MoveWindow('Drawing',640,0)

#Create the text font that will be used in texts showed at the RGB image 
fonte_do_texto = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.6, 0.6, 0, 1, 4)

#Create two 640x480 resolution, 8-bits depth, 3 channels images
quadro = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)
imagem_cv = cv.CreateImage((640,480), cv.IPL_DEPTH_8U, 3)

#Set ao pixels of the Drawing image to white
cv.Set(quadro, (255.0,255.0,255.0))

#Creates the dictionaries that will hold hands and buttons information
hands = {}
buttons_size = (100, 60)
buttons = {'White': {'color': cv.CV_RGB(255,255,255), 'start': (500, 30), 'end': (500 + buttons_size[0], 30 + buttons_size[1])},
          'Black': {'color': cv.CV_RGB(0,0,0), 'start': (500, 100), 'end': (500 + buttons_size[0], 100 + buttons_size[1])},
          'Red': {'color': cv.CV_RGB(255,0,0), 'start': (500, 170), 'end': (500 + buttons_size[0], 170 + buttons_size[1])},
          'Green': {'color': cv.CV_RGB(0,255,0), 'start': (500, 240), 'end': (500 + buttons_size[0], 240 + buttons_size[1])},
          'Blue': {'color': cv.CV_RGB(0,0,255), 'start': (500, 310), 'end': (500 + buttons_size[0], 310 + buttons_size[1])},
          }

#Initialize OpenNI
ni = Context()

#Using Xml file to set Mirroring = True
ni.init_from_xml_file("OpenniConfig.xml")
video = ni.find_existing_node(NODE_TYPE_IMAGE)
depth = ni.find_existing_node(NODE_TYPE_DEPTH)

#Initialize Gesture Recognition same ways as showed in OpenNI samples
gesture_generator = GestureGenerator()
gesture_generator.create(ni)
gesture_generator.add_gesture('Wave')
gesture_generator.add_gesture('Click')

hands_generator = HandsGenerator()
hands_generator.create(ni)

ni.start_generating_all()

# This method translate OpenNI coordinates do OpenCV coordinates
def translate_coordinates(openni_point):
  opencv_point = depth.to_projective([openni_point])
  return (int(opencv_point[0][0]), int(opencv_point[0][1]))

#This method returns true or false point is inside a button, will be used to check if a gesture click was inside any button
def overlap(point, button):
  global buttons
  return point[0] >= buttons[button]['start'][0] and point[0] <= buttons[button]['end'][0] and point[1] >= buttons[button]['start'][1] and point[1] <= buttons[button]['end'][1]

#Callback when a gesture is detected
def gesture_detected(src, gesture, id, end_point):
    global hands, buttons

    # If a click gesture is detected check if it is inside any button, if it is, all hands will have information about the name and color of that button or else change the boolean state of drawing (Start/Stop)
    if gesture == 'Click':
      no_button_clicked = True
      for button in buttons:
        if overlap(translate_coordinates(end_point), button):
          for id in hands:
            hands[id]['color']['name'] = button
            hands[id]['color']['cv'] = buttons[button]['color']
            hands[id]['drawing'] = False
            no_button_clicked = False
            break
      if no_button_clicked:
        for id in hands:
          hands[id]['drawing'] = not hands[id]['drawing']

    hands_generator.start_tracking(end_point)

#Callback called during gesture progress
def gesture_progress(src, gesture, point, progress): pass

#Callback when a new hand is detected, creates a hand with its default values.
def create(src, id, pos, time):
    global hands
    ponto = depth.to_projective([pos])
    centro = (int(ponto[0][0]), int(ponto[0][1])) 
    hands[id] = {'atual': centro, 'drawing': False, 'color': {'name': 'Choose a Color', 'cv': cv.CV_RGB(255,255,255)}}

#Callback called each frame after a hand is created
def update(src, id, pos, time):
    global hands
    hands[id]['anterior'] = hands[id]['atual'] #Hold previous position to draw a line between them
    hands[id]['atual'] = translate_coordinates(pos) #Holds that hand position

#Callback to delete a hand if it is not visible
def destroy(src, id, time):
    global hands
    del hands[id]

gesture_generator.register_gesture_cb(gesture_detected, gesture_progress)
hands_generator.register_hand_cb(create, update, destroy)

#This methods is called each frame and updates the Video RGB image
def processa_frame(imagem):
    #Converts Image from OpenNI to be shown in OpenCV
    cv.SetData(imagem_cv, imagem) 

    #Updates the Start/Stop text if the hand drawing boolean is true/false
    if hands:
      for id in hands:
        if hands[id]['drawing']:
          update_notification('Click to Stop Drawing')
        else:
          update_notification('Click to Start Drawing')

        #Updates text showed near the hands
        cv.PutText(imagem_cv, hands[id]['color']['name'], hands[id]['atual'] ,fonte_do_texto , cv.CV_RGB(255,255,255))

    #If no hand detected should ask the user to Wave.
    else:
      update_notification('Wave to Interact')

    #Draw Buttons in the Video RGB image
    for button in buttons:
      cv.Rectangle(imagem_cv, buttons[button]['start'], buttons[button]['end'] , buttons[button]['color'], -1, cv.CV_AA, 0)
    cv.ShowImage('Video', imagem_cv)

#Method that updates the Start/Stop drawing notification
def update_notification(text):
    cv.PutText(imagem_cv, text, (240,30) ,fonte_do_texto , cv.CV_RGB(255,255,255))

#Method that is called each frame and updates the drawing
def altera_quadro():
    #copy the drawing before drawing the user's hand circle
    blink = cv.CloneImage(quadro)

    # If any hands 
    if hands:

      #Draw circles in each hand detected
      for id in hands:
        cv.Circle(blink, hands[id]['atual'], 10, hands[id]['color']['cv'], -1, cv.CV_AA, 0)

        #If Hand is drawing, draw a line between their previous and actual position
        if hands[id]['drawing'] == True:
          cv.Line(quadro, hands[id]['anterior'], hands[id]['atual'], hands[id]['color']['cv'], 10, cv.CV_AA, 0) 

    #Show the Drawing with the circle where the hand is
    cv.ShowImage('Drawing', blink)

tecla = -1
# Loop that will stop if any key is pressed
while (tecla < 0):
    ni.wait_any_update_all()
    imagem = video.get_raw_image_map_bgr()
    processa_frame(imagem)
    altera_quadro()

    tecla = cv.WaitKey(1)

#Destroy all windows when loop finishes
cv.DestroyAllWindows()

#Save the Drawing in the local folder
cv.SaveImage("Drawing.jpg", quadro)
