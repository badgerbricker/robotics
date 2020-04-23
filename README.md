# Group 14 ME 439 UW Madison Spring 2020 Final Project
This is the catkin_ws folder. Must have ROS, OpenCV, and Python to run this program.

## Camera Segmentation
This section covers how the camera image is segmented and location data determined.

### ArUco setup
The code is capable of detecting ArUco codes 0-49. Id 10 is used for the shoulder, 20 for the elbow, and 30 for the hand. Currently none are used for the background.

### Distance calculations
The final x,y,z cordinate is calculated as the euclidean distance between the center of the shoulder Aruco marker and the hand Aruco marker. The world distance to pixel ratio is calculated using a ratio of the pixels comprising the edge of one Aruco to the actual size in mm of that Aruco. Each Aruco is 100mm on every side. This distance calculation is more accurate than previous ones. This pixel to real world distance is then used to convert the pixel distance betweent he Aruco markers to a distance vector. This distance data is packaged in a *ME439WaypointXYZ* message and published to the topic *segmented_pos_data* in the node *camera_tracker*. The distance data is averaged over the last 15 frames currently but that is subject to change. Assuming a standard 60 fps this average would be over 0.25 seconds.

##Viewing Segmented Images
ROS uses a different image format than OpenCV which detects the Aruco markers. In order to be able to see the images for debugging purposes they are published to the topic ~image_data~ as type *Image* from *sensor_msgs*, a standard ROS message. This image data can then be seen by issuing the 'rqt_image_view /image_data' command in the command line running ROS. This feature was added to the *arm_simulate_camera_controlled.launch* file.


## Networking
A laptop will run the ROS Master node to do the computer vision and decoding, then send the orientation information to the pi over a network connection.

Network Setup:
The pi must be configured to the master by setting environment variables. Get the IP address of the master machine (with "ip -br a"). On the pi, set a hostname for the IP address by adding "<IP_addr>	"master_hostname" to /etc/hosts with sudo. On the pi, run "export ROS_MASTER_URI=http://<master_hostname>:11311". Source this command with "source .bashrc".
Finally, run roscore on the master node. Use roswtf on the non-master to check connection or rosrun a program to check. The talker.y and listener.py in the network_test package can help verify connection.
This will likely be done in the launch file for the nodes running on the pi, but is also here for testing and clarity.

## ROS Structure

