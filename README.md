# Group 14 ME 439 UW Madison Spring 2020 Final Project
This is the catkin_ws folder. Must have ROS, OpenCV, and Python to run this program.

## Camera Semgentation
All image handling is done in the node "camera_tracker". This node takes in images from a build in camera and detects the location of three ArUco markers, one for the background that will enable y distance, one for the elbow joint and one for the hand. This xyz data of each location will be used to calculate robot invers kinematics in a yet to be determined manner.