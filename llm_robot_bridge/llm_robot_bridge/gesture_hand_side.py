#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import time

class GestureHandSideNode(Node):
    def __init__(self):
        super().__init__('gesture_hand_side_node')
        
        # ==========================================
        # RIGHT ARM PUBLISHERS
        # ==========================================
        self.r_pitch_pub      = self.create_publisher(Float64, '/right_arm/shoulder_pitch/cmd_pos', 10)
        self.r_roll_pub       = self.create_publisher(Float64, '/right_arm/shoulder_roll/cmd_pos', 10)
        self.r_yaw_pub        = self.create_publisher(Float64, '/right_arm/shoulder_yaw/cmd_pos', 10)
        self.r_elbow_pub      = self.create_publisher(Float64, '/right_arm/elbow/cmd_pos', 10)
        self.r_elbow_roll_pub = self.create_publisher(Float64, '/right_arm/elbow_roll/cmd_pos', 10)
        self.r_wrist_pitch_pub = self.create_publisher(Float64, '/right_arm/wrist_pitch/cmd_pos', 10)
        self.r_wrist_roll_pub  = self.create_publisher(Float64, '/right_arm/wrist_roll/cmd_pos', 10)

        # ==========================================
        # LEFT ARM PUBLISHERS
        # ==========================================
        self.l_pitch_pub       = self.create_publisher(Float64, '/left_arm/shoulder_pitch/cmd_pos', 10)
        self.l_roll_pub        = self.create_publisher(Float64, '/left_arm/shoulder_roll/cmd_pos', 10)
        self.l_yaw_pub         = self.create_publisher(Float64, '/left_arm/shoulder_yaw/cmd_pos', 10)
        self.l_elbow_pub       = self.create_publisher(Float64, '/left_arm/elbow/cmd_pos', 10)
        self.l_elbow_roll_pub  = self.create_publisher(Float64, '/left_arm/elbow_roll/cmd_pos', 10)
        self.l_wrist_pitch_pub = self.create_publisher(Float64, '/left_arm/wrist_pitch/cmd_pos', 10)
        self.l_wrist_roll_pub  = self.create_publisher(Float64, '/left_arm/wrist_roll/cmd_pos', 10)
        self.l_wrist_yaw_pub   = self.create_publisher(Float64, '/left_arm/wrist_yaw/cmd_pos', 10)

        # Corridor context monitoring
        self.corridor_sub = self.create_subscription(Float64, '/corridor_width', self.corridor_cb, 10)
        self.corridor_width = 2.0
        
        time.sleep(0.1)
        rclpy.spin_once(self, timeout_sec=0.1)
        self.execute()

    def corridor_cb(self, msg):
        self.corridor_width = msg.data

    def publish_value(self, publisher, value):
        msg = Float64()
        msg.data = float(value)
        publisher.publish(msg)

    def execute(self):
        # Scale dynamic extensions based on safety constraints
        scale = max(0.3, min(1.0, (self.corridor_width - 0.5) / 0.9))
        self.get_logger().info(f"↔️ Executing Hand Side Pose (Corridor Scale: {scale:.2f})...")

        # ==========================================
        # EXECUTE RIGHT ARM CONFIGURATION
        # ==========================================
        # Scaled main shoulder dimensions
        self.publish_value(self.r_pitch_pub, -0.49 * scale)
        self.publish_value(self.r_roll_pub, -1.50 * scale)
        
        # Static physical orientations
        self.publish_value(self.r_yaw_pub, 2.00)
        self.publish_value(self.r_elbow_pub, -0.10)
        self.publish_value(self.r_elbow_roll_pub, -0.12)
        self.publish_value(self.r_wrist_pitch_pub, -0.13)
        self.publish_value(self.r_wrist_roll_pub, -0.02)

        # ==========================================
        # EXECUTE LEFT ARM CONFIGURATION
        # ==========================================
        # Scaled main shoulder dimensions
        self.publish_value(self.l_pitch_pub, -0.71 * scale)
        self.publish_value(self.l_roll_pub, 1.57 * scale)
        
        # Static physical orientations
        self.publish_value(self.l_yaw_pub, 2.00)
        self.publish_value(self.l_elbow_pub, 0.00)
        self.publish_value(self.l_elbow_roll_pub, 0.08)
        self.publish_value(self.l_wrist_pitch_pub, 0.01)
        self.publish_value(self.l_wrist_roll_pub, -0.02)
        self.publish_value(self.l_wrist_yaw_pub, 0.02)
        
        time.sleep(2.0)
        self.get_logger().info("✅ Hand Side Execution Sent Successfully.")

def main():
    rclpy.init()
    node = GestureHandSideNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()