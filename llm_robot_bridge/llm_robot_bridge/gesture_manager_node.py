#!/usr/bin/env python3
from time import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import subprocess
import os
import sys

class GestureManagerNode(Node):
    def __init__(self):
        super().__init__('gesture_manager_node')
        
        # Absolute source directory path targeting your verified scripts
        base_path = os.path.expanduser('~/ros2_ws/src/llm_robot_bridge/llm_robot_bridge')
        
        self.gesture_mapping = {
            'wave': os.path.join(base_path, 'gesture_wave.py'),
            'handshake': os.path.join(base_path, 'gesture_handshake.py'),
            'hand_up': os.path.join(base_path, 'gesture_hand_up.py'),
            'hand_side': os.path.join(base_path, 'gesture_hand_side.py'),
            'hand_down': os.path.join(base_path, 'gesture_hand_down.py'),
            'state_thinking': os.path.join(base_path, 'gesture_thinking.py'),
            'walk': os.path.join(base_path, 'gesture_walk.py')
        }
        
        self.log_file_path = os.path.expanduser('~/gesture_execution.log')
        
        with open(self.log_file_path, 'w') as f:
            f.write("=== GESTURE BACKGROUND PROCESS MONITOR ===\n")
            f.write("🚀 Target Topic Linked. Ready for cloud triggers...\n")
        
        # 🎯 TARGET LOCKED: Using your verified pipeline topic
        target_topic = '/robot/high_level_command'
        
        self.subscription = self.create_subscription(
            String,
            target_topic,
            self.gesture_callback,
            10
        )
        
        self.get_logger().info("======================================================")
        self.get_logger().info("🚀 FIXED GESTURE MANAGER IS RUNNING")
        self.get_logger().info(f"📡 Directly Intercepting: {target_topic}")
        self.get_logger().info("======================================================")

    def gesture_callback(self, msg):
        raw_data = msg.data
        command = raw_data.strip().lower()
        
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(f"\n[RECEIVED VIA TUNNEL]: '{raw_data}'\n")
            
            if command in self.gesture_mapping:
                script_path = self.gesture_mapping[command]
                log_file.write(f"[SUCCESS] Launching Trajectory Script: {script_path}\n")
                log_file.flush()
                
                # Keep active ROS variables intact in the environment
                current_env = os.environ.copy()
                current_env["PYTHONPATH"] = os.path.dirname(script_path) + os.pathsep + current_env.get("PYTHONPATH", "")
                
                # --- PIPELINE SEQUENCER WRAPPER ---
                # If it's already a hand_down command, don't wrap it! Just run it directly.
                if command == 'hand_down':
                    log_file.write(f"[SUCCESS] Launching Trajectory Script: {script_path}\n")
                    log_file.flush()
                    subprocess.Popen([sys.executable, script_path], stdout=log_file, stderr=log_file, env=current_env)
                
                else:
                    log_file.write(f"[PIPELINE] ⏳ Step 1: Forcing pre-gesture hand down reset...\n")
                    log_file.flush()
                    # We use subprocess.run (blocking call) here to force the robot to finish moving down
                    subprocess.run([sys.executable, self.hand_down_script], stdout=log_file, stderr=log_file, env=current_env)
                    
                    # Brief structural pause for physics simulation stability
                    time.sleep(1.0)
                    
                    log_file.write(f"[PIPELINE] 🚀 Step 2: Launching Target Trajectory Script: {script_path}\n")
                    log_file.flush()
                    # We use subprocess.run here so the manager waits until your active gesture completes 
                    subprocess.run([sys.executable, script_path], stdout=log_file, stderr=log_file, env=current_env)
                    
                    time.sleep(0.5)
                    
                    log_file.write(f"[PIPELINE] ⏳ Step 3: Returning to post-gesture hand down reset...\n")
                    log_file.flush()
                    subprocess.Popen([sys.executable, self.hand_down_script], stdout=log_file, stderr=log_file, env=current_env)
            else:
                log_file.write(f"[MISMATCH] Command '{command}' not registered in manager keys.\n")
                log_file.flush()

def main(args=None):
    rclpy.init(args=args)
    node = GestureManagerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()