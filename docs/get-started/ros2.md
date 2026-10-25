---
description: "Publish the phone's IMU, GPS, cameras and microphones as standard ROS 2 topics."
---

# ROS 2

Standard ROS 2 topics from the phone: IMU, GPS, camera, audio.
{ .lead }

<div class="ob-meta" markdown><span>:material-timer-outline: 10 minutes</span><span>:material-toolbox-outline: ROS 2 Humble or newer on the robot</span></div>

!!! robot "For example"
    A rover with no wheel encoders gets an IMU and GPS for `robot_localization`, and a camera for driving it remotely, without wiring any of them.

The phone doesn't run ROS: a bridge node on the robot's computer turns its streams into standard messages.

## The shortest way

<div class="steps" markdown>

1. On the robot's computer, install the bridge:

    ```bash
    pip install "allsense @ git+https://github.com/wen-da-ng/otterbridge-allsense-python"
    cd ~/ros2_ws/src && git clone https://github.com/wen-da-ng/otterbridge-allsense-ros2 allsense_ros2
    cd ~/ros2_ws && colcon build --packages-select allsense_ros2 && source install/setup.bash
    ```

2. On the phone: **Home → Start streaming**, then copy the link from **Connect → ROS 2**.

3. Run the bridge with the link's address, and its token (after `?token=`) in `ALLSENSE_TOKEN`, then see the topics:

    ```bash
    export ALLSENSE_TOKEN=abcd
    ros2 run allsense_ros2 bridge --ros-args -p url:="http://192.168.1.20:8765/"
    ros2 topic list | grep allsense
    ```

</div>

## Details

**Why the token goes in an environment variable:** ROS parameters can be read by anything on the same ROS network (`ros2 param get`). A token passed in `url` still works, but the bridge removes it from the parameter and warns. To keep it in a file instead: `token_file:=~/.allsense_token` (make the file readable only by you).

**Topics** follow the app's names: `/allsense/<device>/sensors/<name>`. `/allsense/<device>/imu` combines accelerometer, gyroscope and orientation in one `sensor_msgs/Imu`, the form `robot_localization` wants.

**Robot axes.** Set how the phone sits on the robot in the app (**Robot → Mount**). The bridge then publishes `/allsense/<device>/robot/…` already in the robot's axes, in `base_link`. No transform needed.

**Cameras and microphones** are opt-in: `-p cameras:="['back']"`, `-p microphones:="['mic']"`. Add `-p camera_codec:=h264` for about a tenth of the bandwidth (needs `foxglove_msgs`).

**In WSL**, use Cyclone DDS: Fast DDS discovers nodes there but delivers nothing.

All parameters, frames and fallbacks: the [bridge's README](https://github.com/wen-da-ng/otterbridge-allsense-ros2).

## Reference

| Phone stream | ROS message |
|---|---|
| accelerometer, gyroscope, rotation vector | `sensor_msgs/Imu` (only the fields it has) |
| magnetic field | `sensor_msgs/MagneticField` (T) |
| pressure, light, proximity | `FluidPressure` (Pa), `Illuminance` (lx), `Range` (m) |
| GNSS position | `sensor_msgs/NavSatFix` |
| battery | `sensor_msgs/BatteryState` |
| camera | `sensor_msgs/CompressedImage`, or `foxglove_msgs/CompressedVideo` (H.264) |
| microphone | `audio_common_msgs/AudioData` (+ stamped, info) |
| anything else | `std_msgs/Float64MultiArray` |

| Parameter | Default |
|---|---|
| `url` | (required) the link from the app |
| `streams` | Basic streams that have a ROS message |
| `rate_hz` | 50 |
| `robot_frame_id` | `base_link` |
| `imu_orientation` | `game` (no compass) or `absolute` |
