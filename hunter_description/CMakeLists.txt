cmake_minimum_required(VERSION 3.16)
project(hunter_description)

# NOTE (Jazzy / new Gazebo cleanup):
# This is a description-only package: it ships xacro/URDF, controller configs,
# launch files, rviz and meshes. It contains NO C++ or Python source, so the
# previous find_package() calls for rclcpp, rclcpp_action, control_msgs,
# geometry_msgs, std_msgs and backward_ros (and the CXX language) were unused
# build dependencies and have been removed. Only ament_cmake is required to
# install the shared resources.
find_package(ament_cmake REQUIRED)

install(
  DIRECTORY description launch config rviz meshes
  DESTINATION share/${PROJECT_NAME}/
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
