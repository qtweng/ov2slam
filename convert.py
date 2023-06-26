import time, sys, os
from ros import rosbag
import roslib, rospy
roslib.load_manifest('sensor_msgs')
from sensor_msgs.msg import Image

from cv_bridge import CvBridge
import cv2

TOPIC = '/cam0/image_raw'

# depart1
# vid_start_timestamp = 41772481
# vid_end_timestamp = 100775484 
# timestamps = list(range(vid_start_timestamp, vid_end_timestamp, 16667))[:-16]

# run1
# vid_start_timestamp = 162782611
# vid_end_timestamp = 314795105 
# timestamps = list(range(vid_start_timestamp, vid_end_timestamp, 16667))

# depart2
# vid_start_timestamp = 329801481
# vid_end_timestamp = 404014603 
# timestamps = list(range(vid_start_timestamp, vid_end_timestamp, 16667))[:-7]

# run2
vid_start_timestamp = 415805498
vid_end_timestamp = 571820520 
timestamps = list(range(vid_start_timestamp, vid_end_timestamp, 16667))[:-36]

def CreateVideoBag(videopath, bagname):
    '''Creates a bag file with a video file'''
    bag = rosbag.Bag(bagname, 'w')
    cap = cv2.VideoCapture(videopath)
    cb = CvBridge()
    ret = True
    frame_id = 0
    
    prop_fps = 60
    
    while(ret):
        ret, frame = cap.read()        
        if not ret:
            break
        frame = cv2.resize(frame, (752,480))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # stamp = rospy.Time.from_sec(time.time())
        # stamp = rospy.Time.from_sec(curTime + (float(frame_id) / prop_fps))
        stamp = rospy.Time.from_sec(timestamps[frame_id] / 1e6)
        frame_id += 1
        image = cb.cv2_to_imgmsg(frame, encoding="mono8")
        image.header.stamp = stamp
        image.header.frame_id = "camera"
        bag.write(TOPIC, image, stamp)
    cap.release()
    bag.close()


if __name__ == "__main__":
    if len( sys.argv ) == 3:
        CreateVideoBag(*sys.argv[1:])
    else:
        print( "Usage: video2bag videofilename bagfilename")