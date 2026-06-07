#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import time

class WaveActionNode(Node):
    def __init__(self):
        super().__init__('wave_action_node')
        
        # Publishers matching the bridge topics
        self.pitch_pub = self.create_publisher(Float64, '/left_arm/shoulder_pitch/cmd_pos', 10)
        self.roll_pub = self.create_publisher(Float64, '/left_arm/shoulder_roll/cmd_pos', 10)
        self.elbow_pub = self.create_publisher(Float64, '/left_arm/elbow/cmd_pos', 10)
        
        # Create a timer loop to run the waving state machine sequence
        self.timer = self.create_timer(0.8, self.execute_wave_sequence)
        self.step = 0
        self.get_logger().info("Wave Action Node initialized. Starting sequence...")

    def send_cmd(self, publisher, value):
        msg = Float64()
        msg.data = float(value)
        publisher.publish(msg)

    def execute_wave_sequence(self):
        if self.step == 0:
            # Step 1: Bring arm up into preparation stance
            self.get_logger().info("Raising arm up...")
            self.send_cmd(self.pitch_pub, 1.2)   # Swing forward/up
            self.send_cmd(self.elbow_pub, -0.5)  # Slight bend at elbow
            self.send_cmd(self.roll_pub, 0.5)    # Move arm slightly outward
            self.step = 1
            
        elif self.step == 1:
            # Step 2: Wave Outward
            self.send_cmd(self.roll_pub, 0.9)
            self.step = 2
            
        elif self.step == 2:
            # Step 3: Wave Inward
            self.send_cmd(self.roll_pub, 0.3)
            self.step = 1 # Loop back between step 1 and 2 to keep waving

def main(args=None):
    rclpy.init(args=args)
    node = WaveActionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down waving sequence node safely.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
