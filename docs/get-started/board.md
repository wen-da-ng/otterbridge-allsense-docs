---
description: "Use the phone as an Arduino, ESP32 or Pico board's IMU and compass, by USB cable, Bluetooth or Wi-Fi."
---

# Microcontroller

The phone as your board's IMU, compass and GPS.
{ .lead }

<div class="ob-meta" markdown><span>:material-timer-outline: 10 minutes</span><span>:material-toolbox-outline: Arduino IDE and a board</span></div>

!!! robot "For example"
    An Arduino line-follower reads tilt and heading from the phone over one USB cable. Nothing extra to wire, and the phone even powers the board.

## The shortest way

Install the Arduino library: download [otterbridge-allsense-arduino](https://github.com/wen-da-ng/otterbridge-allsense-arduino) as a ZIP and add it with **Sketch → Include Library → Add .ZIP Library** (it isn't in the Library Manager yet). Then pick how the board reaches the phone:

=== "USB cable (any board)"

    <div class="steps" markdown>

    1. Upload **File → Examples → AllSense → USBQuickstart**.
       ESP32-S3: **Tools → USB CDC On Boot → Enabled**, and use the port labelled USB.
    2. Plug the board into the phone (USB-C to USB-C, or an OTG adapter). Android asks to open AllSense: tick **Always**.
    3. On the phone: **Home → Start streaming**.

    </div>

    The LED blinks blue while it waits, then follows the phone's tilt. In your own sketch, this is all it takes:

    ```cpp title="USBMinimal.ino"
    --8<-- "examples/arduino/examples/USBMinimal/USBMinimal.ino"
    ```

=== "Bluetooth (ESP32)"

    <div class="steps" markdown>

    1. Upload **File → Examples → AllSense → BLEQuickstart**.
    2. On the phone: **Home → Start streaming**, then **Connect → Microcontroller → By Bluetooth → Connect** next to "AllSense S3".
    3. Tilt the phone: values print in the Serial Monitor (115200).

    </div>

    Connect once: the phone reconnects whenever the board is in range. Location must be on for the phone to find boards.

=== "Wi-Fi (ESP32)"

    <div class="steps" markdown>

    1. Install the **WebSockets** (Markus Sattler) and **ArduinoJson** libraries.
    2. Upload **File → Examples → AllSense → WiFiQuickstart**.
    3. In the Serial Monitor (115200, Newline), type `ssid …`, `pass …` and `link …` with the link from **Connect → Browser**. The board saves them.

    </div>

    Board and phone must be on the same Wi-Fi, or the board on the phone's hotspot.

??? example "The full USBQuickstart sketch"

    ```cpp title="USBQuickstart.ino"
    --8<-- "examples/arduino/examples/USBQuickstart/USBQuickstart.ino"
    ```

??? example "The full BLEQuickstart sketch"

    ```cpp title="BLEQuickstart.ino"
    --8<-- "examples/arduino/examples/BLEQuickstart/BLEQuickstart.ino"
    ```

## Details

**Reconnects by itself.** Unplug, reset or restart either side: the board resubscribes when the link is back.

**Several streams.** Call `subscribe()` once per stream (up to 12; 4 on an Uno). `phone.onSample(...)` calls you on every sample instead of polling `latest()`.

**A board that speaks its own protocol.** If your firmware already reads fixed binary frames, the phone can send those instead: see [Frame templates](../TEMPLATES.md).

**Which board?** USB works with ESP32-S2/S3/C3/C6, Arduino Uno, Nano, Mega and R4, Raspberry Pi Pico, and boards with CH340, CP210x or FTDI chips. Bluetooth and Wi-Fi need an ESP32.

## Reference

| Class | Link | Boards | Protocol |
|---|---|---|---|
| `AllSenseSerial` | USB cable | any (fits an Uno: 5 KB flash) | compact binary |
| `AllSenseBLE` | Bluetooth LE | ESP32 | compact binary |
| `AllSense` | Wi-Fi | ESP32 | JSON over WebSocket |

| Call | Does |
|---|---|
| `begin(...)` | Starts the link (a serial port, a Bluetooth name, or a phone link) |
| `subscribe(name, hz)` | Asks for a stream |
| `loop()` | Call every loop: reads the link |
| `latest(name)` | The newest sample, or `nullptr`; `(*a)[0]` is the first value |
| `connected()` | True while the phone answers |
| `lastError()` | The phone's last complaint, e.g. a misspelt name |

Wire format: [Protocol](../PROTOCOL.md).
