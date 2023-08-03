FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && apt install nano vim curl lsb-release gnupg cmake g++ wget unzip -y
RUN apt upgrade -y

RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -

# Install ROS and OV2SLAM
RUN apt update && apt install ros-melodic-ros-base ros-melodic-pcl-ros git libgoogle-glog-dev ros-melodic-roslib ros-melodic-rospy ros-melodic-image-transport -y
RUN mkdir -p /catkin_ws/src
RUN cd /catkin_ws/src; git clone https://github.com/ov2slam/ov2slam.git

# OpenCV_contrib
RUN mkdir -p /opencv/build; cd /opencv; wget -O opencv.zip https://github.com/opencv/opencv/archive/3.4.zip; wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.4.zip; unzip opencv.zip; unzip opencv_contrib.zip;
RUN cd /opencv/build; cmake -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-3.4/modules ../opencv-3.4; cmake --build .; make -j4 install

# Install thirdparty
RUN cd /catkin_ws/src/ov2slam; chmod +x build_thirdparty.sh; ./build_thirdparty.sh

# Install openGV
RUN cd /catkin_ws/src/ov2slam/Thirdparty; git clone https://github.com/laurentkneip/opengv; cd opengv; mkdir build; cd build; cmake ..; make -j4 install

# cv-bridge
RUN cd /catkin_ws/src; git clone -b melodic https://github.com/ros-perception/vision_opencv.git

RUN /bin/bash -c 'cd /catkin_ws; source /opt/ros/melodic/setup.bash; cd /catkin_ws; catkin_make'

RUN apt install python3-pip -y
RUN pip3 install evo --upgrade --no-binary evo