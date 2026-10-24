---
description: "Use the phone's cameras and microphones from your robot: photos, MJPEG or H.264 video, and live audio over HTTP."
---

# Cameras and microphones

Every lens and mic on the phone, on your robot's computer.
{ .lead }

<div class="ob-meta" markdown><span>:material-timer-outline: 5 minutes</span><span>:material-toolbox-outline: Streaming on, same Wi-Fi</span></div>

!!! robot "For example"
    A telepresence robot: the back camera as H.264 at 1 Mbit/s for the driver, and the microphone's loudness to react when someone calls it.

## The shortest way

<div class="steps" markdown>

1. On the phone: **Home → Start streaming**. Allow camera and microphone access when the app asks (or in **Sensors → Cameras** and **Sensors → Microphones**).

2. Take a photo and listen for a second:

    ```python title="camera_and_mic.py"
    --8<-- "examples/python/examples/camera_and_mic.py"
    ```

3. Or just watch: open the phone's link in a browser; the dashboard shows every camera and plays the mic.

</div>

## Details

**Names.** `phone.cameras()` and `phone.microphones()` list them, named by lens (`back_22mm`, `front_25mm`, `mic_bottom`…). Rename them in the app.

**Video.** `phone.camera("back_22mm", fps=10)` gives JPEG frames; `codec="h264"` uses the phone's hardware encoder at about a fifth of the bandwidth. Any player works too: `ffplay -f h264 "<url>"`, VLC or OpenCV's `VideoCapture` with the URL from `camera_url` (C++ and Rust: `phone.camera_url(...)`).

**Lenses through zoom.** Telephoto and ultra-wide lenses often hide behind the main camera: `zoom=0.6` or `zoom=3` switches to them.

**Loudness only?** Each microphone also has a `<name>_level` stream (rms and peak in dBFS, up to 50 Hz) that works on every link, boards included.

**One app at a time.** The camera runs only while someone watches, and Android shows its indicator. Which cameras can run together depends on the phone.

## Reference

| What | Where |
|---|---|
| URLs, options, H.264 details, errors | [Protocol → Camera](../PROTOCOL.md#camera), [Microphone](../PROTOCOL.md#microphone) |
| Camera settings (exposure, focus) | the `camera` command in [Protocol → Commands](../PROTOCOL.md#commands) |
| ROS 2 | `cameras:=`, `camera_codec:=h264`, `microphones:=` in the [bridge's README](https://github.com/wen-da-ng/otterbridge-allsense-ros2) |
