from __future__ import print_function

import rosbag
import os
import pickle

import sys
 

def build_camera_position_and_cloud(bag):
    data = sorted(bag.read_messages(topics=['/tango_pose', '/point_cloud']),
                  key = lambda x: x[2]) #Sort by time
    assoc = []
    for i, msg in enumerate(data):
        if msg.topic != "/point_cloud":
            continue
        back_i = fwd_i = i
        while (data[back_i].topic != '/tango_pose'):
            back_i -= 1
        prev = data[back_i]
        while (data[fwd_i].topic != '/tango_pose'):
            fwd_i -= 1
        nxt = data[fwd_i]
        
        if (msg.timestamp - prev.timestamp) < (nxt.timestamp - msg.timestamp):
            assoc.append((prev, msg))
        else:
            assoc.append((nxt, msg))

    return assoc

if __name__ == "__main__":
    bname = sys.argv[1]
    #bags = [x for x in os.listdir(".") if x.endswith(".bag")] #argparse here
    print(bname)
    bag = rosbag.Bag(bname, 'r')
    assoc = build_camera_position_and_cloud(bag)
    with open(bname+".pcl-camera.pickle", 'w') as f:
        pickle.dump(assoc, f)


