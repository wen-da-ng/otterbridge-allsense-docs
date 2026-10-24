---
title: Contributing
description: "Where each part of AllSense lives, how to test it, how protocol changes flow, and lessons learned with boards and ROS."
---

# Contributing

Where each part lives, how it's tested, and what we've learned the hard way.
{ .lead }

## The repositories

| Repository | What | Test it with |
|---|---|---|
| [otterbridge-allsense](https://github.com/wen-da-ng/otterbridge-allsense) | Home: the app's downloads and **app issues** | |
| [otterbridge-allsense-protocol](https://github.com/wen-da-ng/otterbridge-allsense-protocol) | The spec, shared byte vectors, and the `allsense-testkit` package (fake phones, codecs, conformance runner) | `pytest` |
| [otterbridge-allsense-python](https://github.com/wen-da-ng/otterbridge-allsense-python) | Python client and CLI | `pytest` against the fake phone |
| [otterbridge-allsense-cpp](https://github.com/wen-da-ng/otterbridge-allsense-cpp) | C++17 client | `allsense-conformance` |
| [otterbridge-allsense-rust](https://github.com/wen-da-ng/otterbridge-allsense-rust) | Rust crate | `cargo test`, `allsense-conformance` |
| [otterbridge-allsense-ros2](https://github.com/wen-da-ng/otterbridge-allsense-ros2) | ROS 2 bridge | `colcon test` in a ROS container |
| [otterbridge-allsense-arduino](https://github.com/wen-da-ng/otterbridge-allsense-arduino) | Arduino / ESP32 library | compile matrix, host tests with the shared vectors |
| [otterbridge-allsense-starters](https://github.com/wen-da-ng/otterbridge-allsense-starters) | Module starters and the module skill | `allsense-template check`, `pytest` |
| [otterbridge-allsense-docs](https://github.com/wen-da-ng/otterbridge-allsense-docs) | This site | `mkdocs build --strict` |

Each repository's README says how to set it up and run its tests; its CI runs the same. The app itself is closed source: report app problems in the home repository's issues.

## Sending a change

1. Open an issue first for anything bigger than a typo, so we can agree on the approach.
2. Fork, change, and run the repository's tests (and the conformance scenarios for a client).
3. Open a pull request. A maintainer reviews every change before it's merged.

Code you contribute is under the repository's licence (MIT).

## When the protocol changes

The [protocol](../PROTOCOL.md) is the contract between the phone and everything else, so a change goes in this order:

1. **The protocol repository:** the spec, the shared vectors (if framing changes), the test kit's fake phones and codecs, and a conformance scenario. Then a test kit release.
2. **The app**, against the new test kit.
3. **Every affected client**, each in its own repository, moving to the new test kit.

Version 0 may still change; the app and clients say which protocol version they speak.

## Lessons learned

**Boards**

- **USB serial to an ESP32:** DTR on, **RTS off**. RTS without DTR resets the chip.
- **ESP32-S3:** `Serial` goes over USB only with **USB CDC On Boot: Enabled**.
- **Arduino sketches:** never name a global `link`; it clashes with POSIX `link()` on ESP32.
- **ESP32 Wi-Fi:** modem sleep delivers samples in 100–300 ms bursts, so the library calls `WiFi.setSleep(false)`.
- **ESP32 WebSockets library:** messages over 15 KB are rejected. The catalog is about 18 KB, so boards connect with `&catalog=none`.
- **ESP32 core 3.3 BLE** is NimBLE on the S3: don't add a BLE2902 descriptor (it's automatic), and set the name in the scan response explicitly.
- **Which link is it?** A board running the BLE sketch but plugged into the phone gets power over USB and an idle USB session, while its data flows over BLE. Check which sketch it runs before debugging "USB".
- **A board on the phone's USB port can't also be on your PC.** Test it on the PC first with a fake phone (`allsense-fake-serial`, `allsense-fake-ble`), then move it.
- **BLE scans** find nothing while the phone's Location is off.

**Clients and ROS**

- **Vanishing Wi-Fi doesn't close sockets.** Clients need a stall watchdog (the Python client gives up after 6 s of silence and reconnects).
- **Use sample timestamps** (`t`, phone boot clock) for intervals, not arrival times: Wi-Fi delivers in bursts.
- **ROS 2 in WSL with mirrored networking:** Fast DDS discovers nodes but delivers nothing; use Cyclone DDS (`RMW_IMPLEMENTATION=rmw_cyclonedds_cpp`). The CLI daemon hangs; use `--no-daemon`.
- **rclpy:** don't name node attributes `_publishers` and the like, or you shadow its internals.
