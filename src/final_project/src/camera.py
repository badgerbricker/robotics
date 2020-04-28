#!/usr/bin/env python

import rospy
import numpy as np
import cv2
from final_project.msg import position_msg
from armrob_util.msg import ME439WaypointXYZ

from cv_bridge import CvBridge 
from sensor_msgs.msg import Image

global previous_data

def scale_to_robot(x,y):
	#convert mm to m
	#robot length is 0.27 meters
	#arm length 0.7 meters
	x=x/1000.0
	y=y/1000.0
	return (x/0.7)*0.27, (y/0.7)*0.27 


def find_center(corner):
	x_mid=0
	y_mid=0
	if(corner[0][0][0]>corner[0][2][0]):
		x_mid=corner[0][2][0]+abs(corner[0][0][0]-corner[0][2][0])/2.0
	elif(corner[0][0][0]<corner[0][2][0]):
		x_mid=corner[0][0][0]+abs(corner[0][0][0]-corner[0][2][0])/2.0
	else:
		x_mid=corner[0][0][0]

	if(corner[0][3][1]>corner[0][1][1]):
		y_mid=corner[0][1][1]+abs(corner[0][1][1]-corner[0][3][1])/2.0
	elif(corner[0][3][1]<corner[0][1][1]):
		y_mid=corner[0][3][1]+abs(corner[0][1][1]-corner[0][3][1])/2.0
	else:
		y_mid=corner[0][3][1]

	'''
	x_mid=corner[0][0][0]
	x_mid+=(corner[0][1][0]-corner[0][0][0])

	y_mid=corner[0][0][1]
	y_mid+=(corner[0][3][1]-corner[0][0][1])
	'''
	return int(x_mid),int(y_mid)

def world_frame(corner,image):
	x_distance=abs(corner[0][0][0]-corner[0][1][0])
	y_distance=abs(corner[0][0][1]-corner[0][1][1])

	h=np.sqrt(y_distance**2+x_distance**2)
	scale=100.0/h #100mm square

	x_center,y_center = find_center(corner)

	x_center*=scale
	y_center*=scale

	x_center, y_center = scale_to_robot(x_center,y_center)

	return [x_center,y_center]

def detect_aruco(frame, dictionary, parameters):
	markercorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame,dictionary,parameters=parameters)
	hand_loc=[0,0]
	shoulder_loc=[0,0]
	global previous_data
	final=previous_data
	if(len(markercorners)>1):
		cv2.aruco.drawDetectedMarkers(frame, markercorners, markerIds)
		corner_num=0
		hand_loc_pix=[0,0]
		shoulder_loc_pix=[0,0]

		while corner_num < len(markercorners):
			
			if(markerIds[corner_num]==30):
				hand_loc=world_frame(markercorners[corner_num],frame)
				hand_loc_pix = find_center(markercorners[corner_num])
			if(markerIds[corner_num]==10):
				shoulder_loc=world_frame(markercorners[corner_num],frame)
				shoulder_loc_pix = find_center(markercorners[corner_num])
			corner_num+=1

		if(hand_loc!=[] and shoulder_loc!=[]):
			frame =cv2.line(frame, (hand_loc_pix[0],hand_loc_pix[1]), (shoulder_loc_pix[0],shoulder_loc_pix[1]),(0,0,255),5)
			final[0]=abs(hand_loc[0]-shoulder_loc[0])
			final[2]=abs(hand_loc[1]-shoulder_loc[1])
			previous_data=final

	return final, frame



def start_node():
	#ros node setup
	pub = rospy.Publisher('waypoint_xyz',ME439WaypointXYZ, queue_size=10)
	img_pub = rospy.Publisher('image_data',Image, queue_size=10)
	rospy.init_node("camera_tracker", anonymous=False)
	rate = rospy.Rate(10) #10Hz

	#use build in camera 0
	cap = cv2.VideoCapture(0)

	#Aruco setip
	dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
	parameters = cv2.aruco.DetectorParameters_create()
	bridge = CvBridge()

	average_count=0
	avg_data=[0.1,0,0.2]
	global previous_data
	previous_data=[0.1,0,0.2]

	while not rospy.is_shutdown():
		#get frame
		ret, frame = cap.read()
		aruco_loc, frame = detect_aruco(frame, dictionary, parameters)

		#prepare for average
		avg_data=aruco_loc
		#avg_data[0]+=aruco_loc[0]
		#avg_data[2]+=aruco_loc[2]

		# Display the resulting frame
		cv_image = bridge.cv2_to_imgmsg(frame,"bgr8")
		img_pub.publish(cv_image)

		average_count+=1
		#average data over last 15 frames
		if(average_count>=15):
			#avg_data[0]/=average_count
			#avg_data[2]/=average_count
			msg_out = ME439WaypointXYZ()

			#limit the waypoint
			#avg_data[0]=min(avg_data[0],0.25)
			#avg_data[2]=min(avg_data[2],0.2)

			#publish message
			msg_out.xyz = np.array([avg_data[0],0,avg_data[2]])
			pub.publish(msg_out)
			previous_data= [avg_data[0],0,avg_data[2]]
			average_count=0

		rate.sleep()

	cap.release()
	cv2.destroyAllWindows()

if __name__=='__main__':
	try:
		start_node()
	except rospy.ROSInterruptException:
		#comments
		pass
	