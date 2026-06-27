# Multi-Modal Autonomous Service Robot using LLM, RAG, and ROS2 🤖

**Undergraduate Thesis Project**
**Softwarica College of IT & E-Commerce / Coventry University**

---

# Overview

This project presents a multi-modal autonomous service robot capable of answering user queries, retrieving institutional information using Retrieval-Augmented Generation (RAG), generating responses with a Large Language Model (LLM), speaking in Nepali, and performing context-aware gestures in a ROS2 and Gazebo simulation.

The project separates AI processing from robot control by running the LLM pipeline in Google Colab while ROS2 manages robot communication and motion locally.

---

# Features

* Nepali Speech-to-Text using Whisper
* Retrieval-Augmented Generation (RAG)
* LLM-based conversational responses
* Tool Calling
* Context-aware gesture selection
* Nepali Text-to-Speech
* Physics-based humanoid gestures
* ROS2 and Gazebo integration
* Cloud communication between Google Colab and ROS2

---

# Repository Structure

```
.
├── README.md
├── notebooks/
│   └── llm_robot_pipeline.ipynb
├── llm_robot_bridge/
│   ├── launch/
│   ├── urdf/
│   ├── config/
│   ├── gesture_manager_node.py
│   └── gesture_*.py
└── ...
```

---

# Branches

## simulation

Simulation environment using ROS2 and Gazebo.

## physical

Code adapted for deployment on the physical robot.

---

# Models Used

| Purpose              | Model                                       |
| -------------------- | ------------------------------------------- |
| Speech-to-Text       | Whisper Medium                              |
| Large Language Model | Meta-Llama-3.1-8B-Instruct (4-bit, Unsloth) |
| Translation          | SeamlessM4T v2 Medium                       |
| Embedding Model      | all-MiniLM-L6-v2                            |
| Text-to-Speech       | Piper (ne_NP-google-medium)                 |
| Vector Database      | ChromaDB                                    |

---

# Technologies Used

* ROS2 Humble
* Gazebo (ros_gz_sim)
* ros_gz_bridge
* rosbridge_server
* roslibpy
* Cloudflare Tunnel
* Transformers
* Unsloth
* ChromaDB
* Whisper
* Piper TTS

---

# System Pipeline

```
User Input
      │
      ▼
Speech-to-Text (Whisper) / Text Input
      │
      ▼
Translation (if required)
      │
      ▼
RAG (ChromaDB + all-MiniLM-L6-v2)
      │
      ▼
Meta Llama 3.1
      │
      ├── Tool Calling
      ├── State Selection
      └── Gesture Selection
      │
      ▼
Response Generation
      │
      ▼
Translation to Nepali
      │
      ▼
Piper Text-to-Speech
      │
      ▼
ROSBridge
      │
      ▼
ROS2
      │
      ▼
Gesture Manager
      │
      ▼
Gesture Scripts
      │
      ▼
Gazebo Robot
```

---

# Running the Simulation

## 1. Build the workspace

```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

---

## 2. Launch Gazebo

```bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="-r empty.sdf"
```

---

## 3. Generate the robot URDF

```bash
xacro ~/ros2_ws/src/llm_robot_bridge/urdf/robot.urdf.xacro > /tmp/test_robot.urdf
```

---

## 4. Spawn the robot

```bash
ros2 run ros_gz_sim create \
-world empty \
-file /tmp/test_robot.urdf \
-name dual_arm_service_bot \
-z 0.25
```

---

## 5. Launch the ROS2 nodes

```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash

ros2 launch llm_robot_bridge robot_teleop.launch.py target_domain:=*
```

This launches:

* ROS-Gazebo Bridge
* Gesture Manager Node
* ROSBridge WebSocket Server

---

## 6. Start the Cloudflare Tunnel

```bash
cloudflared tunnel --url http://localhost:9090
```

Copy the generated HTTPS URL and update it in the Google Colab notebook.

---

## 7. Run the Google Colab Notebook

Open the notebook located in:

```
notebooks/llm_robot_pipeline.ipynb
```

Run all cells sequentially.

The notebook:

* Loads the LLM
* Connects to ROS2
* Retrieves relevant context using RAG
* Generates responses
* Performs tool calling
* Converts responses to Nepali
* Synthesizes speech
* Sends gesture commands to ROS2

The robot is now ready to receive user input.

---

# Physical Robot

The `physical` branch contains the code used for deploying the pipeline on the physical robot. Instead of controlling a simulated robot in Gazebo, the generated commands are converted into motor control instructions and executed on the robot hardware.

---

# Future Improvements

* Nepali voice input integrated into the final pipeline
* Speech and gesture synchronization
* Continuous talking gestures during speech
* Concurrent speech, gesture, and navigation
* Deployment and evaluation on the physical robot

---

# Author

**Apala**
Undergraduate Thesis Project
Softwarica College of IT & E-Commerce / Coventry University
