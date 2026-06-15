#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import time

class GestureThinkingNode(Node):
    def __init__(self):
        super().__init__('gesture_thinking_node')
        
        # Arm Joint Publishers
        self.pitch_pub = self.create_publisher(Float64, '/right_arm/shoulder_pitch/cmd_pos', 10)
        self.roll_pub = self.create_publisher(Float64, '/right_arm/shoulder_roll/cmd_pos', 10)
        self.yaw_pub = self.create_publisher(Float64, '/right_arm/shoulder_yaw/cmd_pos', 10)
        self.elbow_pub = self.create_publisher(Float64, '/right_arm/elbow/cmd_pos', 10)
        
        # Index Finger Publishers
        self.index_j1_pub = self.create_publisher(Float64, '/right_hand/index_j1/cmd_pos', 10)
        self.index_j2_pub = self.create_publisher(Float64, '/right_hand/index_j2/cmd_pos', 10)
        self.index_j3_pub = self.create_publisher(Float64, '/right_hand/index_j3/cmd_pos', 10)
        
        # Middle Finger Publishers
        self.middle_j1_pub = self.create_publisher(Float64, '/right_hand/middle_j1/cmd_pos', 10)
        self.middle_j2_pub = self.create_publisher(Float64, '/right_hand/middle_j2/cmd_pos', 10)
        self.middle_j3_pub = self.create_publisher(Float64, '/right_hand/middle_j3/cmd_pos', 10)
        
        # Ring Finger Publishers
        self.ring_j1_pub = self.create_publisher(Float64, '/right_hand/ring_j1/cmd_pos', 10)
        self.ring_j2_pub = self.create_publisher(Float64, '/right_hand/ring_j2/cmd_pos', 10)
        self.ring_j3_pub = self.create_publisher(Float64, '/right_hand/ring_j3/cmd_pos', 10)
        
        # Pinky Finger Publishers
        self.pinky_j1_pub = self.create_publisher(Float64, '/right_hand/pinky_j1/cmd_pos', 10)
        self.pinky_j2_pub = self.create_publisher(Float64, '/right_hand/pinky_j2/cmd_pos', 10)
        self.pinky_j3_pub = self.create_publisher(Float64, '/right_hand/pinky_j3/cmd_pos', 10)
        
        # Thumb Publishers
        self.thumb_j1_pub = self.create_publisher(Float64, '/right_hand/thumb_j1/cmd_pos', 10)
        self.thumb_j2_pub = self.create_publisher(Float64, '/right_hand/thumb_j2/cmd_pos', 10)
        
        # Small delay to ensure publishers are fully connected to the ros_gz_bridge
        time.sleep(0.5)
        self.execute()

    def publish_value(self, publisher, value):
        msg = Float64()
        msg.data = float(value)
        publisher.publish(msg)

    def execute(self):
        self.get_logger().info('Executing updated Thinking Gesture pose...')
        
        # --- Arm Positions ---
        self.publish_value(self.pitch_pub, -0.87)
        self.publish_value(self.elbow_pub, -2.42)
        self.publish_value(self.yaw_pub, 0.46)
        # Keeping shoulder roll at 0.0 unless your pose requires an override
        self.publish_value(self.roll_pub, 0.0) 
        
        # --- Index Finger (Extended/Slightly curved) ---
        self.publish_value(self.index_j1_pub, 0.00)
        self.publish_value(self.index_j2_pub, 0.02)
        self.publish_value(self.index_j3_pub, 0.10)
        
        # --- Middle Finger (Curled In) ---
        self.publish_value(self.middle_j1_pub, 1.56)
        self.publish_value(self.middle_j2_pub, 1.49)
        self.publish_value(self.middle_j3_pub, 1.46)
        
        # --- Ring Finger (Curled In) ---
        self.publish_value(self.ring_j1_pub, 1.54)
        self.publish_value(self.ring_j2_pub, 1.55)
        self.publish_value(self.ring_j3_pub, 1.47)

        # --- Pinky Finger (Curled In) ---
        self.publish_value(self.pinky_j1_pub, 1.54)
        self.publish_value(self.pinky_j2_pub, 1.49)
        self.publish_value(self.pinky_j3_pub, 1.47)
        
        # --- Thumb (Closed over fist base) ---
        self.publish_value(self.thumb_j1_pub, 1.56)
        self.publish_value(self.thumb_j2_pub, 1.48)
        
        # Keep the pose held for a natural processing duration
        time.sleep(2.5)

def main():
    rclpy.init()
    node = GestureThinkingNode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()