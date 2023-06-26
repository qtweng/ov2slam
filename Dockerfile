FROM --platform=linux/arm64  ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && apt install nano curl lsb-release gnupg -y
RUN apt upgrade -y

RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -
RUN apt update && apt install ros-noetic-ros-base -y

RUN apt install ros-noetic-pcl-ros -y
RUN mkdir -p /root/catkin_ws/src
RUN apt install git libgoogle-glog-dev ros-noetic-roslib ros-noetic-rospy ros-noetic-cv-bridge ros-noetic-image-transport -y
RUN cd /root/catkin_ws/src; git clone https://github.com/ov2slam/ov2slam.git
RUN cd ~/catkin_ws/src/ov2slam; chmod +x build_thirdparty.sh; ./build_thirdparty.sh
RUN /bin/bash -c 'cd ~/catkin_ws; sed -i "s|set(WITH_OPENCV_CONTRIB ON)|set(WITH_OPENCV_CONTRIB OFF)|g" /root/catkin_ws/src/ov2slam/CMakeLists.txt; source /opt/ros/noetic/setup.bash; cd /root/catkin_ws; catkin_make --pkg ov2slam'
RUN source ~/catkin_ws/devel/setup.bash

RUN apt install python3-pip -y
RUN pip3 install evo --upgrade --no-binary evo