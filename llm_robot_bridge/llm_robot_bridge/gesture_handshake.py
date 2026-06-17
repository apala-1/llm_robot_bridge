#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import math
import time

class GestureHandshake(Node):
    def __init__(self):
        super().__init__('gesture_handshake')
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

    def send_static(self, elbow_val):
        """Send full pose with only elbow changing during shake."""
        # Right arm — static joints
        self.send(self.r_pitch_pub,       -0.29)
        self.send(self.r_roll_pub,         -0.14)
        self.send(self.r_yaw_pub,           0.02)
        self.send(self.r_elbow_pub,         elbow_val)   # ← oscillates
        self.send(self.r_elbow_roll_pub,   -0.03)
        self.send(self.r_elbow_yaw_pub,    -1.57)
        self.send(self.r_wrist_pitch_pub,   0.02)
        self.send(self.r_wrist_roll_pub,   -0.04)
        self.send(self.r_wrist_yaw_pub,     0.06)
        # Right fingers — slightly curled
        self.send(self.r_index_j1_pub,   0.00)
        self.send(self.r_index_j2_pub,   0.35)
        self.send(self.r_index_j3_pub,   0.00)
        self.send(self.r_middle_j1_pub,  0.00)
        self.send(self.r_middle_j2_pub,  0.35)
        self.send(self.r_middle_j3_pub,  0.00)
        self.send(self.r_ring_j1_pub,    0.00)
        self.send(self.r_ring_j2_pub,    0.35)
        self.send(self.r_ring_j3_pub,    0.00)
        self.send(self.r_pinky_j1_pub,   0.00)
        self.send(self.r_pinky_j2_pub,   0.35)
        self.send(self.r_pinky_j3_pub,   0.00)
        self.send(self.r_thumb_j1_pub,   0.00)
        self.send(self.r_thumb_j2_pub,   0.10)
        # Left arm + fingers stay 0.0 (set by reset_all, never touched)

    def execute(self):
        self.get_logger().info("🤝 Handshake...")
        self.reset_all()
        RATE = 0.02

        # Shake oscillates elbow between FROM and TO
        ELBOW_FROM = -1.15
        ELBOW_TO   = -1.52
        ELBOW_MID  = (ELBOW_FROM + ELBOW_TO) / 2.0   # -1.335
        ELBOW_AMP  = (ELBOW_TO - ELBOW_FROM) / 2.0   # -0.185

        # Phase 1: Reach to FROM pose smoothly (1.5s)
        reach_dur   = 1.5
        reach_steps = int(reach_dur / RATE)
        for i in range(reach_steps):
            s = (1.0 - math.cos((i * RATE / reach_dur) * math.pi)) / 2.0
            self.send(self.r_pitch_pub,       -0.29 * s)
            self.send(self.r_roll_pub,         -0.14 * s)
            self.send(self.r_yaw_pub,           0.02 * s)
            self.send(self.r_elbow_pub,         ELBOW_FROM * s)
            self.send(self.r_elbow_roll_pub,   -0.03 * s)
            self.send(self.r_elbow_yaw_pub,    -1.57 * s)
            self.send(self.r_wrist_pitch_pub,   0.02 * s)
            self.send(self.r_wrist_roll_pub,   -0.04 * s)
            self.send(self.r_wrist_yaw_pub,     0.06 * s)
            self.send(self.r_index_j2_pub,    0.35 * s)
            self.send(self.r_middle_j2_pub,   0.35 * s)
            self.send(self.r_ring_j2_pub,     0.35 * s)
            self.send(self.r_pinky_j2_pub,    0.35 * s)
            self.send(self.r_thumb_j2_pub,    0.10 * s)
            time.sleep(RATE)

        # Phase 2: Shake — elbow oscillates FROM↔TO (2.5s)
        SHAKE_DUR  = 2.5
        FREQ       = 3.0
        FADE       = 0.2
        shake_steps = int(SHAKE_DUR / RATE)
        for i in range(shake_steps):
            t   = i * RATE
            env = min(t / FADE, 1.0, (SHAKE_DUR - t) / FADE)
            elbow = ELBOW_MID + ELBOW_AMP * env * math.sin(2.0 * math.pi * FREQ * t)
            self.send_static(elbow)
            time.sleep(RATE)

        # Phase 3: Return to zero (1.2s)
        drop_dur   = 1.2
        drop_steps = int(drop_dur / RATE)
        for i in range(drop_steps):
            s = (1.0 - math.cos((i * RATE / drop_dur) * math.pi)) / 2.0
            self.send(self.r_pitch_pub,       -0.29 * (1.0 - s))
            self.send(self.r_roll_pub,         -0.14 * (1.0 - s))
            self.send(self.r_yaw_pub,           0.02 * (1.0 - s))
            self.send(self.r_elbow_pub,         ELBOW_FROM * (1.0 - s))
            self.send(self.r_elbow_roll_pub,   -0.03 * (1.0 - s))
            self.send(self.r_elbow_yaw_pub,    -1.57 * (1.0 - s))
            self.send(self.r_wrist_pitch_pub,   0.02 * (1.0 - s))
            self.send(self.r_wrist_roll_pub,   -0.04 * (1.0 - s))
            self.send(self.r_wrist_yaw_pub,     0.06 * (1.0 - s))
            self.send(self.r_index_j2_pub,    0.35 * (1.0 - s))
            self.send(self.r_middle_j2_pub,   0.35 * (1.0 - s))
            self.send(self.r_ring_j2_pub,     0.35 * (1.0 - s))
            self.send(self.r_pinky_j2_pub,    0.35 * (1.0 - s))
            self.send(self.r_thumb_j2_pub,    0.10 * (1.0 - s))
            time.sleep(RATE)

        self.get_logger().info("✅ Handshake done.")

def main():
    rclpy.init()
    node = GestureHandshake()
    node.execute()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()