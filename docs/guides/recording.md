---
description: "Log sensors on the phone itself, with the screen off and no laptop, then take the files home as CSV or MCAP."
---

# Record a run

Log sensors on the phone itself, then take the files home.
{ .lead }

<div class="ob-meta" markdown><span>:material-timer-outline: 2 minutes</span><span>:material-toolbox-outline: Just the phone</span></div>

!!! robot "For example"
    Strap the phone to a rover, record IMU and GPS for a test drive with no laptop along, then replay the run in Foxglove.

## The shortest way

<div class="steps" markdown>

1. On the phone: **Robot → Recording**. Under **What to record**, tap **Choose** and pick the streams (say `accelerometer`, `gyroscope`, `position`), then a **Rate**.

2. Tap **Record**. Streaming doesn't need to be on, and the screen can go off: the notification shows it's recording.

3. Drive. Then tap **Stop** (in the card or the notification).

4. Under **Saved**, tap **Share** to send the run as a .zip: Drive, email, a chat app.

</div>

## Details

**From your program.** With **Robot → Robot can control the phone** on, code can start and stop a recording, e.g. at the start line:

```python title="record_run.py"
--8<-- "examples/python/examples/record_run.py"
```

**Other ways to get the files.** While streaming, `/recordings` on the phone's link lists them for download (`http://<phone>:8765/recordings?token=…`). Over a USB cable they're in `Android/data/io.github.wen_da_ng.otterbridge.allsense/files/recordings/`.

**Reading them.** One CSV per stream plus `meta.json`. In Python: `rec = allsense.load_recording("run.zip")`, then `rec["accelerometer"].arrays()`.

**Foxglove or ROS 2.** Convert to MCAP: `allsense mcap run.zip` (Foxglove) or `allsense mcap run.zip --ros2` (plays with `ros2 bag play`, with the bridge's message types).

**Safe by design.** Files are flushed every second: a crash or a flat battery loses at most the last second.

## Reference

| What | Where |
|---|---|
| Format, columns, `meta.json` | [Recordings](../RECORDING.md) |
| The `record` command | [Protocol → Commands](../PROTOCOL.md#commands) |
| Python | `allsense.load_recording(path)`, `allsense.export_mcap(...)`, `allsense mcap <file>` |
