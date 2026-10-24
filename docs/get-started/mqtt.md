---
description: "Publish the phone's streams to an MQTT broker, for Home Assistant, Node-RED or a cloud dashboard."
---

# MQTT

Publish the phone's streams to any MQTT broker.
{ .lead }

<div class="ob-meta" markdown><span>:material-timer-outline: 5 minutes</span><span>:material-toolbox-outline: a broker: Mosquitto, Home Assistant or cloud</span></div>

!!! robot "For example"
    Show the robot's battery and position on a Home Assistant dashboard, or log a phone on a remote robot through a cloud broker.

## The shortest way

You need a broker: Mosquitto on a PC or Raspberry Pi, the Home Assistant add-on, or a cloud one.

<div class="steps" markdown>

1. On the phone: **Home → Connect → MQTT**.
2. Turn on **Publish to a broker** and enter it, e.g. `tcp://192.168.1.10:1883`.
3. **Choose** the streams, pick a rate and **Save**.
4. **Start streaming**, then watch it arrive:

    ```bash
    mosquitto_sub -h 192.168.1.10 -t 'allsense/#' -v
    ```

</div>

## Details

**One message per sample**, as JSON: `{"t":…, "time":1792239094.64, "seq":0, "v":[-0.76, 4.08, 8.90]}`. `v` holds the values in the order of the stream's fields; `time` is Unix seconds.

**Online or not.** `allsense/<device>/status` is `online` while the phone is connected, and the broker sets it to `offline` if the phone drops off.

**Home Assistant / Node-RED.** Subscribe to a stream's topic and read `value_json.v[0]`, e.g. for the battery level.

**Cloud brokers.** Use `ssl://<host>:8883` with your account's username and password.

**Commands** (vibrate, speak, show a face…) can come in on `allsense/<device>/cmd`, but only after you allow them in the app: anyone who can publish to your broker could use them.

## Reference

| Topic | Payload |
|---|---|
| `allsense/<device>/<category>/<name>` | one sample: `t`, `time`, `seq`, `v` |
| `allsense/<device>/catalog` (retained) | the stream list with fields and units |
| `allsense/<device>/status` (retained) | `online` / `offline` |
| `allsense/<device>/cmd` | a command you send, e.g. `{"command":"vibrate","ms":200}` |
| `allsense/<device>/cmd/result` | its result |

The prefix `allsense/<device>` can be changed in the card. Everything else: [MQTT reference](../MQTT.md).
