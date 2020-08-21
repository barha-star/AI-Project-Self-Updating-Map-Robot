#!/usr/bin/env python
import math
from std_msgs.msg import String
import cv2
import numpy as np
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry

def callback(x):
    pass

def sign(num):
    if num > 0:
        return 1
    else:
        return -1

def distance_dot2line(a, b, c, x0, y0): # x0과 y0 사이의 거리를 구한다. 
    distance = abs(x0*a + y0*b + c)/math.sqrt(a*a + b*b) # ax0 + by0 + c / 루트 a^2 + b^2
    sign_ = sign(x0*a + y0*b + c) * sign(a) # 직선과 a의 기울기 값으로 부호 판단 
    return sign_, distance

def distance_dot2dot(point1, point2): 
    return math.sqrt((point2[1] - point1[1]) * (point2[1] - point1[1]) + (point2[0] - point1[0]) * (point2[0] - point1[0]))

def centroid(arr, low_point, col_start, col_end): # openCV를 통하여 Line Detection을 한 다음 선이 아닌 부분의 가운데 위치를 찾는다.
    count = 0
    center_low = 0
    center_col = 0

    for i in range(col_start,col_end): # 한 열의 시작과 끝 부분 동안
        if arr[low_point][i] == 255: # 한 pixel이 255 즉, 검은색이라면 
            center_col = center_col + i 
            count = count + 1
        i += 4 # 다음 pixel 값은 +4 이므로 

    center_low = low_point # 중심 행
    center_col = center_col / count # 중심 열
    return center_low, center_col



class Lane_tracer():
    def __init__(self):

        self.selecting_sub_image = "raw"  # you can choose image type "compressed", "raw" - raw은 이미지 센서로부터 최소한으로 처리한 데이터
        self.image_show = 'off'  # monitering image on off

        # subscribers
        if self.selecting_sub_image == "compressed":
            self._sub_1 = rospy.Subscriber('/image_birdeye_compressed', CompressedImage, self.callback, queue_size=1) # compressed image
        else:
            self._sub_1 = rospy.Subscriber('/image_birdeye', Image, self.callback, queue_size=1) # raw image
        self._sub_2 = rospy.Subscriber('/command_lane_follower', String, self.receiver_from_core, queue_size=1) # lane Detect
        self._sub_3 = rospy.Subscriber('/odom', Odometry, self.callback3, queue_size=1) # 주행 기록 
        # publishers
        self._pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

        self._cv_bridge = CvBridge()

        self.run = 'yes'

        self.lane_position = 0
        self.lane_existance = 'yes'
        self.stop_count = 0
        self.speed = 2 # Increasing this variable makes angular and linear speed fast in same ratio
        self.fast = 'off'
        self.count = 0
        self.state = "usual" #usual, turn_go, turn_stop
        self.count2 = 0
        self.count3 = 0

        self.position_now = None
        self.position_stop = None


    def PIDcontrol(self, x0, y0, x1, y1, x2, y2): # Proportional 비례 : 현재 상태에서의 오차값의 크기에 비례한 제어작용 / Integral 적분 : 정상상태 오차를 없애는
                                                  # Differential 미분 : 출력값의 급격한 변화에 제동을 걸어 안정성을 높인다. 
                                                  # 오차값은 로봇과 Desired path의 거리를 말한다. 일정한 값으로 유지해야 한다.
                                                  # 값이 높을수록 각속도가 빠르다. 
        Ip = 0.2
        distance = 350
        if x1 != x2:
            a = (float(y2)-float(y1))/(float(x2)-float(x1))
        else:
            a = (float(y2)-float(y1))/1 # a는 비율
        b = -1
        c = -a*x1 + y1
        theta_current = -math.atan(1/a)*180/np.pi # 로봇의 현재 방향
        sign_, err = distance_dot2line(a, b, c, x0, y0) # err는 두 선 사이의 거리 
        theta_desired = (err - distance) * Ip * sign_
        theta_wheel = (theta_desired - theta_current) * 0.005 * self.speed # origin : 0.005 next : 0.007
        return sign_, theta_wheel

    def callback(self, image_msg):
        print self.count
        self.count += 1

        if self.count > 50: # count가 50 초과하면 속도 감소한다. 
            self.speed = 0.3

        if self.count > 250: # count가 250 초과하면 속도 증가한다. 
            self.speed = 2
            self.fast = "on"

        if self.count == 1200: # count가 1200이라면 회전하는 것을 멈춘다. 
            self.state = "turn_stop"
            self.stop_count = 0

        if self.state == "turn_stop": 
            self.publishing_vel(0,0,0,0,0,0)
            self.run = "stop"
            self.stop_count += 1

        if self.stop_count > 40:
            self.state = "turn_go"
            self.run = "yes"

        if self.run == 'stop':
            return


        if self.selecting_sub_image == "compressed":
            np_arr = np.fromstring(image_msg.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
        else:
            cv_image = self._cv_bridge.imgmsg_to_cv2(image_msg, "mono8")

        # setting desired path line
        low_point1 = 599

        while(1):
            try:
                _, col_point1 =  centroid(cv_image, low_point1, 300, cv_image.shape[1]) # low_point1과 300 그리고 cv_image의 원래 열 값으로 중심 열을 구한다. 
                break
            except Exception as e:
                if low_point1 < 200:
                    self.lane_existance = 'no'
                    break
                else:
                    low_point1 -= 50

        low_point2 = low_point1 - 50
        while (1):
            try:
                _, col_point2 = centroid(cv_image, low_point2, 300, cv_image.shape[1])
                self.lane_existance = 'yes'
                break
            except Exception as e:
                if low_point2 < 150:
                    self.lane_existance = 'no'
                    break
                else:
                    low_point2 -= 50


        # drawing desired path using point1, point2
        cv_image = cv2.line(cv_image, (col_point1, low_point1), (col_point2, low_point2), (0, 0, 0), 3)
        cv_image = cv2.line(cv_image, (col_point1, low_point1), (col_point2, low_point2), (255, 255, 255), 1)

        # setting and drawing current position
        low_position = (low_point1 + low_point2)/2
        col_position = 500
        cv_image = cv2.circle(cv_image, (col_position, low_position), 3, (255, 255, 255), thickness=5, lineType=8, shift=0)
        cv_image = cv2.circle(cv_image, (col_position, low_position), 3, (0, 0, 0), thickness=3, lineType=8, shift=0)


        if self.image_show == 'on':
            # showing image
            cv2.imshow('tracer', cv_image), cv2.waitKey(1)

        # setting cmd_vel using PID control function
        self.lane_position, angular_z = self.PIDcontrol(col_position, low_position, col_point1, low_point1, col_point2, low_point2)

        # poblishing cmd_vel topic
        self.publishing_vel(0, 0, angular_z, 0.06 * self.speed, 0, 0)


    def callback3(self, odometry):
        self.position_now = [odometry.pose.pose.position.x, odometry.pose.pose.position.y]
        if self.state == "turn_go":
            if self.position_stop == None:
                self.position_stop = self.position_now
            if distance_dot2dot(self.position_now, self.position_stop) > 0.2:
                self.position_stop = None
                self.state = "turn_stop"
                self.publishing_vel(0,0,0,0,0,0)
                self.run = "stop"
                self.stop_count = 0

    def receiver_from_core(self, command):
        self.run = command.data
        if self.run == 'fast':
            self.fast = 'on'
        if self.run == 'go':
            self.speed = 0.3

        if self.fast == 'on':
            self.speed = 2

        if self.run == 'slowdown':
            self.speed = 0.3

        if self.run == 'stop':
            self.publishing_vel(0, 0, 0, 0, 0, 0)

    def publishing_vel(self, angular_x, angular_y, angular_z, linear_x, linear_y, linear_z):
        vel = Twist()
        vel.angular.x = angular_x
        vel.angular.y = angular_y
        vel.angular.z = angular_z
        vel.linear.x = linear_x
        vel.linear.y = linear_y
        vel.linear.z = linear_z
        self._pub.publish(vel)


    def main(self):
        rospy.spin()

if __name__ == '__main__':
    rospy.init_node('lane_follower')
    node = Lane_tracer()
    node.main()