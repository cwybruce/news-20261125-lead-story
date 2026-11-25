#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261125.

Lead-story layout, 1024x1024, PIL only, fully deterministic.
Provenance: this file is the source of entry.png — rerun it to
reproduce the exact same bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BG = (246, 241, 232)
NAVY = (22, 35, 63)
GOLD = (232, 184, 75)
CARD = (255, 255, 255)
INK = (26, 26, 26)
GREY = (90, 90, 90)
RED = (178, 34, 34)
FOOTER_GREY = (110, 108, 100)

LEAD = {
    "kicker": "TRADE  |  USA",
    "color": RED,
    "headline": "Trump set to unveil new tariffs after probe into excess factory capacity",
    "summary": ("The US Trade Representative is poised to release the findings "
                "of a Section 301 probe into excess industrial capacity in "
                "16 major trading partners, with new import duties expected."),
}

BRIEFS = [
    {
        "kicker": "WAR  |  RUSSIA-UKRAINE",
        "color": (140, 30, 30),
        "headline": "Putin: retaliation \u201cinevitable\u201d after strikes on oil plants",
        "summary": ("Kyiv keeps hitting Russian refineries despite Trump\u2019s "
                    "pleas, Putin tells Kremlin officials."),
    },
    {
        "kicker": "ENERGY  |  IRAQ",
        "color": (14, 110, 110),
        "headline": "Baghdad moves to take over Kurdish oilfields",
        "summary": ("PM al-Zaidi orders federal control of fields in four "
                    "provinces; Kurds reject the move."),
    },
    {
        "kicker": "SANCTIONS  |  EUROPE",
        "color": (30, 70, 160),
        "headline": "EU unveils 22nd sanctions package on Russia",
        "summary": ("Brussels proposes cutting 60 banks from SWIFT and "
                    "listing 70+ shadow-fleet ships."),
    },
    {
        "kicker": "MIDDLE EAST  |  GAZA",
        "color": (90, 110, 30),
        "headline": "UN warns Gaza aid still falling far short",
        "summary": ("Agencies say winter, funding gaps and access limits leave "
                    "1.4m facing acute hunger, with shelter needs unmet."),
    },
    {
        "kicker": "SPORT  |  CRICKET",
        "color": (110, 50, 140),
        "headline": "England crush Australia by eight wickets",
        "summary": ("Donald smashes 85 off 32 and Salt 58 as England chase "
                    "185 in 13.1 overs to level the T20 series 1-1."),
    },
]


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_fitted_block(draw, x, y, w, headline, summary, kicker, color,
                      head_sizes, sum_sizes, max_head_lines, max_sum_lines,
                      pad=20, kicker_size=17, gap_k=8, gap_h=8):
    """Draw kicker + headline + summary inside a card at (x, y, w).
    Returns the y just below the drawn text. Raises if it cannot fit."""
    draw.text((x + pad, y + pad), kicker, font=font(kicker_size, True),
              fill=color)
    ty = y + pad + kicker_size + gap_k
    for hs in head_sizes:
        fnt = font(hs, True)
        lines = wrap(draw, headline, fnt, w - 2 * pad)
        if len(lines) <= max_head_lines:
            break
    else:
        raise ValueError("headline does not fit: %r" % headline)
    for ln in lines:
        draw.text((x + pad, ty), ln, font=font(hs, True), fill=INK)
        ty += hs + 5
    ty += gap_h - 5
    for ss in sum_sizes:
        fnt = font(ss)
        slines = wrap(draw, summary, fnt, w - 2 * pad)
        if len(slines) <= max_sum_lines:
            break
    else:
        raise ValueError("summary does not fit: %r" % summary)
    for ln in slines:
        draw.text((x + pad, ty), ln, font=font(ss), fill=(70, 70, 70))
        ty += ss + 4
    return ty


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 158], fill=NAVY)
    d.rectangle([0, 158, W, 164], fill=GOLD)
    d.text((32, 26), "25 NOVEMBER 2026", font=font(66, True), fill=(255, 255, 255))
    d.text((34, 108), "WEDNESDAY  \u2022  SIX STORIES FROM AROUND THE GLOBE",
           font=font(21, True), fill=GOLD)

    # ---- Lead story panel ----
    lx, ly, lw, lh = 32, 182, 960, 296
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD)
    d.rectangle([lx, ly, lx + 10, ly + lh], fill=RED)
    d.rectangle([lx + lw - 152, ly + 20, lx + lw - 20, ly + 52], fill=RED)
    d.text((lx + lw - 86, ly + 36), "LEAD STORY", font=font(14, True),
           fill=(255, 255, 255), anchor="mm")
    bottom = draw_fitted_block(
        d, lx + 10, ly, lw - 10, LEAD["headline"], LEAD["summary"],
        LEAD["kicker"], LEAD["color"],
        head_sizes=[42, 40, 38], sum_sizes=[22, 21, 20],
        max_head_lines=2, max_sum_lines=3,
        pad=28, kicker_size=19, gap_k=10, gap_h=10)
    assert bottom <= ly + lh - 16, "lead panel overflow: %d" % bottom

    # ---- Brief panels: row 1 (3), row 2 (2) ----
    rows = [
        (494, 228, BRIEFS[0:3], [304, 304, 304]),
        (738, 228, BRIEFS[3:5], [464, 464]),
    ]
    for ry, rh, items, widths in rows:
        x = 32
        for item, w in zip(items, widths):
            d.rectangle([x, ry, x + w, ry + rh], fill=CARD)
            d.rectangle([x, ry, x + w, ry + 6], fill=item["color"])
            bottom = draw_fitted_block(
                d, x, ry + 6, w, item["headline"], item["summary"],
                item["kicker"], item["color"],
                head_sizes=[25, 23, 21], sum_sizes=[18, 17, 16, 15],
                max_head_lines=3, max_sum_lines=3,
                pad=18, kicker_size=15, gap_k=8, gap_h=8)
            assert bottom <= ry + rh - 10, "brief overflow: %r %d" % (
                item["headline"], bottom)
            x += w + 16

    # ---- Footer ----
    d.text((W // 2, 984), "Sources: Reuters, AP, Bloomberg  \u2022  "
           "All events of 25 November 2026",
           font=font(16), fill=FOOTER_GREY, anchor="ma")

    img.save(OUT, format="PNG", optimize=True)
    print("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
