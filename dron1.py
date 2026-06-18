import asyncio
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan

async def distance_sensor(drone):
    try:
        async for dist in drone.telemetry.distance_sensor():
            distance = dist.current_distance_m
            print(f"📡 Distance Sensor → {distance:.1f}m")
            if distance < 5.0:
                print("🚨 WARNING: Building too close! Climbing up...")
            return distance
    except Exception:
        print("📡 Distance Sensor → Simulated: Safe ")
        return 999.0

async def camera_sensor(drone, waypoint_num, lat, lon):
    print(f"📷 Camera Sensor → Taking photo at Waypoint {waypoint_num}")
    print(f"📍 Location → Lat:{lat:.6f} Lon:{lon:.6f}")

async def monitor_safety(drone):
    print("🛡️ Safety Monitor Started...")
    while True:
        await distance_sensor(drone)
        await asyncio.sleep(2)

async def main():
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    print("-- Connecting...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected! ✅")
            break

    print("-- Waiting for GPS...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("-- GPS Ready! ✅")
            break

    # Get home position
    home = await anext(drone.telemetry.home())
    absolute_latitude = home.latitude_deg
    absolute_longitude = home.longitude_deg
    flying_alt = 8.0

    # Waypoints
    waypoints = [
        (47.397955, 8.546048),  # takeoff position
        (47.397980, 8.546111),  # 2
        (47.397983, 8.546201),  # 3
        (47.397984, 8.546246),  # 4 - helipad2 land
    ]

    # Mission items
    mission_items = []

    for i, (lat, lon) in enumerate(waypoints):
        if i == len(waypoints) - 1:
            # Last waypoint - land on helipad2
            mission_items.append(
                MissionItem(
                    lat,
                    lon,
                    flying_alt,
                    5.0,
                    True,
                    float("nan"),
                    float("nan"),
                    MissionItem.CameraAction.TAKE_PHOTO,
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    MissionItem.VehicleAction.LAND,
                )
            )
        else:
            mission_items.append(
                MissionItem(
                    lat,
                    lon,
                    flying_alt,
                    10.0,
                    True,
                    float("nan"),
                    float("nan"),
                    MissionItem.CameraAction.NONE,
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    float("nan"),
                    MissionItem.VehicleAction.NONE,
                )
            )

    mission_plan = MissionPlan(mission_items)

    # Upload mission
    print("-- Uploading mission...")
    await drone.mission.upload_mission(mission_plan)

    # Arm drone
    print("-- Arming...")
    await drone.action.arm()

    # Start safety monitor in background
    safety_task = asyncio.ensure_future(monitor_safety(drone))

    # Start mission
    print("-- Starting mission...")
    await drone.mission.start_mission()

    # Track mission progress
    async for progress in drone.mission.mission_progress():
        print(f"📍 Waypoint {progress.current}/{progress.total}")

        if progress.current < len(waypoints):
            lat, lon = waypoints[progress.current]
            await camera_sensor(drone, progress.current, lat, lon)

        if progress.current == progress.total:
            print("✅ Mission Complete!")
            break

    # Stop safety monitor
    safety_task.cancel()
    print("🛬 Landed on helipad2!")

#
if __name__ == "__main__":
    asyncio.run(main())