#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import math
import time

class GestureWave(Node):
    def __init__(self):
        super().__init__('gesture_wave')
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
        self.get_logger().info("👋 Waving...")
        self.reset_all()
        RATE = 0.02

        PITCH       = -1.63
        ROLL        = -1.5
        YAW         = -1.27
        ELBOW       = -0.44
        ELBOW_ROLL  =  1.9
        WRIST_PITCH =  0.0
        WRIST_ROLL  =  0.0
        WRIST_YAW   =  0.0

        # Phase 1: Raise right arm (2.0s)
        lift_dur   = 2.0
        lift_steps = int(lift_dur / RATE)
        WRIST_LAG  = 0.3

        for i in range(lift_steps):
            s = (1.0 - math.cos((i * RATE / lift_dur) * math.pi)) / 2.0
            p_wrist = max(0.0, (i * RATE - WRIST_LAG) / lift_dur)
            s_wrist = (1.0 - math.cos(min(p_wrist, 1.0) * math.pi)) / 2.0
            self.send(self.r_pitch_pub,       PITCH       * s)
            self.send(self.r_roll_pub,         ROLL        * s)
            self.send(self.r_yaw_pub,          YAW         * s)
            self.send(self.r_elbow_pub,        ELBOW       * s)
            self.send(self.r_elbow_roll_pub,   ELBOW_ROLL  * s)
            self.send(self.r_wrist_pitch_pub,  WRIST_PITCH * s_wrist)
            self.send(self.r_wrist_roll_pub,   WRIST_ROLL  * s_wrist)
            self.send(self.r_wrist_yaw_pub,    WRIST_YAW   * s_wrist)
            time.sleep(RATE)

        # Phase 2: Wave (4.0s)
        WAVE_DUR       = 4.0
        FREQ           = 2.0
        ELBOW_ROLL_AMP = -1.0   # flipped for right arm
        ELBOW_AMP      =  0.2
        WRIST_YAW_AMP  =  0.00
        ELBOW_LAG      =  0.4
        WRIST_LAG2     =  0.7
        FADE           =  0.3

        wave_steps = int(WAVE_DUR / RATE)
        for i in range(wave_steps):
            t   = i * RATE
            env = min(t / FADE, 1.0, (WAVE_DUR - t) / FADE)
            elbow_roll = ELBOW_ROLL + ELBOW_ROLL_AMP * env * math.sin(2.0 * math.pi * FREQ * t)
            elbow      = ELBOW      + ELBOW_AMP      * env * math.sin(2.0 * math.pi * FREQ * t - ELBOW_LAG)
            wrist_yaw  = WRIST_YAW  + WRIST_YAW_AMP  * env * math.sin(2.0 * math.pi * FREQ * t - WRIST_LAG2)
            self.send(self.r_elbow_roll_pub, elbow_roll)
            self.send(self.r_elbow_pub,      elbow)
            self.send(self.r_wrist_yaw_pub,  wrist_yaw)
            time.sleep(RATE)

        # Phase 3: Lower right arm (1.5s)
        drop_dur   = 1.5
        drop_steps = int(drop_dur / RATE)
        for i in range(drop_steps):
            s = (1.0 - math.cos((i * RATE / drop_dur) * math.pi)) / 2.0
            p_wrist = min(1.0, (i * RATE + WRIST_LAG) / drop_dur)
            s_wrist = (1.0 - math.cos(min(p_wrist, 1.0) * math.pi)) / 2.0
            self.send(self.r_pitch_pub,       PITCH       * (1.0 - s))
            self.send(self.r_roll_pub,         ROLL        * (1.0 - s))
            self.send(self.r_yaw_pub,          YAW         * (1.0 - s))
            self.send(self.r_elbow_pub,        ELBOW       * (1.0 - s))
            self.send(self.r_elbow_roll_pub,   ELBOW_ROLL  * (1.0 - s))
            self.send(self.r_wrist_pitch_pub,  WRIST_PITCH * (1.0 - s_wrist))
            self.send(self.r_wrist_roll_pub,   WRIST_ROLL  * (1.0 - s_wrist))
            self.send(self.r_wrist_yaw_pub,    WRIST_YAW   * (1.0 - s_wrist))
            time.sleep(RATE)

        self.get_logger().info("✅ Done.")

def main():
    rclpy.init()
    node = GestureWave()
    node.execute()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()