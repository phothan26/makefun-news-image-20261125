#!/usr/bin/env python3
"""Draw THE WORLD — Wednesday 25 November 2026: one front page.

A light broadsheet front page drawn with PIL only. Six verified stories of
the day plus a footer strip of three more, laid out as: masthead, one lead
panel, a 2x2 grid, a markets strip, and an "also" line. Output: entry.png,
1024x1024. This is build tooling; the submitted program only copies the PNG.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
PANEL = (255, 255, 255)
INK = (22, 22, 22)
RED = (178, 34, 34)
GREY = (92, 92, 88)
LEAD_BG = (16, 18, 20)
LEAD_SUB = (214, 214, 206)
SEA = (14, 60, 92)
SEA_D = (10, 42, 66)
ORANGE = (232, 116, 39)
FLAME = (245, 176, 65)
SKY_NIGHT = (18, 24, 44)
GREEN = (46, 139, 87)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, fnt, fill, leading):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(d, x, y, text, fnt):
    d.text((x, y), text, font=fnt, fill=RED)


# ---- small flat illustrations -------------------------------------------

def art_hormuz(d, x0, y0, x1, y1):
    import math
    d.rectangle([x0, y0, x1, y1], fill=SEA_D)
    d.rectangle([x0, y0, x1, y0 + (y1 - y0) // 3], fill=(24, 76, 110))
    d.ellipse([x1 - 90, y0 + 8, x1 - 30, y0 + 68], fill=(240, 214, 150))
    d.rectangle([x0, y0 + (y1 - y0) // 2, x1, y1], fill=SEA)
    # tanker hull and deck
    hx0, hx1 = x0 + 26, x1 - 60
    hy = y0 + (y1 - y0) // 2 + 34
    d.rectangle([hx0, hy, hx1, hy + 34], fill=(38, 38, 40))
    d.rectangle([hx0, hy + 24, hx1, hy + 34], fill=(150, 42, 38))
    d.rectangle([hx0 + 14, hy - 22, hx0 + 60, hy], fill=(52, 52, 54))
    d.rectangle([hx0 + 70, hy - 12, hx1 - 30, hy], fill=(58, 58, 60))
    d.rectangle([hx0 + 8, hy - 34, hx0 + 16, hy - 22], fill=(70, 70, 72))
    # mine: spiky circle in the water
    mx, my = x0 + 60, y1 - 46
    for ang in range(0, 360, 45):
        r1 = 22
        ex = mx + int(r1 * math.cos(math.radians(ang)))
        ey = my + int(r1 * math.sin(math.radians(ang)))
        d.line([mx, my, ex, ey], fill=(20, 20, 20), width=4)
    d.ellipse([mx - 13, my - 13, mx + 13, my + 13], fill=(20, 20, 20))
    # explosion burst above the tanker
    bx, by = x1 - 130, y0 + 52
    for r, col in ((46, ORANGE), (34, FLAME), (20, (250, 220, 120))):
        pts = []
        for i in range(12):
            ang = math.radians(i * 30)
            rr = r if i % 2 == 0 else r * 0.55
            pts.append((bx + rr * math.cos(ang), by + rr * math.sin(ang)))
        d.polygon(pts, fill=col)
    # smoke puffs
    for cx, cy, r in ((bx - 52, by - 18, 16), (bx - 30, by - 34, 20), (bx + 44, by - 30, 14)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 118))


def art_cairo(d, x0, y0, x1, y1):
    # band is only ~68px tall: keep every shape inside it
    d.rectangle([x0, y0, x1, y1], fill=SKY_NIGHT)
    d.rectangle([x0, y1 - 12, x1, y1], fill=(30, 30, 34))
    for bx, bw, bh in ((x0 + 8, 30, 22), (x0 + 48, 22, 30), (x1 - 58, 26, 24), (x1 - 96, 20, 18)):
        d.rectangle([bx, y1 - 12 - bh, bx + bw, y1 - 12], fill=(44, 46, 58))
    fx = (x0 + x1) // 2
    fy = y1 - 12
    for wdt, hgt, col in ((64, 40, ORANGE), (46, 30, FLAME), (26, 20, (250, 220, 120))):
        d.polygon(
            [(fx - wdt // 2, fy), (fx - wdt // 4, fy - hgt // 2),
             (fx, fy - hgt), (fx + wdt // 4, fy - hgt // 2),
             (fx + wdt // 2, fy)],
            fill=col,
        )
    for cx, cy, r in ((fx - 44, y0 + 12, 8), (fx - 28, y0 + 6, 10), (fx + 42, y0 + 10, 7)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 96, 98))
    for lx in (x0 + 22, x1 - 40):
        d.ellipse([lx - 4, y1 - 8, lx + 4, y1 - 4], fill=(250, 230, 150))


def art_refinery(d, x0, y0, x1, y1):
    # band is only ~68px tall: keep every shape inside it
    d.rectangle([x0, y0, x1, y1], fill=(58, 46, 40))
    d.rectangle([x0, y1 - 10, x1, y1], fill=(34, 30, 28))
    towers = ((x0 + 26, 30, 30), (x0 + 96, 24, 40), (x1 - 70, 28, 28))
    for tx, tw, th in towers:
        d.rectangle([tx, y1 - 10 - th, tx + tw, y1 - 10], fill=(88, 80, 74))
        d.rectangle([tx + tw // 2 - 3, y1 - 10 - th - 8, tx + tw // 2 + 3, y1 - 10 - th], fill=(88, 80, 74))
    d.line([x0 + 26, y1 - 22, x1 - 42, y1 - 22], fill=(110, 102, 94), width=3)
    for tx, tw, th in towers:
        fx = tx + tw // 2
        top = y1 - 10 - th
        d.polygon([(fx - 9, top), (fx, top - 16), (fx + 9, top)], fill=ORANGE)
        d.polygon([(fx - 5, top), (fx, top - 10), (fx + 5, top)], fill=FLAME)
    for cx, cy, r in ((x0 + 60, y0 + 8, 6), (x0 + 90, y0 + 5, 8), (x1 - 50, y0 + 7, 6)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 112, 104))


def art_tariff(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(238, 234, 222))
    base = y1 - 16
    d.line([x0 + 12, base, x1 - 12, base], fill=INK, width=2)
    bars = [("CN", 20, 66), ("EU", 15, 50), ("JP", 15, 50), ("IN", 17, 56)]
    bw = 34
    gap = (x1 - x0 - 24 - bw * len(bars)) // (len(bars) + 1)
    bx = x0 + 12 + gap
    f = font(SANS_B, 15)
    for label, pct, hgt in bars:
        d.rectangle([bx, base - hgt, bx + bw, base], fill=RED if pct >= 20 else (120, 120, 116))
        d.text((bx + bw // 2 - 12, base - hgt - 20), f"{pct}%", font=f, fill=INK)
        d.text((bx + bw // 2 - 10, base + 2), label, font=f, fill=GREY)
        bx += bw + gap


def art_space(d, x0, y0, x1, y1):
    import random
    d.rectangle([x0, y0, x1, y1], fill=(8, 10, 26))
    rng = random.Random(25)
    for _ in range(26):
        sx = rng.randint(x0 + 4, x1 - 4)
        sy = rng.randint(y0 + 4, y1 - 30)
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(230, 230, 230))
    # Earth arc first (clipped to the band), then station and capsule on top
    d.pieslice([x0, y1 - 44, x1, y1 + 44], 180, 360, fill=(28, 90, 160))
    d.pieslice([x0 + 60, y1 - 24, x1 - 60, y1 + 24], 180, 360, fill=(52, 130, 90))
    # station sits high in the band
    cx, cy = (x0 + x1) // 2, y0 + 22
    d.rectangle([cx - 52, cy - 8, cx + 52, cy + 8], fill=(210, 210, 205))
    d.rectangle([cx - 14, cy - 16, cx + 14, cy + 16], fill=(180, 180, 175))
    d.rectangle([cx - 96, cy - 5, cx - 54, cy + 5], fill=(52, 92, 160))
    d.rectangle([cx + 54, cy - 5, cx + 96, cy + 5], fill=(52, 92, 160))
    d.ellipse([cx + 66, cy + 18, cx + 84, cy + 30], fill=(240, 240, 235))
    d.rectangle([cx + 66, cy + 22, cx + 74, cy + 26], fill=(200, 60, 50))


def art_chart(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(238, 234, 222))
    pts = [(x0 + 10, y0 + 14), (x0 + 40, y0 + 26), (x0 + 70, y0 + 22),
           (x0 + 100, y0 + 44), (x0 + 130, y0 + 40), (x0 + 160, y0 + 66),
           (x0 + 190, y0 + 62), (x1 - 12, y1 - 12)]
    d.line(pts, fill=RED, width=4, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 16, ey - 2), (ex - 6, ey - 14)], fill=RED)


# ---- page ---------------------------------------------------------------

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24  # outer margin

    # masthead: 0..~156
    title_f = font(SERIF_B, 72)
    d.text((W // 2, 12), "THE WORLD", font=title_f, fill=INK, anchor="ma")
    d.line([M, 96, W - M, 96], fill=RED, width=3)
    d.line([M, 101, W - M, 101], fill=INK, width=1)
    date_f = font(SANS_B, 22)
    d.text((W // 2, 108), "WEDNESDAY 25 NOVEMBER 2026", font=date_f, fill=INK, anchor="ma")
    sub_f = font(SERIF, 19)
    d.text((W // 2, 136), "Six stories that defined the day", font=sub_f, fill=GREY, anchor="ma")

    # lead panel: Hormuz, 164..404
    lx, ly, lw, lh = M, 164, W - 2 * M, 240
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=LEAD_BG)
    d.rectangle([lx, ly, lx + lw, ly + lh], outline=INK, width=2)
    tx = lx + 24
    kicker(d, tx, ly + 16, "STRAIT OF HORMUZ  ·  MIDDLE EAST", font(SANS_B, 17))
    head_f = font(SERIF_B, 44)
    y = draw_lines(d, ["TANKERS HIT BY MINES", "IN HORMUZ"], tx, ly + 44, head_f, (248, 244, 232), 50)
    body_f = font(SANS, 18)
    draw_lines(
        d,
        wrap(d, "Iran says two tankers struck naval mines in the strait early on Wednesday and caught fire. About a fifth of the world's seaborne oil passes through the strait.", body_f, 560),
        tx, y + 6, body_f, LEAD_SUB, 24,
    )
    art_hormuz(d, lx + 612, ly + 14, lx + lw - 14, ly + lh - 14)

    # 2x2 grid: 416..898
    gy, gh, gap = 416, 236, 10
    gw = (W - 2 * M - gap) // 2
    panels = [
        (0, 0, "EGYPT", "FUEL TANKER BLAST KILLS 31 ON CAIRO RING ROAD",
         "A tanker overturned and exploded on the capital's Ring Road, killing 31 and hurting 25, the Health Ministry says.", art_cairo),
        (1, 0, "UKRAINE  ·  WAR", "DRONES SET TWO RUSSIAN REFINERIES ABLAZE",
         "Ukrainian drones hit the Syzran and Kuibyshev refineries in Samara overnight; one person was killed.", art_refinery),
        (0, 1, "UNITED STATES  ·  TRADE", "US PROPOSES TARIFFS OF UP TO 20% ON 14 ECONOMIES",
         "Washington unveils new duties aimed at excess factory capacity; China faces a capped rate of 20%. Nothing starts before January.", art_tariff),
        (1, 1, "CHINA  ·  SPACE", "PAKISTAN'S FIRST ASTRONAUT DOCKS AT TIANGONG",
         "Shenzhou-24 reaches China's space station about three and a half hours after launch, carrying Pakistan's first astronaut.", art_space),
    ]
    for col, row, kick, head, body, art in panels:
        px = M + col * (gw + gap)
        py = gy + row * (gh + gap)
        d.rectangle([px, py, px + gw, py + gh], fill=PANEL, outline=INK, width=2)
        art(d, px + 8, py + 8, px + gw - 8, py + 76)
        kicker(d, px + 16, py + 82, kick, font(SANS_B, 15))
        hf = font(SERIF_B, 27)
        y = draw_lines(d, wrap(d, head, hf, gw - 48), px + 16, py + 102, hf, INK, 31)
        bf = font(SANS, 15)
        draw_lines(d, wrap(d, body, bf, gw - 32), px + 16, y + 2, bf, (52, 52, 50), 19)

    # markets strip: 908..982
    my = 908
    d.rectangle([M, my, W - M, my + 74], fill=PANEL, outline=INK, width=2)
    kicker(d, M + 16, my + 8, "MARKETS", font(SANS_B, 15))
    mf = font(SERIF_B, 26)
    d.text((M + 16, my + 26), "ASIAN SHARES PLUNGE ON AI DOUBTS", font=mf, fill=INK)
    bf = font(SANS, 15)
    d.text((M + 16, my + 54), "Kospi -6.2%  ·  Nikkei -2.8%  ·  Taiex -5%  ·  Nasdaq -1.5%", font=bf, fill=(52, 52, 50))
    art_chart(d, W - M - 216, my + 8, W - M - 12, my + 66)

    # footer strip
    ff = font(SANS, 13)
    d.text((W // 2, 990), "ALSO:  Bogor mine flood — 9 dead, 17 trapped  ·  Australia's inflation jumps to 4.9%  ·  Australia–Solomons treaty signed",
           font=ff, fill=GREY, anchor="ma")
    d.line([M, 1010, W - M, 1010], fill=INK, width=1)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
