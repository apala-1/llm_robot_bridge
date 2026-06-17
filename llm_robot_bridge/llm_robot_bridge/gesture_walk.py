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
        # Base
        self.cmd_vel_pub = self.create_publisher(Twist, '/model/dual_arm_service_bot/cmd_vel', 10)
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

    def execute_patrol(self):
        self.get_logger().info("🏃 Walking...")
        self.reset_all()

        # ── Exact keyframe values ───────────────────────────────────────────
        # Right arm: FROM → TO
        R_FROM = dict(pitch=-0.44, roll=-0.04, yaw=-1.73, eroll=0.49,  wpitch=0.00, wroll=0.00, wyaw=0.01)
        R_TO   = dict(pitch= 0.30, roll=-0.04, yaw=-1.72, eroll=0.07,  wpitch=0.01, wroll=0.01, wyaw=0.02)
        # Left arm: FROM → TO (opposite phase to right — natural alternating swing)
        L_FROM = dict(pitch=-0.27, roll=0.00, yaw=2.00, eroll=-0.35, wpitch=-0.02, wroll=0.02, wyaw=-0.03)
        L_TO   = dict(pitch= 0.53, roll=0.01, yaw=2.00, eroll=-0.04, wpitch= 0.02, wroll=0.01, wyaw=-0.03)

        move_msg = Twist()
        move_msg.linear.x = 0.25

        total_ticks = 45
        for tick in range(total_ticks):
            self.cmd_vel_pub.publish(move_msg)

            # Smooth sine wave 0→1→0→1... for right arm
            # Left arm gets inverted phase (1→0→1→0) so they always oppose
            t_r = (math.sin(tick * 0.15) + 1.0) / 2.0   # 0.0 to 1.0
            t_l = 1.0 - t_r                               # perfectly opposite

            def blend(a, b, t): return a + (b - a) * t

            # Right arm
            self.send(self.r_pitch_pub,      blend(R_FROM['pitch'],  R_TO['pitch'],  t_r))
            self.send(self.r_roll_pub,        blend(R_FROM['roll'],   R_TO['roll'],   t_r))
            self.send(self.r_yaw_pub,         blend(R_FROM['yaw'],    R_TO['yaw'],    t_r))
            self.send(self.r_elbow_pub,       0.00)
            self.send(self.r_elbow_roll_pub,  blend(R_FROM['eroll'],  R_TO['eroll'],  t_r))
            self.send(self.r_elbow_yaw_pub,   0.00)
            self.send(self.r_wrist_pitch_pub, blend(R_FROM['wpitch'], R_TO['wpitch'], t_r))
            self.send(self.r_wrist_roll_pub,  blend(R_FROM['wroll'],  R_TO['wroll'],  t_r))
            self.send(self.r_wrist_yaw_pub,   blend(R_FROM['wyaw'],   R_TO['wyaw'],   t_r))

            # Left arm — opposite phase
            self.send(self.l_pitch_pub,       blend(L_FROM['pitch'],  L_TO['pitch'],  t_l))
            self.send(self.l_roll_pub,         blend(L_FROM['roll'],   L_TO['roll'],   t_l))
            self.send(self.l_yaw_pub,          blend(L_FROM['yaw'],    L_TO['yaw'],    t_l))
            self.send(self.l_elbow_pub,        0.00)
            self.send(self.l_elbow_roll_pub,   blend(L_FROM['eroll'],  L_TO['eroll'],  t_l))
            self.send(self.l_elbow_yaw_pub,    0.00)
            self.send(self.l_wrist_pitch_pub,  blend(L_FROM['wpitch'], L_TO['wpitch'], t_l))
            self.send(self.l_wrist_roll_pub,   blend(L_FROM['wroll'],  L_TO['wroll'],  t_l))
            self.send(self.l_wrist_yaw_pub,    blend(L_FROM['wyaw'],   L_TO['wyaw'],   t_l))

            # All fingers, thumbs, head — stay at 0.0 (set by reset_all, not touched here)
            time.sleep(0.1)
            rclpy.spin_once(self, timeout_sec=0.01)

        # Stop wheels
        self.cmd_vel_pub.publish(Twist())
        self.get_logger().info("✅ Walk done.")

def main():
    rclpy.init()
    node = GestureWalkNode()
    node.execute_patrol()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()