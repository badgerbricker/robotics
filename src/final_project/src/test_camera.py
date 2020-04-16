#!/usr/bin/env python



import numpy as np
import cv2


def find_center(corner):
	x_mid=corner[0][0][0]
	x_mid+=abs(corner[0][0][0]-corner[0][1][0])

	y_mid=corner[0][0][1]
	y_mid+=abs(corner[0][0][1]-corner[0][3][1])
	return x_mid,y_mid

def find_world_frame(pixel_x,pixel_y,frame):
	#adjustment assumes person stands under (0,0)
	#this is usually right side of frame left arm
	dimensions=frame.shape
	height=dimensions[0]
	width=dimensions[1]
	print("Height: "+str(height))
	print("Width: "+str(width))

	x_frame=(pixel_x/width)*1700 #estimated mm distance
	y_frame=(pixel_y/height)*1350 #mm distance

	return x_frame,y_frame

#def scale_to_robot_arm(x_shoulder, y_shoulder, x_hand, y_hand, frame):
#	return None

cap = cv2.VideoCapture(0)
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters_create()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    markercorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame,dictionary,parameters=parameters)
    #print(markercorners)
    #print()
 
    if(len(markercorners)>0):
    	cv2.aruco.drawDetectedMarkers(frame, markercorners, markerIds)
    	corner_num=0
    	while corner_num < len(markercorners):
    		if(markerIds[corner_num]==10):
    			X,Y=find_center(markercorners[corner_num])
    			x,y=find_world_frame(X,Y,frame)
    			print("Shoulder: "+str(x)+","+str(y)+" mm")
    		if(markerIds[corner_num]==20):
    			X,Y=find_center(markercorners[corner_num])
    			x,y=find_world_frame(X,Y,frame)
    			print("Elbow: "+str(x)+","+str(y)+" mm")
    		if(markerIds[corner_num]==30):
    			X,Y=find_center(markercorners[corner_num])
    			x,y=find_world_frame(X,Y,frame)
    			print("Hand: "+str(x)+","+str(y)+" mm")
    		corner_num+=1

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()