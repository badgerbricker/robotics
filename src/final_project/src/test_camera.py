#!/usr/bin/env python



import numpy as np
import cv2


def find_center(corner):
	x_mid=corner[0][0][0]
	x_mid+=abs(corner[0][0][0]-corner[0][1][0])

	y_mid=corner[0][0][1]
	y_mid+=abs(corner[0][0][1]-corner[0][3][1])
	return x_mid,y_mid

def world_frame(corner,image):
	x_distance=abs(corner[0][0][0]-corner[0][1][0])
	y_distance=abs(corner[0][0][1]-corner[0][1][1])

	h=np.sqrt(y_distance**2+x_distance**2)
	scale=100.0/h #100mm square

	x_center,y_center = find_center(corner)

	x_center*=scale
	y_center*=scale

	return [x_center,y_center]

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
    	hand_loc=[]
    	shoulder_loc=[]
    	while corner_num < len(markercorners):
    		
    		if(markerIds[corner_num]==30):
    			hand_loc=world_frame(markercorners[corner_num],frame)
    		if(markerIds[corner_num]==10):
    			shoulder_loc=world_frame(markercorners[corner_num],frame)
    		corner_num+=1

		if(hand_loc!=[] and shoulder_loc!=[]):
			final=[0,0]
			final[0]=abs(hand_loc[0]-shoulder_loc[0])
			final[1]=abs(hand_loc[1]-shoulder_loc[1])
			print("X_loc: "+str(final[0]))
			print("Y_loc: "+str(final[1]))

			#TODO add a rounding/smoothings

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()