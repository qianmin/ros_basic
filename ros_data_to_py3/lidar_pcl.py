#! /usr/bin/env python3
import roslib
import rospy
from sensor_msgs.msg import PointCloud2,PointCloud
from sensor_msgs.msg import Image
from ros_numpy import msgify
from ros_numpy import numpify

import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')

import os
import time
import cv2
import torch
import pcl
import pcl.pcl_visualization
import numpy as np
from numpy_pc2 import pointcloud2_to_xyz_array,array_to_xyz_pointcloud2

def pc2_to_N3(data):
    pointXYZ = pointcloud2_to_xyz_array(data, remove_nans=True)
    #Nx4
    np_array=pointXYZ[:,:3]
    #Nx3
    d=np_array.astype(np.float32)
    return d

def cloud_to_pc2(data):
    out_array=data.to_array()
    out=array_to_xyz_pointcloud2(out_array,frame_id='laser_link')
    return out


def pc2_callback(pc2data):
    d=pc2_to_N3(pc2data)


    p=pcl.PointCloud()
    p.from_array(d)
    #$$$$$$$$$$$$  add your process of pcl here
    #$$$$$$$$$$$$  add your process of pcl here


    # filter
    passthrough = p.make_passthrough_filter()
    passthrough.set_filter_field_name("z")
    passthrough.set_filter_limits(0.0, 0.5)
    # //pass.setFilterLimitsNegative (true)
    cloud_filtered = passthrough.filter()


    #$$$$$$$$$$$
    #$$$$$$$$$$$
    #$$$$$$$$$$$
    #<PointCloud of 56846 points>
    pc2_out=cloud_to_pc2(cloud_filtered)
    pc2_pub.publish(pc2_out)
    


if __name__ == '__main__':
    rospy.init_node('convert')
    
    image_topic = "/usb_cam/image_raw"
    pc2_topic = "/lslidar_point_cloud"
    rospy.Subscriber(pc2_topic, PointCloud2, pc2_callback,queue_size=1,buff_size=52428800)
    pc2_pub = rospy.Publisher('/numpy_pc2_xyz_pointcloud2', PointCloud2, queue_size=1)

    rospy.spin()
