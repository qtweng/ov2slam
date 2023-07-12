## Prerequisites

### Without Docker
Install ROS (tests have been done with ROS Melodic): http://wiki.ros.org/melodic/Installation

Make sure to source ROS when opening a new terminal (or add to .bashrc):

	source /opt/ros/melodic/setup.bash

Build OV2SLAM by following the instructions at https://github.com/ov2slam/ov2slam . Once built, source the setup.bash file for the catkin workspace:

	$ source devel/setup.bash

Install necessary Python packages (change package names to match ROS version):

	$ sudo apt install ros-melodic-roslib ros-melodic-rospy ros-melodic-cv-bridge
	
To plot the trajectory and calculate ATE, tools from the following library can be used: https://github.com/MichaelGrupp/evo/

### With Docker
	
	$ docker build -t ov2slam .
	$ docker run -it --name ov2slam -v path/to/this/repo:path/on/docker ov2slam

	# source /opt/ros/melodic/setup.bash
	# source /root/catkin_ws/devel/setup.bash

To perform camera calibration, download and install Matlab (tested with version R2023a): https://www.mathworks.com/products/matlab.html

## Convert video files to ROS bags

The frames from an input video can be stored in a bag file by running the convert.py file like the following:

	$ python convert.py <input_video.mp4> <output.bag>
	
Note that the input and output file names can be changed as needed.

## Camera Calibration

Matlab has a "Camera Calibrator" app that can be used to calculate the intrinsic and extrinsic parameters needed by OV2SLAM. It can be accessed from "Apps -> Image Processing and Computer Vision" in the main Matlab IDE, assuming it does not appear in the default app list.

To perform the calibration with the tool, the following steps need to be done. Note that the same steps can be found at the following link: https://www.mathworks.com/help/vision/ug/camera-calibration-using-apriltag-markers.html

- Resize the calibration images to the desired dimensions (e.g. 752x480) by modifying and running the following script:
	
	$ cd calibration/
	$ python img_resizes.py # modify line 10 with the desired resolution
	
- Open the Camera Calibrator app in Matlab, and add the images from the calibration_resized folder.
- In the "Image and Pattern Properties" window, change the pattern to "AprilTag" (requires the MyCustomAprilTagPatternDetector.m file from the mathworks link above).
- Change to the following properties, if necessary:

	Tag Family => "tag36h11"
	Square Size => 63.5 millimeters
	Number of Rows => 5
	Number of Columns => 8
	
- Choose "Ok" and let the images load.
- Perform the "Calibrate" action (green arrow at the top of the Camera Calibrator window).
- When finished, export the parameters to the Matlab IDE window (far left green checkpoint in the Camera Calibrator window). The variable name can be changed, but for the purposes of these steps we assume the name "Params".
- From the Matlab IDE window, format all output to use decimal points and print the intrinsic parameters:

	>> format long g
	>> Params.Intrinsics
	
This will give output like the following that contains all necessary intrinsic parameters:

	ans = 

		cameraIntrinsics with properties:

				 FocalLength: \[Camera.fxl Camera.fyl\]
			  PrincipalPoint: \[Camera.cxl Camera.cyl\]
				   ImageSize: \[Height Width\]
			RadialDistortion: \[Camera.k1l Camera.k2l\]
		TangentialDistortion: \[Camera.p1l Camera.p2l\]
						Skew: 0
						   K: \[3×3 double\]
						  
Likewise, the extrinsic matrix can be printed as follows. Note that each calibration image we have its own matrix, but typically matrices from images that are more front and center tend to perform better. For example, we use the transformation matrix for the A025_C001_0101OH.0000056.jpg image.

	>> Params.PatternExtrinsics.A
	...
	ans =

         0.999983266961351      -0.00300854249095237       0.00494110001763764         -493.642881053884
       0.00299061030481381         0.999988930257324       0.00363257660867245          -269.16403484092
      -0.00495197408201073      -0.00361773891999781         0.999981194782081          1842.16176154069
                         0                         0                         0                         1
	...
	
The selected matrix can then be coped directly to the body_T_cam0->data field in the OV2SLAM yaml parameter file (note that commas need to be added after each matrix value).

Once done, the camera parameters in the OV2SLAM file will be successfully updated. Note that the same process can also be done separately for the Camera.__r parameters if a second camera is used.

## Running OV2SLAM

Open a terminal and launch OV2SLAM with the following command:

	$ rosrun ov2slam ov2slam_node nasa.yaml
	
Note that the yaml parameters filename can be changed as needed.

In a separate terminal play the target bag file:

	$ rosbag play <output.bag>
	
Once started, OV2SLAM will process the video frames from the bag file until they have all been played. When finished, OV2SLAM will output the generated trajectory and exit (or get aborted).

In particular, three trajectory text files get generated. In our case, the "ov2slam_traj.txt" file can be used for plotting and metric calculation.

To plot the generated trajectory without a ground truth reference:

	$ evo_traj tum ov2slam_traj.txt --plot_mode=xz --plot
	
To plot the generated trajectory with a ground truth reference:
	$ evo_traj tum ov2slam_traj.txt --ref <ground.txt> -a --plot_mode=xy --plot
	
Also, the plots can be saved by using the "--save_plot" command line argument, like the following:

	$ evo_traj tum ov2slam_traj.txt --plot_mode=xz --save_plot=gen.pdf
	
Note that the evo_traj tools uses the filenames for the labels in the legend, so you will probably need to copy or rename the ov2slam_traj.txt file, especially if multiple trajectory files are given.
	
To calculate the ATE of the generated trajectory (a ground truth must be given):

	$ evo_ape tum ground.txt ov2slam_traj.txt -a