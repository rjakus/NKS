# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 14:25:04 2017

@author: lenovo
"""

import numpy as np
import cv2
import math
import time
import pyautogui

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
#lbpcascade_frontalface
#haarcascade_frontalface_default
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

trenutni=0
prethodni=0

detekcija=False


while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
   # if (x and y is not 0 ):
   #     detekcija = True
     
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        trenutni+=1
        if (trenutni==1):
            startx=x
            starty=y
        
        
    if (prethodni < trenutni):
        prethodni=trenutni
        print "detektirana glava"+ repr(trenutni) + " " + repr(x) + " "+ repr(y)
        if(y<starty and y<starty-15):
            pyautogui.scroll(1)
        elif(y>starty and y>starty+15):
            pyautogui.scroll(-1)
  
    #    eyes = eye_cascade.detectMultiScale(roi_gray)
    #    for (ex,ey,ew,eh) in eyes:
    #        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()