---
description: "Read the phone's sensors from Rust: a small blocking crate, no async runtime."
---

# Rust

The phone's sensors in your Rust program. Blocking, no async runtime needed.
{ .lead }

<div class="ob-meta" markdown><span>:material-timer-outline: 5 minutes</span><span>:material-toolbox-outline: Rust 1.85+ on the same Wi-Fi</span></div>

!!! robot "For example"
    A lawn robot on a Raspberry Pi: follow the phone's GNSS position and compass heading, and stop when the battery stream drops below 20 %.

## The shortest way

<div class="steps" markdown>

1. Make a project and add the crate (it isn't on crates.io yet, so from GitHub):

    ```bash
    cargo new quickstart && cd quickstart
    cargo add allsense --git https://github.com/wen-da-ng/otterbridge-allsense-rust
    ```

    With a copy of the repository: `cargo add allsense --path path/to/otterbridge-allsense-rust`.

2. On the phone: **Home → Start streaming**, then open **Connect → Programming → Rust**: its steps have your phone's link filled in.

3. Put this in `src/main.rs`:

    ```rust title="src/main.rs"
    --8<-- "examples/rust/examples/quickstart.rs"
    ```

4. Run it with your link, then tilt the phone: the numbers change.

    ```bash
    cargo run -- "http://192.168.1.20:8765/?token=abcd"
    ```

</div>

## Details

**Names.** Use the names the app shows (rename them there). `phone.streams(false)` lists them with fields and units.

**Reading.** Pick the style that fits:

```rust
let accel = phone.subscribe("accelerometer", Some(100.0))?;
let s = accel.get()?;                                // wait for the next sample
let s = accel.get_timeout(Duration::from_secs(1))?;  // or give up (Error::Timeout)
let s = accel.latest();                              // newest, never waits (control loops)
let batch = accel.read();                            // everything since the last call
```

**Values.** `s["x"]` or `s[0]`; `s.get("x")` gives an `Option`. Missing values are NaN.

**Time.** `s.time` is when the sensor measured, in Unix seconds on *your* computer's clock (synced automatically). Use it to line up phone data with your robot's.

**Connection drops.** The client reconnects and resubscribes by itself. Dropping a `Subscription` stops its stream; dropping the `Phone` disconnects.

??? example "A fuller example: print all three axes"

    ```rust title="print_values.rs"
    --8<-- "examples/rust/examples/print_values.rs"
    ```

More: cameras, microphones, commands and options in the [crate's README](https://github.com/wen-da-ng/otterbridge-allsense-rust).

## Reference

| Call | Does |
|---|---|
| `allsense::connect(link)` | Connects; `Options::new().wait(d).connect(link)` keeps trying until the phone answers |
| `phone.streams(all)` | Shared streams (`true` for vendor and raw ones) |
| `phone.subscribe(name, rate)` | A stream; `subscribe_many` for several, `subscribe_with` for a callback |
| `phone.snapshot(name)`, `phone.camera_url(name, &opts)` | One JPEG; a video URL for ffmpeg or OpenCV |
| `phone.microphone_url(name, rate)` | Live WAV audio (16-bit mono) |
| `phone.command("vibrate", json!({"ms": 300}))` | Runs a command, if Commands is on in the app |
