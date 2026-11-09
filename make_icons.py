"""Generate PWA icons: a football next to "Aa" on a dark pitch-green background.
Usage: python make_icons.py   (requires Pillow)
"""
import math
from PIL import Image, ImageDraw, ImageFont

BG = (13, 59, 39)          # #0d3b27
STRIPE = (17, 72, 47)
LINE = (255, 255, 255)
FONT = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"
S = 1024  # master size, downscaled for crisp edges


def pentagon(cx, cy, r, rot=-90):
    return [(cx + r * math.cos(math.radians(rot + i * 72)),
             cy + r * math.sin(math.radians(rot + i * 72))) for i in range(5)]


def ball(d, cx, cy, R):
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(250, 250, 250), outline=(20, 20, 20), width=int(R * 0.05))
    pr = R * 0.36
    center = pentagon(cx, cy, pr)
    d.polygon(center, fill=(25, 25, 25))
    for i, (px, py) in enumerate(center):
        ang = math.radians(-90 + i * 72)
        x2, y2 = cx + R * 0.68 * math.cos(ang), cy + R * 0.68 * math.sin(ang)
        d.line([(px, py), (x2, y2)], fill=(25, 25, 25), width=int(R * 0.05))
        # outer patch
        ox, oy = cx + R * 0.88 * math.cos(ang), cy + R * 0.88 * math.sin(ang)
        patch = pentagon(ox, oy, R * 0.17, rot=-90 + i * 72 + 180)
        d.polygon(patch, fill=(25, 25, 25))


def master():
    img = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(img)
    # pitch stripes
    for i in range(0, S, 128):
        if (i // 128) % 2 == 0:
            d.rectangle([i, 0, i + 127, S], fill=STRIPE)
    # centre circle line (decorative)
    d.ellipse([S * .1, S * .1, S * .9, S * .9], outline=(255, 255, 255, 40), width=0)
    # ball (left-center) and text, kept inside the maskable safe zone (~80%)
    ball(d, S * 0.33, S * 0.5, S * 0.19)
    f = ImageFont.truetype(FONT, int(S * 0.36))
    d.text((S * 0.72, S * 0.5), "Aa", font=f, fill=(255, 214, 10), anchor="mm")
    return img


m = master()
for name, size in [("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)]:
    m.resize((size, size), Image.LANCZOS).save(name, optimize=True)
    print("wrote", name)
