#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Empty

class MotionCoordinator(Node):
    def __init__(self):
        super().__init__('motion_coordinator')
        self.get_logger().info("🎛️ Central Motion Coordinator Activated!")

        # Listen to the main system intent tunnel
        self.cmd_sub = self.create_subscription(
            String, '/robot/high_level_command', self.command_callback, 10)

        # Dedicated execution trigger publishers
        self.pub_wave = self.create_publisher(Empty, '/gesture/wave', 10)
        self.pub_handshake = self.create_publisher(Empty, '/gesture/handshake', 10)

    def command_callback(self, msg):
        intent = msg.data.lower().strip()
        
        if intent == "wave":
            self.get_logger().info("Routing intent -> Wave Node")
            self.pub_wave.publish(Empty())
        elif intent == "handshake":
            self.get_logger().info("Routing intent -> Handshake Node")
            self.pub_handshake.publish(Empty())
        elif intent == "patrol_step":
            # Silently drop or route to a navigation/base node if built later
            pass
        else:
            self.get_logger().warn(f"Intent '{intent}' unhandled by coordinator.")

def main(args=None):
    rclpy.init(args=args)
    node = MotionCoordinator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
