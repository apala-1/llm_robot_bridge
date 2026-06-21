#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import subprocess
import os
import sys
import time

class GestureManagerNode(Node):
    def __init__(self):
        super().__init__('gesture_manager_node')

        base_path = os.path.expanduser('~/ros2_ws/src/llm_robot_bridge/llm_robot_bridge')

        self.gesture_mapping = {
            'wave': os.path.join(base_path, 'gesture_wave.py'),
            'handshake': os.path.join(base_path, 'gesture_handshake.py'),
            'hand_up': os.path.join(base_path, 'gesture_hand_up.py'),
            'hand_side': os.path.join(base_path, 'gesture_hand_side.py'),
            'hand_down': os.path.join(base_path, 'gesture_hand_down.py'),
            'thinking': os.path.join(base_path, 'gesture_thinking.py'),
            'talking': os.path.join(base_path, 'gesture_talking.py'),
            'walk': os.path.join(base_path, 'gesture_walk.py'),
            'walking': os.path.join(base_path, 'gesture_walk.py'),
        }

        # Normalize naming differences between what Colab/CSV sends and our dict keys
        self.alias_map = {
            'hand_shake': 'handshake',
            'handshake_gesture': 'handshake',
            'state_thinking': 'thinking',   # so the state-ping also works as a real gesture trigger
            'raise_hand': 'hand_up',
            'raise_hands': 'hand_up',
            'lower_hand': 'hand_down',
            'side_hand': 'hand_side',
        }

        self.hand_down_script = self.gesture_mapping['hand_down']

        self.log_file_path = os.path.expanduser('~/gesture_execution.log')

        with open(self.log_file_path, 'w') as f:
            f.write("=== GESTURE BACKGROUND PROCESS MONITOR ===\n")
            f.write("🚀 Target Topic Linked. Ready for cloud triggers...\n")

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

        # Normalize aliases before lookup (this is the fix)
        command = self.alias_map.get(command, command)

        with open(self.log_file_path, 'a') as log_file:
            log_file.write(f"\n[RECEIVED VIA TUNNEL]: '{raw_data}' -> normalized: '{command}'\n")

            # Ignore harmless state pings that aren't gestures
            if command in ('state_speaking', 'state_idle'):
                log_file.write(f"[STATE PING] Ignored non-gesture state message.\n")
                log_file.flush()
                return

            if command in self.gesture_mapping:
                script_path = self.gesture_mapping[command]

                current_env = os.environ.copy()
                current_env["PYTHONPATH"] = os.path.dirname(script_path) + os.pathsep + current_env.get("PYTHONPATH", "")

                if command == 'hand_down':
                    log_file.write(f"[SUCCESS] Launching Trajectory Script: {script_path}\n")
                    log_file.flush()
                    subprocess.Popen([sys.executable, script_path], stdout=log_file, stderr=log_file, env=current_env)

                else:
                    log_file.write(f"[PIPELINE] ⏳ Step 1: Forcing pre-gesture hand down reset...\n")
                    log_file.flush()
                    subprocess.run([sys.executable, self.hand_down_script], stdout=log_file, stderr=log_file, env=current_env)

                    time.sleep(1.0)

                    log_file.write(f"[PIPELINE] 🚀 Step 2: Launching Target Trajectory Script: {script_path}\n")
                    log_file.flush()
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