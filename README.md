# Labyrinth — Maze Solving Robot

> ROS2 robot that navigates mazes autonomously using ultrasonic sensors and detects colored markers via camera.

---

## Overview

Labyrinth is a ROS2-based differential drive robot designed to solve mazes. It combines reactive navigation with computer vision — finding its way through walls using distance sensors and counting colored markers along the path.

### What it does
- Navigates autonomously through a maze using a state machine driven by 3 range sensors
- Detects and counts **red**, **green**, and **blue** markers via an onboard camera
- Simulated in **Gazebo** with full ROS2 integration

---

## Architecture

```
                    ┌─────────────────────┐
                    │    Gazebo Sim        │
                    │  (maze world + robot)│
                    └────────┬────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     /sensor_range/*   /frente_camera/...   │
              │              │              │
    ┌─────────▼──────┐  ┌───▼────────────┐ │
    │ NavigationNode │  │ PerceptionNode │ │
    │                │  │                │ │
    │ State Machine: │  │ HSV masking:   │ │
    │  FORWARD       │  │  red mask      │ │
    │  TURN_RIGHT    │  │  green mask    │ │
    │  TURN_LEFT     │  │  blue mask     │ │
    │  REAR          │  │                │ │
    └────────┬───────┘  └───┬────────────┘ │
             │              │              │
    /motor{1,2}/commands   /colour_counts/*│
             │              │              │
    ┌─────────▼──────┐  ┌───▼────────────┐ │
    │  Wheel Motors  │  │  Color Counts  │ │
    └────────────────┘  └────────────────┘ │
```

---

## Package Structure

```
Labyrinth-Hackathon/
├── src/
│   ├── maze_bringup/          # Launch files, world, config
│   │   ├── config/
│   │   │   └── params.yaml
│   │   ├── launch/
│   │   │   └── maze.launch.py
│   │   ├── worlds/            # Gazebo SDF worlds
│   │   └── models/            # Robot URDF/SDF
│   └── maze_robot/            # Core robot nodes
│       ├── include/maze_robot/
│       │   ├── navigation_node.hpp
│       │   └── perception_node.hpp
│       ├── src/
│       │   ├── navigation_node.cpp
│       │   └── perception_node.cpp
│       └── launch/
│           └── maze.launch.py
```

---

## Nodes

### `navigation_node`

Reactive navigation using 3 ultrasonic range sensors.

| State | Condition | Behavior |
|---|---|---|
| `FORWARD` | front > 0.5m | Both motors forward |
| `TURNING_RIGHT` | front blocked, right > left | Pivot right |
| `TURNING_LEFT` | front blocked, left > right | Pivot left |
| `REAR` | front < 0.1m | Both motors reverse |

**Subscribed topics:**
- `/sensor_range/front` — `sensor_msgs/Range`
- `/sensor_range/right` — `sensor_msgs/Range`
- `/sensor_range/left` — `sensor_msgs/Range`

**Published topics:**
- `/motor1/commands` — `std_msgs/Float64MultiArray`
- `/motor2/commands` — `std_msgs/Float64MultiArray`

---

### `perception_node`

Color detection via camera using HSV masking with OpenCV.

| Color | HSV Range |
|---|---|
| Red | [0–10] ∪ [170–180] |
| Green | [35–85] |
| Blue | [100–140] |

Increments a counter every frame a color has more than 500 active pixels.

**Subscribed topics:**
- `/frente_camera/frente_camera_sensor/image_raw` — `sensor_msgs/Image`

**Published topics:**
- `/colour_counts/red` — `std_msgs/Int32`
- `/colour_counts/green` — `std_msgs/Int32`
- `/colour_counts/blue` — `std_msgs/Int32`

---

## 🚀 Getting Started

### Prerequisites

- Ubuntu 24.04
- ROS2 Jazzy
- Gazebo (Harmonic)

```bash
sudo apt install ros-jazzy-cv-bridge ros-jazzy-vision-opencv ros-jazzy-ros-gz
```

### Build

```bash
git clone https://github.com/BlvckJoao/Labyrinth-Hackathon.git
cd Labyrinth-Hackathon
source /opt/ros/jazzy/setup.bash
colcon build
source install/setup.bash
```

### Run

```bash
ros2 launch maze_bringup maze.launch.py
```

---

##  Tech Stack

- **ROS2 Jazzy**
- **Gazebo Harmonic**
- **OpenCV 4** — HSV color segmentation
- **cv_bridge** — ROS ↔ OpenCV image conversion
- **C++17**

---