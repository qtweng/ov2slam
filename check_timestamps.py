import time, sys, os
from ros import rosbag
import roslib, rospy
roslib.load_manifest('sensor_msgs')
from sensor_msgs.msg import Image

from cv_bridge import CvBridge
import cv2

topics = ['/cam0/image_raw']

i = 0

# for topic, msg, t in rosbag.Bag("temp.bag").read_messages():
for topic, msg, t in rosbag.Bag("4-data.bag").read_messages():
    if topic in topics:
        i += 1
        print(t)
        
        if i >= 10:
            quit()