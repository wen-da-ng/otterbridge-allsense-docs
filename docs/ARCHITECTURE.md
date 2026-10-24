---
title: How it works
description: "How AllSense turns a phone into a sensor hub, the ideas behind it, and where it's going."
hide:
  - navigation
---

# How it works

One engine owns the hardware. Every link reads from it, at its own rate, and only what you share.
{ .lead }

<figure class="ob-diagram" markdown="0">
--8<-- "docs/diagrams/overview.svg"
<figcaption>The whole system. Each piece of hardware is opened once, by the engine. Each link (a browser, a board, a broker, the recorder) asks the engine for the streams it needs. <b>Sharing</b> decides, per link, which streams may leave the phone. Each link then speaks its own protocol to its clients.</figcaption>
</figure>

## Five ideas

<div class="grid cards" markdown>

-   :material-source-branch: **One source, many readers**

    A camera can only be opened once. So the engine opens it, and the dashboard, Python and ROS all watch the same capture.

-   :material-power-sleep: **Only run what's read**

    A sensor runs only while something reads it. Close the last reader and it stops, saving battery and heat.

-   :material-tag-text-outline: **Your names**

    Call the left magnetometer `mag_left`. Every client uses that name, and it survives reboots and app updates.

-   :material-shield-lock-outline: **Private by default**

    Nothing leaves the phone until you tap **Start streaming**, and only the streams you share.

-   :material-puzzle-outline: **Any link**

    Each link is a module behind the same small interface. Adding one doesn't touch the others.

</div>

## One sensor, several readers

Suppose a Python script wants the accelerometer at 100 Hz, a board over USB wants 50 Hz, and the Sensors screen is open.

<figure class="ob-diagram" markdown="0">
--8<-- "docs/diagrams/readers.svg"
<figcaption>The sensor runs once, at twice the fastest rate anyone asked for (Android treats rates as hints, so the margin keeps them honest). Each reader has its own Decimator that hands it samples on a schedule. When the last reader leaves, the sensor stops.</figcaption>
</figure>

The same holds for cameras and microphones: one capture, opened by the first viewer and closed after the last.

## Names that stay put

Android lists sensors in an order that can change. So each source gets a **stable ID** built from what it is, and you give it a **name**.

<figure class="ob-diagram" markdown="0">
--8<-- "docs/diagrams/names.svg"
<figcaption>The stable ID never changes and is never shown in Basic mode. Your name is what clients use. Each link writes the full name its own way; boards just number the streams they ask for.</figcaption>
</figure>

The full name is `allsense.<device>.<category>.<name>`. The device name matters once a robot carries two phones. Names use `a-z`, `0-9` and `_`, and are unique per phone.

## Exact time

A robot needs to know when a sample was *measured*, not when it arrived. Every sample carries the sensor's hardware timestamp, on the phone's boot clock. Clients line that up with their own clock:

<figure class="ob-diagram" markdown="0">
--8<-- "docs/diagrams/clock.svg"
<figcaption>The client sends a ping at t0. The phone notes when it got it (t1) and when it answered (t2). The reply arrives at t3. From the four times, the client works out the clock offset and the round trip, and keeps the estimate from the fastest round trip.</figcaption>
</figure>

In Python, `s.time` is that moment on your computer's clock, and `phone.round_trip_ms` shows how good the sync is.

## The links

Each link checks permission in the way that suits it, and uses the protocol that suits its clients.

| Link | Protocol | Who may connect | Typical speed |
|---|---|---|---|
| **WebSocket** (Wi-Fi, hotspot, USB) | JSON; video and audio over HTTP | Anyone with the link (it holds a token) | MB/s: video is fine |
| **USB serial** | Compact binary | The board on the cable | 0.1–1 MB/s |
| **Bluetooth LE** | Compact binary | Boards you tapped **Connect** for | 5–100 KB/s |
| **MQTT** | JSON, one message per sample | Whoever can read your broker | Depends on the network |
| **Recorder** | CSV per stream + `meta.json` | Stays on the phone until you share it | |

The compact protocol is for microcontrollers: checksummed frames, no allocation, about 23 bytes for a 3-axis sample. Details in [Protocol](PROTOCOL.md).

Rough sizes to plan with: IMU at 200 Hz ≈ 6 KB/s, 640×480 MJPEG at 15 fps ≈ 1 MB/s, 720p H.264 ≈ 0.3 MB/s, 16 kHz mono audio ≈ 32 KB/s.

## Processors

A processor turns streams into new streams. They're off by default and run only while read, like sensors.

| Processor | Makes | For |
|---|---|---|
| **Mount** | `robot.*` streams in the robot's axes (REP-103), plus `attitude` | No transforms on the robot side |
| **AprilTags** | `vision.apriltag`: each tag's id, position and distance | Docking, landmarks |
| Optical flow, audio FFT | (planned) | Odometry without wheel encoders; pitch and loudness |

## Making it yours

| Level | Who | How | State |
|---|---|---|---|
| 1. Settings | Everyone | Names, rates, sharing, mount | :material-check: |
| 2. Frame templates | Boards with their own protocol | Describe the frame in JSON, no code ([Frame templates](TEMPLATES.md)) | :material-check: USB, BLE |
| 3. Modules | Developers | Any program or firmware that speaks the protocol ([Modules](MODULES.md)) | :material-check: |
| 4. Plug-in apps | Third parties | A separate app connects through an AIDL API guarded by a permission you grant | Planned |
| 5. Scripting | Power users | Sandboxed encode/decode | Only if 2 isn't enough |

## Why it's built this way

??? question "Why doesn't the phone run ROS?"

    ROS 2 discovers nodes with UDP multicast (DDS). That's heavy on Android and unreliable over Wi-Fi. So the phone speaks a simple protocol, and a small bridge node on the robot's computer publishes standard ROS messages.

??? question "Why is the phone the Bluetooth central, not the board?"

    It matches USB, where the phone is the host. One phone can serve several boards, and the boards stay simple: they just advertise.

??? question "Why two protocols?"

    JSON is easy to read and works in any browser. A microcontroller wants small, checksummed frames it can parse with no memory allocation. Each link uses the one that suits its clients.

??? question "Why not ESP-NOW?"

    Android gives apps no raw Wi-Fi frames. The way round is a bridge: one ESP32 linked to the phone rebroadcasts over ESP-NOW. It's planned, not built.

??? question "Why does the app need the Internet permission?"

    Android requires it for any network socket, even on your own Wi-Fi or a USB cable. Privacy comes from behaviour instead: nothing is sent until you start streaming, and a notification shows that it's on.

??? question "Is it open source?"

    The protocol, its test kit and every client library are open source (MIT), so you can use them in any robot without changing its licence, or write your own client from the spec. The app itself is closed source.

## Where it's going

<div class="grid cards" markdown>

-   :material-check-circle-outline: **Done**

    Explorer, streaming to browser, Python, ROS 2, boards (USB, BLE, Wi-Fi) and MQTT. Cameras, microphones, recording, commands, mount, AprilTags.

-   :material-progress-wrench: **Now**

    These docs.

-   :material-lightbulb-on-outline: **Later**

    Optical flow, audio FFT, several phones on one robot, plug-in apps.

-   :material-dots-horizontal-circle-outline: **Maybe**

    Foxglove protocol, binary WebSocket, the ESP-NOW bridge.

</div>
