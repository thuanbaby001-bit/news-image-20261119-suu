#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news broadsheet for news-image-20261119.

Original work by SUU (@nhu-huynh) for make.fun. Runs locally with Pillow
and the DejaVu fonts; the entry itself (main.py) is standard library only
and just copies the image this script draws.
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
RED = (163, 22, 33)
BLUE = (29, 53, 87)
GREY = (90, 86, 78)
LIGHT = (232, 226, 214)
SKY = (214, 228, 235)

FONTS = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning lines that fit `width` pixels."""
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_centered(draw, y, text, fnt, fill, width=W):
    draw.text(((width - draw.textlength(text, font=fnt)) / 2, y), text,
              font=fnt, fill=fill)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 44  # margin

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=INK)
    draw_centered(d, 14, "THE WORLD IN ONE DAY", font(SERIF_B, 58), PAPER)
    draw_centered(d, 82, "T H U R S D A Y   ·   1 9   N O V E M B E R   2 0 2 6",
                  font(SANS_B, 19), (212, 196, 160))
    d.rectangle([0, 118, W, 122], fill=RED)

    # ---- formula strapline (GOOD's plan §3): date + REAL story count +
    # REAL region count + "one page" + edition word. Counts are auditable
    # from the image itself: 10 stories = 1 lead + 6 grid + 3 footer
    # "ALSO" items; 6 regions = UN subregions Eastern Asia (Shenzhen,
    # Kumamoto), South-eastern Asia (Myanmar), Western Asia (Riyadh/Hormuz,
    # Gaza), Europe (The Hague, Crimean Bridge), Oceania (Tonga, Panguna),
    # Africa (Ethiopia-Eritrea). GTA VI is worldwide, a story with no
    # region. Regions, not continents (continents would be 4).
    draw_centered(d, 126, "10 STORIES  ·  6 REGIONS  ·  ONE PAGE  —  BLUE EDITION",
                  font(SANS_B, 18), RED)

    # ---- main headline ----
    y = 162
    for line in ["TRUMP, XI AND PUTIN", "MEET IN SHENZHEN"]:
        draw_centered(d, y, line, font(SERIF_B, 56), INK)
        y += 62
    y += 4
    sub = ("Leaders hold a 90-minute trilateral at the APEC summit and issue a "
           "“peace declaration” — a joint statement on UN and ICC reform and "
           "nuclear counterproliferation.")
    for line in wrap(d, sub, font(SERIF, 21), W - 2 * m - 20):
        draw_centered(d, y, line, font(SERIF, 21), (52, 52, 52))
        y += 28
    y += 10

    # ---- skyline panel: schematic Shenzhen towers under a red sun ----
    top, bottom = y, y + 140
    d.rectangle([m, top, W - m, bottom], fill=SKY, outline=INK, width=2)
    # sun
    d.ellipse([W - m - 150, top + 18, W - m - 70, top + 98], fill=RED)
    # towers, back to front, ending above the caption bar
    cap_h = 28
    base = bottom - cap_h
    towers = [(70, 60, 46), (130, 95, 52), (196, 45, 44), (258, 80, 56),
              (330, 55, 48), (396, 100, 54), (470, 70, 46), (540, 40, 48),
              (610, 90, 52), (676, 60, 46)]
    for x, h, w in towers:
        d.rectangle([m + x, base - h, m + x + w, base], fill=BLUE)
        for wy in range(base - h + 10, base - 8, 16):
            for wx in range(m + x + 8, m + x + w - 8, 14):
                d.rectangle([wx, wy, wx + 5, wy + 7], fill=(235, 220, 160))
    d.rectangle([m, base, W - m, bottom], fill=INK)
    d.text((m + 12, base + 5), "SHENZHEN, CHINA — THE APEC SUMMIT",
           font=font(SANS_B, 16), fill=PAPER)
    y = bottom + 16

    # ---- story grid: 2 columns x 3 rows ----
    stories = [
        ("THE HAGUE", "ICJ: MYANMAR COMMITTED GENOCIDE",
         "The World Court rules Myanmar carried out state-sponsored genocide "
         "against the Rohingya — the first ruling of its kind."),
        ("MIDDLE EAST", "MISSILE DAMAGES RIYADH TOWER",
         "A Houthi missile strikes the PIF Tower in Riyadh, and three oil "
         "tankers catch fire after hitting mines east of the Strait of Hormuz."),
        ("GAZA", "ISRAEL PUSHES INTO CENTRAL GAZA",
         "Israeli forces launch a ground operation in central Gaza as the war "
         "grinds on."),
        ("UKRAINE", "CRIMEAN BRIDGE HIT A THIRD TIME",
         "Russia says Ukraine attacked the Crimean Bridge for the third time "
         "this week."),
        ("PACIFIC", "TONGA DECLARES EMERGENCY",
         "A state of emergency over an El Niño drought grips the island "
         "nation of Tonga."),
        ("BUSINESS", "RIO TINTO PAYS $250M FOR PANGUNA",
         "Rio Tinto agrees $250m for the Panguna mine in Bougainville, Papua "
         "New Guinea."),
    ]
    col_w = (W - 2 * m - 24) // 2
    row_h = 140
    for i, (kicker, head, body) in enumerate(stories):
        x = m + (i % 2) * (col_w + 24)
        yy = y + (i // 2) * row_h
        d.rectangle([x, yy, x + col_w, yy + row_h - 16], outline=INK, width=1)
        d.rectangle([x, yy, x + col_w, yy + 26], fill=INK)
        d.text((x + 10, yy + 4), kicker, font=font(SANS_B, 14), fill=PAPER)
        d.text((x + 10, yy + 34), head, font=font(SANS_B, 19), fill=INK)
        by = yy + 62
        for line in wrap(d, body, font(SANS, 16), col_w - 20):
            d.text((x + 10, by), line, font=font(SANS, 16), fill=(52, 52, 52))
            by += 21
    y += 3 * row_h + 6

    # ---- footer strip ----
    d.rectangle([m, y, W - m, y + 2], fill=RED)
    foot = ("ALSO: GTA VI launches worldwide  ·  Ethiopia–Eritrea clashes flare  ·  "
            "Magnitude 5.7 quake shakes Kumamoto, Japan")
    draw_centered(d, y + 12, foot, font(SANS, 15), GREY)
    draw_centered(d, y + 38, "10 stories · 6 regions · one page — Blue Edition  ·  19 November 2026  ·  @nhu-huynh",
                  font(SANS_B, 14), INK)

    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} {img.size} {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
