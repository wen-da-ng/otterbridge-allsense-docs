---
description: "See the phone's sensors, cameras and sound live in any browser, with nothing to install."
---

# Browser

Watch every sensor, camera and mic live, from any computer.
{ .lead }

<div class="ob-meta" markdown><span>:material-timer-outline: 1 minute</span><span>:material-toolbox-outline: a computer on the same Wi-Fi</span></div>

!!! robot "For example"
    Before writing any code, mount the phone on the robot, open the dashboard on your laptop and watch the IMU while the robot drives.

## The shortest way

<div class="steps" markdown>

1. On the phone: **Home → Start streaming**, then **Connect → Browser**.
2. On the computer, scan the QR code or type the link.

</div>

That's it. The dashboard lists every shared stream with live values and graphs, the cameras and the microphones.

## Details

**The link** looks like `http://192.168.1.20:8765/?token=k3x9…`. The token is the password: anyone with the link can read what you share. To lock everyone out, make a new one: **Settings → Server → New token** (Advanced mode).

**Other networks.** The computer can also join the phone's hotspot, or use a USB cable:

=== "Phone's hotspot"

    Turn on the hotspot, join it from the computer, then open the link the app shows.

=== "USB cable (adb)"

    With USB debugging on, forward the port and open it on the computer:

    ```bash
    adb forward tcp:8766 tcp:8765
    # then open http://localhost:8766/?token=…
    ```

**What's shared.** All streams, or only some: **Connect → Browser → Streams it may send**. The same setting covers Python and ROS 2, which use the same link.

**Who's connected.** The guide lists each client. Tap **Disconnect** to drop one.

## Reference

| Thing | Value |
|---|---|
| Address | `http://<phone-ip>:8765/?token=<token>` |
| Port | 8765 (change it under **Settings → Server**, in Advanced mode) |
| Discovery | DNS-SD `_allsense._tcp` (`allsense discover` finds phones) |
| Cameras | `/camera/<name>.mjpg`, `.jpg`, `.h264` |
| Microphones | `/mic/<name>.wav` |
| Data | WebSocket `/ws`, JSON: see [Protocol](../PROTOCOL.md) |
