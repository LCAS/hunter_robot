import os

from launch_ros.actions import Node

from launch import LaunchDescription
from launch.event_handlers import OnProcessExit

from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration
from launch.actions import IncludeLaunchDescription, RegisterEventHandler, DeclareLaunchArgument

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Declare the use_sim_time argument
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time'
    )

    # Launch configuration for use_sim_time
    use_sim_time_config = LaunchConfiguration('use_sim_time')

    # Include the Gazebo Sim launch file
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            ])
        ]),
        launch_arguments={'gz_args': '-r -v 4'}.items()
    )

    hunter_description_path = os.path.join(
        get_package_share_directory('hunter_description'))

    # Get URDF via xacro
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("hunter_description"), "description", 'robot.urdf.xacro']
            ),
        ]
    )
    robot_description = {
        "robot_description": ParameterValue(robot_description_content, value_type=str)
    }

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': use_sim_time_config}]
    )

    # Spawn entity in Gazebo Sim
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'hunter', '-allow_renaming', 'true'],
        output='screen'
    )

    # Bridge for clock
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen'
    )

    # Load joint state broadcaster using spawner
    load_joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen'
    )

    # Load ackermann controller using spawner
    load_ackermann_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['ackermann_like_controller'],
        output='screen'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=[
            '-d',
            os.path.join(hunter_description_path, 'rviz/robot_view.rviz'),
        ],
        output='screen',
        parameters=[{'use_sim_time': use_sim_time_config}]
    )

    return LaunchDescription([
        use_sim_time,
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=spawn_entity,
                on_exit=[load_joint_state_broadcaster],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=load_joint_state_broadcaster,
                on_exit=[load_ackermann_controller],
            )
        ),
        gazebo,
        bridge,
        rviz,
        node_robot_state_publisher,
        spawn_entity,
    ])
