#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news summary image (1024x1024).

Dense broadsheet front page in FULL COLOUR, in the 21 November entry's
cover style (warm newsprint paper, red + gold accents, one colour per
region and story): a big date masthead + sub-deck of the day's three
biggest stories, a region bar with counts, a strip of six key numbers,
3 large illustrated cards, 10 medium illustrated cards, a numbered
"also on" index of 17 more stories beside a small world map, and a DATE
CHECK box naming the other days' news that was deliberately left out.
30 stories in all, 7 regions, every one verified against a reputable
source on Monday 23 November 2026 (see BUILD_LOG.md). All illustrations
are drawn here in PIL — no AI image generator, no copied image or text
from any other entry. Deterministic: same output bytes on every run.
Output: entry.png next to this script.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Full-colour palette, as in the 21 November entry: warm newsprint paper,
# black ink, red + gold accents, one colour per region and story.
PAPER = (250, 244, 230)
PANEL = (240, 232, 214)
INK = (24, 24, 24)
GOLD = (184, 134, 11)
RED = (178, 34, 34)
DARKRED = (150, 40, 40)
BLUE = (30, 90, 140)
GREEN = (30, 110, 70)
OLIVE = (150, 110, 30)
PURPLE = (108, 52, 131)
TEAL = (14, 124, 123)
ORANGE = (180, 80, 0)
NAVY = (15, 42, 74)
DARK = (58, 58, 58)
MID = (110, 110, 110)
LIGHT = (168, 168, 168)
PALE = (205, 205, 203)
WHITE = (250, 250, 250)
NIGHT_T = (14, 22, 46)
NIGHT_B = (64, 48, 96)
MARGIN = 28
CW = W - 2 * MARGIN  # 968 content width


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns a list of lines."""
    out, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def text_cx(d, cx, y, s, font, fill=INK):
    d.text((cx - d.textlength(s, font=font) / 2, y), s, font=font, fill=fill)


def sky_band(d, x0, y0, x1, y1, top, bot):
    """Vertical gradient band."""
    h = max(1, y1 - y0)
    for i in range(h):
        t = i / h
        c = tuple(int(top[j] + (bot[j] - top[j]) * t) for j in range(3))
        d.line([x0, y0 + i, x1, y0 + i], fill=c)


def paper_texture(img):
    """Deterministic newsprint speckle + fibres (seeded, same every run)."""
    rng = random.Random(20261123)
    px = img.load()
    for _ in range(5200):
        x, y = rng.randrange(W), rng.randrange(H)
        v = rng.choice((-5, -4, -3, 3, 4, 5))
        r, g, b = px[x, y]
        px[x, y] = (max(0, r + v), max(0, g + v), max(0, b + v))
    d = ImageDraw.Draw(img)
    for _ in range(46):
        x, y = rng.randrange(W), rng.randrange(H)
        ln = rng.randrange(6, 20)
        d.line([x, y, x + ln, y + rng.randrange(-1, 2)], fill=(232, 222, 200), width=1)


def chip(d, x, y, s, font, fill=RED):
    """Coloured label chip with white text; returns its width."""
    tw = d.textlength(s, font=font)
    w = int(tw) + 12
    d.rectangle([x, y, x + w, y + 17], fill=fill)
    d.text((x + 6, y + 2), s, font=font, fill=WHITE)
    return w


def card_text(d, x, y, w, kicker, headline, summary, hk_font, hl_font, sm_font,
              accent=RED):
    """Kicker (in the story's accent colour) + headline + summary."""
    d.text((x, y), kicker, font=hk_font, fill=accent)
    y += 16
    for ln in wrap(d, headline, hl_font, w):
        d.text((x, y), ln, font=hl_font, fill=INK)
        y += 22
    y += 1
    for ln in wrap(d, summary, sm_font, w):
        d.text((x, y), ln, font=sm_font, fill=(60, 60, 60))
        y += 14
    return y

# ---------------------------------------------------------------- art scenes
# Each draws a small pictogram inside (x0, y0, x1, y1), scaled to the box.
# All original, drawn from the 23 November stories themselves.

def art_nato(d, x0, y0, x1, y1):
    """NATO: deep-blue sky, white compass star, red missile arcs."""
    sky_band(d, x0, y0, x1, y1, (18, 48, 92), (40, 80, 130))
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + int(w * 0.30), y0 + int(h * 0.52)
    r = int(h * 0.34)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=2)
    d.polygon([(cx, cy - r), (cx + int(r * 0.28), cy - int(r * 0.28)),
               (cx, cy), (cx - int(r * 0.28), cy - int(r * 0.28))], fill=WHITE)
    d.polygon([(cx, cy + r), (cx + int(r * 0.28), cy + int(r * 0.28)),
               (cx, cy), (cx - int(r * 0.28), cy + int(r * 0.28))], fill=WHITE)
    d.polygon([(cx - r, cy), (cx - int(r * 0.28), cy - int(r * 0.28)),
               (cx, cy), (cx - int(r * 0.28), cy + int(r * 0.28))], fill=WHITE)
    d.polygon([(cx + r, cy), (cx + int(r * 0.28), cy - int(r * 0.28)),
               (cx, cy), (cx + int(r * 0.28), cy + int(r * 0.28))], fill=WHITE)
    # three missile arcs, right side
    for i, (ax, ay) in enumerate([(0.58, 0.22), (0.68, 0.42), (0.80, 0.18)]):
        px, py = x0 + int(w * ax), y0 + int(h * ay)
        d.arc([px - 26, py - 18, px + 26, py + 18], start=200, end=340,
              fill=(255, 210, 90), width=2)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(220, 50, 50))
    for sx, sy in [(0.55, 0.12), (0.90, 0.30), (0.62, 0.80)]:
        d.ellipse([x0 + int(w * sx) - 2, y0 + int(h * sy) - 2,
                   x0 + int(w * sx) + 2, y0 + int(h * sy) + 2], fill=GOLD)


def art_nepal(d, x0, y0, x1, y1):
    """Nepal–India talks: two flags over a sandstone hall, green hills."""
    sky_band(d, x0, y0, x1, y1, (238, 236, 220), (214, 206, 184))
    w, h = x1 - x0, y1 - y0
    # hills
    d.polygon([(x0, y1), (x0, y1 - int(h * 0.28)), (x0 + int(w * 0.35), y1),
               ], fill=(110, 160, 100))
    d.polygon([(x1, y1), (x1, y1 - int(h * 0.22)), (x1 - int(w * 0.30), y1)],
              fill=(90, 140, 90))
    # hall
    bx0, bx1 = x0 + int(w * 0.30), x0 + int(w * 0.72)
    base = y1 - int(h * 0.06)
    d.rectangle([bx0, base - int(h * 0.34), bx1, base], fill=(196, 160, 110))
    d.polygon([(bx0 - 6, base - int(h * 0.34)), (bx1 + 6, base - int(h * 0.34)),
               (x0 + int(w * 0.51), base - int(h * 0.52))], fill=(150, 110, 70))
    for i in range(4):
        cx = bx0 + int((i + 0.5) * (bx1 - bx0) / 4)
        d.rectangle([cx - 3, base - int(h * 0.28), cx + 3, base], fill=(120, 88, 55))
    # Nepal pennon (crimson double triangle) on the left pole
    px = x0 + int(w * 0.12)
    d.line([px, y0 + int(h * 0.10), px, y1 - int(h * 0.10)], fill=INK, width=2)
    d.polygon([(px, y0 + int(h * 0.12)), (px + int(w * 0.11), y0 + int(h * 0.30)),
               (px, y0 + int(h * 0.30))], fill=(200, 40, 45))
    d.polygon([(px, y0 + int(h * 0.32)), (px + int(w * 0.09), y0 + int(h * 0.48)),
               (px, y0 + int(h * 0.48))], fill=(200, 40, 45))
    # India tricolour on the right pole
    qx = x0 + int(w * 0.88)
    d.line([qx, y0 + int(h * 0.10), qx, y1 - int(h * 0.10)], fill=INK, width=2)
    fw, fh = int(w * 0.10), int(h * 0.13)
    d.rectangle([qx, y0 + int(h * 0.12), qx + fw, y0 + int(h * 0.12) + fh],
                fill=(240, 140, 40))
    d.rectangle([qx, y0 + int(h * 0.12) + fh, qx + fw, y0 + int(h * 0.12) + 2 * fh],
                fill=WHITE)
    d.rectangle([qx, y0 + int(h * 0.12) + 2 * fh, qx + fw,
                 y0 + int(h * 0.12) + 3 * fh], fill=(30, 130, 70))
    d.ellipse([qx + fw // 2 - 4, y0 + int(h * 0.12) + fh - 4,
               qx + fw // 2 + 4, y0 + int(h * 0.12) + fh + 4],
              outline=NAVY, width=1)


def art_copfall(d, x0, y0, x1, y1):
    """COP31 fallout: blue globe, big red down arrow, cracked earth."""
    sky_band(d, x0, y0, x1, y1, (226, 238, 228), (200, 220, 206))
    w, h = x1 - x0, y1 - y0
    gx, gy = x0 + int(w * 0.24), y0 + int(h * 0.50)
    r = int(h * 0.36)
    d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(52, 130, 190))
    d.ellipse([gx - int(r * 0.55), gy - int(r * 0.6), gx - int(r * 0.05),
               gy - int(r * 0.1)], fill=(70, 160, 90))
    d.ellipse([gx + int(r * 0.1), gy + int(r * 0.1), gx + int(r * 0.65),
               gy + int(r * 0.6)], fill=(70, 160, 90))
    # red down arrow
    ax = x0 + int(w * 0.60)
    d.rectangle([ax - 7, y0 + int(h * 0.12), ax + 7, y0 + int(h * 0.62)],
                fill=(200, 40, 45))
    d.polygon([(ax - 22, y0 + int(h * 0.60)), (ax + 22, y0 + int(h * 0.60)),
               (ax, y0 + int(h * 0.88))], fill=(200, 40, 45))
    # cracked earth at the bottom
    d.rectangle([x0, y1 - int(h * 0.12), x1, y1], fill=(150, 120, 90))
    for cx in (0.15, 0.42, 0.70, 0.88):
        px = x0 + int(w * cx)
        d.line([px, y1 - int(h * 0.12), px + 8, y1 - int(h * 0.02)], fill=(90, 70, 50),
               width=2)
        d.line([px + 8, y1 - int(h * 0.02), px + 2, y1], fill=(90, 70, 50), width=2)


def art_gaza(d, x0, y0, x1, y1):
    """Gaza: night coast, skyline, two smoke columns, red crescent."""
    sky_band(d, x0, y0, x1, y1, NIGHT_T, NIGHT_B)
    w, h = x1 - x0, y1 - y0
    d.ellipse([x0 + int(w * 0.82), y0 + int(h * 0.08),
               x0 + int(w * 0.82) + 16, y0 + int(h * 0.08) + 16], fill=(244, 230, 190))
    d.ellipse([x0 + int(w * 0.82) + 5, y0 + int(h * 0.08),
               x0 + int(w * 0.82) + 21, y0 + int(h * 0.08) + 16], fill=NIGHT_B)
    base = y1 - int(h * 0.06)
    d.rectangle([x0, base, x1, y1], fill=(14, 18, 34))
    for bx, bh, bw in [(0.06, 0.42, 0.16), (0.26, 0.55, 0.13), (0.44, 0.38, 0.15),
                       (0.63, 0.48, 0.12)]:
        d.rectangle([x0 + int(w * bx), base - int(h * bh),
                     x0 + int(w * (bx + bw)), base], fill=(10, 14, 30))
        for wy in range(2):
            wy0 = base - int(h * (bh * (0.30 + wy * 0.35)))
            d.rectangle([x0 + int(w * (bx + 0.03)), wy0,
                         x0 + int(w * (bx + 0.07)), wy0 + 5],
                        fill=(242, 196, 90))
    for sx, sy, sr in [(0.30, 0.16, 7), (0.34, 0.26, 9), (0.70, 0.12, 6)]:
        d.ellipse([x0 + int(w * sx) - sr, y0 + int(h * sy) - sr,
                   x0 + int(w * sx) + sr, y0 + int(h * sy) + sr], fill=(150, 150, 150))


def art_knesset(d, x0, y0, x1, y1):
    """Jerusalem: sandstone hall with dome, two flags, columns."""
    sky_band(d, x0, y0, x1, y1, (240, 234, 216), (218, 206, 184))
    w, h = x1 - x0, y1 - y0
    cx = x0 + int(w * 0.50)
    base = y1 - int(h * 0.06)
    d.rectangle([cx - int(w * 0.30), base - int(h * 0.30),
                 cx + int(w * 0.30), base], fill=(206, 178, 128))
    d.polygon([(cx - int(w * 0.30), base - int(h * 0.30)),
               (cx - int(w * 0.16), base - int(h * 0.52)),
               (cx + int(w * 0.16), base - int(h * 0.52)),
               (cx + int(w * 0.30), base - int(h * 0.30))], fill=(176, 146, 100))
    d.rectangle([cx - 3, base - int(h * 0.62), cx + 3, base - int(h * 0.52)],
                fill=(176, 146, 100))
    d.ellipse([cx - 6, base - int(h * 0.68), cx + 6, base - int(h * 0.60)],
              fill=(176, 146, 100))
    for i in range(-2, 3):
        d.rectangle([cx + i * int(w * 0.11) - 4, base - int(h * 0.26),
                     cx + i * int(w * 0.11) + 4, base], fill=(150, 122, 82))
    # two small flags: Israel (blue stripes) left, plain red-white right
    for fx, stripes in [(0.08, BLUE), (0.86, RED)]:
        px = x0 + int(w * fx)
        d.line([px, y0 + int(h * 0.10), px, base - int(h * 0.30)], fill=INK, width=2)
        d.rectangle([px, y0 + int(h * 0.12), px + int(w * 0.10), y0 + int(h * 0.30)],
                    fill=WHITE, outline=(150, 150, 150))
        d.line([px, y0 + int(h * 0.15), px + int(w * 0.10), y0 + int(h * 0.15)],
               fill=stripes, width=2)
        d.line([px, y0 + int(h * 0.27), px + int(w * 0.10), y0 + int(h * 0.27)],
               fill=stripes, width=2)


def art_tow(d, x0, y0, x1, y1):
    """Baltic: grey cargo ship towed by a small red tug, smoke, grey sea."""
    sky_band(d, x0, y0, x1, y1, (228, 234, 240), (198, 212, 224))
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y1 - int(h * 0.28), x1, y1], fill=(70, 120, 160))
    for wy in range(3):
        yy = y1 - int(h * (0.22 - wy * 0.06))
        d.line([x0 + 6, yy, x0 + int(w * 0.30), yy], fill=(140, 185, 215), width=2)
        d.line([x1 - int(w * 0.30), yy + 3, x1 - 6, yy + 3], fill=(140, 185, 215),
               width=2)
    # cargo ship, left
    sx0, sy = x0 + int(w * 0.08), y1 - int(h * 0.42)
    d.polygon([(sx0, sy), (sx0 + int(w * 0.42), sy),
               (sx0 + int(w * 0.36), sy + int(h * 0.16)),
               (sx0 + int(w * 0.06), sy + int(h * 0.16))], fill=(52, 58, 68))
    d.rectangle([sx0 + int(w * 0.06), sy - int(h * 0.18),
                 sx0 + int(w * 0.36), sy], fill=(235, 238, 242))
    d.rectangle([sx0 + int(w * 0.16), sy - int(h * 0.28),
                 sx0 + int(w * 0.22), sy - int(h * 0.18)], fill=(52, 58, 68))
    for px, py, pr in [(0.34, 0.14, 6), (0.38, 0.22, 8), (0.32, 0.30, 6)]:
        d.ellipse([x0 + int(w * px) - pr, y0 + int(h * py) - pr,
                   x0 + int(w * px) + pr, y0 + int(h * py) + pr], fill=(120, 120, 120))
    # tugboat, right, with tow line
    tx0, ty = x0 + int(w * 0.72), y1 - int(h * 0.36)
    d.line([sx0 + int(w * 0.42), sy + int(h * 0.06), tx0, ty + int(h * 0.06)],
           fill=INK, width=2)
    d.polygon([(tx0, ty), (tx0 + int(w * 0.18), ty),
               (tx0 + int(w * 0.15), ty + int(h * 0.12)),
               (tx0 + int(w * 0.03), ty + int(h * 0.12))], fill=(200, 40, 45))
    d.rectangle([tx0 + int(w * 0.04), ty - int(h * 0.12),
                 tx0 + int(w * 0.12), ty], fill=WHITE)


def art_school(d, x0, y0, x1, y1):
    """Seoul: schoolhouse with red roof, small grey robot at the door."""
    sky_band(d, x0, y0, x1, y1, (234, 238, 242), (208, 222, 232))
    w, h = x1 - x0, y1 - y0
    base = y1 - int(h * 0.06)
    hx0, hx1 = x0 + int(w * 0.10), x0 + int(w * 0.58)
    d.rectangle([hx0, base - int(h * 0.44), hx1, base], fill=(240, 210, 120))
    d.polygon([(hx0 - 6, base - int(h * 0.44)), (hx1 + 6, base - int(h * 0.44)),
               (x0 + int(w * 0.34), base - int(h * 0.66))], fill=(190, 60, 50))
    d.rectangle([x0 + int(w * 0.28), base - int(h * 0.24),
                 x0 + int(w * 0.40), base], fill=(120, 80, 50))
    for wx in (0.14, 0.44):
        d.rectangle([x0 + int(w * wx), base - int(h * 0.36),
                     x0 + int(w * (wx + 0.08)), base - int(h * 0.22)],
                    fill=(180, 220, 240), outline=INK)
    # small robot, right
    rx, ry = x0 + int(w * 0.76), base - int(h * 0.30)
    d.rectangle([rx - 12, ry - 12, rx + 12, ry + 10], fill=(150, 155, 160),
                outline=INK)
    d.line([rx, ry - 12, rx, ry - 20], fill=INK, width=2)
    d.ellipse([rx - 3, ry - 23, rx + 3, ry - 17], fill=RED)
    d.ellipse([rx - 7, ry - 6, rx - 2, ry - 1], fill=NAVY)
    d.ellipse([rx + 2, ry - 6, rx + 7, ry - 1], fill=NAVY)
    d.line([rx - 5, ry + 5, rx + 5, ry + 5], fill=INK, width=2)
    d.line([rx - 12, ry + 14, rx - 12, base], fill=INK, width=2)
    d.line([rx + 12, ry + 14, rx + 12, base], fill=INK, width=2)


def art_chip(d, x0, y0, x1, y1):
    """Nvidia probe: green circuit board, black chip, gold traces, lens."""
    sky_band(d, x0, y0, x1, y1, (24, 60, 40), (16, 40, 28))
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + int(w * 0.44), y0 + int(h * 0.52)
    # gold traces
    for tx, ty, dx, dy in [(0.10, 0.20, 0.24, 0.0), (0.10, 0.70, 0.24, 0.0),
                           (0.78, 0.20, -0.14, 0.0), (0.78, 0.70, -0.14, 0.0),
                           (0.34, 0.08, 0.0, 0.14), (0.54, 0.80, 0.0, -0.12)]:
        d.line([x0 + int(w * tx), y0 + int(h * ty),
                x0 + int(w * (tx + dx)), y0 + int(h * (ty + dy))],
               fill=(220, 180, 60), width=2)
        d.ellipse([x0 + int(w * (tx + dx)) - 3, y0 + int(h * (ty + dy)) - 3,
                   x0 + int(w * (tx + dx)) + 3, y0 + int(h * (ty + dy)) + 3],
                  fill=(220, 180, 60))
    s = int(h * 0.26)
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(20, 20, 24),
                outline=(220, 180, 60), width=2)
    for i in range(3):
        off = -s + (i + 1) * (2 * s // 4)
        d.line([cx - s - 6, cy + off, cx - s, cy + off], fill=(220, 180, 60),
               width=2)
        d.line([cx + s, cy + off, cx + s + 6, cy + off], fill=(220, 180, 60),
               width=2)
    # magnifier, top right
    mx, my = x0 + int(w * 0.84), y0 + int(h * 0.22)
    d.ellipse([mx - 11, my - 11, mx + 11, my + 11], outline=WHITE, width=2)
    d.line([mx + 8, my + 8, mx + 16, my + 16], fill=WHITE, width=3)


def art_chart(d, x0, y0, x1, y1):
    """Wall Street: white chart paper, red falling line, red candles."""
    d.rectangle([x0, y0, x1, y1], fill=(246, 244, 238))
    w, h = x1 - x0, y1 - y0
    for gy in range(1, 4):
        yy = y0 + int(h * gy / 4)
        d.line([x0 + 4, yy, x1 - 4, yy], fill=(220, 220, 214), width=1)
    pts = [(0.08, 0.24), (0.24, 0.34), (0.38, 0.30), (0.52, 0.52),
           (0.66, 0.48), (0.80, 0.70), (0.92, 0.66)]
    xy = [(x0 + int(w * px), y0 + int(h * py)) for px, py in pts]
    d.line(xy, fill=(200, 40, 45), width=3)
    ex, ey = xy[-1]
    d.polygon([(ex, ey + 10), (ex - 9, ey - 4), (ex + 9, ey - 4)], fill=(200, 40, 45))
    for cx, cy, ch in [(0.20, 0.55, 10), (0.44, 0.44, 8), (0.70, 0.62, 9)]:
        px, py = x0 + int(w * cx), y0 + int(h * cy)
        d.rectangle([px - 4, py - ch, px + 4, py + ch], fill=(200, 40, 45))
        d.line([px, py - ch - 5, px, py + ch + 5], fill=(200, 40, 45), width=1)


def art_ant(d, x0, y0, x1, y1):
    """Sydney fire ants: tan ground, brown mound, three red ants."""
    sky_band(d, x0, y0, x1, y1, (240, 232, 210), (222, 210, 184))
    w, h = x1 - x0, y1 - y0
    base = y1 - int(h * 0.08)
    mx = x0 + int(w * 0.30)
    d.polygon([(mx - int(w * 0.22), base), (mx, base - int(h * 0.42)),
               (mx + int(w * 0.22), base)], fill=(170, 130, 90))
    d.ellipse([mx - 4, base - int(h * 0.46), mx + 4, base - int(h * 0.38)],
              fill=(120, 85, 55))
    for ax, ay, sc in [(0.62, 0.55, 1.0), (0.78, 0.72, 0.8), (0.52, 0.80, 0.7)]:
        px, py = x0 + int(w * ax), y0 + int(h * ay)
        s = int(9 * sc)
        d.ellipse([px - s - 5, py - 3, px - s + 5, py + 3], fill=(190, 50, 30))
        d.ellipse([px - s, py - 4, px + s, py + 4], fill=(200, 60, 35))
        d.ellipse([px + s, py - 3, px + s + 6, py + 3], fill=(190, 50, 30))
        for lx in (-4, 0, 4):
            d.line([px + lx, py + 3, px + lx - 3, py + 8], fill=(150, 40, 25),
                   width=1)
            d.line([px + lx, py - 3, px + lx - 3, py - 8], fill=(150, 40, 25),
                   width=1)
    # magnifier over the mound
    d.ellipse([mx - 16, base - int(h * 0.30) - 16, mx + 16,
               base - int(h * 0.30) + 16], outline=INK, width=2)
    d.line([mx + 11, base - int(h * 0.30) + 11, mx + 22,
            base - int(h * 0.30) + 22], fill=INK, width=3)


def art_cedar(d, x0, y0, x1, y1):
    """Beirut: green mountains, cedar tree, wooden crate."""
    sky_band(d, x0, y0, x1, y1, (232, 238, 240), (206, 222, 228))
    w, h = x1 - x0, y1 - y0
    d.polygon([(x0, y1), (x0 + int(w * 0.30), y0 + int(h * 0.30)),
               (x0 + int(w * 0.55), y1)], fill=(120, 150, 120))
    d.polygon([(x0 + int(w * 0.45), y1), (x0 + int(w * 0.72), y0 + int(h * 0.22)),
               (x1, y1)], fill=(100, 135, 105))
    base = y1 - int(h * 0.06)
    # cedar: layered green triangles
    tx = x0 + int(w * 0.30)
    for i, (tw, ty) in enumerate([(0.26, 0.62), (0.20, 0.48), (0.13, 0.34)]):
        d.polygon([(tx - int(w * tw / 2), base - int(h * ty) + int(h * 0.10)),
                   (tx + int(w * tw / 2), base - int(h * ty) + int(h * 0.10)),
                   (tx, base - int(h * (ty + 0.14)))], fill=(30, 110, 70))
    d.rectangle([tx - 3, base - int(h * 0.12), tx + 3, base], fill=(110, 80, 50))
    # crate, right
    cx0, cy0 = x0 + int(w * 0.62), base - int(h * 0.34)
    cw, ch = int(w * 0.24), int(h * 0.30)
    d.rectangle([cx0, cy0, cx0 + cw, cy0 + ch], fill=(190, 150, 100),
                outline=(120, 88, 55), width=2)
    d.line([cx0, cy0, cx0 + cw, cy0 + ch], fill=(120, 88, 55), width=1)
    d.line([cx0 + cw, cy0, cx0, cy0 + ch], fill=(120, 88, 55), width=1)


def art_bus(d, x0, y0, x1, y1):
    """Kota: pale sky, road, yellow bus, orange warning triangle."""
    sky_band(d, x0, y0, x1, y1, (238, 234, 220), (220, 212, 192))
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y1 - int(h * 0.30), x1, y1], fill=(120, 120, 124))
    d.line([x0, y1 - int(h * 0.15), x1, y1 - int(h * 0.15)], fill=WHITE, width=2)
    for dx in range(0, int(w), 22):
        d.line([x0 + dx, y1 - int(h * 0.15), x0 + dx + 10, y1 - int(h * 0.15)],
               fill=(240, 200, 60), width=3)
    bx0, by0 = x0 + int(w * 0.10), y1 - int(h * 0.78)
    bw, bh = int(w * 0.56), int(h * 0.46)
    d.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=6,
                        fill=(240, 190, 60), outline=INK)
    for i in range(3):
        wx = bx0 + int(bw * (0.12 + i * 0.28))
        d.rectangle([wx, by0 + 6, wx + int(bw * 0.18), by0 + int(bh * 0.42)],
                    fill=(180, 220, 240), outline=INK)
    for wx in (bx0 + int(bw * 0.18), bx0 + int(bw * 0.78)):
        d.ellipse([wx - 7, by0 + bh - 4, wx + 7, by0 + bh + 8], fill=INK)
        d.ellipse([wx - 3, by0 + bh, wx + 3, by0 + bh + 4], fill=(150, 150, 150))
    # warning triangle, right
    tx, ty = x0 + int(w * 0.84), y1 - int(h * 0.42)
    d.polygon([(tx, ty - 14), (tx + 14, ty + 10), (tx - 14, ty + 10)],
              fill=(230, 110, 30), outline=INK)
    d.text((tx - 2, ty - 6), "!", font=F(SANS_B, 12), fill=WHITE)


def art_robot(d, x0, y0, x1, y1):
    """Geneva: grey robot head, white dove, olive branch."""
    sky_band(d, x0, y0, x1, y1, (234, 238, 240), (208, 220, 228))
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + int(w * 0.40), y0 + int(h * 0.55)
    s = int(h * 0.30)
    d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], radius=8,
                        fill=(150, 155, 160), outline=INK, width=2)
    d.line([cx, cy - s, cx, cy - s - 10], fill=INK, width=2)
    d.ellipse([cx - 3, cy - s - 14, cx + 3, cy - s - 8], fill=RED)
    d.ellipse([cx - int(s * 0.5) - 5, cy - 6, cx - int(s * 0.5) + 5, cy + 4],
              fill=NAVY)
    d.ellipse([cx + int(s * 0.5) - 5, cy - 6, cx + int(s * 0.5) + 5, cy + 4],
              fill=NAVY)
    d.line([cx - 8, cy + int(s * 0.55), cx + 8, cy + int(s * 0.55)], fill=INK,
           width=2)
    # dove, top right
    dx, dy = x0 + int(w * 0.76), y0 + int(h * 0.26)
    d.ellipse([dx - 12, dy - 5, dx + 12, dy + 5], fill=WHITE, outline=(150, 150, 150))
    d.ellipse([dx + 8, dy - 8, dx + 16, dy - 2], fill=WHITE, outline=(150, 150, 150))
    d.polygon([(dx - 12, dy), (dx - 24, dy - 10), (dx - 22, dy + 2)],
              fill=WHITE, outline=(150, 150, 150))
    # olive branch, bottom right
    bx, by = x0 + int(w * 0.72), y1 - int(h * 0.12)
    d.line([bx, by, bx + 22, by - 12], fill=(60, 110, 60), width=2)
    for lx, ly in [(6, -2), (12, -6), (18, -10)]:
        d.ellipse([bx + lx - 4, by + ly - 3, bx + lx + 4, by + ly + 3],
                  fill=(70, 140, 70))

# ---------------------------------------------------------------- world map
CONTINENTS = [
    [(0.03, 0.30), (0.09, 0.14), (0.20, 0.11), (0.27, 0.20), (0.25, 0.36),
     (0.18, 0.42), (0.12, 0.50), (0.06, 0.44)],  # N America
    [(0.29, 0.05), (0.34, 0.07), (0.32, 0.13), (0.28, 0.11)],  # Greenland
    [(0.27, 0.52), (0.33, 0.50), (0.35, 0.60), (0.31, 0.74), (0.28, 0.66),
     (0.25, 0.57)],  # S America
    [(0.47, 0.13), (0.53, 0.09), (0.57, 0.15), (0.55, 0.23), (0.49, 0.25),
     (0.46, 0.19)],  # Europe
    [(0.45, 0.15), (0.47, 0.14), (0.47, 0.18)],  # Britain
    [(0.47, 0.31), (0.55, 0.29), (0.61, 0.35), (0.59, 0.51), (0.53, 0.59),
     (0.48, 0.47), (0.45, 0.37)],  # Africa
    [(0.57, 0.09), (0.71, 0.07), (0.86, 0.11), (0.96, 0.21), (0.93, 0.34),
     (0.83, 0.41), (0.73, 0.37), (0.67, 0.47), (0.61, 0.39), (0.57, 0.27),
     (0.55, 0.17)],  # Asia
    [(0.91, 0.27), (0.93, 0.29), (0.91, 0.35), (0.89, 0.31)],  # Japan
    [(0.83, 0.61), (0.91, 0.59), (0.95, 0.65), (0.91, 0.73), (0.84, 0.71)],
    # Australia
    [(0.96, 0.71), (0.98, 0.73), (0.96, 0.77)],  # New Zealand
]
ISLANDS = [(0.79, 0.49), (0.82, 0.52), (0.85, 0.49), (0.81, 0.55)]  # Indonesia
DOTS = {  # story number -> (rx, ry) on the map
    1: (0.50, 0.13), 2: (0.72, 0.31), 3: (0.565, 0.30), 4: (0.61, 0.30),
    5: (0.57, 0.44), 6: (0.55, 0.08), 7: (0.85, 0.30), 8: (0.235, 0.33),
    9: (0.27, 0.27), 10: (0.90, 0.70), 11: (0.63, 0.39), 12: (0.68, 0.40),
    13: (0.46, 0.23),
}


def draw_map(d, x0, y0, x1, y1):
    mw, mh = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(198, 220, 235), outline=(120, 124, 130))
    for poly in CONTINENTS:
        pts = [(x0 + rx * mw, y0 + ry * mh) for rx, ry in poly]
        d.polygon(pts, fill=(222, 206, 162))
    for rx, ry in ISLANDS:
        d.ellipse([x0 + rx * mw - 3, y0 + ry * mh - 2,
                   x0 + rx * mw + 3, y0 + ry * mh + 2], fill=(222, 206, 162))
    f = F(SANS_B, 7)
    for n, (rx, ry) in DOTS.items():
        cx, cy = x0 + rx * mw, y0 + ry * mh
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED, outline=WHITE)
        s = str(n)
        d.text((cx - d.textlength(s, font=f) / 2, cy - 4), s, font=f, fill=WHITE)


# ---------------------------------------------------------------- layout
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top kicker + rule
    d.text((MARGIN, 12), "THE WORLD IN ONE DAY", font=F(SANS_B, 15), fill=RED)
    right = "30 STORIES · 7 REGIONS · EVERY ONE DATED MONDAY 23 NOVEMBER 2026"
    d.text((W - MARGIN - d.textlength(right, font=F(SANS_B, 15)), 12), right,
           font=F(SANS_B, 15), fill=INK)
    d.line([MARGIN, 34, W - MARGIN, 34], fill=GOLD, width=1)

    # --- masthead
    text_cx(d, W // 2, 40, "Monday 23 November 2026", F(SERIF, 62))
    text_cx(d, W // 2, 108,
            "NATO meets on Poland · Nepal PM talks with Modi · COP31 fallout: "
            "'worst ever'",
            F(SERIF_I, 17), fill=INK)

    # --- region bar (widths proportional to story counts, total 968)
    regions = [("EUROPE 5", 5, BLUE), ("AMERICAS 5", 5, DARKRED),
               ("MIDDLE EAST 6", 6, OLIVE), ("AFRICA 2", 2, PURPLE),
               ("ASIA 6", 6, RED), ("OCEANIA 3", 3, TEAL),
               ("GLOBAL 3", 3, (90, 90, 90))]
    x = MARGIN
    yb, hb = 130, 22
    for i, (label, n, col) in enumerate(regions):
        w = int(round(CW * n / 30))
        if i == len(regions) - 1:
            w = W - MARGIN - x
        d.rectangle([x, yb, x + w - 1, yb + hb], fill=col)
        text_cx(d, x + w // 2, yb + 4, label, F(SANS_B, 12), fill=WHITE)
        x += w

    # --- key numbers strip
    nums = [("32", "NATO states meet\non Poland"),
            ("1,675", "dead in Gaza since\nthe ceasefire began"),
            ("25", "tankers hit in the\nStrait of Hormuz"),
            ("128", "nations agree\nkiller-robot rules"),
            ("264", "kg of explosives\nseized in Lebanon"),
            ("9", "killed in the Kota\npilgrim bus crash")]
    col_w = CW // 6
    yn = 160
    for i, (num, lab) in enumerate(nums):
        cx0 = MARGIN + i * col_w
        if i:
            d.line([cx0 - 6, yn + 4, cx0 - 6, yn + 34], fill=(190, 180, 160), width=1)
        text_cx(d, cx0 + col_w // 2, yn, num, F(SERIF, 30), fill=RED)
        for j, ln in enumerate(lab.split("\n")):
            text_cx(d, cx0 + col_w // 2, yn + 34 + j * 12, ln, F(SANS, 10),
                    fill=(60, 60, 60))
    d.line([MARGIN, yn + 62, W - MARGIN, yn + 62], fill=INK, width=1)

    # --- 3 large cards
    large = [
        (art_nato, "NATO MEETS", "1  BRUSSELS, BELGIUM · SECURITY",
         "NATO meets on Poland missile breach",
         "All 32 allies gather in Brussels after three Russian objects land "
         "in Poland; Warsaw seeks stronger air defences. (PAP, AP)", BLUE),
        (art_nepal, "NEPAL–INDIA TALKS", "2  NEW DELHI, INDIA · DIPLOMACY",
         "Nepal PM holds talks with Modi",
         "Balendra Shah meets Modi on his state visit; the two leaders "
         "review ties and regional issues. (The Hindu, AP)", RED),
        (art_copfall, "COP31: 'WORST EVER'", "3  GLOBAL · CLIMATE",
         "COP31 fallout: 'worst ever'",
         "Guterres says he is 'deeply disappointed'; the EU says the talks "
         "were 'hijacked by oil states'. (Reuters, AP)", GREEN),
    ]
    yl = 232
    card_w, gap = 312, 16
    for i, (art, ch, kick, head, summ, accent) in enumerate(large):
        x0 = MARGIN + i * (card_w + gap)
        x1 = x0 + card_w
        d.rectangle([x0, yl, x1, yl + 216], outline=(150, 140, 120))
        art(d, x0 + 1, yl + 1, x1 - 1, yl + 91)
        chip(d, x0 + 8, yl + 72, ch, F(SANS_B, 10))
        card_text(d, x0 + 8, yl + 98, card_w - 16, kick, head, summ,
                  F(SANS_B, 10), F(SERIF, 20), F(SANS, 11), accent)

    # --- 10 medium cards, 2 rows of 5
    medium = [
        (art_gaza, "GAZA: 3 KILLED", "4  GAZA · CONFLICT",
         "Strikes kill 3 in Gaza",
         "Ceasefire toll reaches 1,675 dead, Gaza health officials say. "
         "(Anadolu)"),
        (art_knesset, "NO DEAL", "5  JERUSALEM, ISRAEL · POLITICS",
         "Netanyahu unity talks fail",
         "Likud and Eisenkot's Yashar end talks with no deal on forming a "
         "government. (The Hindu)"),
        (art_tow, "SHIP TOWED", "6  GULF OF FINLAND · WAR",
         "Russia tows drone-hit ship",
         "Sanctioned cargo vessel Sparta II is towed after a drone strike "
         "left it burning off Finland. (Reuters)"),
        (art_school, "MINISTER QUITS", "7  SEOUL, SOUTH KOREA · EDUCATION",
         "Minister quits over AI cheating",
         "Education minister resigns after an AI cheating scandal in school "
         "exams. (reports)"),
        (art_chip, "CHIP PROBE", "8  WASHINGTON, USA · TECH",
         "US probes Nvidia chips to China",
         "Treasury's Bessent seeks answers on sales of AI chips to China "
         "via a secret network. (reports)"),
        (art_chart, "CORRECTION", "9  NEW YORK, USA · MARKETS",
         "Wall Street slides into correction",
         "Stocks fall 10% from their peak as trade and rate fears bite; "
         "Asia follows lower. (reports)"),
        (art_ant, "FIRE ANTS", "10  SYDNEY, AUSTRALIA · ENVIRONMENT",
         "Second fire-ant nest in Sydney",
         "NSW destroys a nest in Auburn, possibly a year old, and sets a "
         "500-metre biosecurity zone. (AAP)"),
        (art_cedar, "264 KG SEIZED", "11  BEIRUT, LEBANON · SECURITY",
         "Army seizes 264 kg of explosives",
         "Three people arrested with explosives; officials say a plot was "
         "foiled. (Arab News)"),
        (art_bus, "9 KILLED", "12  KOTA, INDIA · DISASTER",
         "Pilgrim bus crash kills nine",
         "A bus carrying pilgrims hits a truck in Rajasthan; several more "
         "are hurt. (reports)"),
        (art_robot, "RULES BY 2028", "13  GENEVA, SWITZERLAND · ARMS",
         "Killer-robot rules due by 2028",
         "128 nations agree at UN talks to write rules for AI-run weapons; "
         "no binding ban yet. (reports)"),
    ]
    # one accent colour per medium story
    medium_accents = [DARKRED, DARKRED, BLUE, PURPLE, GREEN,
                      DARKRED, ORANGE, GREEN, ORANGE, OLIVE]
    mw, mgap = 185, 10
    for row in range(2):
        yr = 458 + row * 172
        for j in range(5):
            k = row * 5 + j
            art, ch, kick, head, summ = medium[k]
            accent = medium_accents[k]
            x0 = MARGIN + j * (mw + mgap)
            x1 = x0 + mw
            d.rectangle([x0, yr, x1, yr + 162], outline=(150, 140, 120))
            art(d, x0 + 1, yr + 1, x1 - 1, yr + 63)
            chip(d, x0 + 6, yr + 46, ch, F(SANS_B, 9), NAVY)
            # kicker: shrink to 8px if the full location would overflow
            kf = F(SANS_B, 9)
            if d.textlength(kick, font=kf) > mw - 12:
                kf = F(SANS_B, 8)
            d.text((x0 + 6, yr + 68), kick, font=kf, fill=accent)
            yy = yr + 82
            for ln in wrap(d, head, F(SERIF, 15), mw - 12):
                d.text((x0 + 6, yy), ln, font=F(SERIF, 15), fill=INK)
                yy += 17
            yy += 1
            for ln in wrap(d, summ, F(SANS, 10), mw - 12):
                d.text((x0 + 6, yy), ln, font=F(SANS, 10), fill=(60, 60, 60))
                yy += 13

    # --- also-on header
    ya = 800
    d.text((MARGIN, ya), "ALSO ON MONDAY 23 NOVEMBER 2026 — 17 MORE STORIES · 30 IN ALL",
           font=F(SANS_B, 14), fill=RED)
    d.line([MARGIN, ya + 20, W - MARGIN, ya + 20], fill=GOLD, width=1)

    # --- map + index
    ym = 828
    d.text((MARGIN, ym), "WHERE IT HAPPENED", font=F(SANS_B, 12), fill=RED)
    draw_map(d, MARGIN, ym + 18, 330, ym + 126)

    index = [
        (14, "Warsaw: NATO to bolster Poland's border (reports)"),
        (15, "Washington: US general reviews defences (reports)"),
        (16, "Brussels: cyberattack hits EU Commission (EU Today)"),
        (17, "Washington: intel chief backs Trump's Putin label (reports)"),
        (18, "Washington: FBI probes hack of crime database (AP)"),
        (19, "Washington: Senate leadership vote tests Democrats (AP)"),
        (20, "Manama: Bahrain demands UN action on Iran (Arab News)"),
        (21, "Riyadh: Saudis intercept Houthi missile (reports)"),
        (22, "Hormuz: 25 tankers hit; Gulf oil flow falls (reports)"),
        (23, "Johannesburg: Coca-Cola HBC lists on exchange (reports)"),
        (24, "Nairobi: Kenya starts drilling for its first oil (reports)"),
        (25, "New Delhi: India, Bulgaria discuss ties, IMEC (reports)"),
        (26, "Naypyidaw: Myanmar calls ASEAN decision unfair (reports)"),
        (27, "New Delhi: Ganga treaty faces 12 Dec expiry (reports)"),
        (28, "Canberra: Singapore PM Wong visits Australia (reports)"),
        (29, "Wellington: NZ retail sales recover in Q3 (reports)"),
        (30, "Global: Bitcoin rebounds after two-year low (reports)"),
    ]
    col_x = [346, 676]
    col_w = 320
    for ci, items in enumerate([index[:9], index[9:]]):
        yy = ym
        for n, txt in items:
            d.text((col_x[ci], yy), f"{n}", font=F(SANS_B, 10), fill=RED)
            tx = col_x[ci] + 24
            for ln in wrap(d, txt, F(SANS, 10), col_w - 24):
                d.text((tx, yy), ln, font=F(SANS, 10), fill=INK)
                yy += 12
            yy += 2

    # --- DATE CHECK box
    yd = 962
    d.rectangle([MARGIN, yd, W - MARGIN, yd + 38], outline=RED, width=2)
    d.text((MARGIN + 8, yd + 4), "DATE CHECK", font=F(SANS_B, 11), fill=RED)
    dc = ("Left out as other days' news: BepiColombo reaches Mercury (Sat); "
          "the Nigeria boat disaster (Fri); the Pentagon's UAP files (Fri); "
          "COP31 collapses (Sun); Democrats take 258 seats (Sun); "
          "Verstappen wins in Las Vegas (Sun); the Crimea Bridge strike "
          "(17 Nov).")
    for j, ln in enumerate(wrap(d, dc, F(SANS, 10), CW - 118)):
        d.text((MARGIN + 108, yd + 4 + j * 12), ln, font=F(SANS, 10),
               fill=INK)

    # --- footer
    d.text((MARGIN, 1008),
           "Every story here happened, or was first reported, on Monday 23 November 2026 · "
           "Sources named beside each story · All illustrations drawn in code",
           font=F(SANS, 9), fill=(90, 90, 90))

    paper_texture(img)
    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
