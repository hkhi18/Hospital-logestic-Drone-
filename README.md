# 🚁 Hospital Logistics Drone (HLD) — KFSHRC Initiative

> **Autonomous aerial delivery system for intra-campus medical supply transport at King Faisal Specialist Hospital & Research Centre (KFSHRC)**

-----

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Gazebo World](#gazebo-world)
- [Flight Mission](#flight-mission)
- [Setup & Installation](#setup--installation)
- [Running the Simulation](#running-the-simulation)
- [Safety System](#safety-system)
- [Waypoint Coordinates](#waypoint-coordinates)

-----

## 📌 Project Overview

The **Hospital Logistics Drone (HLD)** is a specialized autonomous drone logistics platform designed for **King Faisal Specialist Hospital & Research Centre (KFSHRC)**. It automates the transport of time-sensitive medical assets — blood samples, pathology specimens, medications, and lab supplies — between hospital buildings using aerial delivery, eliminating ground-level delays and human error.

The system is simulated in **Gazebo** using a custom-built 3D hospital campus world, controlled via **MAVSDK Python** over **MAVLink**, and powered by the **PX4 Autopilot SITL** flight stack.

-----

## ✨ Key Features

|Feature                        |Description                                                                         |
|-------------------------------|------------------------------------------------------------------------------------|
|🎯 **GPS Waypoint Navigation**  |Pre-programmed multi-stop mission plan across the KFSHRC campus                     |
|🛡️ **Async Safety Monitor**     |Continuous background task detects obstacles within 5.0 m and triggers evasive climb|
|📷 **Camera Logging**           |Photo capture at every delivery waypoint for mission accountability                 |
|🏥 **Medical-Grade Reliability**|Health checks before arming; fail-safe logic on GPS or connection loss              |
|🌍 **Realistic Simulation**     |Custom Gazebo world with hospital buildings, helipads, and GPS-aligned coordinates  |
|🔓 **Open Source Stack**        |PX4 + MAVSDK + Gazebo — no proprietary hardware required                            |

-----

## 🏗️ System Architecture

The system is divided into **three operational layers**:

```
┌──────────────────────────────────────────────────┐
│           MISSION MANAGEMENT LAYER                │
│  MissionPlan → MissionItems → GPS Waypoints       │
│  Upload → Arm → Start → Track Progress            │
└────────────────────┬─────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────┐
│           SAFETY & OVERSIGHT LAYER                │
│  monitor_safety() — asyncio background task       │
│  distance_sensor() — obstacle proximity check     │
│  Auto-climb if distance < 5.0 m                   │
└────────────────────┬─────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────┐
│           DATA & TELEMETRY LAYER                  │
│  camera_sensor() — photo at each waypoint         │
│  GPS coordinates logged per delivery stop         │
│  Mission progress tracking (current / total)      │
└──────────────────────────────────────────────────┘
```

-----

## 🛠️ Technology Stack

|Component                 |Technology                                 |
|--------------------------|-------------------------------------------|
|**Flight Controller**     |PX4 Autopilot (SITL — Software In The Loop)|
|**High-Level SDK**        |MAVSDK-Python                              |
|**Communication Protocol**|MAVLink (UDP `0.0.0.0:14540`)              |
|**Simulation Environment**|Gazebo (custom `.world` SDF file)          |
|**Programming Language**  |Python 3 (`asyncio`)                       |
|**Physics Engine**        |ODE — 250 Hz update rate                   |
|**GPS Reference Frame**   |ENU / WGS84                                |

-----

## 📁 Project Structure

```
hospital-logistics-drone/
│
├── 📄 README.md                    # Project documentation (this file)
│
├── 🌍 world/
│   └── finalproject1.sdf           # Custom Gazebo hospital campus world
│
├── 🏗️ models/
│   ├── hospital/                   # Hospital building model assets & meshes
│   │   ├── model.config
│   │   └── model.sdf
│   ├── helipad/                    # Helipad model assets & configuration
│   │   ├── model.config
│   │   └── model.sdf
│   └── fountain/                   # Decorative courtyard fountain model
│       ├── model.config
│       └── model.sdf
│
├── 🐍 scripts/
│   └── mission.py                  # Main flight script (MAVSDK + asyncio)
│
└── 🎨 meshes/
    ├── hospital.glb                # 3D mesh — hospital building
    ├── helipad.dae                 # 3D mesh — helipad
    └── fountain.dae                # 3D mesh — fountain
```

-----

## 🌍 Gazebo World

The simulation world (`finalproject1.sdf`) represents a realistic hospital campus with **5 models** placed using real GPS-aligned coordinates:

|#|Model        |Pose (X, Y, Z)      |Role                               |
|-|-------------|--------------------|-----------------------------------|
|1|🏥 `hospital` |(5.72, −2.44, 0.07) |Main building — delivery **source**|
|2|🏥 `hospital2`|(−6.01, 2.39, −0.05)|Second wing — delivery **target**  |
|3|🟢 `helipad1` |(−8.73, −1.78, 0.21)|**Takeoff** pad                    |
|4|🟢 `helipad2` |(6.07, 1.60, 0.22)  |**Landing** destination            |
|5|⛲ `fountain` |(0.02, −2.40, 0.55) |Central courtyard landmark         |

**World Properties:**

- Ground plane: `100 × 100 m`, gray (`diffuse 0.3 0.3 0.3`)
- Physics: ODE, `max_step_size: 0.004`, `real_time_update_rate: 250`
- GPS Home: `lat 47.397971°`, `lon 8.546163°`, WGS84 ENU

-----

## ✈️ Flight Mission

The drone executes an autonomous 4-waypoint mission from Helipad 1 to Helipad 2:

```
Helipad 1 (Takeoff)
    │
    ▼  Waypoint 1 — (47.397959, 8.546419)
    │
    ▼  Waypoint 2 — (47.397980, 8.546111)
    │
    ▼  Waypoint 3 — (47.397983, 8.546201)
    │
    ▼  Waypoint 4 — (47.397984, 8.546246)  ← LAND on Helipad 2
```

- **Cruise altitude:** 10 m
- **Cruise speed:** 10 m/s
- **Final approach speed:** 5 m/s
- **Camera action:** `TAKE_PHOTO` at final waypoint
- **Vehicle action:** `LAND` at final waypoint

-----

## ⚙️ Setup & Installation

### Prerequisites

```bash
# 1. PX4 Autopilot (SITL)
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
cd PX4-Autopilot
bash ./Tools/setup/ubuntu.sh

# 2. Gazebo (Harmonic or Garden)
sudo apt install gazebo

# 3. MAVSDK Python
pip install mavsdk

# 4. Clone this project
git clone https://github.com/your-username/hospital-logistics-drone.git
cd hospital-logistics-drone
```

### Install Python Dependencies

```bash
pip install mavsdk asyncio
```

-----

## 🚀 Running the Simulation

### Step 1 — Launch PX4 SITL with Gazebo

```bash
cd PX4-Autopilot
make px4_sitl gz_x500
```

### Step 2 — Load the Custom World

```bash
gz sim world/finalproject1.sdf
```

### Step 3 — Run the Mission Script

```bash
cd scripts
python3 mission.py
```

**Expected terminal output:**

```
-- Connecting...
-- Connected! ✅
-- Waiting for GPS...
-- GPS Ready! ✅
-- Uploading mission...
-- Arming...
🛡️ Safety Monitor Started...
-- Starting mission...
📍 Waypoint 1/4
📍 Waypoint 2/4
📷 Camera Sensor → Taking photo at Waypoint 3
📍 Waypoint 3/4
📍 Waypoint 4/4
✅ Mission Complete!
🛬 Landed on helipad2!
```

-----

## 🛡️ Safety System

The safety monitor runs as a **concurrent asyncio task** alongside the main mission:

```python
async def monitor_safety(drone):
    while True:
        distance = await distance_sensor(drone)
        if distance < 5.0:
            print("🚨 WARNING: Building too close! Climbing up...")
            # Evasive climb triggered
        await asyncio.sleep(2)
```

|Trigger                   |Action                                |
|--------------------------|--------------------------------------|
|Obstacle within **5.0 m** |Log warning + initiate evasive climb  |
|GPS health check **fails**|Halt mission before arming            |
|Connection **lost**       |Async state monitor triggers fail-safe|

-----

## 📍 Waypoint Coordinates

All GPS coordinates are aligned to the **KFSHRC campus** via the world’s spherical coordinate origin:

```python
waypoints = [
    (47.397955, 8.546048),  # Takeoff position
    (47.397959, 8.546419),  # Waypoint 1 — Helipad 1 area
    (47.397980, 8.546111),  # Waypoint 2 — Mid-campus
    (47.397983, 8.546201),  # Waypoint 3 — Hospital 2 approach
    (47.397984, 8.546246),  # Waypoint 4 — Helipad 2 (LAND)
]
```

-----

## 📄 License

This project was developed as part of the **Tuwaiq Academy** robotics & drone engineering program.

-----

*Built with PX4 · MAVSDK · Gazebo · Python*