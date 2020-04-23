#!/usr/bin/env python

import rospy
import numpy as np
import cv2
from final_project.msg import position_msg

def get_frame(cap):

	ret, frame = cap.read()

	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

	return gray


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

def detect_aruco(frame, dictionary, parameters, debug):
	markercorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame,dictionary,parameters=parameters)
	hand_loc=[0,0]
	shoulder_loc=[0,0]
	final=[0,0]
	if(len(markercorners)>0):
		cv2.aruco.drawDetectedMarkers(frame, markercorners, markerIds)
		corner_num=0

		while corner_num < len(markercorners):
			
			if(markerIds[corner_num]==30):
				hand_loc=world_frame(markercorners[corner_num],frame)
			if(markerIds[corner_num]==10):
				shoulder_loc=world_frame(markercorners[corner_num],frame)
			corner_num+=1

		if(hand_loc!=[] and shoulder_loc!=[]):
			final[0]=abs(hand_loc[0]-shoulder_loc[0])
			final[1]=abs(hand_loc[1]-shoulder_loc[1])

	#if(debug):
		# Display the resulting frame
	#	cv2.imshow('frame',frame)

	return final



def start_node():
	#ros node setup
	pub = rospy.Publisher('segmented_pos_data',position_msg, queue_size=10)
	rospy.init_node("camera_tracker", anonymous=False)
	rate = rospy.Rate(10) #10Hz

	#use build in camera 0
	cap = cv2.VideoCapture(0)

	#Aruco setip
	dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
	parameters = cv2.aruco.DetectorParameters_create()

	while not rospy.is_shutdown():
		#get frame
		ret, frame = cap.read()
		aruco_loc = detect_aruco(frame, dictionary, parameters, False)
		
		msg_out = position_msg()
		msg_out.x = aruco_loc[0]
		msg_out.y = -1
		msg_out.z = aruco_loc[1] 

		# TODO:
		#use array of float32 x,y,z  or use the ME439 armrob_util_message should be good with pull
		#add smoothing to the message. Average last 60? (one second)
		#find a way to add a debug window

		pub.publish(msg_out)
		rate.sleep()

	cap.release()
	cv2.destroyAllWindows()

if __name__=='__main__':
	try:
		start_node()
	except rospy.ROSInterruptException:
		#comments
		pass
	