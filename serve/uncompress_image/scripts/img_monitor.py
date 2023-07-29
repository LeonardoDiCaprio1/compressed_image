#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import CompressedImage
import time

class ImageReceiver:
    def __init__(self):
        self.image_count = 0
        self.start_time = time.time()
        self.running = True

    def image_callback(self, msg):
        self.image_count += 1

    def compute_transfer_rate(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        # 传输速率 = 图像计数 / 经过的时间
        transfer_rate = self.image_count / elapsed_time 
        rospy.loginfo(f"Image transfer rate: {transfer_rate} images/s")

        self.start_time = current_time  # 更新起始时间
        self.image_count = 0  # 重置图像计数

    def shutdown(self):
        self.running = False

def image_receiver():
    # 初始化ROS节点
    rospy.init_node('image_receiver', anonymous=True)

    receiver = ImageReceiver()
    # 订阅压缩图像话题
    rospy.Subscriber('/compressed_camera_topic', CompressedImage, receiver.image_callback)

    # 每5秒钟计算一次传输速率
    rate = rospy.Rate(0.2)
    while receiver.running and not rospy.is_shutdown():
        receiver.compute_transfer_rate()
        rate.sleep()

    rospy.on_shutdown(receiver.shutdown)

if __name__ == '__main__':
    image_receiver()
