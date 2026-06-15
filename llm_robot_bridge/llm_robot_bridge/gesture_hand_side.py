#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import time

class GestureHandSideNode(Node):
    def __init__(self):
        super().__init__('gesture_hand_side_node')
        self.r_roll = self.create_publisher(Float64, '/right_arm/shoulder_roll/cmd_pos', 10)
        self.r_pitch = self.create_publisher(Float64, '/right_arm/shoulder_pitch/cmd_pos', 10)
        self.l_roll = self.create_publisher(Float64, '/left_arm/shoulder_roll/cmd_pos', 10)
        self.l_pitch = self.create_publisher(Float64, '/left_arm/shoulder_pitch/cmd_pos', 10)
        self.corridor_sub = self.create_subscription(Float64, '/corridor_width', self.corridor_cb, 10)
        self.corridor_width = 2.0
        
        time.sleep(0.1)
        rclpy.spin_once(self, timeout_sec=0.1)
        self.execute()

    def corridor_cb(self, msg):
        self.corridor_width = msg.data

    def execute(self):
        scale = max(0.3, min(1.0, (self.corridor_width - 0.5) / 0.9))

        r_msg = Float64()
        p_msg = Float64()
        
        # Right arm outwards configuration
        r_msg.data = float(1.3 * scale)
        p_msg.data = float(0.1)
        self.r_roll.publish(r_msg)
        self.r_pitch.publish(p_msg)
        
        # Left arm mirror outwards configuration (Opposing roll orientation symbol)
        r_msg.data = float(-1.3 * scale)
        p_msg.data = float(0.1)
        self.l_roll.publish(r_msg)
        self.l_pitch.publish(p_msg)
        
        time.sleep(2.0)

def main():
    rclpy.init()
    node = GestureHandSideNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()