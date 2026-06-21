import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource # 💡 Fixed Capitalization
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    config_file_path = os.path.expanduser('~/ros2_ws/src/llm_robot_bridge/config/bridge_config.yaml')

    # Node 1: ROS GZ Parameter Bridge
    parameter_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        parameters=[{'config_file': config_file_path}],
        output='screen'
    )

    # Node 2: Dynamic Live Gesture Manager
    gesture_node = Node(
        package='llm_robot_bridge',
        executable='gesture_manager_node',
        name='gesture_manager_node',
        output='screen'
    )

    # Node 3: Local WebSocket Server
    rosbridge_launch = IncludeLaunchDescription(
        XMLLaunchDescriptionSource([
            os.path.join(get_package_share_directory('rosbridge_server'), 'launch', 'rosbridge_websocket_launch.xml')
        ]),
        launch_arguments={'port': '9090'}.items()
    )

    return LaunchDescription([
        parameter_bridge_node,
        gesture_node,
        rosbridge_launch
    ])
