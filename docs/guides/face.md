---
description: "Use the phone as the robot's face, voice and buzzer: show faces or text, speak, vibrate, beep, light the flash."
---

# Give the robot a face

The phone's screen, speaker and motor, driven by your code.
{ .lead }

<div class="ob-meta" markdown><span>:material-timer-outline: 5 minutes</span><span>:material-toolbox-outline: Any client: Python, C++, Rust or MQTT</span></div>

!!! robot "For example"
    A desk robot smiles when someone walks up, says hello, and shows "Charging" with a sleepy face when its battery is low.

## The shortest way

<div class="steps" markdown>

1. On the phone: **Robot → Robot can control the phone**, turn it on. It's off by default, so nobody on your network can make the phone speak without you allowing it.

2. If the app may be in the background, also allow **Screen from the background** in that card (Android's "Display over other apps").

3. Run this with your link:

    ```python title="robot_face.py"
    --8<-- "examples/python/examples/robot_face.py"
    ```

</div>

## Details

**Faces:** `happy`, `sad`, `neutral`, `surprised`, `thinking`, `sleepy`, `angry`, with or without `text`, in any `color` and `background`. Sending `display` again updates the screen; `action="clear"` (or a long press on the phone) ends it. The screen stays on meanwhile.

**More commands:** `say` (text to speech), `vibrate`, `tone`, `torch`, `volume`, `sound` (the phone's own or your saved sounds: `phone.upload_sound("beep.wav")`), `camera` (exposure, focus, white balance) and `record`.

**In other languages:** C++ `phone.command("say", {{"text", "Hi"}})`, Rust `phone.command("say", json!({"text": "Hi"}))?`. Over MQTT, publish the same JSON to `<prefix>/cmd`.

**Refusals** come back as errors with the reason, e.g. "Commands are off on the phone: Robot → Robot can control the phone".

## Reference

| What | Where |
|---|---|
| Every command and its arguments | [Protocol → Commands](../PROTOCOL.md#commands) |
| Over MQTT | [MQTT](../MQTT.md) |
