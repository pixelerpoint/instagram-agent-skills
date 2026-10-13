#!/usr/bin/env python3
"""warmnode renderer - the 'espresso & chai' look.

The owner's own café / coffee / food photos become the background, graded warm and dark,
with cream serif text, a chai-amber accent line and an optional café label.

  python3 warmnode.py carousel spec.json out_dir/      -> slide_01.jpg ... (1080x1350)
  python3 warmnode.py story    spec.json out_dir/      -> story_01.jpg ...  (1080x1920)
  python3 warmnode.py reel     spec.json out.mp4       -> 1080x1920 MP4, silent track (add music in Instagram)

spec.json
{
  "media_dir": "/path/to/photos_and_videos",      # optional, prefix for relative paths
  "handle": "@warmnode",                          # optional
  "slides" | "frames" | "segments": [
     {"photo": "IMG.jpg", "title": "...", "body": "...", "place": "Polo Lounge · Lahore",
      "y": 0.05, "x": 0.5, "zoom": 1.0, "dim": 0.72},                  # carousel slide
     {"photo": "IMG.jpg", "text": "...", "y": 0.0, "zoom": 1.0},          # story frame
     {"video": "CLIP.mp4", "start": 1.0, "secs": 2.8, "text": "...", "big": true},   # reel segment
     {"photo": "IMG.jpg", "secs": 3.0, "text": "..."}                     # reel segment (slow push-in)
  ]
}
- "photo" may be omitted: the slide then uses a plain espresso background.
- "y" = where the crop window sits vertically (0 top .. 1 bottom). Snapchat exports have a
  location sticker near the bottom; the default 0.05 keeps it out of a 4:5 crop.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance

CREAM = (244, 235, 221)
AMBER = (224, 161, 90)
MUTED = (200, 186, 168)
ESPRESSO = (21, 16, 12)

SERIF_BOLD = [("/usr/share/fonts/opentype/noto/NotoSerifCJK-SemiBold.ttc", 0),
              ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 0),
              ("DejaVuSerif-Bold.ttf", 0), ("Georgia Bold.ttf", 0)]
SERIF_REG = [("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc", 0),
             ("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 0),
             ("DejaVuSerif.ttf", 0), ("Georgia.ttf", 0)]
SANS = [("/usr/share/fonts/opentype/inter/Inter-Medium.otf", 0),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 0), ("DejaVuSans.ttf", 0), ("Arial.ttf", 0)]


def _font(cands, size):
    for p, i in cands:
        try:
            return ImageFont.truetype(p, size, index=i)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


serif = lambda size, bold=True: _font(SERIF_BOLD if bold else SERIF_REG, size)
sans = lambda size: _font(SANS, size)


def load(path):
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def cover(im, W, H, y=0.05, x=0.5, zoom=1.0):
    iw, ih = im.size
    s = max(W / iw, H / ih) * zoom
    im = im.resize((int(iw * s + .5), int(ih * s + .5)), Image.LANCZOS)
    iw, ih = im.size
    left = int((iw - W) * x)
    top = int((ih - H) * min(max(y, 0), 1)) if ih > H else 0
    return im.crop((left, top, left + W, top + H))


def grade(im, dim=0.72):
    im = ImageEnhance.Brightness(im).enhance(dim)
    im = ImageEnhance.Color(im).enhance(0.85)
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.05)))
    b = b.point(lambda v: int(v * 0.9))
    return Image.merge("RGB", (r, g, b))


def shade(W, H, start=0.3, max_a=248, bottom=True):
    col = Image.new("L", (1, H))
    for yy in range(H):
        t = yy / H if bottom else 1 - yy / H
        col.putpixel((0, yy), 0 if t < start else int(max_a * ((t - start) / (1 - start)) ** 1.3))
    over = Image.new("RGBA", (W, H), ESPRESSO + (0,))
    over.putalpha(col.resize((W, H)))
    return over


def wrap(d, text, f, mw):
    out = []
    for para in text.split("\n"):
        if not para.strip():
            out.append(""); continue
        cur = ""
        for w in para.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) <= mw:
                cur = t
            else:
                out.append(cur); cur = w
        out.append(cur)
    return out


def background(spec, W, H, media_dir, default_y=0.05, dim=0.72):
    if spec.get("photo"):
        p = spec["photo"]
        p = p if os.path.isabs(p) else os.path.join(media_dir, p)
        im = grade(cover(load(p), W, H, y=spec.get("y", default_y), x=spec.get("x", .5),
                         zoom=spec.get("zoom", 1.0)), dim=spec.get("dim", dim))
    else:
        im = Image.new("RGB", (W, H), ESPRESSO)
    return im.convert("RGBA")


def text_block(d, x, y_bottom, mw, title, body, tsize, bsize, max_h):
    while True:
        ft, fb = serif(tsize, True), serif(bsize, False)
        tl = wrap(d, title, ft, mw) if title else []
        bl = wrap(d, body, fb, mw) if body else []
        th, bh = int(tsize * 1.22), int(bsize * 1.5)
        gap = int(bsize * .9) if tl and bl else 0
        h = len(tl) * th + gap + len(bl) * bh
        if h <= max_h or tsize < 40:
            break
        tsize -= 4; bsize = max(30, bsize - 2)
    y = top = y_bottom - h
    for ln in tl:
        d.text((x, y), ln, font=ft, fill=CREAM); y += th
    y += gap
    for ln in bl:
        d.text((x, y), ln, font=fb, fill=MUTED if tl else CREAM); y += bh
    return top


def render_slide(s, i, n, media_dir, handle, W=1080, H=1350):
    im = background(s, W, H, media_dir)
    im.alpha_composite(shade(W, H, start=s.get("grad", .25)))
    if s.get("place"):
        im.alpha_composite(shade(W, 260, start=0, max_a=170, bottom=False), (0, 0))
    d = ImageDraw.Draw(im)
    M = 92
    first = i == 0
    top = text_block(d, M, H - 150, W - 2 * M, s.get("title", ""), s.get("body", ""),
                     96 if first else 62, 44 if first else 40, int(H * .52))
    d.rectangle([M, top - 44, M + 64, top - 38], fill=AMBER)
    f = sans(28)
    d.text((M, H - 96), handle, font=f, fill=MUTED)
    right = "swipe  →" if first else f"{i + 1}/{n}"
    d.text((W - M - d.textlength(right, font=f), H - 96), right, font=f, fill=AMBER if first else MUTED)
    if s.get("place"):
        d.text((M, 84), s["place"].upper(), font=sans(30), fill=AMBER)
    return im.convert("RGB")


def render_story(s, media_dir, handle, W=1080, H=1920):
    im = background(s, W, H, media_dir, default_y=0.0, dim=0.62)
    im.alpha_composite(shade(W, H, start=0, max_a=200, bottom=False))
    d = ImageDraw.Draw(im)
    M = 96
    f = serif(84)
    y = 330
    d.rectangle([M, y - 50, M + 64, y - 44], fill=AMBER)
    for ln in wrap(d, s["text"], f, W - 2 * M):
        d.text((M, y), ln, font=f, fill=CREAM); y += 104
    d.text((M, H - 230), handle, font=sans(32), fill=MUTED)
    # keep the middle-lower area clear: the poll / question sticker goes there in the app
    return im.convert("RGB")


def _reel_overlay(text, path, handle, big, W=1080, H=1920):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    im.alpha_composite(shade(W, H, start=.3, max_a=225))
    d = ImageDraw.Draw(im)
    M, size = 96, (84 if big else 66)
    f = serif(size)
    lines = wrap(d, text, f, W - 2 * M)
    lh = int(size * 1.3)
    y = H - 430 - lh * len(lines)
    d.rectangle([M, y - 50, M + 64, y - 44], fill=AMBER)
    for ln in lines:
        d.text((M, y), ln, font=f, fill=CREAM); y += lh
    d.text((M, H - 300), handle, font=sans(32), fill=MUTED)
    im.save(path)


def render_reel(segments, out, media_dir, handle, fps=30):
    tmp = tempfile.mkdtemp()
    parts = []
    for k, s in enumerate(segments):
        secs = float(s.get("secs", 2.8))
        ov = os.path.join(tmp, f"o{k}.png")
        _reel_overlay(s.get("text", ""), ov, handle, s.get("big", False))
        seg = os.path.join(tmp, f"s{k}.mp4")
        fade = f"fade=in:st=0:d=0.25,fade=out:st={secs - .25}:d=0.25"
        if s.get("video"):
            v = s["video"] if os.path.isabs(s["video"]) else os.path.join(media_dir, s["video"])
            src = ["-ss", str(s.get("start", 0)), "-t", str(secs), "-i", v]
            base = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=brightness=-0.06:saturation=0.85"
        else:
            bg = os.path.join(tmp, f"b{k}.jpg")
            background(s, 1296, 2304, media_dir, default_y=0.0, dim=0.8).convert("RGB").save(bg, quality=95)
            src = ["-loop", "1", "-t", str(secs), "-i", bg]
            fr = int(secs * fps)
            base = (f"scale=1296:2304,zoompan=z='1+0.06*on/{fr}':x='iw/2-(iw/zoom/2)':"
                    f"y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={fps}")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *src, "-loop", "1", "-t", str(secs), "-i", ov,
                        "-filter_complex", f"[0:v]{base},fps={fps},setsar=1[b];[b][1:v]overlay=0:0,{fade},format=yuv420p[v]",
                        "-map", "[v]", "-r", str(fps), "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-an", seg],
                       check=True)
        parts.append(f"file '{seg}'")
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("\n".join(parts))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                    "-c:v", "copy", "-c:a", "aac", "-movflags", "+faststart", out], check=True)


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ("carousel", "story", "reel"):
        sys.exit(__doc__)
    kind, spec_path, out = sys.argv[1:]
    spec = json.load(open(spec_path))
    md = spec.get("media_dir", os.path.dirname(os.path.abspath(spec_path)))
    handle = spec.get("handle", "@warmnode")
    if kind == "carousel":
        os.makedirs(out, exist_ok=True)
        sl = spec["slides"]
        for i, s in enumerate(sl):
            render_slide(s, i, len(sl), md, handle).save(os.path.join(out, f"slide_{i + 1:02d}.jpg"), quality=94)
    elif kind == "story":
        os.makedirs(out, exist_ok=True)
        for i, s in enumerate(spec["frames"]):
            render_story(s, md, handle).save(os.path.join(out, s.get("name", f"story_{i + 1:02d}") + ".jpg"), quality=94)
    else:
        render_reel(spec["segments"], out, md, handle)
    print("done:", out)


if __name__ == "__main__":
    main()
