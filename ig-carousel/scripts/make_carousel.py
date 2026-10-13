#!/usr/bin/env python3
"""Render Instagram carousel slides (1080x1350) in the @warmnode style.

Usage: python3 make_carousel.py slides.json out_dir/
slides.json: {"slides": [{"title": "optional", "body": "text"}, ...], "handle": "@warmnode"}
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
MARGIN = 110
BG = (243, 234, 224)        # warm cream
INK = (43, 33, 24)          # coffee brown
ACCENT = (200, 105, 58)     # terracotta
MUTED = (140, 120, 104)

SERIF_BOLD = ["DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf", "Georgia Bold.ttf"]
SERIF = ["DejaVuSerif.ttf", "LiberationSerif-Regular.ttf", "Georgia.ttf"]
SANS = ["DejaVuSans.ttf", "LiberationSans-Regular.ttf", "Arial.ttf"]
FONT_DIRS = ["/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/truetype/liberation",
             "/usr/share/fonts/truetype", "/Library/Fonts", "C:/Windows/Fonts", ""]


def font(names, size):
    for d in FONT_DIRS:
        for n in names:
            p = os.path.join(d, n) if d else n
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default(size=size)


def wrap(draw, text, f, max_w):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        if not words:
            lines.append("")
            continue
        for w in words:
            test = (cur + " " + w).strip()
            if draw.textlength(test, font=f) <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def fit(draw, text, names, start, min_size, max_w, max_h, spacing=1.35):
    size = start
    while size >= min_size:
        f = font(names, size)
        lines = wrap(draw, text, f, max_w)
        h = len(lines) * size * spacing
        if h <= max_h:
            return f, lines, size
        size -= 4
    f = font(names, min_size)
    return f, wrap(draw, text, f, max_w), min_size


def draw_block(draw, lines, f, size, y, color, spacing=1.35):
    for line in lines:
        draw.text((MARGIN, y), line, font=f, fill=color)
        y += size * spacing
    return y


def render(slide, idx, total, handle, path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    max_w = W - 2 * MARGIN
    title = (slide.get("title") or "").strip()
    body = (slide.get("body") or "").strip()
    cover = idx == 1

    # accent bar
    d.rectangle([MARGIN, 150, MARGIN + 90, 160], fill=ACCENT)

    blocks = []
    if title:
        tf, tl, ts = fit(d, title, SERIF_BOLD, 104 if cover else 76, 44, max_w, 620 if cover else 380, 1.2)
        blocks.append((tl, tf, ts, INK, 1.2))
    if body:
        bf, bl, bs = fit(d, body, SERIF, 52 if title else 64, 32, max_w, 760 if not title else 560)
        blocks.append((bl, bf, bs, INK if not title else MUTED if cover else INK, 1.35))

    total_h = sum(len(l) * s * sp for l, _, s, _, sp in blocks) + (50 if len(blocks) == 2 else 0)
    y = max(230, (H - total_h) / 2 - 20)
    for i, (l, f, s, c, sp) in enumerate(blocks):
        y = draw_block(d, l, f, s, y, c, sp)
        if i == 0 and len(blocks) == 2:
            y += 50

    small = font(SANS, 30)
    d.text((MARGIN, H - 130), handle, font=small, fill=MUTED)
    tag = "swipe  \u2192" if cover else f"{idx}/{total}"
    tw = d.textlength(tag, font=small)
    d.text((W - MARGIN - tw, H - 130), tag, font=small, fill=ACCENT if cover else MUTED)
    img.save(path, "PNG")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as fh:
        data = json.load(fh)
    slides = data["slides"]
    handle = data.get("handle", "@warmnode")
    os.makedirs(sys.argv[2], exist_ok=True)
    for i, s in enumerate(slides, 1):
        out = os.path.join(sys.argv[2], f"slide_{i:02d}.png")
        render(s, i, len(slides), handle, out)
        print(out)


if __name__ == "__main__":
    main()
