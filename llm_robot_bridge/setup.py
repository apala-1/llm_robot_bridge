import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'llm_robot_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include your launch files
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['tests'],
    entry_points={
        'console_scripts': [
            'gesture_manager_node = llm_robot_bridge.gesture_manager_node:main',
            'gesture_wave = llm_robot_bridge.gesture_wave:main',
            'gesture_handshake = llm_robot_bridge.gesture_handshake:main',
            'gesture_hand_up = llm_robot_bridge.gesture_hand_up:main',
            'gesture_hand_side = llm_robot_bridge.gesture_hand_side:main',
            'gesture_hand_down = llm_robot_bridge.gesture_hand_down:main',
            'gesture_thinking = llm_robot_bridge.gesture_thinking:main',
            'gesture_walk = llm_robot_bridge.gesture_walk:main',
            'gesture_talking = llm_robot_bridge.gesture_talking:main',
            'wall_spawner = llm_robot_bridge.spawn_walls:main',
        ],
    },
)
