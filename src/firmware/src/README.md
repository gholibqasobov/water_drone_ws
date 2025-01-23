# ESP32 Firmware

This package contains the firmware for the ESP32 microcontroller used in the water drone project. The firmware is responsible for motor control via ROS 2 `/cmd_vel` commands using micro-ROS.

## Required Libraries

Before uploading the firmware, ensure you have installed the following libraries in the Arduino IDE:

1. **ESP32Servo**
   - Open the Arduino IDE.
   - Go to **Sketch > Include Library > Manage Libraries**.
   - Search for `ESP32Servo` and click **Install**.

2. **micro_ros_arduino**
   - Open the Arduino IDE.
   - Go to **Sketch > Include Library > Manage Libraries**.
   - Search for `micro_ros_arduino` and click **Install**.

## Flashing Instructions

1. Connect your ESP32 to your computer via USB.
2. Open the Arduino IDE and load `main.ino` from the `src/` directory.
3. Select your ESP32 board under **Tools > Board**.
4. Select the appropriate port under **Tools > Port**.
5. Click the **Upload** button to flash the firmware.
6. Open the Serial Monitor to debug.

## Notes
- Ensure the micro-ROS-Agent is running on your host machine. Use the following command:
  ```bash
  ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0
