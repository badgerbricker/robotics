#!/usr/bin/env python

import rospy
import numpy as np
import cv2
from final_project.msg import position_msg
from armrob_util.msg import ME439WaypointXYZ

from cv_bridge import CvBridge 
from sensor_msgs.msg import Image


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

def detect_aruco(frame, dictionary, parameters):
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

	return final, frame



def start_node():
	#ros node setup
	pub = rospy.Publisher('segmented_pos_data',ME439WaypointXYZ, queue_size=10)
	img_pub = rospy.Publisher('image_data',Image, queue_size=10)
	rospy.init_node("camera_tracker", anonymous=False)
	rate = rospy.Rate(10) #10Hz

	#use build in camera 0
	cap = cv2.VideoCapture(0)

	#Aruco setip
	dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
	parameters = cv2.aruco.DetectorParameters_create()
	bridge = CvBridge()

	while not rospy.is_shutdown():
		#get frame
		ret, frame = cap.read()
		aruco_loc, frame = detect_aruco(frame, dictionary, parameters)

		# Display the resulting frame
		cv_image = bridge.cv2_to_imgmsg(frame,"bgr8")
		#cv_image = bridge.imgmsg_to_cv2(frame, "bgr8")
		img_pub.publish(cv_image)

		msg_out = ME439WaypointXYZ()
		msg_out.xyz = np.array([aruco_loc[0],0,aruco_loc[1]])

		# TODO:
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
	