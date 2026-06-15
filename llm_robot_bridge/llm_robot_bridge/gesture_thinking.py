#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import math
import time

class GestureThinkingNode(Node):
    def __init__(self):
        super().__init__('gesture_thinking_node')
        self.pitch_pub = self.create_publisher(Float64, '/right_arm/shoulder_pitch/cmd_pos', 10)
        self.roll_pub = self.create_publisher(Float64, '/right_arm/shoulder_roll/cmd_pos', 10)
        self.elbow_pub = self.create_publisher(Float64, '/right_arm/elbow_flex/cmd_pos', 10)
        self.execute()

    def execute(self):
        p_msg = Float64()
        r_msg = Float64()
        e_msg = Float64()
        
        # Bring arm forward, angle it inward toward centerline, bend elbow up to face
        p_msg.data = float(0.6)   # Shoulder forward elevation
        r_msg.data = float(-0.4)  # Bring arm inward toward the face/chin line
        e_msg.data = float(1.6)   # Sharp elbow flex to lift hand up to the face level
        
        self.pitch_pub.publish(p_msg)
        self.roll_pub.publish(r_msg)
        self.elbow_pub.publish(e_msg)
        
        # Keep the pose held for a natural processing duration
        time.sleep(2.5)

def main():
    rclpy.init()
    node = GestureThinkingNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()