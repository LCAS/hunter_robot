cmake_minimum_required(VERSION 3.16)
project(hunter_description LANGUAGES CXX)

if(CMAKE_CXX_COMPILER_ID MATCHES "(GNU|Clang)")
  add_compile_options(-Wall -Wextra)
endif()

# find dependencies
set(THIS_PACKAGE_INCLUDE_DEPENDS
  hardware_interface
  pluginlib
  rclcpp
  rclcpp_lifecycle
)

# find dependencies
find_package(backward_ros REQUIRED)
find_package(ament_cmake REQUIRED)
foreach(Dependency IN ITEMS ${THIS_PACKAGE_INCLUDE_DEPENDS})
  find_package(${Dependency} REQUIRED)
endforeach()

## COMPILE
add_library(
  hunter_description
  SHARED
  hardware/carlikebot_system.cpp
)
target_compile_features(hunter_description PUBLIC cxx_std_17)
target_include_directories(hunter_description PUBLIC
$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/hardware/include>
$<INSTALL_INTERFACE:include/hunter_description>
)
ament_target_dependencies(
  hunter_description PUBLIC
  ${THIS_PACKAGE_INCLUDE_DEPENDS}
)

# Export hardware plugins
pluginlib_export_plugin_description_file(hardware_interface ros2_control_carlikebot.xml)

# INSTALL
install(
  DIRECTORY hardware/include/
  DESTINATION include/hunter_description
)
install(
  DIRECTORY description launch config rviz meshes
  DESTINATION share/hunter_description
)
install(TARGETS hunter_description
  EXPORT export_hunter_description
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)


## EXPORTS
ament_export_targets(export_hunter_description HAS_LIBRARY_TARGET)
ament_export_dependencies(${THIS_PACKAGE_INCLUDE_DEPENDS})
ament_package()
