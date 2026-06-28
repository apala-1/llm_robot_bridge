import json
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MockHandNode(Node):
    def __init__(self):
        super().__init__('mock_hand_node')
        # Listen exactly on the topic your Colab code is targeting
        self.sub = self.create_subscription(String, '/hand_state', self.callback, 10)
        self.get_logger().info("🏠 Mock Robot Home Listener Started! Awaiting Colab payloads...")

    def callback(self, msg):
        try:
            # Parse the incoming string into a JSON dictionary
            data = json.loads(msg.data)
            self.get_logger().info(f"📥 RECEIVED JSON DICTIONARY: {data}")
            
            # Print out what the robot would be doing
            for behavior, state in data.items():
                if state == 1:
                    print(f"   ▶ Starting Behavior: '{behavior}'")
                elif state == 0:
                    print(f"   ■ Stopping Behavior cleanly: '{behavior}'")
        except Exception as e:
            print(f"⚠️ Failed to parse message. Raw string was: {msg.data} | Error: {e}")

def main():
    rclpy.init()
    node = MockHandNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
