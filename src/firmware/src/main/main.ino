#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <geometry_msgs/msg/twist.h>
#include <ESP32Servo.h>

// Motor setup
Servo leftMotor;
Servo rightMotor;
const int LEFT_MOTOR_PIN = 19;
const int RIGHT_MOTOR_PIN = 18;
const int MAX_SPEED = 180; // Max speed for ESC
const int MIN_SPEED = 0;   // Min speed for ESC

// ROS variables
rcl_subscription_t twist_subscriber;
geometry_msgs__msg__Twist twist_msg;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;

// Error handling macros
#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)) { error_loop(); }}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)) {} }

// Error loop
void error_loop() {
  while (1) {
    delay(100);
  }
}

// Callback for Twist messages
void twist_callback(const void *msgin) {
  const geometry_msgs__msg__Twist *msg = (const geometry_msgs__msg__Twist *)msgin;

  // Map linear.x to motor speed (forward/backward)
  int base_speed = map(msg->linear.x, -1.0, 1.0, MIN_SPEED, MAX_SPEED);

  // Map angular.z to differential speed for turning
  int turn_offset = map(msg->angular.z, -1.0, 1.0, -50, 50);

  // Calculate motor speeds
  int left_speed = constrain(base_speed - turn_offset, MIN_SPEED, MAX_SPEED);
  int right_speed = constrain(base_speed + turn_offset, MIN_SPEED, MAX_SPEED);

  // Set motor speeds
  leftMotor.write(left_speed);
  rightMotor.write(right_speed);

}

void setup() {
  Serial.begin(115200);

  // Setup motor control pins and timers
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  leftMotor.setPeriodHertz(50);
  rightMotor.setPeriodHertz(50);
  leftMotor.attach(LEFT_MOTOR_PIN, 1000, 2000);
  rightMotor.attach(RIGHT_MOTOR_PIN, 1000, 2000);

  // Initialize micro-ROS
  set_microros_transports();
  delay(2000); // Allow time for initialization

  allocator = rcl_get_default_allocator();
  RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

  // Create node
  RCCHECK(rclc_node_init_default(&node, "micro_ros_esp32_twist_node", "", &support));

  // Create Twist subscriber
  RCCHECK(rclc_subscription_init_default(
    &twist_subscriber,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(geometry_msgs, msg, Twist),
    "cmd_vel"
  ));

  // Create executor
  RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
  RCCHECK(rclc_executor_add_subscription(&executor, &twist_subscriber, &twist_msg, &twist_callback, ON_NEW_DATA));
}

void loop() {
  // Spin the executor to process callbacks
  RCSOFTCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100)));
  delay(100); // Prevent CPU overuse
}
