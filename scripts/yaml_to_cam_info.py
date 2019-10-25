#!/usr/bin/env python
import rospy
import yaml
from sensor_msgs.msg import CameraInfo

class yamlPublisher:

    def __init__(self):

        self.file_name = rospy.get_param("file_name", "/home/prashant/.ros/camera_info/rgb_Astra_Orbbec.yaml")
        self.camera_info_msg = CameraInfo()
        self.publisher = rospy.Publisher("camera_info", CameraInfo, queue_size=10)
        self.yaml_to_msg()
        print(self.file_name)

    def yaml_to_msg(self):

        with open(self.file_name, "r") as file_handle:
            calib_data = yaml.load(file_handle)
        self.camera_info_msg.width = calib_data["image_width"]
        self.camera_info_msg.height = calib_data["image_height"]
        self.camera_info_msg.K = calib_data["camera_matrix"]["data"]
        self.camera_info_msg.D = calib_data["distortion_coefficients"]["data"]
        self.camera_info_msg.R = calib_data["rectification_matrix"]["data"]
        self.camera_info_msg.P = calib_data["projection_matrix"]["data"]
        self.camera_info_msg.distortion_model = calib_data["distortion_model"]

    def spin(self):
        self.publisher.publish(self.camera_info_msg)


if __name__ == "__main__":
    rospy.init_node("camera_info_publisher", anonymous=True)
    rate = rospy.Rate(10)

    cam_pub = yamlPublisher()

    while not rospy.is_shutdown():
        cam_pub.spin()
        rate.sleep()





