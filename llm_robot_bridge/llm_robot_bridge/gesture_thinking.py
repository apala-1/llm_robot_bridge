#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import time

class GestureThinkingNode(Node):
    def __init__(self):
        super().__init__('gesture_thinking_node')
        # Left arm
        self.l_pitch_pub       = self.create_publisher(Float64, '/left_arm/shoulder_pitch/cmd_pos', 10)
        self.l_roll_pub        = self.create_publisher(Float64, '/left_arm/shoulder_roll/cmd_pos', 10)
        self.l_yaw_pub         = self.create_publisher(Float64, '/left_arm/shoulder_yaw/cmd_pos', 10)
        self.l_elbow_pub       = self.create_publisher(Float64, '/left_arm/elbow/cmd_pos', 10)
        self.l_elbow_roll_pub  = self.create_publisher(Float64, '/left_arm/elbow_roll/cmd_pos', 10)
        self.l_elbow_yaw_pub   = self.create_publisher(Float64, '/left_arm/elbow_yaw/cmd_pos', 10)
        self.l_wrist_pitch_pub = self.create_publisher(Float64, '/left_arm/wrist_pitch/cmd_pos', 10)
        self.l_wrist_roll_pub  = self.create_publisher(Float64, '/left_arm/wrist_roll/cmd_pos', 10)
        self.l_wrist_yaw_pub   = self.create_publisher(Float64, '/left_arm/wrist_yaw/cmd_pos', 10)
        self.l_index_j1_pub    = self.create_publisher(Float64, '/left_hand/index_j1/cmd_pos', 10)
        self.l_index_j2_pub    = self.create_publisher(Float64, '/left_hand/index_j2/cmd_pos', 10)
        self.l_index_j3_pub    = self.create_publisher(Float64, '/left_hand/index_j3/cmd_pos', 10)
        self.l_middle_j1_pub   = self.create_publisher(Float64, '/left_hand/middle_j1/cmd_pos', 10)
        self.l_middle_j2_pub   = self.create_publisher(Float64, '/left_hand/middle_j2/cmd_pos', 10)
        self.l_middle_j3_pub   = self.create_publisher(Float64, '/left_hand/middle_j3/cmd_pos', 10)
        self.l_ring_j1_pub     = self.create_publisher(Float64, '/left_hand/ring_j1/cmd_pos', 10)
        self.l_ring_j2_pub     = self.create_publisher(Float64, '/left_hand/ring_j2/cmd_pos', 10)
        self.l_ring_j3_pub     = self.create_publisher(Float64, '/left_hand/ring_j3/cmd_pos', 10)
        self.l_pinky_j1_pub    = self.create_publisher(Float64, '/left_hand/pinky_j1/cmd_pos', 10)
        self.l_pinky_j2_pub    = self.create_publisher(Float64, '/left_hand/pinky_j2/cmd_pos', 10)
        self.l_pinky_j3_pub    = self.create_publisher(Float64, '/left_hand/pinky_j3/cmd_pos', 10)
        self.l_thumb_j1_pub    = self.create_publisher(Float64, '/left_hand/thumb_j1/cmd_pos', 10)
        self.l_thumb_j2_pub    = self.create_publisher(Float64, '/left_hand/thumb_j2/cmd_pos', 10)
        # Right arm
        self.r_pitch_pub       = self.create_publisher(Float64, '/right_arm/shoulder_pitch/cmd_pos', 10)
        self.r_roll_pub        = self.create_publisher(Float64, '/right_arm/shoulder_roll/cmd_pos', 10)
        self.r_yaw_pub         = self.create_publisher(Float64, '/right_arm/shoulder_yaw/cmd_pos', 10)
        self.r_elbow_pub       = self.create_publisher(Float64, '/right_arm/elbow/cmd_pos', 10)
        self.r_elbow_roll_pub  = self.create_publisher(Float64, '/right_arm/elbow_roll/cmd_pos', 10)
        self.r_elbow_yaw_pub   = self.create_publisher(Float64, '/right_arm/elbow_yaw/cmd_pos', 10)
        self.r_wrist_pitch_pub = self.create_publisher(Float64, '/right_arm/wrist_pitch/cmd_pos', 10)
        self.r_wrist_roll_pub  = self.create_publisher(Float64, '/right_arm/wrist_roll/cmd_pos', 10)
        self.r_wrist_yaw_pub   = self.create_publisher(Float64, '/right_arm/wrist_yaw/cmd_pos', 10)
        self.r_index_j1_pub    = self.create_publisher(Float64, '/right_hand/index_j1/cmd_pos', 10)
        self.r_index_j2_pub    = self.create_publisher(Float64, '/right_hand/index_j2/cmd_pos', 10)
        self.r_index_j3_pub    = self.create_publisher(Float64, '/right_hand/index_j3/cmd_pos', 10)
        self.r_middle_j1_pub   = self.create_publisher(Float64, '/right_hand/middle_j1/cmd_pos', 10)
        self.r_middle_j2_pub   = self.create_publisher(Float64, '/right_hand/middle_j2/cmd_pos', 10)
        self.r_middle_j3_pub   = self.create_publisher(Float64, '/right_hand/middle_j3/cmd_pos', 10)
        self.r_ring_j1_pub     = self.create_publisher(Float64, '/right_hand/ring_j1/cmd_pos', 10)
        self.r_ring_j2_pub     = self.create_publisher(Float64, '/right_hand/ring_j2/cmd_pos', 10)
        self.r_ring_j3_pub     = self.create_publisher(Float64, '/right_hand/ring_j3/cmd_pos', 10)
        self.r_pinky_j1_pub    = self.create_publisher(Float64, '/right_hand/pinky_j1/cmd_pos', 10)
        self.r_pinky_j2_pub    = self.create_publisher(Float64, '/right_hand/pinky_j2/cmd_pos', 10)
        self.r_pinky_j3_pub    = self.create_publisher(Float64, '/right_hand/pinky_j3/cmd_pos', 10)
        self.r_thumb_j1_pub    = self.create_publisher(Float64, '/right_hand/thumb_j1/cmd_pos', 10)
        self.r_thumb_j2_pub    = self.create_publisher(Float64, '/right_hand/thumb_j2/cmd_pos', 10)
        # Head
        self.head_pitch_pub    = self.create_publisher(Float64, '/head/pitch/cmd_pos', 10)
        self.head_yaw_pub      = self.create_publisher(Float64, '/head/yaw/cmd_pos', 10)
        time.sleep(0.5)

    def send(self, pub, val):
        pub.publish(Float64(data=float(val)))

    def reset_all(self):
        """Zero every joint before gesture starts."""
        all_pubs = [
            self.l_pitch_pub, self.l_roll_pub, self.l_yaw_pub,
            self.l_elbow_pub, self.l_elbow_roll_pub, self.l_elbow_yaw_pub,
            self.l_wrist_pitch_pub, self.l_wrist_roll_pub, self.l_wrist_yaw_pub,
            self.l_index_j1_pub, self.l_index_j2_pub, self.l_index_j3_pub,
            self.l_middle_j1_pub, self.l_middle_j2_pub, self.l_middle_j3_pub,
            self.l_ring_j1_pub, self.l_ring_j2_pub, self.l_ring_j3_pub,
            self.l_pinky_j1_pub, self.l_pinky_j2_pub, self.l_pinky_j3_pub,
            self.l_thumb_j1_pub, self.l_thumb_j2_pub,
            self.r_pitch_pub, self.r_roll_pub, self.r_yaw_pub,
            self.r_elbow_pub, self.r_elbow_roll_pub, self.r_elbow_yaw_pub,
            self.r_wrist_pitch_pub, self.r_wrist_roll_pub, self.r_wrist_yaw_pub,
            self.r_index_j1_pub, self.r_index_j2_pub, self.r_index_j3_pub,
            self.r_middle_j1_pub, self.r_middle_j2_pub, self.r_middle_j3_pub,
            self.r_ring_j1_pub, self.r_ring_j2_pub, self.r_ring_j3_pub,
            self.r_pinky_j1_pub, self.r_pinky_j2_pub, self.r_pinky_j3_pub,
            self.r_thumb_j1_pub, self.r_thumb_j2_pub,
            self.head_pitch_pub, self.head_yaw_pub,
        ]
        zero = Float64(data=0.0)
        for pub in all_pubs:
            pub.publish(zero)
        time.sleep(0.3)

    def execute(self):
        self.get_logger().info('🤔 Thinking...')
        self.reset_all()  # zero everything first

        # ── Right arm — exact values from spec ─────────────────────────────
        self.send(self.r_pitch_pub,        -0.87)
        self.send(self.r_roll_pub,          -0.04)
        self.send(self.r_yaw_pub,            0.46)
        self.send(self.r_elbow_pub,         -2.42)
        self.send(self.r_elbow_roll_pub,     0.04)
        self.send(self.r_elbow_yaw_pub,      0.01)
        self.send(self.r_wrist_pitch_pub,    0.00)
        self.send(self.r_wrist_roll_pub,     0.01)
        self.send(self.r_wrist_yaw_pub,     -0.01)
        # Right hand fingers
        self.send(self.r_index_j1_pub,    0.00)
        self.send(self.r_index_j2_pub,    0.02)
        self.send(self.r_index_j3_pub,    0.10)
        self.send(self.r_middle_j1_pub,   1.56)
        self.send(self.r_middle_j2_pub,   1.49)
        self.send(self.r_middle_j3_pub,   1.46)
        self.send(self.r_ring_j1_pub,     1.54)
        self.send(self.r_ring_j2_pub,     1.55)
        self.send(self.r_ring_j3_pub,     1.47)
        self.send(self.r_pinky_j1_pub,    1.54)
        self.send(self.r_pinky_j2_pub,    1.49)
        self.send(self.r_pinky_j3_pub,    1.47)
        self.send(self.r_thumb_j1_pub,    1.56)
        self.send(self.r_thumb_j2_pub,    1.48)

        # ── Everything else stays 0.0 (already set by reset_all) ───────────
        self.get_logger().info('✅ Thinking pose held.')
        time.sleep(2.5)

def main():
    rclpy.init()
    node = GestureThinkingNode()
    node.execute()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()