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
        self.l_pitch_pub      = self.create_publisher(Float64, '/left_arm/shoulder_pitch/cmd_pos', 10)
        self.l_roll_pub       = self.create_publisher(Float64, '/left_arm/shoulder_roll/cmd_pos', 10)
        self.l_yaw_pub        = self.create_publisher(Float64, '/left_arm/shoulder_yaw/cmd_pos', 10)
        self.l_elbow_pub      = self.create_publisher(Float64, '/left_arm/elbow/cmd_pos', 10)
        self.l_elbow_roll_pub = self.create_publisher(Float64, '/left_arm/elbow_roll/cmd_pos', 10)
        # Right arm
        self.r_pitch_pub      = self.create_publisher(Float64, '/right_arm/shoulder_pitch/cmd_pos', 10)
        self.r_roll_pub       = self.create_publisher(Float64, '/right_arm/shoulder_roll/cmd_pos', 10)
        self.r_yaw_pub        = self.create_publisher(Float64, '/right_arm/shoulder_yaw/cmd_pos', 10)
        self.r_elbow_pub      = self.create_publisher(Float64, '/right_arm/elbow/cmd_pos', 10)
        self.r_elbow_roll_pub = self.create_publisher(Float64, '/right_arm/elbow_roll/cmd_pos', 10)

        self.l_wrist_yaw_pub = self.create_publisher(Float64, '/left_arm/wrist_yaw/cmd_pos', 10)
        self.r_wrist_yaw_pub = self.create_publisher(Float64, '/right_arm/wrist_yaw/cmd_pos', 10)
        time.sleep(0.5)

    def send(self, pub, val):
        pub.publish(Float64(data=float(val)))

    def send_both(self, l_pub, r_pub, l_val, r_val):
        self.send(l_pub, l_val)
        self.send(r_pub, r_val)

    def execute(self):
        self.get_logger().info("🙌 Hands Up...")
        RATE = 0.02

        # ── Target pose ─────────────────────────────────────────────────────
        # Both arms raise overhead, slightly apart, elbows bent naturally
        # Left and right are mirrored (roll/yaw opposite signs)
        #
        # pitch  : -2.0 = forward, so overhead needs negative + roll combo
        # roll   :  left= -1.2 (arm sweeps up and out), right= +1.2
        # yaw    :  left=  1.57, right= -1.57 (palms face each other)
        # elbow  : -1.2 (bent — forearm stays bent overhead, not locked straight)
        # elbow_roll: slight outward tilt for natural feel

        L_PITCH      = -2.0
        L_ROLL       = 1.9   # sweeps arm up and slightly out
        L_YAW        = -1.57  # palm faces inward
        L_ELBOW      = -1.5   # elbow bent
        L_ELBOW_ROLL =  0.3   # slight outward tilt
        L_WRIST_YAW =  0.0   # rotate left palm to face outward

        R_PITCH      = -2.0
        R_ROLL       = -1.9   # mirror of left
        R_YAW        = 1.57
        R_ELBOW      = -1.5
        R_ELBOW_ROLL = -0.3   # mirror of left
        R_WRIST_YAW = 0.0   # mirror for right

        # Phase 1: Raise both arms smoothly (2.0s)
        # Physics: shoulders lead, elbows naturally lag behind (phase lag)
        ELBOW_LAG  = 0.3   # elbows reach target slightly after shoulders
        raise_dur   = 2.0
        raise_steps = int(raise_dur / RATE)

        for i in range(raise_steps):
            p        = (i * RATE) / raise_dur
            s        = (1.0 - math.cos(p * math.pi)) / 2.0

            # Elbow lags — uses a shifted progress so it arrives a bit later
            p_elbow  = max(0.0, (i * RATE - ELBOW_LAG) / raise_dur)
            s_elbow  = (1.0 - math.cos(min(p_elbow, 1.0) * math.pi)) / 2.0

            # Shoulders
            self.send_both(self.l_pitch_pub, self.r_pitch_pub, L_PITCH * s, R_PITCH * s)
            self.send_both(self.l_roll_pub,  self.r_roll_pub,  L_ROLL  * s, R_ROLL  * s)
            self.send_both(self.l_yaw_pub,   self.r_yaw_pub,   L_YAW   * s, R_YAW   * s)
            # Elbows lag behind
            self.send_both(self.l_elbow_pub,      self.r_elbow_pub,      L_ELBOW      * s_elbow, R_ELBOW      * s_elbow)
            self.send_both(self.l_elbow_roll_pub, self.r_elbow_roll_pub, L_ELBOW_ROLL * s_elbow, R_ELBOW_ROLL * s_elbow)

            self.send_both(self.l_wrist_yaw_pub, self.r_wrist_yaw_pub, L_WRIST_YAW * s_elbow, R_WRIST_YAW * s_elbow)
            time.sleep(RATE)

        # Phase 2: Hold (2.0s)
        self.get_logger().info("🙌 Holding...")
        time.sleep(2.0)

        # Phase 3: Lower both arms smoothly (1.5s)
        # Elbows lead slightly on the way down (gravity effect)
        drop_dur   = 1.5
        drop_steps = int(drop_dur / RATE)

        for i in range(drop_steps):
            p        = (i * RATE) / drop_dur
            s        = (1.0 - math.cos(p * math.pi)) / 2.0

            # Elbows drop first (gravity pulls forearm down faster)
            p_elbow  = min(1.0, (i * RATE + ELBOW_LAG) / drop_dur)
            s_elbow  = (1.0 - math.cos(min(p_elbow, 1.0) * math.pi)) / 2.0

            self.send_both(self.l_pitch_pub, self.r_pitch_pub, L_PITCH * (1.0 - s), R_PITCH * (1.0 - s))
            self.send_both(self.l_roll_pub,  self.r_roll_pub,  L_ROLL  * (1.0 - s), R_ROLL  * (1.0 - s))
            self.send_both(self.l_yaw_pub,   self.r_yaw_pub,   L_YAW   * (1.0 - s), R_YAW   * (1.0 - s))
            self.send_both(self.l_elbow_pub,      self.r_elbow_pub,      L_ELBOW      * (1.0 - s_elbow), R_ELBOW      * (1.0 - s_elbow))
            self.send_both(self.l_elbow_roll_pub, self.r_elbow_roll_pub, L_ELBOW_ROLL * (1.0 - s_elbow), R_ELBOW_ROLL * (1.0 - s_elbow))
            self.send_both(self.l_wrist_yaw_pub, self.r_wrist_yaw_pub, L_WRIST_YAW * (1.0 - s_elbow), R_WRIST_YAW * (1.0 - s_elbow))
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