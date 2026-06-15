import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random
import os
import subprocess

class WallSpawner(Node):
    def __init__(self):
        super().__init__('wall_spawner')
        # 1. Setup a publisher to tell your LLM pipeline how narrow the hall is
        self.distance_pub = self.create_publisher(Float32, '/corridor_width', 10)
        
        # 2. Generate a random corridor width between 0.6 meters (very tight) and 1.8 meters (wide)
        self.corridor_width = random.uniform(0.6, 1.8)
        self.get_logger().info(f"🎲 Random Corridor Width Generated: {self.corridor_width:.2f} meters")
        
        # 3. Spawn the left and right walls in Gazebo Sim
        self.spawn_wall("left_wall", y_pos=(self.corridor_width / 2.0))
        self.spawn_wall("right_wall", y_pos=-(self.corridor_width / 2.0))
        
        # 4. Broadcast the value continuously so other nodes (and Colab) can hear it
        self.timer = self.create_timer(1.0, self.publish_width)

    def spawn_wall(self, name, y_pos):
        # Path to a simple box/wall URDF or SDF file
        # Creating a simple box model argument string on the fly for the Gazebo spawn service
        xml_box = f'''<?xml version="1.0"?>
        <sdf version="1.6">
          <model name="{name}">
            <static>true</static>
            <link name="link">
              <collision name="collision">
                <geometry><box><size>5.0 0.1 2.0</size></box></geometry>
              </collision>
              <visual name="visual">
                <geometry><box><size>5.0 0.1 2.0</size></box></geometry>
                <material><ambient>0.7 0.2 0.2 1</ambient></material>
              </visual>
            </link>
          </model>
        </sdf>'''
        
        # Write to temporary file to feed to ros_gz_sim spawn service
        tmp_path = f"/tmp/{name}.sdf"
        with open(tmp_path, "w") as f:
            f.write(xml_box)
            
        # Call the Gazebo spawn service
        cmd = f"ros2 run ros_gz_sim create -file {tmp_path} -name {name} -x 0.0 -y {y_pos} -z 1.0"
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL)

    def publish_width(self):
        msg = Float32()
        msg.data = self.corridor_width
        self.distance_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = WallSpawner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
