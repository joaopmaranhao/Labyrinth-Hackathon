from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    ros_gz_sim = get_package_share_directory('ros_gz_sim')

    gz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': 'empty.sdf -r'}.items()
    )

    perception = Node(
        package='maze_robot',
        executable='perception_node',
        output='screen'
    )

    navigation = Node(
        package='maze_robot',
        executable='navigation_node',
        output='screen'
    )

    return LaunchDescription([
        gz,
        perception,
        navigation,
    ])