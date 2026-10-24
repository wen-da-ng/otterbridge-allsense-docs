---
description: "Read the phone's sensors from C++17 on Linux, Windows or macOS, with CMake."
---

# C++

The phone's sensors in your C++ program, for control loops on the robot's computer.
{ .lead }

<div class="ob-meta" markdown><span>:material-timer-outline: 10 minutes</span><span>:material-toolbox-outline: C++17, CMake 3.18+, on the same Wi-Fi</span></div>

!!! robot "For example"
    A balancing robot on a Raspberry Pi: read the phone's gyroscope at 200 Hz in the control loop, and stamp each reading on the Pi's own clock.

## The shortest way

<div class="steps" markdown>

1. Make a folder with this `CMakeLists.txt` (CMake downloads the client and its one header-only dependency):

    ```cmake title="CMakeLists.txt"
    --8<-- "examples/cpp/examples/project/CMakeLists.txt"
    ```

2. On the phone: **Home → Start streaming**, then open **Connect → Programming → C++**: its steps have your phone's link filled in.

3. Save this next to it as `quickstart.cpp`:

    ```cpp title="quickstart.cpp"
    --8<-- "examples/cpp/examples/quickstart.cpp"
    ```

4. Build it, run it with your link, then tilt the phone: the numbers change.

    ```bash
    cmake -S . -B build && cmake --build build
    ./build/quickstart "http://192.168.1.20:8765/?token=abcd"
    ```

    With a copy of the repository instead of the download, point CMake at it:

    ```bash
    cmake -S . -B build -DFETCHCONTENT_SOURCE_DIR_ALLSENSE=path/to/otterbridge-allsense
    ```

</div>

## Details

**Names.** Use the names the app shows (rename them there). `phone.streams()` lists them with fields and units.

**Reading.** Pick the style that fits:

```cpp
auto accel = phone.subscribe("accelerometer", 100);
allsense::Sample s = accel.get();   // wait for the next sample
auto next = accel.get(1s);          // std::optional: empty after the timeout
auto last = accel.latest();         // newest, never waits (control loops)
auto batch = accel.read();          // everything since the last call
```

**Values.** `s["x"]` or `s[0]`; missing values are NaN.

**Time.** `s.time` is when the sensor measured, in Unix seconds on *your* computer's clock (synced automatically). Use it to line up phone data with your robot's.

**Connection drops.** The client reconnects and resubscribes by itself. A wrong token throws `allsense::TokenError`.

??? example "A fuller example: print all three axes"

    ```cpp title="print_values.cpp"
    --8<-- "examples/cpp/examples/print_values.cpp"
    ```

More: cameras (OpenCV), microphones, commands and options in the [client's README](https://github.com/wen-da-ng/otterbridge-allsense-cpp).

## Reference

| Call | Does |
|---|---|
| `allsense::connect(link, options)` | Connects; `Options::wait` keeps trying until the phone answers |
| `phone.streams()` | Shared streams (`streams(true)` for vendor and raw ones) |
| `phone.subscribe(name, rate)` | A stream, or a vector of them; a third argument for a callback |
| `phone.snapshot(name)`, `phone.camera_url(name, options)` | One JPEG; a video URL for OpenCV or ffmpeg |
| `phone.microphone_url(name)` | Live WAV audio (16-bit mono) |
| `phone.command("vibrate", {{"ms", 300}})` | Runs a command, if Commands is on in the app |

Builds with GCC, Clang and MSVC; tested on Windows and Linux.
