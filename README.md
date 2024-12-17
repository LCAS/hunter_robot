# Hunter Robot Simulation

This repository contains the **URDF** description and Gazebo simulation for the **Hunter V2** robot. The Hunter V2 is an **Ackermann-steered** mobile robot with front-wheel steering, simulated using ROS 2 control.

Official Robot Website: [AgileX Hunter V2B](https://robosavvy.co.uk/agilex-hunter-2b.html)

---

## Key Features

- **Ackermann Steering**: Configured for front-wheel steering with accurate kinematics.
- **ROS 2 Control Integration**: Leverages `ros2_control` for simulating robot kinematics and dynamics.
- **URDF Description**: Detailed robot description based on manufacturer specifications.
- **Gazebo Simulation**: Visualize and simulate the Hunter V2 robot in Gazebo.
- **Rviz Support**: Visualize the robot and interact with its joints using Rviz.

---


## Installation and Build Instructions

### Prerequisites
Ensure you have a ROS 2 workspace set up. If not, create one:
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
```

### Clone and Build
1. Clone this repository into your ROS 2 workspace:
    ```bash
    cd ~/ros2_ws/src
    git clone https://github.com/LCAS/hunter_robot.git
    ```
2. Install dependencies:
    ```bash
    rosdep update
    rosdep install --from-paths . --ignore-src -r -y
    ```
3. Build the workspace:
    ```bash
    cd ~/ros2_ws
    colcon build
    source install/setup.bash
    ```

---

## Packages Overview

This repository includes the following ROS 2 packages:

1. **`hunter_description`**: URDF and robot description files.
2. **`hunter_gazebo`**: Simulation environment for the Hunter V2 in Gazebo.

---

## Usage

### 1. Visualize the Robot in Rviz

To view the robot model and interact with its joints in Rviz:

```bash
ros2 launch hunter_description robot_view.launch.py
```

This launch file starts Rviz and loads the Hunter V2 model.

[Rviz Simulation](https://github.com/user-attachments/assets/1cc10c03-fad7-47b0-8816-74c49d79be31)

---

### 2. Simulate the Robot in Gazebo

To load the Hunter V2 in a Gazebo simulation environment:

```bash
ros2 launch hunter_gazebo launch_sim.launch.py
```

[Gazebo Simulation](https://github.com/user-attachments/assets/90757617-af3b-4bc8-bf1f-f08c5ecc1247)

---

### 3. Control the Robot with Teleop

You can control the Hunter V2 using the `teleop_twist_keyboard` package. First, ensure the simulation is running, then execute:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/ackermann_like_controller/cmd_vel
```

Use the keyboard inputs to move the robot in the simulation.

---

## Robot Controller Configuration

The main configuration of the robot controller is available [here](https://github.com/LCAS/hunter_robot/blob/refactor/hunter_description/config/ackermann_like_controller.yaml)

---

## Robot Specifications

The primary robot parameters, such as mass, wheel size, and turning angles, are derived from the manufacturer's specifications and the following reference repository:

- [Hunter 2 Base URDF (AgileX Robotics)](https://github.com/agilexrobotics/ugv_gazebo_sim/blob/master/hunter/hunter2_base/urdf/hunter2_base_gazebo.xacro)

---

## License

This project is licensed under the **Apache License**. See the [LICENSE](LICENSE) file for details.

---

## References

For more details on ROS 2 Control and Gazebo integration, see:

- [ros2_controllers](https://github.com/ros-controls/ros2_controllers/tree/master)
- [gazebo_ros2_control](https://github.com/ros-controls/gazebo_ros2_control)
- [Getting Started with ros2_control](https://control.ros.org/humble/doc/getting_started/getting_started.html)
- [ros2controlcli Documentation](https://control.ros.org/master/doc/ros2_control/ros2controlcli/doc/userdoc.html)
- [gazebo_ros2_control User Guide](https://control.ros.org/rolling/doc/gazebo_ros2_control/doc/index.html)
- [Video Tutorial](https://youtu.be/BcjHyhV0kIs?si=dUpg7IF-kHSUgB-w)

---
