"""Load a 4-cell sprite sheet and knock out a magenta backdrop.

Pink clothes stay opaque. Only pixels that are strongly magenta
(red and blue high, green low) become transparent.
"""

import subprocess
from pathlib import Path


def dims(path: Path) -> tuple[int, int]:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(path),
        ],
        text=True,
    )
    width, height = out.strip().split("x")
    return int(width), int(height)


def load_sheet_cells(path: Path) -> list[tuple[int, int, bytearray]]:
    width, height = dims(path)
    cell = width // 4
    key = (
        "format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
        "a='if(gt(r(X,Y),200)*lt(g(X,Y),100)*gt(b(X,Y),200),0,255)'"
    )
    cells = []
    for index in range(4):
        raw = subprocess.run(
            [
                "ffmpeg", "-v", "error", "-i", str(path),
                "-vf", f"crop={cell}:{height}:{index * cell}:0,{key}",
                "-f", "rawvideo", "-pix_fmt", "rgba", "-",
            ],
            capture_output=True,
            check=True,
        ).stdout
        buf = bytearray(raw)
        if len(buf) != cell * height * 4:
            raise SystemExit(f"bad cell {path} {index}")
        cells.append((cell, height, buf))
    return cells


def tidy(buf: bytearray, width: int, height: int) -> None:
    seen = bytearray(width * height)
    stack = [(x, 0) for x in range(width)] + [(x, height - 1) for x in range(width)]
    stack += [(0, y) for y in range(height)] + [(width - 1, y) for y in range(height)]
    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= width or y >= height:
            continue
        pixel = y * width + x
        if seen[pixel]:
            continue
        seen[pixel] = 1
        i = pixel * 4
        if not (buf[i + 3] > 10 and buf[i] > 246 and buf[i + 1] > 246 and buf[i + 2] > 246):
            continue
        buf[i + 3] = 0
        stack.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    for y in range(max(0, height - 40), height):
        dark = 0
        for x in range(width):
            i = (y * width + x) * 4
            r, g, b, a = buf[i], buf[i + 1], buf[i + 2], buf[i + 3]
            if a > 40 and r < 180 and g < 110 and b < 180:
                dark += 1
        if dark > width * 0.85:
            for x in range(width):
                i = (y * width + x) * 4
                r, g, b, a = buf[i], buf[i + 1], buf[i + 2], buf[i + 3]
                if a > 40 and r < 180 and g < 110 and b < 180:
                    buf[i + 3] = 0
    seen = bytearray(width * height)
    keep = bytearray(width * height)
    for y in range(height):
        for x in range(width):
            pixel = y * width + x
            if seen[pixel] or buf[pixel * 4 + 3] < 40:
                continue
            comp = []
            stack = [(x, y)]
            seen[pixel] = 1
            while stack:
                cx, cy = stack.pop()
                comp.append(cy * width + cx)
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if nx < 0 or ny < 0 or nx >= width or ny >= height:
                        continue
                    nxt = ny * width + nx
                    if seen[nxt] or buf[nxt * 4 + 3] < 40:
                        continue
                    seen[nxt] = 1
                    stack.append((nx, ny))
            if len(comp) >= 1800:
                for item in comp:
                    keep[item] = 1
    for pixel in range(width * height):
        if not keep[pixel]:
            buf[pixel * 4 + 3] = 0


def scale_cell(buf: bytearray, width: int, height: int, target_h: int) -> tuple[int, int, bytes]:
    x0, y0, x1, y1 = _bbox(buf, width, height)
    src_h = max(1, y1 - y0)
    scale = target_h / src_h
    dw = max(1, int(round((x1 - x0 + 1) * scale)))
    dh = max(1, int(round(src_h * scale)))
    out = bytearray(dw * dh * 4)

    def sample(x: int, y: int) -> tuple[int, int, int, int]:
        if x < 0 or y < 0 or x >= width or y >= height:
            return 0, 0, 0, 0
        i = (y * width + x) * 4
        return buf[i], buf[i + 1], buf[i + 2], buf[i + 3]

    for dy in range(dh):
        sy = y0 + dy / scale
        y_i = int(sy)
        fy = sy - y_i
        for dx in range(dw):
            sx = x0 + dx / scale
            x_i = int(sx)
            fx = sx - x_i
            acc = [0.0, 0.0, 0.0, 0.0]
            for oy, wy in ((0, 1 - fy), (1, fy)):
                for ox, wx in ((0, 1 - fx), (1, fx)):
                    r, g, b, a = sample(x_i + ox, y_i + oy)
                    weight = wx * wy * (a / 255)
                    acc[0] += r * weight
                    acc[1] += g * weight
                    acc[2] += b * weight
                    acc[3] += weight
            if acc[3] < 0.08:
                continue
            i = (dy * dw + dx) * 4
            out[i] = min(255, int(acc[0] / acc[3]))
            out[i + 1] = min(255, int(acc[1] / acc[3]))
            out[i + 2] = min(255, int(acc[2] / acc[3]))
            out[i + 3] = min(255, int(acc[3] * 255))
    return dw, dh, bytes(out)


def _bbox(buf: bytearray, width: int, height: int) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = width, height, -1, -1
    for y in range(height):
        row = y * width * 4
        for x in range(width):
            if buf[row + x * 4 + 3] > 40:
                x0 = min(x0, x)
                x1 = max(x1, x)
                y0 = min(y0, y)
                y1 = max(y1, y)
    if x1 < 0:
        raise SystemExit("empty sprite")
    return x0, y0, x1, y1
