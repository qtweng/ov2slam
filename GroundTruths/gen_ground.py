import numpy as np
import pandas as pd
import csv

########################################
# CHANGE BELOW VALUES AS NEEDED
########################################
# ground_csv = "depart1-ground.csv"
# ground_txt = "depart1-ground-reversed.txt"
# vid_start_timestamp = 41772481
# vid_end_timestamp = 100775484 
# vid_num_frames = 3525 # Add 1 to value in README
# times = list(range(vid_start_timestamp, vid_end_timestamp, 16667))[:-16]

# ground_csv = "run1-ground.csv"
# ground_txt = "run1-ground.txt"
# vid_start_timestamp = 162782611
# vid_end_timestamp = 314795105 
# vid_num_frames = 9121 # Add 1 to value in README
# times = list(range(vid_start_timestamp, vid_end_timestamp, 16667))

ground_csv = "depart2-ground.csv"
ground_txt = "depart2-ground-reversed.txt"
vid_start_timestamp = 329801481
vid_end_timestamp = 404014603 
vid_num_frames = 4446 # Add 1 to value in README
times = list(range(vid_start_timestamp, vid_end_timestamp, 16667))[:-7]

# ground_csv = "run2-ground.csv"
# ground_txt = "run2-ground.txt"
# vid_start_timestamp = 415805498
# vid_end_timestamp = 571820520 
# vid_num_frames = 9325 # Add 1 to value in README
# times = list(range(vid_start_timestamp, vid_end_timestamp, 16667))[:-36]

raw_data = pd.read_csv(ground_csv) # add "sep" argument if necessary

x_interp = np.interp(times, raw_data["localPos_ts"].values, raw_data["x"].values)
y_interp = np.interp(times, raw_data["localPos_ts"].values, raw_data["y"].values)
z_interp = np.interp(times, raw_data["localPos_ts"].values, raw_data["z"].values)

q0_interp = np.interp(times, raw_data["attitude_ts"].values, raw_data["q0"].values)
q1_interp = np.interp(times, raw_data["attitude_ts"].values, raw_data["q1"].values)
q2_interp = np.interp(times, raw_data["attitude_ts"].values, raw_data["q2"].values)
q3_interp = np.interp(times, raw_data["attitude_ts"].values, raw_data["q3"].values)

assert len(x_interp) == len (y_interp) == len(z_interp) == len(q0_interp) == \
       len(q1_interp) == len(q2_interp) == len(q3_interp)
       
# Reverse timestamps if necessary (e.g. for the depart runs)       
times.reverse()

ground_output = open(ground_txt, "w")
ground_output.write("# timestamp(s) tx ty tz qx qy qz qw\n")

for i in range(len(x_interp)-1):        # For loop for normal sets (run1, run2)
for i in range(len(x_interp)-1,0,-1):   # For loop for reversed sets (depart1, depart2)
    ground_output.write("{} {} {} {} {} {} {} {}\n".format(times[i]/1e6, \
                        x_interp[i], y_interp[i], z_interp[i], \
                        q0_interp[i], q1_interp[i], q2_interp[i], q3_interp[i]))
ground_output.close()
    