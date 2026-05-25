#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Empty
import time

class HandshakeController(Node):
    def __init__(self):
        super().__init__('handshake_controller')
        self.get_logger().info("🤝 Handshake Controller Node Online!")

        # Listen for trigger from Coordinator
        self.trigger_sub = self.create_subscription(
            Empty, '/gesture/handshake', self.execute_handshake_callback, 10)

        # Joint Command Publishers
        self.pub_l_roll  = self.create_publisher(Float64, '/model/service_robot/joint/left_shoulder_roll_joint/cmd_pos', 10)
        self.pub_l_pitch = self.create_publisher(Float64, '/model/service_robot/joint/left_shoulder_pitch_joint/cmd_pos', 10)
        self.pub_l_yaw   = self.create_publisher(Float64, '/model/service_robot/joint/left_shoulder_yaw_joint/cmd_pos', 10)
        self.pub_l_elbow = self.create_publisher(Float64, '/model/service_robot/joint/left_elbow_joint/cmd_pos', 10)

    def execute_handshake_callback(self, msg):
        self.get_logger().info("Processing Handshake Trajectory...")
        
        # Setup Stance
        for _ in range(15):
            self.pub_l_roll.publish(Float64(data=0.0))     
            self.pub_l_yaw.publish(Float64(data=0.0))      
            self.pub_l_pitch.publish(Float64(data=-0.95))  
            self.pub_l_elbow.publish(Float64(data=-0.75))  
            time.sleep(0.03)
        time.sleep(0.3)

        # Active Shaking Loop
        for cycle in range(3):
            for _ in range(8):
                self.pub_l_pitch.publish(Float64(data=-1.15))
                self.pub_l_elbow.publish(Float64(data=-0.70))
                time.sleep(0.03)
            time.sleep(0.1)
            
            for _ in range(8):
                self.pub_l_pitch.publish(Float64(data=-0.75))
                self.pub_l_elbow.publish(Float64(data=-0.40))
                time.sleep(0.03)
            time.sleep(0.1)

        self.reset_arm()

    def reset_arm(self):
        self.get_logger().info("Resetting Left Arm...")
        for _ in range(15):
            self.pub_l_roll.publish(Float64(data=0.0))
            self.pub_l_pitch.publish(Float64(data=0.0))
            self.pub_l_yaw.publish(Float64(data=0.0))
            self.pub_l_elbow.publish(Float64(data=0.0))
            time.sleep(0.02)

def main(args=None):
    rclpy.init(args=args)
    node = HandshakeController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
