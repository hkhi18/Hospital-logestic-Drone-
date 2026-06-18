#  Project:Hospital Logistics Drone (HLD) for KFSHRC

## 1. Project Overview

The **HLD-KFSHRC Initiative** is a specialized autonomous drone logistics platform designed to optimize the transport of time-sensitive medical assets—such as blood samples, pathology specimens, and critical medication—between hospital departments or research facilities. By implementing an automated aerial delivery network, the system aims to reduce transit times within the complex, minimize human error, and ensure sterile, direct transport.

## 2. Key Features

* **Precision Navigation:** GPS-guided mission execution customized to the specific campus layout of KFSHRC, ensuring takeoff and landing only at verified helipads.
* **Safety-First Redundancy:** A dedicated asynchronous safety monitor that scans for obstacles and initiates emergency hovering or altitude adjustments if the flight path is compromised.
* **Sterile/Secure Handling:** Designed to support a gimbal-stabilized payload delivery system, ensuring sensitive medical samples remain upright and stable during flight.
* **Operational Integration:** Seamlessly integrates with internal telemetry systems to provide real-time updates on location, battery status, and mission completion.

## 3. Core Technology & Environment

* **Flight Control:** PX4 Autopilot SITL (Software-In-The-Loop) providing industrial-grade flight dynamics.
* **Environment Simulation:** High-fidelity Gazebo 3D models representing KFSHRC campus infrastructure, including helipads, hospital wings, and ground-level logistics zones.
* **System Brain:** MAVSDK-Python, serving as the high-level logic controller for automated mission sequence management.
* **Protocol:** MAVLink messaging for secure communication between the drone and the hospital’s command center.

## 4. System Architecture

The architecture is divided into three critical layers to ensure maximum safety:

1. **Mission Management Layer:** Handles the `MissionPlan`, converting clinical delivery requests into coordinate-based flight paths.
2. **Safety & Oversight Layer:** A high-frequency monitoring service (`monitor_safety`) that runs parallel to the flight commands to handle obstacle avoidance.
3. **Data & Telemetry Layer:** Records mission logs for compliance and accountability, crucial for hospital documentation standards.

## 5. Project Structure

Hhospital-logistics-drone/
├── README.md           # Project documentation and setup guide
├── world/
│   └── finalproject1.sdf # The main hospital campus world file
├── models/
│   ├── hospital/       # Hospital building assets & meshes
│   ├── helipad/        # Helipad assets & configuration
│   └── fountain/       # Decorative site models
├── scripts/
│   └── mission.py      # Main Python script using MAVSDK
└── meshes/             # 3D GLB/DAE files for all structures
