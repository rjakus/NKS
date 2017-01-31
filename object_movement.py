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

profile_cascade = cv2.CascadeClassifier('lbpcascade_profileface2.xml')
face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')

#import scroll

pyautogui.FAILSAFE = False
SCREEN_X, SCREEN_Y = pyautogui.size()

print SCREEN_Y
# construct the argument parse and parse the arguments


# define the lower and upper boundaries of the "green"
# ball in the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
#pts = deque(maxlen=args["buffer"])
#qqvvvvbqqcounter = 0
(dX, dY) = (0, 0)

scroll=False


camera = cv2.VideoCapture(0)

# keep looping
while True:
	# grab the current frame
    (grabbed, frame) = camera.read()
    frame = imutils.resize(frame, width=640)
    frame = imutils.resize(frame, height=480)

    CAMERA_Y, CAMERA_X, channels = frame.shape
   # print CAMERA_X, CAMERA_Y
    
   # print SCREEN_X, SCREEN_Y
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    profile = profile_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x2,y2,w2,h2) in profile:
            cv2.rectangle(frame, (x2,y2), (x2+w2,y2+h2), (0,255,0),2)
            roi_gray = gray[y2:y2+h2, x2:x2+w2]
            roi_color = frame[y2:y2+h2, x2:x2+w2]
            
            scroll=True
            

	# resize the frame, blur it, and convert it to the HSV
	# color space
    
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
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
 
        #print y
         
        
    
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
            #pts.appendleft(center)
            pyautogui.moveTo(mouse_x, mouse_y)
            

	# show the movement deltas and the direction of movement on
	# the frame
  

	# show the frame to our screen and increment the frame counter
    rimg=cv2.flip(frame,1)
    cv2.imshow("Frame", rimg)
    key = cv2.waitKey(1) & 0xFF
   # counter += 1

	# if the 'q' key is pressed, stop the loopbbbvvvvcvbvvvvvvvv
    if key == ord("q"):
        break
    
    elif key == 118:
        print "tu sam"
        pyautogui.click(button='left')
        
    elif key == ord("b"):
        pyautogui.click(button='right')
        
    elif scroll == True:
        ###############################################################
    
   #     face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
   #     profile_cascade = cv2.CascadeClassifier('lbpcascade_profileface2.xml')
        
        browser = webdriver.Firefox()
        #browser.get('http://www.riteh.uniri.hr')
        
       # cap = cv2.VideoCapture(0)
        
        trenutni = 0
        prethodni = 0
        tabs = 0
        activeTab = 0
        
        detekcija_frontal=False
        detekcija_profila=False
    
    
        while True:
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
        
            cv2.imshow('frame',img)
            k = cv2.waitKey(30) & 0xff
            if k == ord("q"):
                scroll=False
                browser.close()
                cv2.destroyAllWindows()
                break  
            #elif k == 32:
             #   return        
    ################################################################
     #   scroll.start()
    
    
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()