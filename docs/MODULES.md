---
title: Modules
description: "Add your own board, program or bridge to AllSense: a frame template, or a program that speaks the protocol."
---

# Building modules

Add a new way to use the phone, usually without touching the app.
{ .lead }

AllSense works like MCP: the phone is the hub, the protocol is written down, and anything that speaks it can join. You don't need permission or a change to the app.

There are two kinds. Pick the first one that can do what you need.

| Kind | You write | Runs on | Test it with | Starter |
|---|---|---|---|---|
| **Frame template** | A JSON file | The phone (no code) | `allsense-template check`, `allsense-fake-template` | [`frame-template/`](https://github.com/wen-da-ng/otterbridge-allsense-starters/tree/main/frame-template) |
| **Outside module** | A program or firmware, any language | A PC, robot computer or board | The fake phones (below) | [`python-module/`](https://github.com/wen-da-ng/otterbridge-allsense-starters/tree/main/python-module), [the Arduino library's examples](https://github.com/wen-da-ng/otterbridge-allsense-arduino/tree/main/examples) |

The starters live in [otterbridge-allsense-starters](https://github.com/wen-da-ng/otterbridge-allsense-starters). For step-by-step instructions (for a person or an AI agent), see its [module skill](https://github.com/wen-da-ng/otterbridge-allsense-starters/blob/main/skills/allsense-module/SKILL.md).

Need a new way to reach the phone that the app itself must drive (a radio or network protocol it doesn't speak)? First see whether an outside module can bridge it. If not, the app is closed source: [open an issue](https://github.com/wen-da-ng/otterbridge-allsense/issues) describing what you want to connect.

## 1. Frame templates (no code)

For a board that already has its own serial protocol. You describe the bytes; the phone sends them. Full format: [TEMPLATES.md](TEMPLATES.md).

**Done when:** `allsense-template check` prints `OK`, and the board reads the frames (with `allsense-fake-template` on a PC, then from the phone).

## 2. Outside modules (the MCP-server kind)

Anything off the phone that talks to it: a logger, a ROS or Foxglove bridge, a dashboard, a board library, a bridge to another radio. Pick the protocol by where it runs:

| Where it runs | Protocol | Link | Library |
|---|---|---|---|
| PC, robot computer, browser | JSON over WebSocket ([PROTOCOL.md](PROTOCOL.md)) | Wi-Fi, hotspot, USB tethering, `adb forward` | [Python client](https://github.com/wen-da-ng/otterbridge-allsense-python), [C++](https://github.com/wen-da-ng/otterbridge-allsense-cpp), [Rust](https://github.com/wen-da-ng/otterbridge-allsense-rust) |
| Microcontroller | Compact binary ([PROTOCOL.md](PROTOCOL.md), "Compact protocol") | USB cable to the phone, BLE | [Arduino library](https://github.com/wen-da-ng/otterbridge-allsense-arduino) |
| ESP32 on Wi-Fi | JSON over WebSocket with `&catalog=none` | Wi-Fi | [Arduino library](https://github.com/wen-da-ng/otterbridge-allsense-arduino) (`AllSense` class) |

**Rules every outside module follows:**
- Find streams by the name set in the app (`accelerometer`), not by list position. Store the stable `id` if you need the same hardware again after a rename.
- Expect streams you can't receive: `refused` (Android won't deliver it) and `not_shared` (the user didn't share it over that link). A `not_shared` subscription starts by itself once the user shares it. Tell the user which one it is and where to fix it (Python: `sub.state`).
- Survive the phone going away. The libraries reconnect and resubscribe after a drop. A program that may start before the phone must also wait for the first connection (Python: `connect(url, wait=float("inf"))`). A rejected token (Python: `TokenError`) won't fix itself: stop and ask for the current link.
- Use the sample's timestamp `t` (phone boot clock), not your arrival time, when timing matters.

**Fake phones, so you can test without the phone:**

| Tests | Command |
|---|---|
| A WebSocket client | `allsense-fake-phone` (or `FakePhone` from `allsense_testkit` in a test) |
| A USB board (compact protocol) | `allsense-fake-serial --port COM3` (or `/dev/ttyUSB0`) |
| A BLE board | `allsense-fake-ble --serial COM3` |
| A frame template board | `allsense-fake-template --port COM3 --template t.json` |

**Steering the WebSocket fake phone from a test** (`FakePhone` in `allsense_testkit`; the Python starter's tests use all of these):

| To test | Do |
|---|---|
| The user stops or starts sharing a stream | `server.set_shared("accelerometer", False)` / `True` |
| Specific values (a bump, a fault) | `server.set_values("accelerometer", lambda t, seq: [0, 0, 30])`, or a fixed list; `None` restores the default |
| Wi-Fi vanishing (silent link) | `server.frozen.set()`, later `server.frozen.clear()`; connect with a short `stall_timeout` to keep tests fast |
| The phone going away and coming back | `server.stop()`, then `server.restart()` (same port) |
| A stream Android refuses | subscribe to `locked` |
| A wrong token | connect with `?token=nope` |

**Done when:** your tests pass against the fake phone, then it works once with the real phone.

## Versioning

- Protocol version 0 may still change. When it does, the spec, the test kit's fake phones, the app and every client change together.
- Templates and outside modules depend only on the written spec.
- Licences: the clients, the test kit, the starters and the protocol specification are MIT, so outside modules can use any licence.
