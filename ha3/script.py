#! /usr/bin/python

import rospy
from geometry_msgs.msg import Twist
from rospy import Publisher, Subscriber
from turtlesim.msg import Pose
import math
import numpy as np


class Follower:
    def __init__(self):
        self.pub_2 = Publisher('/leo/cmd_vel', Twist, queue_size=10)

	self.sub_1 = Subscriber('/turtle1/pose', Pose, self.follow)
        self.sub_2 = Subscriber('/leo/pose', Pose, self.update)
        
        self.pose = Pose()
	self.eps = 1

    def update(self, my_pose):
        self.pose = my_pose

    def follow(self, pose):
        msg = Twist()
        dist = np.sqrt((pose.y - self.pose.y) ** 2 + (pose.x - self.pose.x) ** 2)

	if dist <= self.eps:
	    return

        angle = (math.atan2(pose.y - self.pose.y, pose.x - self.pose.x) - self.pose.theta)

        while angle > np.pi:
            angle -= 2 * np.pi
        while angle < -np.pi:
            angle += 2 * np.pi

        msg.linear.x = min(dist, 1.0)
        msg.angular.z = angle
        
        self.pub_2.publish(msg)


rospy.init_node('main')

Follower()

rospy.spin()
