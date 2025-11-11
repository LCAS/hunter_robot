# Gazebo Classic to Gazebo Sim Migration Guide

This document describes the migration from Gazebo Classic to Gazebo Sim (formerly Ignition Gazebo) for the hunter_robot package.

## Overview

The hunter_gazebo package now supports both Gazebo Classic and Gazebo Sim, allowing users to choose their preferred simulation environment.

## What Changed

### 1. Package Dependencies (hunter_gazebo/package.xml)

Added new dependencies for Gazebo Sim while keeping Gazebo Classic dependencies:

```xml
<exec_depend>ros_gz_sim</exec_depend>
<exec_depend>ros_gz_bridge</exec_depend>
<exec_depend>gz_ros2_control</exec_depend>
```

### 2. Launch Files

- **launch_sim.launch.py** (unchanged): For Gazebo Classic
- **launch_gz_sim.launch.py** (new): For Gazebo Sim

Key differences in the Gazebo Sim launch file:
- Uses `ros_gz_sim/gz_sim.launch.py` instead of `gazebo_ros/gazebo.launch.py`
- Uses `ros_gz_sim/create` instead of `gazebo_ros/spawn_entity.py`
- Adds clock bridge: `/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock`
- Uses `controller_manager/spawner` nodes instead of `ExecuteProcess` with ros2 CLI

### 3. URDF/Xacro (hunter_description/description/ros2_control.xacro)

Added conditional plugin loading using xacro arguments to prevent both plugins from loading simultaneously:

```xml
<!-- Argument to select simulator type: 'classic' or 'sim' (default: classic) -->
<xacro:arg name="sim_gazebo" default="classic"/>

<!-- Gazebo Classic plugin - loaded when sim_gazebo:=classic -->
<xacro:if value="$(arg sim_gazebo == 'classic')">
  <gazebo>
    <plugin filename="libgazebo_ros2_control.so" name="gazebo_ros2_control">
      <parameters>$(find-pkg-share hunter_description)/config/ackermann_like_controller.yaml</parameters>
    </plugin>
  </gazebo>
</xacro:if>

<!-- Gazebo Sim plugin - loaded when sim_gazebo:=sim -->
<xacro:if value="$(arg sim_gazebo == 'sim')">
  <gazebo>
    <plugin filename="libgz_ros2_control-system.so" name="gz_ros2_control::GazeboSimROS2ControlPlugin">
      <parameters>$(find-pkg-share hunter_description)/config/ackermann_like_controller.yaml</parameters>
    </plugin>
  </gazebo>
</xacro:if>
```

The launch files pass the appropriate `sim_gazebo` argument to ensure only the correct plugin is loaded for each simulator. Also updated the parameter path syntax from `$(find ...)` (ROS1 style) to `$(find-pkg-share ...)` (ROS2 style).

## Usage

### Gazebo Sim (Recommended)

```bash
ros2 launch hunter_gazebo launch_gz_sim.launch.py
```

### Gazebo Classic (Legacy)

```bash
ros2 launch hunter_gazebo launch_sim.launch.py
```

### Teleop Control (works with both)

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/ackermann_like_controller/cmd_vel
```

## Technical Details

### Controller Loading

**Gazebo Classic approach** (ExecuteProcess):
```python
load_joint_state_broadcaster = ExecuteProcess(
    cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
         'joint_state_broadcaster'],
    output='screen'
)
```

**Gazebo Sim approach** (spawner node):
```python
load_joint_state_broadcaster = Node(
    package='controller_manager',
    executable='spawner',
    arguments=['joint_state_broadcaster'],
    output='screen'
)
```

### Clock Synchronization

Gazebo Sim requires explicit clock bridging:
```python
bridge = Node(
    package='ros_gz_bridge',
    executable='parameter_bridge',
    arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
    output='screen'
)
```

### Plugin Selection

The URDF uses xacro conditional logic to load only one plugin at a time based on the `sim_gazebo` argument:
- `sim_gazebo:=classic` (default) loads `libgazebo_ros2_control.so` for Gazebo Classic
- `sim_gazebo:=sim` loads `libgz_ros2_control-system.so` for Gazebo Sim

This prevents both plugins from attempting to load simultaneously.

## Backward Compatibility

All changes maintain backward compatibility:
- Original Gazebo Classic launch file remains unchanged
- Only the appropriate plugin loads based on which simulator is running (controlled by xacro argument)
- Original dependencies are kept alongside new ones
- Default behavior (when no argument is passed) is Gazebo Classic

## Testing

To test the migration:

1. **Build the package**:
   ```bash
   colcon build --packages-select hunter_gazebo hunter_description
   source install/setup.bash
   ```

2. **Test Gazebo Sim**:
   ```bash
   ros2 launch hunter_gazebo launch_gz_sim.launch.py
   ```
   
3. **Test Gazebo Classic** (ensure backward compatibility):
   ```bash
   ros2 launch hunter_gazebo launch_sim.launch.py
   ```

4. **Verify controllers**:
   ```bash
   ros2 control list_controllers
   ```
   
   Expected output:
   - `joint_state_broadcaster[joint_state_broadcaster/JointStateBroadcaster] active`
   - `ackermann_like_controller[tricycle_controller/TricycleController] active`

5. **Test robot control**:
   ```bash
   ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/ackermann_like_controller/cmd_vel
   ```

## References

- [LCAS Migration Guide](https://github.com/LCAS/aoc_distro/wiki/Migration-to-new-Gazebo)
- [ros_gz_sim Documentation](https://github.com/gazebosim/ros_gz)
- [gz_ros2_control Documentation](https://github.com/ros-controls/gz_ros2_control)
- [RBT1001 Reference Implementation](https://github.com/LCAS/RBT1001)
