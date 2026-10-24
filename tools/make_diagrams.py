"""Writes the How it works diagrams to docs/diagrams/*.svg (inlined into ARCHITECTURE.md by snippets): python tools/make_diagrams.py
Colours come from classes styled in docs/stylesheets/extra.css (dg-*), so they follow light/dark."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "docs" / "diagrams"
OUT.mkdir(exist_ok=True)

DEFS = ('<defs><marker id="{id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0 0L10 5L0 10z" class="dg-tip"/></marker>'
        '<marker id="{id}-o" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0 0L10 5L0 10z" class="dg-tip-accent"/></marker></defs>')


def svg(name, w, h, label, body):
    s = (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">'
         + DEFS.format(id=f"a-{name}") + "".join(body) + "</svg>\n")
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")


def box(x, y, w, h, title, sub=None, cls="dg-box", anchor="start"):
    tx = x + 14 if anchor == "start" else x + w / 2
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" class="{cls}"/>']
    if sub:
        out.append(f'<text x="{tx}" y="{y + h / 2 - 3}" class="dg-title" text-anchor="{anchor}">{title}</text>')
        out.append(f'<text x="{tx}" y="{y + h / 2 + 13}" class="dg-sub" text-anchor="{anchor}">{sub}</text>')
    else:
        out.append(f'<text x="{tx}" y="{y + h / 2 + 4}" class="dg-title" text-anchor="{anchor}">{title}</text>')
    return out


def arrow(name, x1, y1, x2, y2, label=None, accent=False, lx=None, ly=None):
    cls = "dg-arrow dg-accent" if accent else "dg-arrow"
    m = f"a-{name}-o" if accent else f"a-{name}"
    out = [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}" marker-end="url(#{m})"/>']
    if label:
        out.append(f'<text x="{lx if lx is not None else (x1 + x2) / 2}" y="{ly if ly is not None else y1 - 6}" '
                   f'class="dg-label" text-anchor="middle">{label}</text>')
    return out


def head(x, y, text, anchor="start"):
    return [f'<text x="{x}" y="{y}" class="dg-head" text-anchor="{anchor}">{text}</text>']


# ---------- 1. Overview: sources -> engine -> sharing -> links -> clients ----------
n = "overview"
b = []
b += [f'<rect x="10" y="20" width="640" height="372" rx="20" class="dg-frame"/>',
      '<text x="30" y="44" class="dg-title">Phone · AllSense app</text>']
ys = [84, 142, 200, 258, 316]
b += head(30, 72, "SOURCES")
for y, (t, s) in zip(ys, [("Motion sensors", "IMU, compass, baro"), ("Location, radios", "GNSS, Wi-Fi, cell"),
                          ("Battery", "level, charging"), ("Cameras", "every lens"), ("Microphones", "every input")]):
    b += box(30, y, 140, 46, t, s)
    b += arrow(n, 170, y + 23, 206, y + 23)
# engine
b += head(210, 72, "ENGINE")
b += [f'<rect x="210" y="84" width="170" height="278" rx="12" class="dg-box"/>']
for y, (t, s) in zip([96, 162, 228, 294], [("SensorHub", "runs only while read"), ("Camera / MicHub", "one capture, shared"),
                                           ("Decimator", "each reader, own rate"), ("Processors", "mount, AprilTags")]):
    b += box(222, y, 146, 54, t, s, cls="dg-inner")
# sharing gate
b += [f'<line x1="405" y1="80" x2="405" y2="372" class="dg-gate"/>',
      '<text x="398" y="72" class="dg-head dg-accent-text" text-anchor="end">SHARING</text>',
      '<text x="405" y="386" class="dg-label dg-accent-text" text-anchor="middle">per link</text>']
# links
b += head(430, 72, "LINKS")
clients = [("Browser, Python, ROS 2", "Wi-Fi, hotspot, USB"), ("Arduino, ESP32, Pico", "a USB cable"),
           ("ESP32", "Bluetooth LE"), ("MQTT broker", "Home Assistant, cloud"), ("Files", "CSV, MCAP: share later")]
for y, (t, s), proto, (ct, cs) in zip(ys, [("WebSocket", "+ HTTP video, audio"), ("USB serial", None), ("Bluetooth LE", None),
                                          ("MQTT", None), ("Recorder", "on the phone")],
                                      ["JSON", "compact", "compact", "JSON", "CSV"], clients):
    b += arrow(n, 380, y + 23, 426, y + 23)
    b += box(430, y, 150, 46, t, s)
    b += arrow(n, 580, y + 23, 690, y + 23, proto)
    b += box(694, y, 206, 46, ct, cs)
b += head(694, 72, "CLIENTS")
svg(n, 910, 400, "Sources feed one engine; the engine feeds every link, gated per link by Sharing; each link speaks its own protocol to its clients.", b)

# ---------- 2. One sensor, several readers ----------
n = "readers"
b = []
b += box(20, 104, 140, 56, "Accelerometer", "up to 400 Hz")


def ticks(x1, x2, y, step, accent=False):
    cls = "dg-tick dg-accent" if accent else "dg-tick"
    out, x = [], x1 + step / 2
    while x < x2:
        out.append(f'<line x1="{x:.1f}" y1="{y - 6}" x2="{x:.1f}" y2="{y + 6}" class="{cls}"/>')
        x += step
    return out


b += [f'<line x1="160" y1="132" x2="336" y2="132" class="dg-arrow" marker-end="url(#a-{n})"/>']
b += ticks(166, 326, 132, 5)
b += ['<text x="248" y="116" class="dg-label" text-anchor="middle">200 Hz: 2 × the fastest reader</text>']
b += [f'<rect x="340" y="88" width="160" height="88" rx="12" class="dg-box"/>',
      '<text x="420" y="124" class="dg-title" text-anchor="middle">SensorHub</text>',
      '<text x="420" y="142" class="dg-sub" text-anchor="middle">+ a Decimator</text>',
      '<text x="420" y="157" class="dg-sub" text-anchor="middle">per reader</text>']
readers = [(40, "Python", "100 Hz", 10), (132, "Board over USB", "50 Hz", 20), (224, "Sensors screen", "10 Hz", 100)]
for y, t, s, step in readers:
    b += [f'<polyline points="500,132 530,{y} 726,{y}" class="dg-arrow" marker-end="url(#a-{n})"/>']
    b += ticks(540, 716, y, step, accent=True)
    b += box(730, y - 24, 160, 48, t, s)
b += ['<text x="628" y="20" class="dg-label" text-anchor="middle">each gets its own rate, on a schedule</text>']
svg(n, 900, 262, "One accelerometer runs once at 200 Hz; the SensorHub gives Python 100 Hz, a USB board 50 Hz and the Sensors screen 10 Hz.", b)

# ---------- 3. Names ----------
n = "names"
b = []
b += box(20, 92, 230, 56, "sensors/2/bosch/mag/n/0", "stable ID · never changes", cls="dg-inner")
b += arrow(n, 250, 120, 326, 120, "you name it", lx=288, ly=110)
b += [f'<rect x="330" y="92" width="130" height="56" rx="10" class="dg-box dg-box-accent"/>',
      '<text x="395" y="117" class="dg-title" text-anchor="middle">mag_left</text>',
      '<text x="395" y="133" class="dg-sub" text-anchor="middle">your name</text>']
outs = [(20, "allsense.rover.sensors.mag_left", "WebSocket, Python"), (76, "/allsense/rover/sensors/mag_left", "ROS 2"),
        (132, "allsense/rover/sensors/mag_left", "MQTT"), (188, "stream 3", "USB, BLE: the board numbers it")]
for y, t, s in outs:
    b += [f'<polyline points="460,120 490,{y + 22} 526,{y + 22}" class="dg-arrow" marker-end="url(#a-{n})"/>']
    b += [f'<rect x="530" y="{y}" width="330" height="44" rx="10" class="dg-box"/>',
          f'<text x="544" y="{y + 20}" class="dg-mono">{t}</text>',
          f'<text x="544" y="{y + 36}" class="dg-sub">{s}</text>']
svg(n, 870, 244, "A stable hardware ID gets your name, mag_left; each link writes it its own way.", b)

# ---------- 4. Clock sync ----------
n = "clock"
b = []
b += ['<text x="20" y="54" class="dg-title">Your computer</text>', '<text x="20" y="164" class="dg-title">Phone</text>',
      f'<line x1="140" y1="50" x2="700" y2="50" class="dg-axis" marker-end="url(#a-{n})"/>',
      f'<line x1="140" y1="160" x2="700" y2="160" class="dg-axis" marker-end="url(#a-{n})"/>']
for x, y, t, ty in [(200, 50, "t0", 34), (330, 160, "t1", 182), (380, 160, "t2", 182), (510, 50, "t3", 34)]:
    b += [f'<circle cx="{x}" cy="{y}" r="4" class="dg-dot"/>',
          f'<text x="{x}" y="{ty}" class="dg-mono" text-anchor="middle">{t}</text>']
b += [f'<line x1="200" y1="54" x2="326" y2="156" class="dg-arrow dg-accent" marker-end="url(#a-{n}-o)"/>',
      '<text x="250" y="118" class="dg-label" text-anchor="end">ping</text>',
      f'<line x1="380" y1="156" x2="506" y2="54" class="dg-arrow dg-accent" marker-end="url(#a-{n}-o)"/>',
      '<text x="460" y="118" class="dg-label">pong: t1, t2</text>',
      '<text x="545" y="96" class="dg-label">offset = ((t1−t0) + (t2−t3)) / 2</text>',
      '<text x="545" y="114" class="dg-label">round trip = (t3−t0) − (t2−t1)</text>']
svg(n, 790, 200, "The client pings the phone and gets the phone's receive and send times back; from four timestamps it works out the clock offset and the round trip.", b)
print("ok")
