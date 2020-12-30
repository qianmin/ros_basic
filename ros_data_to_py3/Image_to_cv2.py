#! /usr/bin/env python3
import roslib
import rospy
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import Image
from ros_numpy import msgify
from ros_numpy import numpify

import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')

import os
import time
import cv2
import torch


def image_callback(image):
    #Image->np.img
    np_image=numpify(image)
    #encoding np_img to cv2_img
    cv_image=cv2.cvtColor(np_image,cv2.cv2.COLOR_BGR2RGB)
    #encoding np_img to ros_Image_img
    ros_img=msgify(Image,np_image,encoding='rgb8')

    cv2.imshow('Image_2_cvImg',cv_image)
    cv2.waitKey(1)
    image_pub.publish(ros_img)
    print('img_pubed')

if __name__ == '__main__':
    rospy.init_node('convert')
    image_topic = "/usb_cam/image_raw"

    rospy.Subscriber(image_topic, Image, image_callback, queue_size=1, buff_size=52428800)

    image_pub = rospy.Publisher('/ros_numpy_img_out', Image, queue_size=1)
    rospy.spin()
