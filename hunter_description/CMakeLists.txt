cmake_minimum_required(VERSION 3.16)
project(hunter_description LANGUAGES CXX)

if(CMAKE_CXX_COMPILER_ID MATCHES "(GNU|Clang)")
  add_compile_options(-Wall -Wextra)
endif()

find_package(ament_cmake REQUIRED)
find_package(control_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(std_msgs REQUIRED)
find_package(backward_ros REQUIRED)

install(
  DIRECTORY description launch config rviz meshes
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
