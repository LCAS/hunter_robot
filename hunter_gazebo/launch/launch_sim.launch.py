import os

from launch_ros.actions import Node

from launch import LaunchDescription
from launch.event_handlers import OnProcessExit
from launch.conditions import IfCondition

from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration, PythonExpression
from launch.actions import IncludeLaunchDescription, RegisterEventHandler, DeclareLaunchArgument, SetEnvironmentVariable

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Force gz-transport and DDS to use localhost (needed when multicast is blocked)
    set_gz_ip = SetEnvironmentVariable('GZ_IP', '127.0.0.1')

    # Declare the use_sim_time argument
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time'
    )
    use_gazebo = DeclareLaunchArgument(
        'use_gazebo',
        default_value='true',
        description='Whether to start Gazebo server (set false if starting separately)'
    )
    gui = DeclareLaunchArgument(
        'gui',
        default_value='false',
        description='Whether to start the Gazebo GUI client'
    )
    use_rviz = DeclareLaunchArgument(
        'use_rviz',
        default_value='false',
        description='Whether to start RViz'
    )

    # Launch configuration for use_sim_time
    use_sim_time_config = LaunchConfiguration('use_sim_time')
    use_gazebo_config = LaunchConfiguration('use_gazebo')
    gui_config = LaunchConfiguration('gui')
    use_rviz_config = LaunchConfiguration('use_rviz')

    # Gazebo and RViz need a working OpenGL/GLX display. Default to server-only
    # Gazebo so remote/headless launches do not abort the whole simulation.
    gazebo_with_gui = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': '-r -v4 empty.sdf', 'on_exit_shutdown': 'true'}.items(),
        condition=IfCondition(PythonExpression([
            "'", use_gazebo_config, "' == 'true' and '", gui_config, "' == 'true'"
        ])),
    )
    gazebo_headless = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': '-s -r -v4 empty.sdf', 'on_exit_shutdown': 'true'}.items(),
        condition=IfCondition(PythonExpression([
            "'", use_gazebo_config, "' == 'true' and '", gui_config, "' != 'true'"
        ])),
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

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'hunter'],
        output='screen',
        parameters=[{'use_sim_time': use_sim_time_config}]
    )
    
    bridge_params = os.path.join(
        get_package_share_directory('hunter_gazebo'),
        'config',
        'gz_bridge.yaml'
    )
        
    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['--ros-args', '-p', f'config_file:={bridge_params}'],
    )

    load_joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager', '/controller_manager',
            '--controller-manager-timeout', '60',
        ],
        output='screen',
    )

    load_ackermann_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'ackermann_controller',
            '--controller-manager', '/controller_manager',
            '--controller-manager-timeout', '60',
        ],
        output='screen',
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=[
            '-d',
            os.path.join(hunter_description_path, 'rviz/robot_view.rviz'),
        ],
        output='screen',
        parameters=[{'use_sim_time': use_sim_time_config}],
        condition=IfCondition(use_rviz_config),
    )

    return LaunchDescription([
        set_gz_ip,
        use_sim_time,
        use_gazebo,
        gui,
        use_rviz,
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
        gazebo_with_gui,
        gazebo_headless,
        node_robot_state_publisher,
        rviz,
        ros_gz_bridge,
        spawn_entity,
    ])
