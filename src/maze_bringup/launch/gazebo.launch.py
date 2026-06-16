import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Nome do pacote interno atualizado
    pkg_name = 'robot_ras_ros'
    pkg_share = get_package_share_directory(pkg_name)
    
    # Define o caminho do arquivo de mundo correto do labirinto
    world_file = os.path.join(pkg_share, 'worlds', 'hacka_labyrinth.world')

    # Configura os caminhos de modelos para o Gazebo Sim encontrar as paredes
    models_path = os.path.join(pkg_share, 'models')
    if 'GZ_SIM_RESOURCE_PATH' in os.environ:
        os.environ['GZ_SIM_RESOURCE_PATH'] += f":{models_path}"
    else:
        os.environ['GZ_SIM_RESOURCE_PATH'] = models_path

    # Inclui o Launch do próprio Gazebo Sim (Nativo e moderno para o ROS Jazzy)
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f"-r {world_file}"}.items(),
    )

    # Inclui o seu arquivo de spawn (que coloca o robô lá dentro)
    spawn_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'spawn.launch.py')
        )
    )

    return LaunchDescription([
        gazebo,
        spawn_robot
    ])
