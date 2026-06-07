#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import math
import time

class GestureWave(Node):
    def __init__(self):
        super().__init__('gesture_wave')
        self.pitch_pub       = self.create_publisher(Float64, '/left_arm/shoulder_pitch/cmd_pos', 10)
        self.roll_pub        = self.create_publisher(Float64, '/left_arm/shoulder_roll/cmd_pos', 10)
        self.yaw_pub         = self.create_publisher(Float64, '/left_arm/shoulder_yaw/cmd_pos', 10)
        self.elbow_pub       = self.create_publisher(Float64, '/left_arm/elbow/cmd_pos', 10)
        self.elbow_roll_pub  = self.create_publisher(Float64, '/left_arm/elbow_roll/cmd_pos', 10)
        self.wrist_pitch_pub = self.create_publisher(Float64, '/left_arm/wrist_pitch/cmd_pos', 10)
        self.wrist_roll_pub  = self.create_publisher(Float64, '/left_arm/wrist_roll/cmd_pos', 10)
        self.wrist_yaw_pub   = self.create_publisher(Float64, '/left_arm/wrist_yaw/cmd_pos', 10)
        time.sleep(0.5)

    def send(self, pub, val):
        pub.publish(Float64(data=float(val)))

    def execute(self):
        self.get_logger().info("👋 Waving...")
        RATE = 0.02

        # ── Raised waving pose ──────────────────────────────────────────────
        PITCH       = -2.0
        ROLL        =  1.5
        YAW         =  1.27   # rotates palm to face outward/forward for wave
        ELBOW       =  -0.2
        ELBOW_ROLL  = -1.9
        WRIST_PITCH =  0.0    # neutral
        WRIST_ROLL  =  0.0    # neutral
        WRIST_YAW   =  0.0    # angled so palm faces viewer during wave

        # Phase 1: Raise arm (2.0s) — wrist lags slightly behind shoulder
        lift_dur   = 2.0
        lift_steps = int(lift_dur / RATE)
        WRIST_LAG  = 0.3

        for i in range(lift_steps):
            s = (1.0 - math.cos((i * RATE / lift_dur) * math.pi)) / 2.0

            p_wrist  = max(0.0, (i * RATE - WRIST_LAG) / lift_dur)
            s_wrist  = (1.0 - math.cos(min(p_wrist, 1.0) * math.pi)) / 2.0

            self.send(self.pitch_pub,       PITCH       * s)
            self.send(self.roll_pub,        ROLL        * s)
            self.send(self.yaw_pub,         YAW         * s)
            self.send(self.elbow_pub,       ELBOW       * s)
            self.send(self.elbow_roll_pub,  ELBOW_ROLL  * s)
            self.send(self.wrist_pitch_pub, WRIST_PITCH * s_wrist)
            self.send(self.wrist_roll_pub,  WRIST_ROLL  * s_wrist)
            self.send(self.wrist_yaw_pub,   WRIST_YAW   * s_wrist)
            time.sleep(RATE)

        # Phase 2: Wave (4.0s)
        # elbow_roll  = primary big swing (most visible)
        # elbow       = secondary bend wobble
        # wrist_yaw   = hand flop lag (most human-like touch)
        WAVE_DUR       = 4.0
        FREQ           = 2.0    # Hz
        ELBOW_ROLL_AMP = 0.7    # primary wave swing
        ELBOW_AMP      = 0.2    # secondary elbow wobble
        WRIST_YAW_AMP  = 0.25   # wrist flop trails elbow_roll
        ELBOW_LAG      = 0.4    # elbow trails elbow_roll
        WRIST_LAG2     = 0.7    # wrist trails even more (pendulum tip)
        FADE           = 0.3

        wave_steps = int(WAVE_DUR / RATE)
        for i in range(wave_steps):
            t   = i * RATE
            env = min(t / FADE, 1.0, (WAVE_DUR - t) / FADE)

            elbow_roll = ELBOW_ROLL + ELBOW_ROLL_AMP * env * math.sin(2.0 * math.pi * FREQ * t)
            elbow      = ELBOW      + ELBOW_AMP      * env * math.sin(2.0 * math.pi * FREQ * t - ELBOW_LAG)
            wrist_yaw  = WRIST_YAW  + WRIST_YAW_AMP  * env * math.sin(2.0 * math.pi * FREQ * t - WRIST_LAG2)

            self.send(self.elbow_roll_pub, elbow_roll)
            self.send(self.elbow_pub,      elbow)
            self.send(self.wrist_yaw_pub,  wrist_yaw)
            time.sleep(RATE)

        # Phase 3: Lower arm (1.5s)
        drop_dur   = 1.5
        drop_steps = int(drop_dur / RATE)

        for i in range(drop_steps):
            s = (1.0 - math.cos((i * RATE / drop_dur) * math.pi)) / 2.0

            p_wrist = min(1.0, (i * RATE + WRIST_LAG) / drop_dur)
            s_wrist = (1.0 - math.cos(min(p_wrist, 1.0) * math.pi)) / 2.0

            self.send(self.pitch_pub,       PITCH       * (1.0 - s))
            self.send(self.roll_pub,        ROLL        * (1.0 - s))
            self.send(self.yaw_pub,         YAW         * (1.0 - s))
            self.send(self.elbow_pub,       ELBOW       * (1.0 - s))
            self.send(self.elbow_roll_pub,  ELBOW_ROLL  * (1.0 - s))
            self.send(self.wrist_pitch_pub, WRIST_PITCH * (1.0 - s_wrist))
            self.send(self.wrist_roll_pub,  WRIST_ROLL  * (1.0 - s_wrist))
            self.send(self.wrist_yaw_pub,   WRIST_YAW   * (1.0 - s_wrist))
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