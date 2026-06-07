#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import math
import time

class GestureHandshake(Node):
    def __init__(self):
        super().__init__('gesture_handshake')
        self.pitch_pub      = self.create_publisher(Float64, '/left_arm/shoulder_pitch/cmd_pos', 10)
        self.roll_pub       = self.create_publisher(Float64, '/left_arm/shoulder_roll/cmd_pos', 10)
        self.yaw_pub        = self.create_publisher(Float64, '/left_arm/shoulder_yaw/cmd_pos', 10)
        self.elbow_pub      = self.create_publisher(Float64, '/left_arm/elbow/cmd_pos', 10)
        self.elbow_roll_pub = self.create_publisher(Float64, '/left_arm/elbow_roll/cmd_pos', 10)
        time.sleep(0.5)

    def send(self, pub, val):
        pub.publish(Float64(data=float(val)))

    def execute(self):
        self.get_logger().info("🤝 Handshake...")
        RATE = 0.02

        # Confirmed axes:
        # pitch  : -2.0 = arm forward
        # roll   :  1.0 = arm out to side
        # yaw    :  1.57 = palm faces inward (correct for handshake)
        # elbow  : 1.5 = bent up; 0.0 = straight
        # elbow_roll: rotates forearm

        # Handshake reach pose — arm forward, elbow slightly bent, palm facing down/inward
        PITCH      = -1.0   # not fully forward, natural reach
        ROLL       =  0.2   # slight outward
        YAW        =  1.57  # palm faces inward toward other person
        ELBOW      = 0.7   # slight bend
        ELBOW_ROLL =  -0.8   # neutral

        # Phase 1: Reach forward (1.5s)
        reach_dur   = 1.5
        reach_steps = int(reach_dur / RATE)
        for i in range(reach_steps):
            s = (1.0 - math.cos((i * RATE / reach_dur) * math.pi)) / 2.0
            self.send(self.pitch_pub,      PITCH      * s)
            self.send(self.roll_pub,       ROLL       * s)
            self.send(self.yaw_pub,        YAW        * s)
            self.send(self.elbow_pub,      ELBOW      * s)
            self.send(self.elbow_roll_pub, ELBOW_ROLL * s)
            time.sleep(RATE)

        # Phase 2: Shake — forearm pumps up and down from elbow (2.5s)
        # elbow drives the up/down pump (main shake motion)
        # elbow_roll adds slight side wobble for realism
        SHAKE_DUR  = 2.5
        FREQ       = 3.0    # Hz — natural handshake cadence
        ELBOW_AMP  = 0.5   # rad — up/down pump
        EROLL_AMP  = 0.8   # rad — slight side wobble
        PHASE_LAG  = 0.3
        FADE       = 0.2

        shake_steps = int(SHAKE_DUR / RATE)
        for i in range(shake_steps):
            t   = i * RATE
            env = min(t / FADE, 1.0, (SHAKE_DUR - t) / FADE)

            elbow      = ELBOW      + ELBOW_AMP * env * math.sin(2.0 * math.pi * FREQ * t)
            elbow_roll = ELBOW_ROLL + EROLL_AMP * env * math.sin(2.0 * math.pi * FREQ * t - PHASE_LAG)

            self.send(self.elbow_pub,      elbow)
            self.send(self.elbow_roll_pub, elbow_roll)
            time.sleep(RATE)

        # Phase 3: Return arm to side (1.2s)
        drop_dur   = 1.2
        drop_steps = int(drop_dur / RATE)
        for i in range(drop_steps):
            s = (1.0 - math.cos((i * RATE / drop_dur) * math.pi)) / 2.0
            self.send(self.pitch_pub,      PITCH      * (1.0 - s))
            self.send(self.roll_pub,       ROLL       * (1.0 - s))
            self.send(self.yaw_pub,        YAW        * (1.0 - s))
            self.send(self.elbow_pub,      ELBOW      * (1.0 - s))
            self.send(self.elbow_roll_pub, ELBOW_ROLL * (1.0 - s))
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