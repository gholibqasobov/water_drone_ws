# Water Drone Workspace

This repository contains the ROS 2 workspace for a water drone, including firmware for the ESP32 and ROS 2 packages for navigation, control, and system bringup.

## Packages
1. **firmware**: Firmware for the ESP32 microcontroller, enabling motor control via micro-ROS.
2. **water_drone_navigation**: ROS 2 nodes for navigation and path planning.
3. **water_drone_control**: ROS 2 nodes for controlling the drone's movement and sensors.

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/gholibqasobov/water_drone_ws.git
   cd water_drone_ws

2. Build the workspace:
   ```bash
   colcon build --symlink-install

3. For firmware instructions, see the firmware README
