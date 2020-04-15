#!/usr/bin/env python

import rospy
import numpy as np
import cv2 as cv
from final_project.msg import position_msg

def segment(frame):
	return None

def get_frame(cap):

	
	ret, frame = cap.read()

	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

	return gray

def start_node():
	pub = rospy.Publisher('segmented_pos_data',position_msg, queue_size=10)
	rospy.init_node("camera_tracker", anonymous=False)
	rate = rospy.Rate(10) #10Hz
	cap = cv.VideoCapture(0)

	while not rospy.is_shutdown():
		frame = get_frame(cap)
		location = segment(frame)
		msg_out = position_msg()
		msg_out.x = 0
		msg_out.y = 0
		msg_out.z = 0

		pub.publish(msg_out)
		rate.sleep()

if __name__=='__main__':
	try:
		start_node()
	except rospy.ROSInterruptException:
		#comments
		pass
	