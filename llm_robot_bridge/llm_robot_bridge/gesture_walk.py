#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import math
import time

class GestureWalkNode(Node):
    def __init__(self):
        super().__init__('gesture_walk_node')
        self.cmd_vel_pub = self.create_publisher(Twist, '/model/dual_arm_service_bot/cmd_vel', 10)
        self.r_elbow = self.create_publisher(Float64, '/right_arm/elbow_flex/cmd_pos', 10)
        self.l_elbow = self.create_publisher(Float64, '/left_arm/elbow_flex/cmd_pos', 10)
        self.r_pitch = self.create_publisher(Float64, '/right_arm/shoulder_pitch/cmd_pos', 10)
        self.l_pitch = self.create_publisher(Float64, '/left_arm/shoulder_pitch/cmd_pos', 10)
        self.corridor_sub = self.create_subscription(Float64, '/corridor_width', self.corridor_cb, 10)
        self.corridor_width = 2.0
        
        time.sleep(0.1)
        rclpy.spin_once(self, timeout_sec=0.1)
        self.execute_patrol()

    def corridor_cb(self, msg):
        self.corridor_width = msg.data

    def execute_patrol(self):
        scale = max(0.3, min(1.0, (self.corridor_width - 0.5) / 0.9))
        
        # Pre-set a natural bent elbow position for walking
        elbow_msg = Float64()
        elbow_msg.data = float(1.1)
        self.r_elbow.publish(elbow_msg)
        self.l_elbow.publish(elbow_msg)

        move_msg = Twist()
        move_msg.linear.x = 0.25 # Set operational target velocity
        
        pitch_msg = Float64()
        # Keep publishing cmd_vel inside the loop so the robot doesn't stop moving!
        for tick in range(45):
            self.cmd_vel_pub.publish(move_msg) # Keep wheels spinning active
            
            # Oscillate the elbows/forearms slightly back and forth
            swing = 0.25 * math.sin(tick * 0.4) * scale
            pitch_msg.data = float(0.2 + swing)
            self.r_pitch.publish(pitch_msg)
            pitch_msg.data = float(0.2 - swing)
            self.l_pitch.publish(pitch_msg)
            
            time.sleep(0.1)
            rclpy.spin_once(self, timeout_sec=0.01)

        # Bring base back to a complete stop smoothly
        self.cmd_vel_pub.publish(Twist())

def main():
    rclpy.init()
    node = GestureWalkNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()