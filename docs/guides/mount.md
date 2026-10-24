---
description: "Tell the app how the phone sits on the robot, and get the IMU, tilt and heading in the robot's own axes."
---

# Mount on the robot

Get motion data in the robot's axes, not the phone's.
{ .lead }

<div class="ob-meta" markdown><span>:material-timer-outline: 2 minutes</span><span>:material-toolbox-outline: The phone fixed to the robot</span></div>

!!! robot "For example"
    The phone stands upright on a rover, camera forward. Without a mount, "forward" is the phone's −z axis; with it, the accelerometer, gyroscope and heading come out as the robot sees them: x forward, y left, z up.

## The shortest way

<div class="steps" markdown>

1. Fix the phone to the robot.

2. On the phone: **Robot → Mount on the robot → Set**, and pick how it sits, e.g. **Upright (portrait), back camera to the front**. Not in the list? **Any mount** lets you pick which phone axis points forward and which up.

3. Check it on the card: on level ground roll and pitch are near 0; lift the nose and pitch goes negative; turn left and the heading goes down.

4. Read the robot's attitude in your code:

    ```python title="robot_attitude.py"
    --8<-- "examples/python/examples/robot_attitude.py"
    ```

</div>

## Details

**What you get.** With a mount set, these streams appear in the `robot` category, next to the phone's own: `accelerometer`, `gyroscope`, `magnetic_field`, `gravity`, `linear_acceleration`, `rotation_vector`, `game_rotation_vector`, and `attitude` (roll, pitch, yaw, heading in degrees).

**Names.** A plain name is still the phone's stream. Ask for the robot's with the category in front: `robot.accelerometer`, `robot.attitude`. That works in every client and on boards.

**ROS 2.** The bridge publishes them as `/allsense/<device>/robot/…` in frame `base_link`, and its combined `/allsense/<device>/imu` uses them. No static transform needed.

**Heading** needs a compass-based rotation vector; without one it's empty (`None` in Python, NaN in C++ and Rust).

## Reference

| What | Where |
|---|---|
| Axes, fields, signs | [Protocol → Robot frame](../PROTOCOL.md#robot-frame-robot-category) |
| ROS 2 | `robot_frame_id` parameter (default `base_link`) in the [bridge's README](https://github.com/wen-da-ng/otterbridge-allsense-ros2) |
