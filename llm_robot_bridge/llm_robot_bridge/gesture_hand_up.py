#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import math
import time

class GestureHandUp(Node):
    def __init__(self):
        super().__init__('gesture_hand_up')
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

    def execute(self):
        self.get_logger().info("🙌 Hands Up...")
        self.reset_all()
        RATE = 0.02

        # ── Exact target values ─────────────────────────────────────────────
        # Right arm
        R_PITCH      = -0.72
        R_ROLL       = -1.60
        R_YAW        = -1.97
        R_ELBOW      =  0.00
        R_ELBOW_ROLL =  1.57
        R_ELBOW_YAW  =  0.00
        R_WRIST_P    =  0.03
        R_WRIST_R    =  0.00
        R_WRIST_Y    =  0.00

        # Left arm
        L_PITCH      = -1.36
        L_ROLL       =  1.54
        L_YAW        =  2.00
        L_ELBOW      = -0.55
        L_ELBOW_ROLL = -1.57
        L_ELBOW_YAW  =  0.20
        L_WRIST_P    = -0.03
        L_WRIST_R    = -0.04
        L_WRIST_Y    = -0.02

        # Phase 1: Raise both arms smoothly (2.0s) — elbows lag shoulders
        ELBOW_LAG  = 0.3
        raise_dur   = 2.0
        raise_steps = int(raise_dur / RATE)

        for i in range(raise_steps):
            p       = (i * RATE) / raise_dur
            s       = (1.0 - math.cos(p * math.pi)) / 2.0
            p_elbow = max(0.0, (i * RATE - ELBOW_LAG) / raise_dur)
            s_elbow = (1.0 - math.cos(min(p_elbow, 1.0) * math.pi)) / 2.0

            # Right shoulder
            self.send(self.r_pitch_pub,       R_PITCH      * s)
            self.send(self.r_roll_pub,         R_ROLL       * s)
            self.send(self.r_yaw_pub,          R_YAW        * s)
            self.send(self.r_wrist_pitch_pub,  R_WRIST_P    * s)
            self.send(self.r_wrist_roll_pub,   R_WRIST_R    * s)
            self.send(self.r_wrist_yaw_pub,    R_WRIST_Y    * s)
            # Right elbow lags
            self.send(self.r_elbow_pub,        R_ELBOW      * s_elbow)
            self.send(self.r_elbow_roll_pub,   R_ELBOW_ROLL * s_elbow)
            self.send(self.r_elbow_yaw_pub,    R_ELBOW_YAW  * s_elbow)
            # Right fingers
            self.send(self.r_index_j2_pub,   0.35 * s_elbow)
            self.send(self.r_middle_j2_pub,  0.35 * s_elbow)
            self.send(self.r_ring_j2_pub,    0.35 * s_elbow)
            self.send(self.r_pinky_j2_pub,   0.35 * s_elbow)
            self.send(self.r_thumb_j2_pub,   0.10 * s_elbow)

            # Left shoulder
            self.send(self.l_pitch_pub,       L_PITCH      * s)
            self.send(self.l_roll_pub,         L_ROLL       * s)
            self.send(self.l_yaw_pub,          L_YAW        * s)
            self.send(self.l_wrist_pitch_pub,  L_WRIST_P    * s)
            self.send(self.l_wrist_roll_pub,   L_WRIST_R    * s)
            self.send(self.l_wrist_yaw_pub,    L_WRIST_Y    * s)
            # Left elbow lags
            self.send(self.l_elbow_pub,        L_ELBOW      * s_elbow)
            self.send(self.l_elbow_roll_pub,   L_ELBOW_ROLL * s_elbow)
            self.send(self.l_elbow_yaw_pub,    L_ELBOW_YAW  * s_elbow)
            # Left fingers
            self.send(self.l_index_j2_pub,   0.35 * s_elbow)
            self.send(self.l_middle_j2_pub,  0.35 * s_elbow)
            self.send(self.l_ring_j2_pub,    0.35 * s_elbow)
            self.send(self.l_pinky_j2_pub,   0.35 * s_elbow)
            self.send(self.l_thumb_j2_pub,   0.10 * s_elbow)

            time.sleep(RATE)

        # Phase 2: Hold (2.0s)
        self.get_logger().info("🙌 Holding...")
        time.sleep(2.0)

        # Phase 3: Lower both arms (1.5s) — elbows drop first
        drop_dur   = 1.5
        drop_steps = int(drop_dur / RATE)

        for i in range(drop_steps):
            p       = (i * RATE) / drop_dur
            s       = (1.0 - math.cos(p * math.pi)) / 2.0
            p_elbow = min(1.0, (i * RATE + ELBOW_LAG) / drop_dur)
            s_elbow = (1.0 - math.cos(min(p_elbow, 1.0) * math.pi)) / 2.0

            # Right
            self.send(self.r_pitch_pub,       R_PITCH      * (1.0 - s))
            self.send(self.r_roll_pub,         R_ROLL       * (1.0 - s))
            self.send(self.r_yaw_pub,          R_YAW        * (1.0 - s))
            self.send(self.r_wrist_pitch_pub,  R_WRIST_P    * (1.0 - s))
            self.send(self.r_wrist_roll_pub,   R_WRIST_R    * (1.0 - s))
            self.send(self.r_wrist_yaw_pub,    R_WRIST_Y    * (1.0 - s))
            self.send(self.r_elbow_pub,        R_ELBOW      * (1.0 - s_elbow))
            self.send(self.r_elbow_roll_pub,   R_ELBOW_ROLL * (1.0 - s_elbow))
            self.send(self.r_elbow_yaw_pub,    R_ELBOW_YAW  * (1.0 - s_elbow))
            self.send(self.r_index_j2_pub,   0.35 * (1.0 - s_elbow))
            self.send(self.r_middle_j2_pub,  0.35 * (1.0 - s_elbow))
            self.send(self.r_ring_j2_pub,    0.35 * (1.0 - s_elbow))
            self.send(self.r_pinky_j2_pub,   0.35 * (1.0 - s_elbow))
            self.send(self.r_thumb_j2_pub,   0.10 * (1.0 - s_elbow))

            # Left
            self.send(self.l_pitch_pub,       L_PITCH      * (1.0 - s))
            self.send(self.l_roll_pub,         L_ROLL       * (1.0 - s))
            self.send(self.l_yaw_pub,          L_YAW        * (1.0 - s))
            self.send(self.l_wrist_pitch_pub,  L_WRIST_P    * (1.0 - s))
            self.send(self.l_wrist_roll_pub,   L_WRIST_R    * (1.0 - s))
            self.send(self.l_wrist_yaw_pub,    L_WRIST_Y    * (1.0 - s))
            self.send(self.l_elbow_pub,        L_ELBOW      * (1.0 - s_elbow))
            self.send(self.l_elbow_roll_pub,   L_ELBOW_ROLL * (1.0 - s_elbow))
            self.send(self.l_elbow_yaw_pub,    L_ELBOW_YAW  * (1.0 - s_elbow))
            self.send(self.l_index_j2_pub,   0.35 * (1.0 - s_elbow))
            self.send(self.l_middle_j2_pub,  0.35 * (1.0 - s_elbow))
            self.send(self.l_ring_j2_pub,    0.35 * (1.0 - s_elbow))
            self.send(self.l_pinky_j2_pub,   0.35 * (1.0 - s_elbow))
            self.send(self.l_thumb_j2_pub,   0.10 * (1.0 - s_elbow))

            time.sleep(RATE)

        self.get_logger().info("✅ Done.")

def main():
    rclpy.init()
    node = GestureHandUp()
    node.execute()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()