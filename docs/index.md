---
title: Home
description: "What AllSense is, and where to start."
template: home.html
hide:
  - navigation
  - toc
---

## Three steps, about five minutes { .ob-section-title }

From a phone in a drawer to live data on your robot.
{ .ob-section-sub }

<div class="ob-steps3" markdown>

<div markdown>
**Install the app**

On any Android 12+ phone. Old and cracked is fine.
</div>

<div markdown>
**Tap Start streaming**

Nothing leaves the phone until you do. It keeps going with the screen off.
</div>

<div markdown>
**Connect your robot**

Scan a code, paste a link, or plug in a cable.
</div>

</div>

## Pick how your robot connects { .ob-section-title }

Each one matches a guide in the app, with your phone's link already filled in.
{ .ob-section-sub }

<div class="grid cards ways" markdown>

- <span class="ob-icon">:material-monitor:</span><br>**[Browser](get-started/browser.md)**

    Any computer, nothing to install. Watch every sensor live.

- <span class="ob-icon">:material-code-braces:</span><br>**Programming**

    Read the IMU in a few lines of [Python](get-started/python.md), [C++](get-started/cpp.md) or [Rust](get-started/rust.md).

- <span class="ob-icon">:material-graph-outline:</span><br>**[ROS 2](get-started/ros2.md)**

    Standard topics: `Imu`, `NavSatFix`, camera and audio.

- <span class="ob-icon">:material-chip:</span><br>**[Microcontroller](get-started/board.md)**

    Arduino, ESP32, Pico. By USB cable, Bluetooth or Wi-Fi.

- <span class="ob-icon">:material-cloud-outline:</span><br>**[MQTT](get-started/mqtt.md)**

    Home Assistant, Node-RED, any broker.

</div>

## A taste { .ob-section-title }

Real code from the repository, tested on every change.
{ .ob-section-sub }

<div class="ob-taste" markdown>

=== "Python"

    ```python title="quickstart.py"
    --8<-- "examples/python/examples/quickstart.py"
    ```

=== "C++"

    ```cpp title="quickstart.cpp"
    --8<-- "examples/cpp/examples/quickstart.cpp"
    ```

=== "Rust"

    ```rust title="quickstart.rs"
    --8<-- "examples/rust/examples/quickstart.rs"
    ```

=== "Arduino"

    ```cpp title="USBMinimal.ino"
    --8<-- "examples/arduino/examples/USBMinimal/USBMinimal.ino"
    ```

=== "ROS 2"

    ```bash
    ros2 run allsense_ros2 bridge --ros-args -p url:="http://192.168.1.20:8765/?token=abcd"
    ros2 topic echo /allsense/phone/imu
    ```

</div>

## What people build { .ob-section-title }

<div class="ob-uses" markdown>

<div markdown>
<span class="ob-icon">:material-car-side:</span>
**A rover with no wheel encoders**

IMU and GPS as ROS 2 topics, already in the robot's own axes.
</div>

<div markdown>
<span class="ob-icon">:material-robot-outline:</span>
**An Arduino line-follower**

Tilt and compass over one USB cable. Nothing extra to wire.
</div>

<div markdown>
<span class="ob-icon">:material-emoticon-happy-outline:</span>
**A desk robot with a face**

The phone is the camera, the mic, the speaker and the face.
</div>

<div markdown>
<span class="ob-icon">:material-flask-outline:</span>
**A class experiment**

Accelerometer into Python and a CSV, in ten lines.
</div>

</div>

<div class="ob-ai" markdown>

![](images/logo.png){ .ob-otter }

<div markdown>
**Building with an AI assistant?**

Every page has a **Copy page** button. Or give it [`llms.txt`](llms.txt) (the index) or [`llms-full.txt`](llms-full.txt) (everything). Add `index.md` to any page's address for its Markdown.
</div>

</div>
