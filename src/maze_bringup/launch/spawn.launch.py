import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'robot_ras_ros'
    pkg_share = get_package_share_directory(pkg_name)

    # Caminho para o arquivo URDF/XACRO mestre do robô
    xacro_file = os.path.join(pkg_share, 'urdf', 'robot.urdf.xacro')

    # Nó do Robot State Publisher (converte XACRO para URDF em tempo de execução)
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': Command(['xacro ', xacro_file]),
            'use_sim_time': True
        }]
    )

    # Nó de Spawn MODERNO para o Gazebo Sim (Harmonic / Jazzy)
    # Substitui o antigo 'spawn_entity.py' do 'gazebo_ros'
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_robot',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'robot_diff',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.2'
        ],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        spawn_robot
    ])
