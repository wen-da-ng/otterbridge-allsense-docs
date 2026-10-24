---
description: "Read the phone's sensors, cameras and microphones from Python in a few lines."
---

# Python

The phone's sensors, cameras and mics in your Python code.
{ .lead }

<div class="ob-meta" markdown><span>:material-timer-outline: 5 minutes</span><span>:material-toolbox-outline: Python 3.9+ on the same Wi-Fi</span></div>

!!! robot "For example"
    A class experiment: read the accelerometer at 100 Hz while a cart rolls down a ramp, then save it to CSV.

## The shortest way

<div class="steps" markdown>

1. Install the client (it isn't on PyPI yet, so from GitHub):

    ```bash
    pip install "allsense[all] @ git+https://github.com/wen-da-ng/otterbridge-allsense-python"
    ```

2. On the phone: **Home → Start streaming**, then open **Connect → Programming**: its steps have your phone's link filled in.

3. Save this as `quickstart.py`:

    ```python title="quickstart.py"
    --8<-- "examples/python/examples/quickstart.py"
    ```

4. Run it with your link, then tilt the phone: the numbers change.

    ```bash
    python quickstart.py "http://192.168.1.20:8765/?token=abcd"
    ```

</div>

## Details

**Names.** Use the names the app shows (rename them there). `phone.streams()` lists them with fields and units.

**Reading.** Pick the style that fits:

```python
accel = phone.subscribe("accelerometer", rate=100)
s = accel.get(timeout=1)    # wait for the next sample
s = accel.latest            # newest, never waits (control loops)
batch = accel.read()        # everything since the last call
```

**Time.** `s.time` is when the sensor measured, in Unix seconds on *your* computer's clock (synced automatically). Use it to line up phone data with your robot's.

**Connection drops.** The client reconnects and resubscribes by itself.

??? example "A fuller example: print all three axes"

    ```python title="print_values.py"
    --8<-- "examples/python/examples/print_values.py"
    ```

More: cameras, microphones, commands, recordings and NumPy in the [client's README](https://github.com/wen-da-ng/otterbridge-allsense-python).

## Reference

| Call | Does |
|---|---|
| `allsense.connect(link)` | Connects; `wait=` keeps trying until the phone answers |
| `phone.streams()` | Shared streams (`all=True` for vendor and raw ones) |
| `phone.subscribe(name, rate=)` | A stream, or a list of them; `callback=` for a function |
| `phone.camera(name)`, `phone.snapshot(name)` | Video (MJPEG or `codec="h264"`), one JPEG |
| `phone.microphone(name)` | Audio chunks (16-bit mono) |
| `phone.command("vibrate", ms=300)` | Runs a command, if Commands is on in the app |
| `allsense.load_recording(path)` | Reads a recording the app saved |

Command line: `allsense discover`, `allsense list <link>`, `allsense echo <link> accelerometer --csv`.
