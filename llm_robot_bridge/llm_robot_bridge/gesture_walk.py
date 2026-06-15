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
        
        # Base Velocity Publisher
        self.cmd_vel_pub = self.create_publisher(Twist, '/model/dual_arm_service_bot/cmd_vel', 10)
        
        # ==========================================
        # RIGHT ARM PUBLISHERS
        # ==========================================
        self.r_pitch_pub       = self.create_publisher(Float64, '/right_arm/shoulder_pitch/cmd_pos', 10)
        self.r_roll_pub        = self.create_publisher(Float64, '/right_arm/shoulder_roll/cmd_pos', 10)
        self.r_yaw_pub         = self.create_publisher(Float64, '/right_arm/shoulder_yaw/cmd_pos', 10)
        self.r_elbow_pub       = self.create_publisher(Float64, '/right_arm/elbow/cmd_pos', 10)
        self.r_elbow_roll_pub  = self.create_publisher(Float64, '/right_arm/elbow_roll/cmd_pos', 10)
        self.r_wrist_pitch_pub = self.create_publisher(Float64, '/right_arm/wrist_pitch/cmd_pos', 10)
        self.r_wrist_roll_pub  = self.create_publisher(Float64, '/right_arm/wrist_roll/cmd_pos', 10)
        self.r_wrist_yaw_pub   = self.create_publisher(Float64, '/right_arm/wrist_yaw/cmd_pos', 10)

        # ==========================================
        # LEFT ARM PUBLISHERS
        # ==========================================
        self.l_pitch_pub       = self.create_publisher(Float64, '/left_arm/shoulder_pitch/cmd_pos', 10)
        self.l_roll_pub        = self.create_publisher(Float64, '/left_arm/shoulder_roll/cmd_pos', 10)
        self.l_yaw_pub         = self.create_publisher(Float64, '/left_arm/shoulder_yaw/cmd_pos', 10)
        self.l_elbow_pub       = self.create_publisher(Float64, '/left_arm/elbow/cmd_pos', 10)
        self.l_elbow_roll_pub  = self.create_publisher(Float64, '/left_arm/elbow_roll/cmd_pos', 10)
        self.l_wrist_pitch_pub = self.create_publisher(Float64, '/left_arm/wrist_pitch/cmd_pos', 10)
        self.l_wrist_roll_pub  = self.create_publisher(Float64, '/left_arm/wrist_roll/cmd_pos', 10)
        self.l_wrist_yaw_pub   = self.create_publisher(Float64, '/left_arm/wrist_yaw/cmd_pos', 10)

        # Corridor Context Subscription
        self.corridor_sub = self.create_subscription(Float64, '/corridor_width', self.corridor_cb, 10)
        self.corridor_width = 2.0
        
        time.sleep(0.1)
        rclpy.spin_once(self, timeout_sec=0.1)
        self.execute_patrol()

    def corridor_cb(self, msg):
        self.corridor_width = msg.data

    def publish_value(self, publisher, value):
        msg = Float64()
        msg.data = float(value)
        publisher.publish(msg)

    def execute_patrol(self):
        scale = max(0.3, min(1.0, (self.corridor_width - 0.5) / 0.9))
        self.get_logger().info(f"🏃 Executing Updated Keyframe Walk Sequence (Corridor Scale: {scale:.2f})...")
        
        # Base drive message configuration
        move_msg = Twist()
        move_msg.linear.x = 0.25 

        # Define 45 ticks loop execution window
        total_ticks = 45
        for tick in range(total_ticks):
            # Keep wheels rolling actively
            self.cmd_vel_pub.publish(move_msg) 
            
            # Interpolation variable alternating smoothly between 0.0 and 1.0
            t = abs(math.sin(tick * 0.15))
            
            # --------------------------------------------------
            # RIGHT ARM INTERPOLATION (From State A to State B)
            # --------------------------------------------------
            # State A Values (from)
            r_pitch_A  = -0.44
            r_roll_A   = -0.04
            r_yaw_A    = -1.73
            r_eroll_A  = 0.49
            r_wpitch_A = 0.00
            r_wroll_A  = 0.00
            r_wyaw_A   = 0.01
            
            # State B Values (to)
            r_pitch_B  = 0.30
            r_roll_B   = -0.04
            r_yaw_B    = -1.72
            r_eroll_B  = 0.07
            r_wpitch_B = 0.01
            r_wroll_B  = 0.01
            r_wyaw_B   = 0.02
            
            # Blend values using the dynamic t timing multiplier
            r_pitch  = (r_pitch_A + (r_pitch_B - r_pitch_A) * t) * scale
            r_roll   = (r_roll_A + (r_roll_B - r_roll_A) * t) * scale
            r_yaw    = r_yaw_A + (r_yaw_B - r_yaw_A) * t
            r_eroll  = r_eroll_A + (r_eroll_B - r_eroll_A) * t
            r_wpitch = r_wpitch_A + (r_wpitch_B - r_wpitch_A) * t
            r_wroll  = r_wroll_A + (r_wroll_B - r_wroll_A) * t
            r_wyaw   = r_wyaw_A + (r_wyaw_B - r_wyaw_A) * t
            
            self.publish_value(self.r_elbow_pub, 0.00) # Always static at 0.0
            self.publish_value(self.r_pitch_pub, r_pitch)
            self.publish_value(self.r_roll_pub, r_roll)
            self.publish_value(self.r_yaw_pub, r_yaw)
            self.publish_value(self.r_elbow_roll_pub, r_eroll)
            self.publish_value(self.r_wrist_pitch_pub, r_wpitch)
            self.publish_value(self.r_wrist_roll_pub, r_wroll)
            self.publish_value(self.r_wrist_yaw_pub, r_wyaw)

            # --------------------------------------------------
            # LEFT ARM INTERPOLATION (From State A to State B)
            # --------------------------------------------------
            # State A Values (from)
            l_pitch_A  = -0.27
            l_roll_A   = 0.00
            l_yaw_A    = 2.00
            l_eroll_A  = -0.35
            l_wpitch_A = -0.02
            l_wroll_A  = 0.02
            l_wyaw_A   = -0.03
            
            # State B Values (to)
            l_pitch_B  = 0.53
            l_roll_B   = 0.01
            l_yaw_B    = 2.00
            l_eroll_B  = -0.04
            l_wpitch_B = 0.02
            l_wroll_B  = 0.01
            l_wyaw_B   = -0.03
            
            # Inverting phase time for a natural human-like alternating arm swing
            t_left = 1.0 - t
            
            l_pitch  = (l_pitch_A + (l_pitch_B - l_pitch_A) * t_left) * scale
            l_roll   = (l_roll_A + (l_roll_B - l_roll_A) * t_left) * scale
            l_yaw    = l_yaw_A + (l_yaw_B - l_yaw_A) * t_left
            l_eroll  = l_eroll_A + (l_eroll_B - l_eroll_A) * t_left
            l_wpitch = l_wpitch_A + (l_wpitch_B - l_wpitch_A) * t_left
            l_wroll  = l_wroll_A + (l_wroll_B - l_wroll_A) * t_left
            l_wyaw   = l_wyaw_A + (l_wyaw_B - l_wyaw_A) * t_left

            self.publish_value(self.l_elbow_pub, 0.00) # Always static at 0.0
            self.publish_value(self.l_pitch_pub, l_pitch)
            self.publish_value(self.l_roll_pub, l_roll)
            self.publish_value(self.l_yaw_pub, l_yaw)
            self.publish_value(self.l_elbow_roll_pub, l_eroll)
            self.publish_value(self.l_wrist_pitch_pub, l_wpitch)
            self.publish_value(self.l_wrist_roll_pub, l_wroll)
            self.publish_value(self.l_wrist_yaw_pub, l_wyaw)

            time.sleep(0.1)
            rclpy.spin_once(self, timeout_sec=0.01)

        # Bring base back to a complete stop smoothly
        self.get_logger().info("✅ Patrol sequence over. Bringing wheels to complete stop.")
        self.cmd_vel_pub.publish(Twist())

def main():
    rclpy.init()
    node = GestureWalkNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()