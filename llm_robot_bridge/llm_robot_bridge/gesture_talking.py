#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import math
import time

class GestureTalkingNode(Node):
    def __init__(self):
        super().__init__('gesture_talking_node')
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
        self.get_logger().info("🗣️ Talking gesture...")
        self.reset_all()
        RATE = 0.02

        # ── Keyframes ───────────────────────────────────────────────────────
        L_FROM = dict(pitch=-0.29, roll=-0.02, yaw=0.01, elbow=-2.49,
                      eroll=0.24, eyaw=1.57, wpitch=-0.16, wroll=-0.22, wyaw=-0.11)
        L_TO   = dict(pitch=-0.27, roll=-0.02, yaw=0.01, elbow=-2.20,
                      eroll=0.40, eyaw=1.57, wpitch=-0.14, wroll=-0.26, wyaw=-0.13)

        R_FROM = dict(pitch=-0.45, roll=0.04, yaw=-0.49, elbow=-2.49,
                      eroll=0.13, eyaw=-1.57, wpitch=-0.18, wroll=0.00, wyaw=0.10)
        R_TO   = dict(pitch=-0.40, roll=0.02, yaw=-0.47, elbow=-2.12,
                      eroll=0.37, eyaw=-1.57, wpitch=-0.14, wroll=0.02, wyaw=0.11)

        def blend(a, b, t): return a + (b - a) * t

        def send_pose(t_l, t_r):
            # Left arm
            self.send(self.l_pitch_pub,       blend(L_FROM['pitch'],  L_TO['pitch'],  t_l))
            self.send(self.l_roll_pub,         blend(L_FROM['roll'],   L_TO['roll'],   t_l))
            self.send(self.l_yaw_pub,          blend(L_FROM['yaw'],    L_TO['yaw'],    t_l))
            self.send(self.l_elbow_pub,        blend(L_FROM['elbow'],  L_TO['elbow'],  t_l))
            self.send(self.l_elbow_roll_pub,   blend(L_FROM['eroll'],  L_TO['eroll'],  t_l))
            self.send(self.l_elbow_yaw_pub,    blend(L_FROM['eyaw'],   L_TO['eyaw'],   t_l))
            self.send(self.l_wrist_pitch_pub,  blend(L_FROM['wpitch'], L_TO['wpitch'], t_l))
            self.send(self.l_wrist_roll_pub,   blend(L_FROM['wroll'],  L_TO['wroll'],  t_l))
            self.send(self.l_wrist_yaw_pub,    blend(L_FROM['wyaw'],   L_TO['wyaw'],   t_l))
            # Right arm
            self.send(self.r_pitch_pub,        blend(R_FROM['pitch'],  R_TO['pitch'],  t_r))
            self.send(self.r_roll_pub,          blend(R_FROM['roll'],   R_TO['roll'],   t_r))
            self.send(self.r_yaw_pub,           blend(R_FROM['yaw'],    R_TO['yaw'],    t_r))
            self.send(self.r_elbow_pub,         blend(R_FROM['elbow'],  R_TO['elbow'],  t_r))
            self.send(self.r_elbow_roll_pub,    blend(R_FROM['eroll'],  R_TO['eroll'],  t_r))
            self.send(self.r_elbow_yaw_pub,     blend(R_FROM['eyaw'],   R_TO['eyaw'],   t_r))
            self.send(self.r_wrist_pitch_pub,   blend(R_FROM['wpitch'], R_TO['wpitch'], t_r))
            self.send(self.r_wrist_roll_pub,    blend(R_FROM['wroll'],  R_TO['wroll'],  t_r))
            self.send(self.r_wrist_yaw_pub,     blend(R_FROM['wyaw'],   R_TO['wyaw'],   t_r))
            # All fingers stay 0.0 (set by reset_all, never touched here)

        # Phase 1: Move to FROM pose smoothly (1.5s)
        lift_dur   = 1.5
        lift_steps = int(lift_dur / RATE)
        for i in range(lift_steps):
            s = (1.0 - math.cos((i * RATE / lift_dur) * math.pi)) / 2.0
            # Blend from zero to FROM using s
            t_l = 0.0  # start at FROM (s=0 means FROM values * 0 = zero → FROM)
            # Actually lerp from 0→FROM using s directly on each value
            self.send(self.l_pitch_pub,       L_FROM['pitch']  * s)
            self.send(self.l_roll_pub,         L_FROM['roll']   * s)
            self.send(self.l_yaw_pub,          L_FROM['yaw']    * s)
            self.send(self.l_elbow_pub,        L_FROM['elbow']  * s)
            self.send(self.l_elbow_roll_pub,   L_FROM['eroll']  * s)
            self.send(self.l_elbow_yaw_pub,    L_FROM['eyaw']   * s)
            self.send(self.l_wrist_pitch_pub,  L_FROM['wpitch'] * s)
            self.send(self.l_wrist_roll_pub,   L_FROM['wroll']  * s)
            self.send(self.l_wrist_yaw_pub,    L_FROM['wyaw']   * s)
            self.send(self.r_pitch_pub,        R_FROM['pitch']  * s)
            self.send(self.r_roll_pub,          R_FROM['roll']   * s)
            self.send(self.r_yaw_pub,           R_FROM['yaw']    * s)
            self.send(self.r_elbow_pub,         R_FROM['elbow']  * s)
            self.send(self.r_elbow_roll_pub,    R_FROM['eroll']  * s)
            self.send(self.r_elbow_yaw_pub,     R_FROM['eyaw']   * s)
            self.send(self.r_wrist_pitch_pub,   R_FROM['wpitch'] * s)
            self.send(self.r_wrist_roll_pub,    R_FROM['wroll']  * s)
            self.send(self.r_wrist_yaw_pub,     R_FROM['wyaw']   * s)
            time.sleep(RATE)

        # Phase 2: Oscillate FROM↔TO (4.0s)
        # Both arms talk together — same phase, natural conversational gesture
        TALK_DUR = 4.0
        FREQ     = 1.5   # Hz — relaxed talking pace
        FADE     = 0.3
        talk_steps = int(TALK_DUR / RATE)

        for i in range(talk_steps):
            t    = i * RATE
            env  = min(t / FADE, 1.0, (TALK_DUR - t) / FADE)
            # Smooth 0→1→0 oscillation
            osc  = (math.sin(2.0 * math.pi * FREQ * t) + 1.0) / 2.0 * env
            send_pose(osc, osc)
            time.sleep(RATE)

        # Phase 3: Lower arms back to zero (1.5s)
        drop_dur   = 1.5
        drop_steps = int(drop_dur / RATE)
        for i in range(drop_steps):
            s = (1.0 - math.cos((i * RATE / drop_dur) * math.pi)) / 2.0
            self.send(self.l_pitch_pub,       L_FROM['pitch']  * (1.0 - s))
            self.send(self.l_roll_pub,         L_FROM['roll']   * (1.0 - s))
            self.send(self.l_yaw_pub,          L_FROM['yaw']    * (1.0 - s))
            self.send(self.l_elbow_pub,        L_FROM['elbow']  * (1.0 - s))
            self.send(self.l_elbow_roll_pub,   L_FROM['eroll']  * (1.0 - s))
            self.send(self.l_elbow_yaw_pub,    L_FROM['eyaw']   * (1.0 - s))
            self.send(self.l_wrist_pitch_pub,  L_FROM['wpitch'] * (1.0 - s))
            self.send(self.l_wrist_roll_pub,   L_FROM['wroll']  * (1.0 - s))
            self.send(self.l_wrist_yaw_pub,    L_FROM['wyaw']   * (1.0 - s))
            self.send(self.r_pitch_pub,        R_FROM['pitch']  * (1.0 - s))
            self.send(self.r_roll_pub,          R_FROM['roll']   * (1.0 - s))
            self.send(self.r_yaw_pub,           R_FROM['yaw']    * (1.0 - s))
            self.send(self.r_elbow_pub,         R_FROM['elbow']  * (1.0 - s))
            self.send(self.r_elbow_roll_pub,    R_FROM['eroll']  * (1.0 - s))
            self.send(self.r_elbow_yaw_pub,     R_FROM['eyaw']   * (1.0 - s))
            self.send(self.r_wrist_pitch_pub,   R_FROM['wpitch'] * (1.0 - s))
            self.send(self.r_wrist_roll_pub,    R_FROM['wroll']  * (1.0 - s))
            self.send(self.r_wrist_yaw_pub,     R_FROM['wyaw']   * (1.0 - s))
            time.sleep(RATE)

        self.get_logger().info("✅ Done.")

def main():
    rclpy.init()
    node = GestureTalkingNode()
    node.execute()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()