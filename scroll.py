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

import webbrowser

import tkMessageBox
from Tkinter import *

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
#lbpcascade_frontalface
#haarcascade_frontalface_default
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
profile_cascade = cv2.CascadeClassifier('lbpcascade_profileface2.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

trenutni=0
prethodni=0

detekcija_frontal=False
detekcija_profila=False


while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    profile=profile_cascade.detectMultiScale(gray, 1.3, 5)
   # if (x and y is not 0 ):
   #     detekcija = True
    ###################################

    #######################################

      
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        trenutni+=1
        detekcija_frontal=True
        detekcija_profila=False
        
        if (trenutni==1):
            startx=x
            starty=y

  
        
    if (prethodni < trenutni):
        prethodni=trenutni
        print "detektirana glava"+ repr(trenutni) + " " + repr(x) + " "+ repr(y)
        if(y<starty and y<starty-20):
            pyautogui.scroll(1)
        elif(y>starty and y>starty+20):
            pyautogui.scroll(-1)
    
    #pogled u desno!!!!
    for (x2,y2,w2,h2) in profile:
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(0,255,0),2)
        roi_gray = gray[y2:y2+h2, x2:x2+w2]
        roi_color = img[y2:y2+h2, x2:x2+w2]

        detekcija_profila=True
        if(detekcija_frontal==True and detekcija_profila==True):
            detekcija_frontal=False            
            print "detektiran profil"
            webbrowser.open("http://google.hr", new=2)
    #    eyes = eye_cascade.detectMultiScale(roi_gray)
    #    for (ex,ey,ew,eh) in eyes:
    #        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break  
    elif k == 116:
        webbrowser.open("http://google.hr", new=2)

cap.release()
cv2.destroyAllWindows()
