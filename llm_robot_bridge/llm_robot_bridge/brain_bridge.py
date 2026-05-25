#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, String
import time

class LeftArmGestureBridge(Node):
    def __init__(self):
        super().__init__('left_arm_gesture_bridge')
        self.get_logger().info("🚀 Left-Arm Only Gesture Controller Node Activated!")

        # Subscribe to the high level command topic listening over your tunnel
        self.cmd_sub = self.create_subscription(String, '/robot/high_level_command', self.command_callback, 10)

        # Left arm publishers exclusively
        self.pub_l_roll  = self.create_publisher(Float64, '/model/service_robot/joint/left_shoulder_roll_joint/cmd_pos', 10)
        self.pub_l_pitch = self.create_publisher(Float64, '/model/service_robot/joint/left_shoulder_pitch_joint/cmd_pos', 10)
        self.pub_l_yaw   = self.create_publisher(Float64, '/model/service_robot/joint/left_shoulder_yaw_joint/cmd_pos', 10)
        self.pub_l_elbow = self.create_publisher(Float64, '/model/service_robot/joint/left_elbow_joint/cmd_pos', 10)

    def command_callback(self, msg):
        command = msg.data.lower().strip()
        self.get_logger().info(f"📥 Received High-Level Intent: '{command}'")

        if command == "wave":
            self.execute_left_arm_wave()
        elif command == "handshake":
            self.execute_left_arm_handshake()
        elif command == "patrol_step":
            pass
        else:
            self.get_logger().info("Command unknown or requires driving mechanics. Standing by...")

    def execute_left_arm_wave(self):
        self.get_logger().info("👋 Initializing Friendly Left Arm Wave...")
        
        # --- 1. SETUP STANCE: Arm out to the side, elbow bent up at 90 degrees ---
        for _ in range(15):
            self.pub_l_yaw.publish(Float64(data=-1.57))    
            self.pub_l_roll.publish(Float64(data=1.57))   
            self.pub_l_elbow.publish(Float64(data=-1.57)) 
            self.pub_l_pitch.publish(Float64(data=0.0))   
            time.sleep(0.03)
        time.sleep(0.3)

        # --- 2. ACTIVE WAVING LOOP: Gentle windshield-wiper motion using shoulder pitch ---
        for cycle in range(3):
            # Tilt Forward
            for _ in range(8):
                self.pub_l_elbow.publish(Float64(data=2.40))
                time.sleep(0.03)
            time.sleep(0.1)
            
            # Tilt Backward
            for _ in range(8):
                self.pub_l_elbow.publish(Float64(data=-2.40))
                time.sleep(0.03)
            time.sleep(0.1)

        self.reset_left_arm()

    def execute_left_arm_handshake(self):
        self.get_logger().info("🤝 Presenting Gentle Left Arm Handshake...")
        
        # --- 1. SETUP STANCE: Arm down, reaching slightly forward at waist height ---
        for _ in range(15):
            self.pub_l_roll.publish(Float64(data=0.0))     
            self.pub_l_yaw.publish(Float64(data=0.0))      
            self.pub_l_pitch.publish(Float64(data=-0.95))  # Lowered significantly for realism
            self.pub_l_elbow.publish(Float64(data=-0.75))  # Relaxed bend
            time.sleep(0.03)
        time.sleep(0.3)

        # --- 2. ACTIVE SHAKING LOOP: Small, gentle up-and-down motions ---
        for cycle in range(3):
            # Shake UP (Slight raise and deeper elbow bend)
            for _ in range(8):
                self.pub_l_pitch.publish(Float64(data=-1.15))
                self.pub_l_elbow.publish(Float64(data=-0.70))
                time.sleep(0.03)
            time.sleep(0.1)
            
            # Shake DOWN (Drop back to starting position)
            for _ in range(8):
                self.pub_l_pitch.publish(Float64(data=-0.75))
                self.pub_l_elbow.publish(Float64(data=-0.40))
                time.sleep(0.03)
            time.sleep(0.1)

        self.reset_left_arm()

    def reset_left_arm(self):
        self.get_logger().info("💤 Resetting Left Arm to resting position...")
        for _ in range(15):
            self.pub_l_roll.publish(Float64(data=0.0))
            self.pub_l_pitch.publish(Float64(data=0.0))
            self.pub_l_yaw.publish(Float64(data=0.0))
            self.pub_l_elbow.publish(Float64(data=0.0))
            time.sleep(0.02)

def main(args=None):
    rclpy.init(args=args)
    node = LeftArmGestureBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()