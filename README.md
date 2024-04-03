# hunter_robot

## Setup and Build Hunter Robot Packages in Your Catkin Workspace

Clone the packages into your catkin workspace and compile

```
$ cd ~/ros2_ws/src
$ git https://github.com/LCAS/hunter_robot.git
$ cd hunter_robot
$ git submodule update --init --recursive  # Pull the submodules
$ cd ../..
$ colcon build
```
