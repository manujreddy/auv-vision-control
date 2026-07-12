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
