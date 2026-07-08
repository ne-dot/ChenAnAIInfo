from __future__ import annotations

import math
import os
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path("/Users/zj/Documents/AI 自媒体")
BG_PATH = ROOT / "assets/backgrounds/ai-research-lab-dark-bg.png"
OUT_DIR = ROOT / "renders/segment-01"
FRAME_DIR = OUT_DIR / "frames"
OUTPUT = OUT_DIR / "segment-01-opening.mp4"
POSTER = OUT_DIR / "segment-01-poster.png"

W, H = 1920, 1080
FPS = 30
DURATION = 16
TOTAL = FPS * DURATION

FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size=size)


def clamp(v: float, a: float = 0.0, b: float = 1.0) -> float:
    return max(a, min(b, v))


def ease(v: float) -> float:
    x = clamp(v)
    return 1 - (1 - x) ** 3


def mix(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def alpha(c: tuple[int, int, int], a: float) -> tuple[int, int, int, int]:
    return (*c, int(255 * clamp(a)))


def composite(base: Image.Image, layer: Image.Image, opacity: float = 1.0) -> None:
    if opacity < 1:
        layer = layer.copy()
        layer.putalpha(layer.getchannel("A").point(lambda p: int(p * opacity)))
    base.alpha_composite(layer)


def text_center(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, fnt, fill, anchor="mm") -> None:
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def glow_line(layer: Image.Image, pts: list[tuple[float, float]], color=(54, 184, 255), width=3, glow=16, opacity=0.6) -> None:
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    gd.line(pts, fill=alpha(color, opacity * 0.55), width=width + glow, joint="curve")
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(glow / 2))
    layer.alpha_composite(glow_layer)
    d = ImageDraw.Draw(layer)
    d.line(pts, fill=alpha(color, opacity), width=width, joint="curve")


def rounded_path(layer: Image.Image, box: tuple[int, int, int, int], radius: int, progress: float) -> None:
    # For the prototype, draw a rounded rectangle as the burden loop.
    if progress <= 0:
        return
    x1, y1, x2, y2 = box
    temp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(temp)
    for w, a in [(24, 0.15), (10, 0.25)]:
        d.rounded_rectangle(box, radius=radius, outline=alpha((170, 220, 255), a * progress), width=w)
    d.rounded_rectangle(box, radius=radius, outline=alpha((238, 248, 255), 0.78 * progress), width=4)
    layer.alpha_composite(temp.filter(ImageFilter.GaussianBlur(1)))


def draw_panel(layer: Image.Image, rect: tuple[int, int, int, int], label: str, p: float, color=(94, 231, 255)) -> None:
    if p <= 0:
        return
    x1, y1, x2, y2 = rect
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    s = mix(0.9, 1.0 + 0.012 * math.sin(p * 8), ease(p))
    w, h = (x2 - x1) * s, (y2 - y1) * s
    rr = (int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2))

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rounded_rectangle(rr, radius=24, fill=alpha((54, 184, 255), 0.14 * p))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    layer.alpha_composite(glow)

    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(rr, radius=24, fill=(8, 24, 48, int(190 * p)), outline=alpha(color, 0.56 * p), width=2)
    # Minimal outline icon: a small tech circle plus line, intentionally generic.
    icon_x = rr[0] + 35
    icon_y = int(cy)
    d.ellipse((icon_x - 13, icon_y - 13, icon_x + 13, icon_y + 13), outline=alpha(color, 0.9 * p), width=3)
    d.line((icon_x + 18, icon_y, icon_x + 42, icon_y), fill=alpha(color, 0.7 * p), width=3)
    d.text((rr[0] + 72, cy), label, font=font(34, True), fill=alpha((245, 250, 255), 0.96 * p), anchor="lm")


def draw_burden_label(layer: Image.Image, rect: tuple[int, int, int, int], label: str, p: float) -> None:
    if p <= 0:
        return
    x1, y1, x2, y2 = rect
    y = y1 + int(8 * (1 - ease(p)))
    r = (x1, y, x2, y + (y2 - y1))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(r, radius=22, fill=(4, 13, 30, int(190 * p)), outline=alpha((214, 236, 255), 0.36 * p), width=2)
    text_center(d, ((r[0] + r[2]) / 2, (r[1] + r[3]) / 2 - 2), label, font(32, True), alpha((245, 250, 255), 0.92 * p))


def fit_background(t: float) -> Image.Image:
    bg = Image.open(BG_PATH).convert("RGBA").resize((W, H), Image.Resampling.LANCZOS)
    # Gentle push-in by cropping an increasingly smaller region.
    z = mix(1.0, 1.045, ease(t / DURATION))
    cw, ch = int(W / z), int(H / z)
    left = (W - cw) // 2
    top = (H - ch) // 2 + int(mix(0, 10, ease(t / DURATION)))
    bg = bg.crop((left, top, left + cw, top + ch)).resize((W, H), Image.Resampling.LANCZOS)

    shade = Image.new("RGBA", (W, H), (0, 6, 18, 112))
    bg.alpha_composite(shade)

    vignette = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse((-120, -80, W + 120, H + 120), fill=170)
    vignette = Image.eval(vignette.filter(ImageFilter.GaussianBlur(130)), lambda p: 255 - p)
    dark = Image.new("RGBA", (W, H), (0, 4, 14, 160))
    bg.alpha_composite(Image.composite(dark, Image.new("RGBA", (W, H), (0, 0, 0, 0)), vignette))
    return bg


def draw_frame(i: int) -> Image.Image:
    t = i / FPS
    img = fit_background(t)

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    brand_p = ease((t - 0.1) / 0.8)
    d.text((88, 76), "AI RESEARCH LAB", font=font(26, True), fill=alpha((196, 231, 255), 0.72 * brand_p))

    matrix_p = clamp((t - 0.2) / 1.2) * clamp((14.2 - t) / 1.2)
    if matrix_p > 0:
        cx, cy = 960, 518
        for r, a, w in [(250, 0.2, 2), (180, 0.14, 2), (112, 0.16, 2)]:
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=alpha((112, 202, 255), a * matrix_p), width=w)
        for angle in range(0, 360, 45):
            rad = math.radians(angle + t * 6)
            d.line((cx, cy, cx + math.cos(rad) * 250, cy + math.sin(rad) * 250), fill=alpha((94, 231, 255), 0.08 * matrix_p), width=2)

    task_p = clamp((t - 0.55) / 1.0) * clamp((14.0 - t) / 1.0)
    if task_p > 0:
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse((845, 403, 1075, 633), fill=alpha((54, 184, 255), 0.24 * task_p))
        glow = glow.filter(ImageFilter.GaussianBlur(30))
        layer.alpha_composite(glow)
        d.ellipse((845, 403, 1075, 633), fill=(10, 31, 63, int(186 * task_p)), outline=alpha((137, 221, 255), 0.58 * task_p), width=2)
        text_center(d, (960, 488), "用户任务", font(28), alpha((205, 225, 255), 0.74 * task_p))
        text_center(d, (960, 538), "完成工作", font(44, True), alpha((245, 250, 255), 0.96 * task_p))

    nodes = [
        ("写作", (458, 250, 642, 328), 1.2, "path1"),
        ("摘要", (1276, 248, 1460, 326), 1.65, "path2"),
        ("修图", (320, 534, 504, 612), 2.1, "path3"),
        ("客服", (1418, 532, 1602, 610), 2.55, "path4"),
        ("代码", (864, 742, 1048, 820), 3.0, "path5"),
    ]
    for label, rect, delay, _ in nodes:
        p = clamp((t - delay) / 0.75) * clamp((10.5 - t) / 1.7)
        draw_panel(layer, rect, label, p)

    path_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    paths = [
        ([(642, 289), (824, 289), (824, 489), (845, 489)], 1.65),
        ([(1276, 287), (1096, 287), (1096, 489), (1075, 489)], 2.1),
        ([(504, 573), (706, 573), (706, 449), (845, 449)], 2.55),
        ([(1418, 571), (1214, 571), (1214, 449), (1075, 449)], 3.0),
        ([(956, 742), (956, 606)], 3.45),
    ]
    for pts, delay in paths:
        p = clamp((t - delay) / 0.9) * clamp((10.5 - t) / 1.4)
        if p > 0:
            # Approximate path reveal by drawing only the first p fraction of segments.
            reveal = []
            remaining = p * sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
            reveal.append(pts[0])
            for a, b in zip(pts, pts[1:]):
                seg = math.dist(a, b)
                if remaining >= seg:
                    reveal.append(b)
                    remaining -= seg
                else:
                    ratio = remaining / seg if seg else 0
                    reveal.append((mix(a[0], b[0], ratio), mix(a[1], b[1], ratio)))
                    break
            if len(reveal) > 1:
                glow_line(path_layer, reveal, opacity=0.58 * p)
    layer.alpha_composite(path_layer)

    headline_p = clamp((t - 3.7) / 0.9) * clamp((9.1 - t) / 1.0)
    if headline_p > 0:
        text_center(d, (960, 86), "AI 功能越来越多", font(58, True), alpha((248, 252, 255), 0.96 * headline_p))
        text_center(d, (960, 156), "为什么你还是累？", font(58, True), alpha((94, 231, 255), 0.96 * headline_p))

    ring_p = clamp((t - 8.2) / 1.25) * clamp((13.4 - t) / 0.8)
    rounded_path(layer, (724, 322, 1196, 658), 66, ring_p)
    labels = [
        ("找入口", (690, 282, 846, 346), 8.7),
        ("选工具", (1046, 282, 1202, 346), 9.0),
        ("排步骤", (1044, 596, 1200, 660), 9.3),
        ("检查结果", (684, 596, 872, 660), 9.6),
    ]
    for label, rect, delay in labels:
        p = clamp((t - delay) / 0.6) * clamp((13.4 - t) / 0.8)
        draw_burden_label(layer, rect, label, p)

    caption_p = clamp((t - 10.6) / 0.8) * clamp((13.8 - t) / 0.7)
    if caption_p > 0:
        d.rounded_rectangle((110, 948, 706, 1012), radius=22, fill=(5, 15, 34, int(164 * caption_p)), outline=alpha((118, 206, 255), 0.25 * caption_p), width=2)
        d.text((134, 980), "很多 AI 功能，只是把某一步变快了", font=font(28, True), fill=alpha((218, 237, 255), 0.72 * caption_p), anchor="lm")

    question_p = ease((t - 13.0) / 0.85)
    if question_p > 0:
        overlay = Image.new("RGBA", (W, H), (0, 5, 14, int(108 * question_p)))
        img.alpha_composite(overlay)
        q = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        qd = ImageDraw.Draw(q)
        rect = (580, 398, 1340, 626)
        qd.rounded_rectangle(rect, radius=32, fill=(3, 12, 28, int(218 * question_p)), outline=alpha((125, 211, 255), 0.44 * question_p), width=2)
        text_center(qd, (960, 466), "真正的问题是", font(34, True), alpha((180, 219, 255), 0.76 * question_p))
        text_center(qd, (960, 546), "工作还在谁身上？", font(68, True), alpha((255, 255, 255), 0.98 * question_p))
        glow = q.filter(ImageFilter.GaussianBlur(18))
        img.alpha_composite(glow)
        layer.alpha_composite(q)

    img.alpha_composite(layer)
    return img.convert("RGB")


def main() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    FRAME_DIR.mkdir(parents=True, exist_ok=True)

    for i in range(TOTAL):
        frame = draw_frame(i)
        frame.save(FRAME_DIR / f"frame-{i:05d}.jpg", quality=94)
        if i == 390:
            frame.save(POSTER)
        if i % 60 == 0:
            print(f"rendered {i}/{TOTAL}")

    cmd = [
        "ffmpeg",
        "-y",
        "-framerate",
        str(FPS),
        "-i",
        str(FRAME_DIR / "frame-%05d.jpg"),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-profile:v",
        "high",
        "-crf",
        "18",
        "-movflags",
        "+faststart",
        str(OUTPUT),
    ]
    subprocess.run(cmd, check=True)
    print(OUTPUT)


if __name__ == "__main__":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    main()
