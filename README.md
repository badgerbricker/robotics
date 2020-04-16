# Group 14 ME 439 UW Madison Spring 2020 Final Project
This is the catkin_ws folder. Must have ROS, OpenCV, and Python to run this program.

## Camera Semgentation
This section covers how the camera image is segmented and location data determined.
### ArUco setup
The code is capable of detecting ArUco codes 0-49. Id 10 is used for the shoulder, 20 for the elbow, and 30 for the hand. Currently none are used for the background
### Distance calculations
The distance of each Aruco is calculated by taking a ratio of the x,y pixel location to the total number of pixels in each direction then multiplying this ratio by the measured milimeter distance along the x and y axis as measured in real life and hard coded into the code. This is why it is ~critical~ that the person holding the Aruco items stand in the right side of the frame, opencv puts the origin of an image (0,0) at the top left from the camera's view.
