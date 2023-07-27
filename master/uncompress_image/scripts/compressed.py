#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import rospy
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError

class ImageProcessor:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber('/compressed_camera_topic', CompressedImage,
                                          self.image_callback, queue_size=1, buff_size=52428800)
        self.image_pub = rospy.Publisher('/uncompressed_topic_image', Image, queue_size=1)

    def image_callback(self, compressed_image):
        try:
            # 将压缩的图像消息转换为OpenCV格式
            cv_image = self.bridge.compressed_imgmsg_to_cv2(compressed_image, desired_encoding="bgr8")
            if cv_image is None:
                rospy.logwarn("Failed to convert image to OpenCV format.")
                return
        except CvBridgeError as e:
            rospy.logerr(e)
            return

        # 检查图像维度
        if cv_image.shape[2] != 3:
            rospy.logwarn("Image has an invalid number of channels.")
            return

        try:
            # 将解压缩后的图像转换为ROS图像消息并发布
            ros_image = self.bridge.cv2_to_imgmsg(cv_image, encoding="bgr8")
            self.image_pub.publish(ros_image)
        except CvBridgeError as e:
            rospy.logerr(e)

def main():
    # 初始化ROS节点
    rospy.init_node('image_processing_node', anonymous=True)
    processor = ImageProcessor()
    rospy.loginfo("Image processing node initialization complete")
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == "__main__":
    main()
