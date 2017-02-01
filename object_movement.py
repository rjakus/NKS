# USAGE
# python object_movement.py --video object_tracking_example.mp4
# python object_movement.py

#sudo pip install inputs

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyxhook
import time

profile_cascade = cv2.CascadeClassifier('lbpcascade_profileface2.xml')
face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
pyautogui.FAILSAFE = False

# This function is called every time a key is presssed
def kbevent(event):
    global running
    # space pressed
    if event.Ascii == 32:
        global space
        global scroll
        scroll = False
        browser.quit()
        cv2.destroyAllWindows()
        space = False
    # v pressed    
    elif event.Ascii == 118:
        pyautogui.click(button='left')
    # b pressed
    elif event.Ascii == 98:
        pyautogui.click(button='right')
    # q pressed
    elif event.Ascii == 113:
        running = False       

running = True
scroll = False
space = True
SCREEN_X, SCREEN_Y = pyautogui.size()
# define the lower and upper boundaries of the "green"
# ball in the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
(dX, dY) = (0, 0)
camera = cv2.VideoCapture(0)
# Create hookmanager
hookman = pyxhook.HookManager()
# Define our callback to fire when a key is pressed down
hookman.KeyDown = kbevent
# Hook the keyboard
hookman.HookKeyboard()
# Start our listener
hookman.start()
# keep looping
while running:
    # grab the current frame
    (grabbed, frame) = camera.read()
    frame = imutils.resize(frame, width=640)
    frame = imutils.resize(frame, height=480)

    CAMERA_Y, CAMERA_X, channels = frame.shape
      
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    profile = profile_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x2,y2,w2,h2) in profile:
        cv2.rectangle(frame, (x2,y2), (x2+w2,y2+h2), (0,255,0),2)
        roi_gray = gray[y2:y2+h2, x2:x2+w2]
        roi_color = frame[y2:y2+h2, x2:x2+w2]
        
        scroll=True
            
    # resize the frame and convert it to the HSV color
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color, then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        mouse_x= x*(2.215)
        mouse_x=1360-mouse_x
        mouse_y= y*(1.6)
       
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points 
            cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            pyautogui.moveTo(mouse_x, mouse_y)
           
    # show the frame to our screen and increment the frame counter
    rimg=cv2.flip(frame,1)
    cv2.imshow("Frame", rimg)
    cv2.waitKey(30) & 0xFF
        
    if scroll == True:
        browser = webdriver.Firefox()
        
        trenutni = 0
        prethodni = 0
        tabs = 0
        activeTab = 0
        
        detekcija_frontal=False
        detekcija_profila=False 
    
        while space:
            ret, img = camera.read()
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
                    browser.switch_to_window(browser.window_handles[activeTab])
                    
# cleanup the camera and close any open windows
hookman.cancel()
camera.release()
cv2.destroyAllWindows()