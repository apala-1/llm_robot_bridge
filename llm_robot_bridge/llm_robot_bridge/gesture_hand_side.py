#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import math
import time

class GestureHandSide(Node):
    def __init__(self):
        super().__init__('gesture_hand_side')
        self.pitch_pub = self.create_publisher(Float64, '/left_arm/shoulder_pitch/cmd_pos', 10)
        self.roll_pub = self.create_publisher(Float64, '/left_arm/shoulder_roll/cmd_pos', 10)
        self.elbow_pub = self.create_publisher(Float64, '/left_arm/elbow/cmd_pos', 10)
        time.sleep(0.5)

    def send(self, pub, val):
        pub.publish(Float64(data=float(val)))

    def execute(self):
        self.get_logger().info("🌐 Executing Fluid Explaining Sweep...")
        rate = 0.02
        duration = 1.0
        steps = int(duration / rate)

        # Phase 1: Bring arm up to presentation position
        for i in range(steps):
            t = i * rate
            progress = t / duration
            smooth_step = (1.0 - math.cos(progress * math.pi)) / 2.0
            
            self.send(self.pitch_pub, 0.0 + (0.4 * smooth_step))
            self.send(self.roll_pub, 0.0 + (0.3 * smooth_step))
            self.send(self.elbow_pub, 0.0 + (-0.9 * smooth_step))
            time.sleep(rate)

        # Phase 2: Smooth fluid outward expansion sweep
        sweep_duration = 2.0
        sweep_steps = int(sweep_duration / rate)
        for i in range(sweep_steps):
            t = i * rate
            progress = t / sweep_duration
            # A single smooth slow arc out and back
            sweep_step = math.sin(progress * math.pi)
            
            self.send(self.roll_pub, 0.3 + (0.4 * sweep_step))    # Move arm wide open
            self.send(self.elbow_pub, -0.9 + (0.3 * sweep_step))  # Open elbow up slightly
            time.sleep(rate)

        # Phase 3: Retract smoothly
        for i in range(steps):
            t = i * rate
            progress = t / duration
            smooth_step = (1.0 - math.cos(progress * math.pi)) / 2.0
            
            self.send(self.pitch_pub, 0.4 - (0.4 * smooth_step))
            self.send(self.roll_pub, 0.3 - (0.3 * smooth_step))
            self.send(self.elbow_pub, -0.9 - (-0.9 * smooth_step))
            time.sleep(rate)

        self.get_logger().info("✅ Sweep Finished.")

def main():
    rclpy.init()
    node = GestureHandSide()
    node.execute()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
