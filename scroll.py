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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import tkMessageBox
from Tkinter import *

face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
profile_cascade = cv2.CascadeClassifier('lbpcascade_profileface2.xml')

browser = webdriver.Firefox()
browser.get('http://www.riteh.uniri.hr')

cap = cv2.VideoCapture(0)

trenutni = 0
prethodni = 0
tabs = 0
activeTab = 0

detekcija_frontal=False
detekcija_profila=False

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayLeft = cv2.cvtColor(cv2.flip(img,1), cv2.COLOR_BGR2GRAY)
    
    face = face_cascade.detectMultiScale(gray, 1.3, 5)
    profile = profile_cascade.detectMultiScale(gray, 1.3, 5)
    profileLeft = profile_cascade.detectMultiScale(grayLeft, 1.3, 5)
    

    #Implementacija scrolla (pogled gore - dole)       
    for (x,y,w,h) in face:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        trenutni += 1
        detekcija_frontal = True
        detekcija_profila = False
        
        if (trenutni == 1):
            startx = x
            starty = y
    
    if (prethodni < trenutni):
        prethodni = trenutni
        #print "Detektirana glava "+ repr(trenutni) + " x:" + repr(x) + " y:" + repr(y)
        if(y < starty and y < starty-20):
            pyautogui.scroll(1)
        elif(y > starty and y > starty+20):
            pyautogui.scroll(-1)
    
    #Implementacija otvaranja taba (pogled u desno)
    for (x2,y2,w2,h2) in profile:
        cv2.rectangle(img, (x2,y2), (x2+w2,y2+h2), (0,255,0),2)
        roi_gray = gray[y2:y2+h2, x2:x2+w2]
        roi_color = img[y2:y2+h2, x2:x2+w2]

        detekcija_profila=True
        if(detekcija_frontal == True and detekcija_profila == True):
            detekcija_frontal=False            
            print "Detektiran desni profil"
            browser.execute_script("window.open('https://stackoverflow.com');")
            tabs = tabs + 1            
            activeTab = tabs
    
    #Implementacija izmjene (selekcije) tabova (pogled u lijevo)    
    for (x2,y2,w2,h2) in profileLeft:
        cv2.rectangle(img, (x2,y2), (x2+w2,y2+h2), (0,255,0),2)
        roi_gray = gray[y2:y2+h2, x2:x2+w2]
        roi_color = img[y2:y2+h2, x2:x2+w2]

        detekcija_profila=True
        if(detekcija_frontal == True and detekcija_profila == True):
            detekcija_frontal=False            
            print "Detektiran lijevi profil"
            if(activeTab-1 < 0):
                activeTab = tabs
            else:
                activeTab = activeTab - 1
            #browser.switch_to_window(browser.window_handles[activeTab])
            browser.switch_to_active_element()

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break  
    elif k == 116:
        print "Enzo"        
        
browser.close()
cap.release()
cv2.destroyAllWindows()
