"""Two-minute long-slide film.

Ayzel, Moiz, Lina, Rafi, and Mama climb the stairs and ride the chute
one at a time. Motion is interpolated every frame. Voices, when the
wavs exist, play while that character is talking or sliding.
"""

import json
import math
import subprocess
import sys
from pathlib import Path

import sprite_io as sheets

HERE = Path(__file__).resolve().parent
SPRITES = HERE / "sprites"
OUT = HERE / "renders" / "long-slide.mp4"
AUDIO = HERE / "audio"
W, H = 1280, 720
FPS = 24
NAMES = ["ayzel", "moiz", "lina", "rafi", "mama"]
HEIGHT = {"ayzel": 190, "moiz": 190, "lina": 190, "rafi": 190, "mama": 220}
GROUND = 652
HORIZON = 500

# i = 0 is the bottom tread. Feet stand on y.
TREADS = [(118 + i * 8 + 70, 630 - i * 43) for i in range(11)]
SLIDE_PTS = [(248, 196), (430, 248), (690, 214), (900, 300), (820, 450), (690, 608)]
INTRO_X = [300, 450, 600, 750, 920]
QUEUE_X = [250, 360, 470, 580, 690]
POOL_X = [860, 960, 1060, 1160, 1248]

INTRO_LINES = [
    ("ayzel-look", "ayzel", 1.7),
    ("moiz-high", "moiz", 1.5),
    ("mama-one", "mama", 3.2),
    ("lina-hold", "lina", 1.4),
    ("rafi-fast", "rafi", 1.5),
]
AGAIN_LINES = [("mama-again", "mama", 1.6), ("ayzel-again", "ayzel", 1.3)]
MORE_LINES = [("mama-more", "mama", 1.4), ("ayzel-more", "ayzel", 1.2)]
END_LINES = [
    ("mama-longest", "mama", 2.8),
    ("ayzel-fast", "ayzel", 1.5),
    ("moiz-too", "moiz", 1.1),
    ("lina-tight", "lina", 1.5),
    ("rafi-tomorrow", "rafi", 1.5),
    ("mama-yes", "mama", 1.8),
]


def durations() -> dict[str, float]:
    path = AUDIO / "durations.json"
    if path.exists():
        return {key: float(value) for key, value in json.loads(path.read_text()).items()}
    return {}


def line_len(key: str, fallback: float, heard: dict[str, float]) -> float:
    # A short tail keeps the next action from clipping the last word.
    return max(0.7, heard.get(key, fallback)) + 0.2


def smoothstep(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def slide_path(count: int = 240) -> list[tuple[float, float]]:
    points = []
    for i in range(count):
        t = i / (count - 1)
        segment = t * (len(SLIDE_PTS) - 1)
        index = min(int(segment), len(SLIDE_PTS) - 2)
        local = segment - index
        x0, y0 = SLIDE_PTS[index]
        x1, y1 = SLIDE_PTS[index + 1]
        points.append((x0 + (x1 - x0) * local, y0 + (y1 - y0) * local))
    return points


PATH = slide_path()
ARC = [0.0]
for (x0, y0), (x1, y1) in zip(PATH, PATH[1:]):
    ARC.append(ARC[-1] + math.hypot(x1 - x0, y1 - y0))
ARC_LEN = ARC[-1]


def point_at(u: float) -> tuple[float, float]:
    u = max(0.0, min(1.0, u))
    dist = u * ARC_LEN
    index = 0
    while index < len(ARC) - 2 and ARC[index + 1] < dist:
        index += 1
    span = ARC[index + 1] - ARC[index] or 1
    local = (dist - ARC[index]) / span
    x0, y0 = PATH[index]
    x1, y1 = PATH[index + 1]
    return (lerp(x0, x1, local), lerp(y0, y1, local))


def climb_pos(u: float) -> tuple[float, float]:
    u = smoothstep(u)
    span = (len(TREADS) - 1) * u
    index = min(int(span), len(TREADS) - 2)
    local = smoothstep(span - index)
    x0, y0 = TREADS[index]
    x1, y1 = TREADS[index + 1]
    return (lerp(x0, x1, local), lerp(y0, y1, local))


def seat_drop(name: str) -> float:
    """Feet below the chute line, so the lap sits down inside it."""
    return HEIGHT[name] * 0.20


def build(heard: dict[str, float]):
    segs = {name: [] for name in NAMES}
    cues = []
    markers = []
    pos = {name: (INTRO_X[i] - 520, GROUND) for i, name in enumerate(NAMES)}

    def add(name, t0, t1, kind, **payload):
        if t1 <= t0:
            t1 = t0 + 0.04
        segs[name].append({"t0": t0, "t1": t1, "kind": kind, **payload})

    def hold(t0, t1, action="front", talk=None, where=None):
        for name in NAMES:
            x, y = (where or pos)[name]
            if name == talk:
                add(name, t0, t1, "talk", action="talking", x=x, y=y)
            else:
                add(name, t0, t1, "still", action=action, x=x, y=y)

    def move_all(t, targets, speed, action="walk"):
        own = {}
        for name in NAMES:
            x1, y1 = targets[name]
            own[name] = math.hypot(x1 - pos[name][0], y1 - pos[name][1]) / speed
        dur = max(own.values()) if own else 0
        for name in NAMES:
            x0, y0 = pos[name]
            x1, y1 = targets[name]
            add(name, t, t + own[name], "move", action=action, x0=x0, y0=y0, x1=x1, y1=y1, mirror=x1 < x0 - 1)
            if own[name] < dur:
                arrived = "back" if action == "back" else "front"
                add(name, t + own[name], t + dur, "still", action=arrived, x=x1, y=y1)
            pos[name] = (x1, y1)
        return t + dur

    t = 0.0
    markers.append(("walk", t))
    t = move_all(t, {name: (INTRO_X[i], GROUND) for i, name in enumerate(NAMES)}, 104)
    for key, speaker, fallback in INTRO_LINES:
        dur = line_len(key, fallback, heard)
        markers.append((key, t))
        cues.append((t, key))
        hold(t, t + dur, talk=speaker)
        t += dur

    markers.append(("queue", t))
    t = move_all(t, {name: (QUEUE_X[i], GROUND) for i, name in enumerate(NAMES)}, 160, action="walk")
    # Face the stairs while they wait.
    for name in NAMES:
        pos[name] = (QUEUE_X[NAMES.index(name)], GROUND)

    def round_trip(t, climb_for, slide_for, say_turn, speed_label):
        markers.append((speed_label, t))
        for index, name in enumerate(NAMES):
            if say_turn:
                key = f"{name}-turn"
                dur = line_len(key, 1.05, heard)
                markers.append((key, t))
                cues.append((t, key))
                hold(t, t + dur, action="back", talk=name)
                t += dur
            climb_t = t
            if index == 0:
                markers.append((f"{speed_label}-climb", climb_t + climb_for * 0.45))
            for other in NAMES:
                if other == name:
                    add(name, climb_t, climb_t + climb_for, "climb")
                else:
                    x, y = pos[other]
                    add(other, climb_t, climb_t + climb_for, "still", action="back" if other in NAMES[index + 1 :] else "front", x=x, y=y)
            t += climb_for
            settle = 0.28
            cx, cy = climb_pos(1)
            sx, sy = point_at(0)
            sy += seat_drop(name)
            for other in NAMES:
                if other == name:
                    add(name, t, t + settle, "move", action="sitting", x0=cx, y0=cy, x1=sx, y1=sy, mirror=False)
                else:
                    x, y = pos[other]
                    waiting = other in NAMES[index + 1 :]
                    add(other, t, t + settle, "still", action="back" if waiting else "front", x=x, y=y)
            t += settle
            markers.append((f"{name}-slide", t))
            slide_key = f"{name}-slide"
            slide_dur = max(slide_for, line_len(slide_key, slide_for, heard))
            cues.append((t, slide_key))
            for other in NAMES:
                if other == name:
                    add(name, t, t + slide_dur, "slide")
                else:
                    x, y = pos[other]
                    waiting = other in NAMES[index + 1 :]
                    add(other, t, t + slide_dur, "still", action="back" if waiting else "front", x=x, y=y)
            t += slide_dur
            land_for = 0.55
            exit_x, exit_y = point_at(1)
            exit_y += seat_drop(name)
            slot = (POOL_X[index], GROUND)
            for other in NAMES:
                if other == name:
                    add(name, t, t + land_for, "move", action="walk", x0=exit_x, y0=max(exit_y, GROUND - 8), x1=slot[0], y1=slot[1], mirror=False)
                else:
                    x, y = pos[other]
                    add(other, t, t + land_for, "still", action="back" if other in NAMES[index + 1 :] else "front", x=x, y=y)
            pos[name] = slot
            t += land_for
            for other in NAMES:
                x, y = pos[other]
                waiting = other in NAMES[index + 1 :]
                add(other, t, t + 0.24, "still", action="back" if waiting else "front", x=x, y=y)
            t += 0.24
        return t

    t = round_trip(t, 2.30, 1.55, True, "round1")
    for key, speaker, fallback in AGAIN_LINES:
        dur = line_len(key, fallback, heard)
        markers.append((key, t))
        cues.append((t, key))
        hold(t, t + dur, talk=speaker)
        t += dur
    markers.append(("back1", t))
    t = move_all(t, {name: (QUEUE_X[i], GROUND) for i, name in enumerate(NAMES)}, 190)
    t = round_trip(t, 1.85, 1.30, True, "round2")
    for key, speaker, fallback in MORE_LINES:
        dur = line_len(key, fallback, heard)
        markers.append((key, t))
        cues.append((t, key))
        hold(t, t + dur, talk=speaker)
        t += dur
    markers.append(("back2", t))
    t = move_all(t, {name: (QUEUE_X[i], GROUND) for i, name in enumerate(NAMES)}, 200)
    t = round_trip(t, 1.60, 1.15, False, "round3")
    for key, speaker, fallback in END_LINES:
        dur = line_len(key, fallback, heard)
        markers.append((key, t))
        cues.append((t, key))
        hold(t, t + dur, talk=speaker)
        t += dur
    end = t + 3.5
    markers.append(("bounce", t))
    hold(t, end, action="front")
    for name in NAMES:
        segs[name][-1]["bounce"] = True
    return segs, cues, markers, end


def pose(segs, name: str, t: float):
    chosen = segs[name][0]
    for seg in segs[name]:
        if t < seg["t0"]:
            break
        chosen = seg
        if t < seg["t1"]:
            break
    kind = chosen["kind"]
    local = 0 if chosen["t1"] == chosen["t0"] else (t - chosen["t0"]) / (chosen["t1"] - chosen["t0"])
    local = max(0.0, min(1.0, local))
    mirror = False
    if kind == "move":
        u = smoothstep(local)
        x = lerp(chosen["x0"], chosen["x1"], u)
        y = lerp(chosen["y0"], chosen["y1"], u)
        action = chosen["action"]
        mirror = chosen.get("mirror", False)
        frame = int(t * 6.5) % 4
    elif kind == "climb":
        x, y = climb_pos(local)
        action = "back"
        frame = int(t * 8) % 4
    elif kind == "slide":
        # Accelerate down the chute, seat locked to the path.
        u = local ** 1.45
        x, y = point_at(u)
        y += seat_drop(name)
        action = "sitting"
        frame = int(t * 8) % 4
    else:
        x, y = chosen["x"], chosen["y"]
        action = chosen["action"]
        frame = int((t - chosen["t0"]) * 6) % 4 if kind == "talk" else 0
        if chosen.get("bounce"):
            y -= abs(math.sin((t - chosen["t0"]) * 6.5)) * 14
            frame = 1 if abs(math.sin((t - chosen["t0"]) * 6.5)) > 0.55 else 0
        else:
            y += math.sin(t * 3.2 + GROUND) * 1.4
    return action, frame % 4, x, y, mirror, kind == "slide"


def strip_rules(sw: int, sh: int, src: bytes) -> tuple[int, int, bytes]:
    """Drop a solid black rule left on the edge of a keyed cell."""
    buf = bytearray(src)
    for x in list(range(min(4, sw))) + list(range(max(0, sw - 4), sw)):
        dark = opaque = 0
        for y in range(sh):
            i = (y * sw + x) * 4
            if buf[i + 3] < 16:
                continue
            opaque += 1
            if buf[i] < 45 and buf[i + 1] < 45 and buf[i + 2] < 45:
                dark += 1
        if opaque > sh * 0.35 and dark > opaque * 0.75:
            for y in range(sh):
                buf[(y * sw + x) * 4 + 3] = 0
    return sw, sh, bytes(buf)


def load_frames(name: str, action: str):
    filename = "walk" if action == "walk" else action
    frames = []
    for width, height, buf in sheets.load_sheet_cells(SPRITES / f"{name}-{filename}.png"):
        sheets.tidy(buf, width, height)
        frames.append(strip_rules(*sheets.scale_cell(buf, width, height, HEIGHT[name])))
    print(name, action, flush=True)
    return frames


def disc(canvas, cx, cy, rx, ry, color, y_min=None, y_max=None) -> None:
    cx, cy, rx, ry = int(cx), int(cy), int(rx), int(ry)
    if rx < 1 or ry < 1:
        return
    shade = bytes(color)
    for y in range(max(0, cy - ry), min(H, cy + ry + 1)):
        if y_min is not None and y < y_min:
            continue
        if y_max is not None and y > y_max:
            continue
        dy = (y - cy) / ry
        span = int(rx * (1 - dy * dy) ** 0.5)
        row = y * W * 3
        for x in range(max(0, cx - span), min(W, cx + span + 1)):
            i = row + x * 3
            canvas[i : i + 3] = shade


def frond(canvas, x, y, dx, dy, droop, color) -> None:
    for i in range(9):
        u = i / 8
        cx = x + dx * u
        cy = y + dy * u + droop * u * u
        radius = int(lerp(8, 2, u))
        disc(canvas, cx, cy, radius + 7, max(3, radius), color)


def palm(canvas, x, ground, height, lean) -> None:
    crown_x = x + lean
    crown_y = ground - height
    for y in range(int(crown_y), int(ground)):
        u = (y - crown_y) / max(1, height)
        half = int(lerp(7, 15, u))
        cx = int(lerp(crown_x, x, u))
        row = y * W * 3
        tone = b"\x8a\x5a\x32" if (y // 7) % 2 else b"\xa0\x6c\x3c"
        for px in range(max(0, cx - half), min(W, cx + half)):
            canvas[row + px * 3 : row + px * 3 + 3] = tone
    leaf = (36, 140, 68)
    leaf2 = (58, 168, 84)
    for ang, droop, color in (
        (-70, 36, leaf), (-40, 18, leaf2), (-15, 8, leaf),
        (15, 8, leaf2), (40, 18, leaf), (70, 36, leaf),
        (-55, 28, leaf2), (55, 28, leaf),
    ):
        rad = math.radians(ang)
        frond(canvas, crown_x, crown_y, math.cos(rad) * 78, math.sin(rad) * 18 - 8, droop, color)
    disc(canvas, crown_x, crown_y + 2, 8, 8, (122, 78, 42))


def paint_slide(canvas) -> None:
    for x, y in PATH:
        disc(canvas, x, y + 18, 54, 36, (30, 136, 194))
        disc(canvas, x, y + 6, 38, 14, (148, 220, 246))


def background() -> bytearray:
    canvas = bytearray(W * H * 3)
    for y in range(H):
        if y < HORIZON:
            u = y / HORIZON
            color = (int(148 + 48 * u), int(206 + 26 * u), 255)
        else:
            color = (118, 196, 92)
        shade = bytes(color)
        row = y * W * 3
        for x in range(0, W * 3, 3):
            canvas[row + x : row + x + 3] = shade
    disc(canvas, 1080, 92, 54, 54, (255, 214, 96))
    palm(canvas, 46, HORIZON + 6, 300, -12)
    palm(canvas, 980, HORIZON + 18, 220, 8)
    palm(canvas, 1148, HORIZON + 4, 290, -8)
    palm(canvas, 1252, HORIZON + 10, 250, 10)
    for i in range(len(TREADS)):
        cx, top = TREADS[i]
        left = int(cx - 74)
        for y in range(int(top), min(H, int(top) + 34)):
            row = y * W * 3
            tone = b"\xff\xdc\x86" if y < top + 6 else b"\xf0\xc2\x58"
            for x in range(max(0, left), min(W, left + 148)):
                canvas[row + x * 3 : row + x * 3 + 3] = tone
    paint_slide(canvas)
    disc(canvas, 760, 648, 170, 46, (78, 188, 220))
    return canvas


def blit(canvas, sprite, foot_x, foot_y, mirror=False) -> None:
    sw, sh, src = sprite
    left = int(foot_x - sw / 2)
    top = int(foot_y - sh)
    for y in range(sh):
        dy = top + y
        if dy < 0 or dy >= H:
            continue
        row = dy * W * 3
        for x in range(sw):
            dx = left + x
            if dx < 0 or dx >= W:
                continue
            sx = sw - 1 - x if mirror else x
            i = (y * sw + sx) * 4
            a = src[i + 3]
            if a < 16:
                continue
            j = row + dx * 3
            sa = a / 255
            canvas[j] = int(src[i] * sa + canvas[j] * (1 - sa))
            canvas[j + 1] = int(src[i + 1] * sa + canvas[j + 1] * (1 - sa))
            canvas[j + 2] = int(src[i + 2] * sa + canvas[j + 2] * (1 - sa))


def shadow(canvas, x, y) -> None:
    disc(canvas, x, y - 6, 26, 8, (96, 168, 74))


def render_frame(base, bank, segs, t):
    canvas = bytearray(base)
    items = []
    for name in NAMES:
        action, frame, x, y, mirror, sliding = pose(segs, name, t)
        items.append((y, name, action, frame, x, mirror, sliding))
    rider = None
    for foot_y, name, action, frame, x, mirror, sliding in sorted(items):
        if not sliding:
            shadow(canvas, x, foot_y)
        blit(canvas, bank[name][action][frame], x, foot_y, mirror)
        if sliding:
            rider = (x, foot_y - seat_drop(name))
    if rider:
        rx, path_y = rider
        y0 = int(path_y + 12)
        y1 = int(path_y + 56)
        x0 = int(rx - 58)
        x1 = int(rx + 58)
        for y in range(max(0, y0), min(H, y1)):
            row = y * W * 3
            for px in range(max(0, x0), min(W, x1)):
                i = row + px * 3
                r, g, b = base[i], base[i + 1], base[i + 2]
                if r < 90 and g > 90 and b > 150:
                    canvas[i : i + 3] = base[i : i + 3]
    return canvas


def probe(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        text=True,
    )
    return float(out.strip())


def fit_wav(src: Path, dest: Path, limit: float) -> None:
    dur = probe(src)
    if dur <= limit + 0.02:
        if src != dest:
            dest.write_bytes(src.read_bytes())
        return
    tempo = min(2.4, dur / max(0.35, limit))
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(src), "-af", f"atempo={tempo:.4f}", str(dest)],
        check=True,
    )


def mix_audio(cues, video: Path) -> None:
    present = []
    fit_dir = AUDIO / "fit"
    fit_dir.mkdir(parents=True, exist_ok=True)
    times = [t for t, key in cues if (AUDIO / f"{key}.wav").exists()]
    for index, (t, key) in enumerate(cues):
        src = AUDIO / f"{key}.wav"
        if not src.exists():
            continue
        later = [stamp for stamp in times if stamp > t + 0.05]
        limit = (min(later) - t - 0.08) if later else 4.0
        dest = fit_dir / f"{index:02d}-{key}.wav"
        fit_wav(src, dest, max(0.45, limit))
        present.append((t, dest))
    if not present:
        return
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(video)]
    for _, path in present:
        cmd.extend(["-i", str(path)])
    filters = []
    labels = []
    for index, (t, _) in enumerate(present, start=1):
        delay = int(round(t * 1000))
        filters.append(f"[{index}:a]adelay={delay}|{delay},volume=1.4[a{index}]")
        labels.append(f"[a{index}]")
    filters.append("".join(labels) + f"amix=inputs={len(labels)}:duration=longest:normalize=0:dropout_transition=0[a]")
    voiced = video.with_name(video.stem + "-voiced.mp4")
    cmd.extend([
        "-filter_complex", ";".join(filters),
        "-map", "0:v", "-map", "[a]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
        str(voiced),
    ])
    subprocess.run(cmd, check=True)
    voiced.replace(video)


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "mux":
        saved = json.loads((AUDIO / "cues.json").read_text())
        mix_audio([(item["t"], item["key"]) for item in saved], OUT)
        print(OUT, flush=True)
        return
    heard = durations()
    segs, cues, markers, end = build(heard)
    print(f"story {end:.2f}s  cues {len(cues)}", flush=True)
    for label, stamp in markers:
        print(f"  {stamp:6.2f}  {label}", flush=True)
    bank = {
        name: {action: load_frames(name, action) for action in ("walk", "front", "talking", "back", "sitting")}
        for name in NAMES
    }
    base = background()
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        frames = HERE / "frames"
        frames.mkdir(parents=True, exist_ok=True)
        wanted = {"walk", "queue", "round1-climb", "ayzel-slide", "mama-slide", "bounce"}
        for label, stamp in markers:
            if label not in wanted:
                continue
            canvas = render_frame(base, bank, segs, stamp + (0.1 if "climb" in label else 0.55))
            path = frames / f"{label}.png"
            subprocess.run(
                ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-i", "-", "-frames:v", "1", "-update", "1", str(path)],
                input=bytes(canvas),
                check=True,
            )
            print(path, flush=True)
        return
    frames = int(round(end * FPS))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    encode = subprocess.Popen(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
            "-i", "-",
            "-frames:v", str(frames),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an",
            str(OUT),
        ],
        stdin=subprocess.PIPE,
    )
    assert encode.stdin is not None
    for frame in range(frames):
        canvas = render_frame(base, bank, segs, frame / FPS)
        encode.stdin.write(bytes(canvas))
        if frame % 240 == 0:
            print(f"frame {frame}/{frames}", flush=True)
    encode.stdin.close()
    if encode.wait() != 0:
        raise SystemExit("ffmpeg failed")
    (HERE / "audio").mkdir(parents=True, exist_ok=True)
    (AUDIO / "cues.json").write_text(json.dumps([{"t": t, "key": key} for t, key in cues], indent=2))
    mix_audio(cues, OUT)
    print(OUT, flush=True)


if __name__ == "__main__":
    main()
