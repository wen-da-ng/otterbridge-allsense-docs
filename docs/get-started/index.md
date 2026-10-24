---
description: "Install the app, start streaming, then pick how your robot connects."
---

# Get started

Three steps: install the app, tap **Start streaming**, connect something.
{ .lead }

<div class="steps" markdown>

1. **Install the app.** It isn't in a store yet: download the APK from the [latest release](https://github.com/wen-da-ng/otterbridge-allsense/releases/latest) and open it on the phone (Android asks you to allow installs from your browser or files app once). Any phone with Android 12 or newer.

2. **Start streaming.** On **Home**, tap **Start streaming**. Nothing leaves the phone until you do, and it keeps going with the screen off. **Stop** ends it.

3. **Connect something.** Pick the way that fits your robot. Each matches a guide in the app (**Home → Connect**) that fills in your phone's link.

</div>

<div class="grid cards ways" markdown>

- <span class="ob-icon">:material-monitor:</span><br>**[Browser](browser.md)**

    Any computer, nothing to install. Live values, cameras, sound.

- <span class="ob-icon">:material-code-braces:</span><br>**Programming**

    A few lines in [Python](python.md), [C++](cpp.md) or [Rust](rust.md).

- <span class="ob-icon">:material-graph-outline:</span><br>**[ROS 2](ros2.md)**

    Standard ROS topics: IMU, GPS, camera, audio.

- <span class="ob-icon">:material-chip:</span><br>**[Microcontroller](board.md)**

    Arduino, ESP32, Pico. By USB cable, Bluetooth or Wi-Fi.

- <span class="ob-icon">:material-cloud-outline:</span><br>**[MQTT](mqtt.md)**

    Home Assistant, Node-RED, any broker.

</div>

## Which one?

| You have | Use |
|---|---|
| A laptop and want to look | [Browser](browser.md) |
| Code in Python, C++ or Rust | [Python](python.md), [C++](cpp.md), [Rust](rust.md) |
| A ROS 2 robot | [ROS 2](ros2.md) |
| A microcontroller and no Wi-Fi | [Microcontroller](board.md), by USB cable |
| Home automation or a cloud dashboard | [MQTT](mqtt.md) |

You can use several at once: every link shares the same sensors, and each sensor runs only while something reads it.
