#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import time

class GestureHandDown(Node):
    def __init__(self):
        super().__init__('gesture_hand_down')
        
        # ==========================================
        # LEFT ARM & HAND PUBLISHERS
        # ==========================================
        self.l_pitch_pub       = self.create_publisher(Float64, '/left_arm/shoulder_pitch/cmd_pos', 10)
        self.l_roll_pub        = self.create_publisher(Float64, '/left_arm/shoulder_roll/cmd_pos', 10)
        self.l_yaw_pub         = self.create_publisher(Float64, '/left_arm/shoulder_yaw/cmd_pos', 10)
        self.l_elbow_pub       = self.create_publisher(Float64, '/left_arm/elbow/cmd_pos', 10)
        self.l_elbow_roll_pub  = self.create_publisher(Float64, '/left_arm/elbow_roll/cmd_pos', 10)
        self.l_wrist_pitch_pub = self.create_publisher(Float64, '/left_arm/wrist_pitch/cmd_pos', 10)
        self.l_wrist_roll_pub  = self.create_publisher(Float64, '/left_arm/wrist_roll/cmd_pos', 10)
        self.l_wrist_yaw_pub   = self.create_publisher(Float64, '/left_arm/wrist_yaw/cmd_pos', 10)
        
        # Left Fingers
        self.l_index_j1_pub  = self.create_publisher(Float64, '/left_hand/index_j1/cmd_pos', 10)
        self.l_index_j2_pub  = self.create_publisher(Float64, '/left_hand/index_j2/cmd_pos', 10)
        self.l_index_j3_pub  = self.create_publisher(Float64, '/left_hand/index_j3/cmd_pos', 10)
        
        self.l_middle_j1_pub = self.create_publisher(Float64, '/left_hand/middle_j1/cmd_pos', 10)
        self.l_middle_j2_pub = self.create_publisher(Float64, '/left_hand/middle_j2/cmd_pos', 10)
        self.l_middle_j3_pub = self.create_publisher(Float64, '/left_hand/middle_j3/cmd_pos', 10)
        
        self.l_ring_j1_pub   = self.create_publisher(Float64, '/left_hand/ring_j1/cmd_pos', 10)
        self.l_ring_j2_pub   = self.create_publisher(Float64, '/left_hand/ring_j2/cmd_pos', 10)
        self.l_ring_j3_pub   = self.create_publisher(Float64, '/left_hand/ring_j3/cmd_pos', 10)
        
        self.l_pinky_j1_pub  = self.create_publisher(Float64, '/left_hand/pinky_j1/cmd_pos', 10)
        self.l_pinky_j2_pub  = self.create_publisher(Float64, '/left_hand/pinky_j2/cmd_pos', 10)
        self.l_pinky_j3_pub  = self.create_publisher(Float64, '/left_hand/pinky_j3/cmd_pos', 10)
        
        self.l_thumb_j1_pub  = self.create_publisher(Float64, '/left_hand/thumb_j1/cmd_pos', 10)
        self.l_thumb_j2_pub  = self.create_publisher(Float64, '/left_hand/thumb_j2/cmd_pos', 10)

        # ==========================================
        # RIGHT ARM & HAND PUBLISHERS
        # ==========================================
        self.r_pitch_pub       = self.create_publisher(Float64, '/right_arm/shoulder_pitch/cmd_pos', 10)
        self.r_roll_pub        = self.create_publisher(Float64, '/right_arm/shoulder_roll/cmd_pos', 10)
        self.r_yaw_pub         = self.create_publisher(Float64, '/right_arm/shoulder_yaw/cmd_pos', 10)
        self.r_elbow_pub       = self.create_publisher(Float64, '/right_arm/elbow/cmd_pos', 10)
        self.r_elbow_roll_pub  = self.create_publisher(Float64, '/right_arm/elbow_roll/cmd_pos', 10)
        self.r_wrist_pitch_pub = self.create_publisher(Float64, '/right_arm/wrist_pitch/cmd_pos', 10)
        self.r_wrist_roll_pub  = self.create_publisher(Float64, '/right_arm/wrist_roll/cmd_pos', 10)
        self.r_wrist_yaw_pub   = self.create_publisher(Float64, '/right_arm/wrist_yaw/cmd_pos', 10)
        
        # Right Fingers
        self.r_index_j1_pub  = self.create_publisher(Float64, '/right_hand/index_j1/cmd_pos', 10)
        self.r_index_j2_pub  = self.create_publisher(Float64, '/right_hand/index_j2/cmd_pos', 10)
        self.r_index_j3_pub  = self.create_publisher(Float64, '/right_hand/index_j3/cmd_pos', 10)
        
        self.r_middle_j1_pub = self.create_publisher(Float64, '/right_hand/middle_j1/cmd_pos', 10)
        self.r_middle_j2_pub = self.create_publisher(Float64, '/right_hand/middle_j2/cmd_pos', 10)
        self.r_middle_j3_pub = self.create_publisher(Float64, '/right_hand/middle_j3/cmd_pos', 10)
        
        self.r_ring_j1_pub   = self.create_publisher(Float64, '/right_hand/ring_j1/cmd_pos', 10)
        self.r_ring_j2_pub   = self.create_publisher(Float64, '/right_hand/ring_j2/cmd_pos', 10)
        self.r_ring_j3_pub   = self.create_publisher(Float64, '/right_hand/ring_j3/cmd_pos', 10)
        
        self.r_pinky_j1_pub  = self.create_publisher(Float64, '/right_hand/pinky_j1/cmd_pos', 10)
        self.r_pinky_j2_pub  = self.create_publisher(Float64, '/right_hand/pinky_j2/cmd_pos', 10)
        self.r_pinky_j3_pub  = self.create_publisher(Float64, '/right_hand/pinky_j3/cmd_pos', 10)
        
        self.r_thumb_j1_pub  = self.create_publisher(Float64, '/right_hand/thumb_j1/cmd_pos', 10)
        self.r_thumb_j2_pub  = self.create_publisher(Float64, '/right_hand/thumb_j2/cmd_pos', 10)

        time.sleep(0.5)

    def execute(self):
        self.get_logger().info("⬇️ Initializing Hand Down position sequence...")
        zero = Float64(data=0.0)
        
        # Reset everything except the target shoulder yaw positions to 0.0 first
        all_pubs_to_zero = [
            # Left Arm (Without Yaw)
            self.l_pitch_pub, self.l_roll_pub,
            self.l_elbow_pub, self.l_elbow_roll_pub,
            self.l_wrist_pitch_pub, self.l_wrist_roll_pub, self.l_wrist_yaw_pub,
            # Left Hand Fingers
            self.l_index_j1_pub, self.l_index_j2_pub, self.l_index_j3_pub,
            self.l_middle_j1_pub, self.l_middle_j2_pub, self.l_middle_j3_pub,
            self.l_ring_j1_pub, self.l_ring_j2_pub, self.l_ring_j3_pub,
            self.l_pinky_j1_pub, self.l_pinky_j2_pub, self.l_pinky_j3_pub,
            self.l_thumb_j1_pub, self.l_thumb_j2_pub,
            
            # Right Arm (Without Yaw)
            self.r_pitch_pub, self.r_roll_pub,
            self.r_elbow_pub, self.r_elbow_roll_pub,
            self.r_wrist_pitch_pub, self.r_wrist_roll_pub, self.r_wrist_yaw_pub,
            # Right Hand Fingers
            self.r_index_j1_pub, self.r_index_j2_pub, self.r_index_j3_pub,
            self.r_middle_j1_pub, self.r_middle_j2_pub, self.r_middle_j3_pub,
            self.r_ring_j1_pub, self.r_ring_j2_pub, self.r_ring_j3_pub,
            self.r_pinky_j1_pub, self.r_pinky_j2_pub, self.r_pinky_j3_pub,
            self.r_thumb_j1_pub, self.r_thumb_j2_pub
        ]
        
        for pub in all_pubs_to_zero:
            pub.publish(zero)
            
        # --- Specific Shoulder Yaw Command Alignments ---
        left_yaw_msg = Float64(data=2.0)
        right_yaw_msg = Float64(data=-1.32)
        
        self.l_yaw_pub.publish(left_yaw_msg)
        self.r_yaw_pub.publish(right_yaw_msg)
        
        time.sleep(0.5)
        self.get_logger().info("✅ Hand Down Sequence with Custom Yaws Complete.")

def main():
    rclpy.init()
    node = GestureHandDown()
    node.execute()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()