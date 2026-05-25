#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64
from geometry_msgs.msg import Twist
import time

class RobotBrainBridge(Node):
    def __init__(self):
        super().__init__('robot_brain_bridge')
        
        # 1. Listen to Colab commands
        self.command_subscription = self.create_subscription(
            String, '/robot/high_level_command', self.command_callback, 10)
            
        # 2. Base Movement Publisher
        self.vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # 3. LEFT ARM Joint Publishers (7-DOF)
        self.left_shoulder_pitch_pub = self.create_publisher(Float64, '/model/service_robot/joint/left_shoulder_pitch_joint/cmd_pos', 10)
        self.left_shoulder_roll_pub  = self.create_publisher(Float64, '/model/service_robot/joint/left_shoulder_roll_joint/cmd_pos', 10)
        self.left_shoulder_yaw_pub   = self.create_publisher(Float64, '/model/service_robot/joint/left_shoulder_yaw_joint/cmd_pos', 10)
        self.left_elbow_pub          = self.create_publisher(Float64, '/model/service_robot/joint/left_elbow_joint/cmd_pos', 10)
        self.left_wrist_pitch_pub    = self.create_publisher(Float64, '/model/service_robot/joint/left_wrist_pitch_joint/cmd_pos', 10)
        self.left_wrist_roll_pub     = self.create_publisher(Float64, '/model/service_robot/joint/left_wrist_roll_joint/cmd_pos', 10)
        self.left_wrist_yaw_pub      = self.create_publisher(Float64, '/model/service_robot/joint/left_wrist_yaw_joint/cmd_pos', 10)
        
        # 4. RIGHT ARM Joint Publishers (7-DOF)
        self.right_shoulder_pitch_pub = self.create_publisher(Float64, '/model/service_robot/joint/right_shoulder_pitch_joint/cmd_pos', 10)
        self.right_shoulder_roll_pub  = self.create_publisher(Float64, '/model/service_robot/joint/right_shoulder_roll_joint/cmd_pos', 10)
        self.right_shoulder_yaw_pub   = self.create_publisher(Float64, '/model/service_robot/joint/right_shoulder_yaw_joint/cmd_pos', 10)
        self.right_elbow_pub          = self.create_publisher(Float64, '/model/service_robot/joint/right_elbow_joint/cmd_pos', 10)
        self.right_wrist_pitch_pub    = self.create_publisher(Float64, '/model/service_robot/joint/right_wrist_pitch_joint/cmd_pos', 10)
        self.right_wrist_roll_pub     = self.create_publisher(Float64, '/model/service_robot/joint/right_wrist_roll_joint/cmd_pos', 10)
        self.right_wrist_yaw_pub      = self.create_publisher(Float64, '/model/service_robot/joint/right_wrist_yaw_joint/cmd_pos', 10)
            
        self.get_logger().info('🧠 14-DOF Master Brain Bridge Active with advanced multi-axis gestures!')

    def command_callback(self, msg):
        command = msg.data.lower().strip()
        self.get_logger().info(f'Received execution intent: "{command}"')

        # Add "small_wave" or "wave" fallbacks here to bypass tight_corridor limits
        if command in ["move", "patrol_step"]:
            self.drive_robot(speed=0.3, duration_steps=15)
        elif command == "stop_patrol":
            self.drive_robot(speed=0.0, duration_steps=1)
        elif command in ["wave", "small_wave", "forced_wave"]:  # ◀️ Add fallbacks here
            self.execute_natural_wave()
        elif command == "handshake":
            self.execute_handshake()
        elif command == "hand_up":
            self.execute_hand_up()
        elif command == "hand_down":
            self.reset_arms()
        else:
            self.get_logger().warn(f'Unknown action payload: "{command}"')

    def drive_robot(self, speed, duration_steps):
        twist = Twist()
        twist.linear.x = speed
        for _ in range(duration_steps):
            self.vel_publisher.publish(twist)
            time.sleep(0.1)
        twist.linear.x = 0.0
        self.vel_publisher.publish(twist)

    def execute_natural_wave(self):
        self.get_logger().info('Executing natural 7-DOF right-hand greeting wave...')
        self.reset_arms()
        time.sleep(0.2)
        
        # Bring right shoulder out to the side horizontally (Roll)
        # In URDF, right side angles are mirrored; lifting up out-sideways uses negative roll
        self.right_shoulder_roll_pub.publish(Float64(data=-1.2))
        
        # Fold the elbow inward slightly to clear the workspace and orient the hand up
        self.right_elbow_pub.publish(Float64(data=-0.8))
        time.sleep(0.3)
        
        # Shake the hand side-to-side using the wrist roll joint back and forth
        for _ in range(3):
            self.right_wrist_roll_pub.publish(Float64(data=0.5))
            time.sleep(0.3)
            self.right_wrist_roll_pub.publish(Float64(data=-0.5))
            time.sleep(0.3)
            
        self.reset_arms()

    def execute_handshake(self):
        self.get_logger().info('Executing advanced 7-DOF kinematic handshake with LEFT arm...')
        self.reset_arms()
        time.sleep(0.2)
        
        # 1. Swing upper arm directly FORWARD by pitching down around the Y-axis
        self.left_shoulder_pitch_pub.publish(Float64(data=-1.0))
        
        # 2. Lift the elbow joint so the forearm levels out flat towards the person
        self.left_elbow_pub.publish(Float64(data=0.6))
        
        # 3. Correct the wrist angle so the hand faces vertically (palm to the side), ready to meet a hand
        self.left_wrist_yaw_pub.publish(Float64(data=1.57))
        
        # Keep shoulder roll/yaw and other wrist axes locked neutral
        self.left_shoulder_roll_pub.publish(Float64(data=0.0))
        self.left_shoulder_yaw_pub.publish(Float64(data=0.0))
        self.left_wrist_pitch_pub.publish(Float64(data=0.0))
        self.left_wrist_roll_pub.publish(Float64(data=0.0))
        
        # Hold out presentation stance for engagement
        time.sleep(4.0) 
        self.reset_arms()

    def execute_hand_up(self):
        self.get_logger().info('Raising left arm forward and upward...')
        self.left_shoulder_pitch_pub.publish(Float64(data=-1.2))
        self.left_elbow_pub.publish(Float64(data=0.3))

    def reset_arms(self):
        # Reset LEFT arm joints to neutral zero positions
        self.left_shoulder_pitch_pub.publish(Float64(data=0.0))
        self.left_shoulder_roll_pub.publish(Float64(data=0.0))
        self.left_shoulder_yaw_pub.publish(Float64(data=0.0))
        self.left_elbow_pub.publish(Float64(data=0.0))
        self.left_wrist_pitch_pub.publish(Float64(data=0.0))
        self.left_wrist_roll_pub.publish(Float64(data=0.0))
        self.left_wrist_yaw_pub.publish(Float64(data=0.0))
        
        # Reset RIGHT arm joints to neutral zero positions
        self.right_shoulder_pitch_pub.publish(Float64(data=0.0))
        self.right_shoulder_roll_pub.publish(Float64(data=0.0))
        self.right_shoulder_yaw_pub.publish(Float64(data=0.0))
        self.right_elbow_pub.publish(Float64(data=0.0))
        self.right_wrist_pitch_pub.publish(Float64(data=0.0))
        self.right_wrist_roll_pub.publish(Float64(data=0.0))
        self.right_wrist_yaw_pub.publish(Float64(data=0.0))

def main(args=None):
    rclpy.init(args=args)
    node = RobotBrainBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()