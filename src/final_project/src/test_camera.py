#!/usr/bin/env python

import numpy as np
import cv2

cap = cv2.VideoCapture(0)
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters_create()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    markercorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame,dictionary,parameters=parameters)
 
    if(len(markercorners)>0):
    	cv2.aruco.drawDetectedMarkers(frame, markercorners, markerIds)
	    #for rect in markercorners:
	    #	cv2.rectangle(frame,rect[0],rect[2],(0,0,255),15)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()