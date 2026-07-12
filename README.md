# Autonomous Underwater Vehicle (AUV) - Vision & Control System

A personal engineering project focusing on the software architecture for an autonomous underwater vehicle. This project integrates AI-driven defect detection, ROS2-based PID control, and a real-time digital twin visualization.

## 🚀 Core Features

* **ROS2 Navigation & Control:** Custom Proportional-Integral-Derivative (PID) controller written in Python (`rclpy`) that dynamically calculates motor thrust to reach and maintain target depth.
* **AI-Based Defect Detection:** Lightweight YOLOv8 Nano model trained to achieve real-time inference for crack and corrosion detection using OpenCV.
* **Real-Time Digital Twin:** RViz2 integration acts as a live digital twin, using a custom physics bridge to translate motor thrust into simulated Z-axis depth.
* **Edge-AI Event-Driven Recording:** Saves energy and storage by actively monitoring the video feed and only logging frames to an `Anomalies` directory when a defect is detected with >70% confidence.

## 📁 Repository Structure

```text
├── ai_vision/
│   ├── vision_node.py       # YOLOv8 inference and event-driven logging
│   ├── best.pt              # Custom trained YOLOv8 Nano weights
│   └── Anomalies/           # Auto-generated folder containing logged defects
└── sub_control/             # Custom ROS2 Python package
    ├── pid_node.py          # ROS2 PID Depth Controller
    └── sim_bridge.py        # RViz2 Digital Twin Physics Bridge

⚙️ Complete Installation & Setup

Prerequisites: You must have Python 3 and a working installation of ROS2 installed on your Ubuntu machine.

Step 1: Download the Repository

Open your terminal and download this project to your home directory:
Bash

cd ~
git clone [https://github.com/YOUR_USERNAME/auv-vision-control.git](https://github.com/YOUR_USERNAME/auv-vision-control.git)

(Note: Replace YOUR_USERNAME in the link above with your actual GitHub username).

Step 2: Setup the AI Vision Environment

Install the required computer vision libraries. We restrict NumPy to version 1.x to prevent compatibility crashes with the YOLO library:
Bash

pip install "numpy<2" ultralytics opencv-python

Step 3: Build the ROS2 Workspace

Because sub_control is a custom ROS2 package, it cannot be run directly. It must be copied into a ROS2 workspace and compiled. Run these exact commands to build the workspace:
Bash

# 1. Create the workspace folders
mkdir -p ~/auv_ws/src

# 2. Copy the package from the downloaded repo into the workspace
cp -r ~/auv-vision-control/sub_control ~/auv_ws/src/

# 3. Navigate to the workspace and compile it
cd ~/auv_ws
colcon build

🛠️ How to Run the Full System

To see the Software-in-the-Loop system working, you will need to open 4 separate terminal windows.
Terminal 1: Run the AI Vision Node

This will open your camera/video feed and begin actively scanning for pipe defects.
Bash

cd ~/auv-vision-control/ai_vision
python3 vision_node.py

Terminal 2: Launch the Control Nodes

This boots up the PID "brain" and the physics bridge.
Bash

# Source the workspace
source ~/auv_ws/install/setup.bash

# Run the PID controller
ros2 run sub_control pid_node

(Open a new tab in this terminal, run source ~/auv_ws/install/setup.bash again, and run ros2 run sub_control sim_bridge)
Terminal 3: Launch the Digital Twin

This opens the 3D visualizer to watch the submarine move.
Bash

rviz2

Inside RViz2:

    Look at the left panel under Displays. Change the Fixed Frame from map to world.

    Click the Add button at the bottom left.

    Select the By topic tab.

    Find /auv_marker, click the Marker underneath it, and click OK. You will see the blue 3D model appear.

Terminal 4: Issue a Depth Command

Act as the mission planner and send a target depth (e.g., 5.0 meters) to the PID controller:
Bash

source ~/auv_ws/install/setup.bash
ros2 topic pub -1 /target_depth std_msgs/msg/Float32 "{data: 5.0}"

The Result: Watch Terminal 2 and the RViz2 window. You will see the PID controller dynamically adjust the motor thrust to smoothly move the 3D model down the grid and ease to a perfect stop at the target depth!
👤 Author

Manoj Reddy
