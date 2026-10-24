---
description: "Let the phone find AprilTags in its camera view: which tag, how far, and which way, as a plain stream."
---

# Follow an AprilTag

The phone spots printed tags and tells your robot how far and which way.
{ .lead }

<div class="ob-meta" markdown><span>:material-timer-outline: 10 minutes</span><span>:material-toolbox-outline: A printed tag (tag36h11) and a ruler</span></div>

!!! robot "For example"
    A robot that docks to its charger: tag 7 sits above the dock, and the robot steers until the tag is straight ahead and 20 cm away.

## The shortest way

<div class="steps" markdown>

1. Print a tag from the `tag36h11` family (any [AprilTag generator](https://github.com/AprilRobotics/apriltag-imgs) works) and measure the black square's edge.

2. On the phone: **Robot → AprilTags**, turn it on. In **Settings**, pick the camera and enter the **Tag size, cm**.

3. Hold the tag in front of the camera. The card shows what the detector sees: the tag outlined with its number and distance, and its axes (x red, y green, z blue, out of the tag).

4. Steer towards it:

    ```python title="follow_tag.py"
    --8<-- "examples/python/examples/follow_tag.py"
    ```

</div>

## Details

**One sample per tag per frame.** Each has `id`, where it is in the picture (`u`, `v` from 0 to 1), where it is in space (`x`, `y`, `z` in metres, camera frame), `distance`, `bearing` (left is positive), `yaw` (how far the tag is turned) and `margin` (above ~30 is a sure detection). No tag in view: no samples.

**Without the tag size** you still get `id`, `u` and `v`; the distances are empty.

**It only runs while subscribed**, and shares the camera with anyone watching its video.

**Accuracy.** Expect a few percent of error in distance; calibrate the camera yourself for precise work. Bigger tags and 1280×720 reach further; 640×480 is faster.

**On a board.** It's a plain stream, so an Arduino can subscribe to `vision.apriltag` over USB or Bluetooth like any sensor.

## Reference

| What | Where |
|---|---|
| Fields, units, families, options | [Protocol → Vision](../PROTOCOL.md#vision-vision-category-apriltags) |
| Stream name | `vision.apriltag` (topic `allsense.<device>.vision.apriltag`) |
