// ref: https://github.com/ros-controls/ros2_control_demos.git

#ifndef _CARLIKEBOT_SYSTEM_HPP_
#define _CARLIKEBOT_SYSTEM_HPP_

#include <map>
#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "hardware_interface/handle.hpp"
#include "hardware_interface/hardware_info.hpp"
#include "hardware_interface/system_interface.hpp"
#include "hardware_interface/types/hardware_interface_return_values.hpp"
#include "rclcpp/clock.hpp"
#include "rclcpp/duration.hpp"
#include "rclcpp/logger.hpp"
#include "rclcpp/macros.hpp"
#include "rclcpp/time.hpp"
#include "rclcpp_lifecycle/node_interfaces/lifecycle_node_interface.hpp"
#include "rclcpp_lifecycle/state.hpp"

namespace hunter_description
{
struct JointValue {
  double position{0.0};
  double velocity{0.0};
  double effort{0.0};
};

struct Joint {
  explicit Joint(const std::string & name) : joint_name(name)   {
    state = JointValue();
    command = JointValue();
  }

  Joint() = default;

  std::string joint_name;
  JointValue state;
  JointValue command;
};

class CarlikeBotSystemHardware : public hardware_interface::SystemInterface {
public:
  RCLCPP_SHARED_PTR_DEFINITIONS(CarlikeBotSystemHardware);

  hardware_interface::CallbackReturn on_init(const hardware_interface::HardwareInfo & info) override;

  std::vector<hardware_interface::StateInterface> export_state_interfaces() override;
  std::vector<hardware_interface::CommandInterface> export_command_interfaces() override;
  hardware_interface::CallbackReturn on_activate(const rclcpp_lifecycle::State & previous_state) override;
  hardware_interface::CallbackReturn on_deactivate(const rclcpp_lifecycle::State & previous_state) override;
  hardware_interface::return_type read(const rclcpp::Time & time, const rclcpp::Duration & period) override;
  hardware_interface::return_type write(const rclcpp::Time & time, const rclcpp::Duration & period) override;

  // Get the logger of the SystemInterface.
  rclcpp::Logger get_logger() const { return *logger_; }

  // Get the clock of the SystemInterface.
  rclcpp::Clock::SharedPtr get_clock() const { return clock_; }

private:
  // Parameters for the CarlikeBot simulation
  double hw_start_sec_;
  double hw_stop_sec_;

  // Objects for logging
  std::shared_ptr<rclcpp::Logger> logger_;
  rclcpp::Clock::SharedPtr clock_;
  std::map<std::string, Joint> hw_interfaces_;
};

}  // namespace hunter_description

#endif  // _CARLIKEBOT_SYSTEM_HPP_
