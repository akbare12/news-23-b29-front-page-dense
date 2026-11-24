#!/usr/bin/env python3
"""news-23 b29 front-page-dense: THE WORLD TODAY, Monday 23 November 2026."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 253, 248)
INK = (17, 17, 17)
RED = (185, 28, 28)
GOLD = (201, 162, 39)
TEAL = (15, 118, 110)
NAVY = (30, 58, 95)
DARKNAVY = (13, 27, 62)
PURPLE = (107, 33, 168)
BROWN = (146, 64, 14)
GRAY = (100, 100, 100)
LIGHTBLUE = (219, 234, 244)
GREEN = (139, 180, 120)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, font, fill=INK):
    d.text(xy, s, font=font, fill=fill)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 12  # margin
    X0, X1 = M, W - M

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 58], fill=INK)
    text(d, (M, 8), "THE WORLD TODAY", F(SERIF, 40), (255, 255, 255))
    dt = "MONDAY  23 NOVEMBER 2026"
    text(d, (W - M - d.textlength(dt, font=F(SANSB, 20)), 18), dt, F(SANSB, 20), GOLD)

    # ---------- kicker ----------
    kick = "AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at record low  ·  Anthropic IPO $107.3B"
    text(d, (M, 63), kick, F(SANSB, 14), RED)

    # ---------- number strip (5 cols x 2 rows) ----------
    strip = [
        [("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", NAVY),
         ("11,762", "EBOLA CASES, DRC", (101, 90, 0)), ("10T won", "SEOUL STABILISATION FUND", BROWN),
         ("2%", "BILLIONAIRE TAX IN PARIS", PURPLE)],
        [("$450M", "SKUBAL DEAL", PURPLE), ("165", "RUSSIAN MISSILES IN A WEEK", RED),
         ("12,000", "CLEARED IN MANCHESTER", (37, 99, 235)), ("264 kg", "EXPLOSIVES SEIZED IN LEBANON", BROWN),
         ("$107.3B", "ANTHROPIC IPO — LARGEST EVER", PURPLE)],
    ]
    cw = (X1 - X0) // 5
    y = 84
    for row in strip:
        for i, (num, lab, col) in enumerate(row):
            x = X0 + i * cw
            text(d, (x, y), num, F(SANSB, 21), col)
            text(d, (x, y + 24), lab, F(SANSB, 9), INK)
        y += 34
    d.line([(X0, 152), (X1, 152)], fill=INK, width=2)

    # ---------- region bar ----------
    regions = [("ASIA-PACIFIC 7", TEAL, 190), ("AMERICAS 8", NAVY, 190),
               ("MIDDLE EAST 6", (180, 130, 29), 170), ("EUROPE 5", PURPLE, 160),
               ("AFRICA 3", (153, 77, 77), 150), ("WORLD 2", GRAY, 140)]
    x = X0
    for name, col, wdt in regions:
        d.rectangle([x, 156, x + wdt, 172], fill=col)
        text(d, (x + 6, 159), name, F(SANSB, 10), (255, 255, 255))
        x += wdt

    # ---------- UTC strip ----------
    d.rectangle([0, 176, W, 192], fill=DARKNAVY)
    utc = "~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles   ~18:00 Anthropic $97.17"
    text(d, (M, 179), "THE DAY IN UTC", F(SANSB, 10), GOLD)
    text(d, (150, 179), utc, F(SANS, 10), (255, 255, 255))
    text(d, (W - M - d.textlength("~ APPROX", font=F(SANS, 10)), 179), "~ APPROX", F(SANS, 10), (200, 200, 200))

    # ---------- heroes ----------
    hx = [X0, 352, 692]
    hw = 328
    hy, scene_h = 196, 110
    # hero 1: Kospi skyline chart
    d.rectangle([hx[0], hy, hx[0] + hw, hy + scene_h], fill=DARKNAVY)
    import random
    random.seed(7)
    bx = hx[0] + 8
    while bx < hx[0] + hw - 14:
        bw = random.randint(14, 26)
        bh = random.randint(30, 78)
        d.rectangle([bx, hy + scene_h - 16 - bh, bx + bw, hy + scene_h - 16], fill=(24, 48, 96))
        for wy in range(hy + scene_h - 12 - bh, hy + scene_h - 18, 10):
            for wx in range(bx + 3, bx + bw - 3, 7):
                if random.random() < 0.5:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        bx += bw + 4
    pts = [(hx[0] + 22 + i * 29, hy + 40 + i * 5 + (4 if i % 3 == 0 else 0)) for i in range(11)]
    d.line(pts, fill=(239, 68, 68), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 214, 90), outline=RED)
    text(d, (hx[0] + 8, hy + 2), "-3.3%", F(SANSB, 30), (239, 68, 68))
    d.rectangle([hx[0], hy + scene_h - 16, hx[0] + hw, hy + scene_h], fill=INK)
    text(d, (hx[0] + 8, hy + scene_h - 14), "KOSPI  4,708.54    ·    -161 PTS", F(SANSB, 11), (255, 255, 255))
    # hero 2: Guterres
    d.rectangle([hx[1], hy, hx[1] + hw, hy + scene_h], fill=TEAL)
    text(d, (hx[1] + 10, hy + 6), "150 DELEGATES", F(SANSB, 30), (250, 204, 21))
    text(d, (hx[1] + 10, hy + 40), "BACK A RISK", F(SANSB, 26), (255, 255, 255))
    text(d, (hx[1] + 10, hy + 68), "FRAMEWORK", F(SANSB, 26), (255, 255, 255))
    d.ellipse([hx[1] + hw - 52, hy + 58, hx[1] + hw - 12, hy + 92], fill=(167, 243, 208))
    d.ellipse([hx[1] + hw - 44, hy + 66, hx[1] + hw - 30, hy + 80], fill=(52, 211, 153))
    d.ellipse([hx[1] + hw - 30, hy + 78, hx[1] + hw - 18, hy + 90], fill=(52, 211, 153))
    d.rectangle([hx[1], hy + scene_h - 16, hx[1] + hw, hy + scene_h], fill=INK)
    text(d, (hx[1] + 8, hy + scene_h - 14), "UN  ·  BRIDGETOWN", F(SANSB, 11), (255, 255, 255))
    # hero 3: Asia Power Index bars
    d.rectangle([hx[2], hy, hx[2] + hw, hy + scene_h], fill=(250, 247, 236))
    text(d, (hx[2] + 8, hy + 2), "NARROWEST SINCE 2018", F(SANSB, 12), INK)
    text(d, (hx[2] + hw - 8 - d.textlength("GAP 5.3", font=F(SANSB, 12)), hy + 2), "GAP 5.3", F(SANSB, 12), GOLD)
    bars = [("US", 78.9, NAVY, 0), ("CHINA", 73.6, RED, 1), ("INDIA", 40.5, (180, 130, 29), 2)]
    base = hy + scene_h - 30
    for name, val, col, i in bars:
        bx0 = hx[2] + 16 + i * 106
        bh = int(val * 0.58)
        d.rectangle([bx0, base - bh, bx0 + 62, base], fill=col)
        v = f"{val}"
        text(d, (bx0 + 31 - d.textlength(v, font=F(SANSB, 13)) / 2, base - bh + 4), v, F(SANSB, 13), (255, 255, 255))
        text(d, (bx0 + 31 - d.textlength(name, font=F(SANSB, 10)) / 2, base + 3), name, F(SANSB, 10), INK)
    d.rectangle([hx[2], hy + scene_h - 16, hx[2] + hw, hy + scene_h], fill=INK)
    text(d, (hx[2] + 8, hy + scene_h - 14), "ASIA POWER INDEX 2026", F(SANSB, 11), (255, 255, 255))

    # ---------- hero headlines + bodies ----------
    heroes = [
        ("1", "AI ROUT HITS ASIA",
         "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5.",
         "KOREA EXCHANGE", "REPORTED"),
        ("2", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
         "UNITED NATIONS", "REPORTED"),
        ("3", "US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India third at 40.5.",
         "LOWY INSTITUTE", "REPORTED"),
    ]
    hy2 = hy + scene_h + 6
    for i, (num, head, body, src, chip) in enumerate(heroes):
        x = hx[i]
        d.ellipse([x, hy2, x + 18, hy2 + 18], fill=RED)
        tw = d.textlength(num, font=F(SANSB, 11))
        text(d, (x + 9 - tw / 2, hy2 + 3), num, F(SANSB, 11), (255, 255, 255))
        lines = wrap(d, head, F(SANSB, 15), hw - 24)
        ly = hy2
        for ln in lines[:2]:
            text(d, (x + 24, ly), ln, F(SANSB, 15), INK)
            ly += 18
        blines = wrap(d, body, F(SANS, 11), hw - 4)
        by = hy2 + 36
        for ln in blines[:2]:
            text(d, (x, by), ln, F(SANS, 11), INK)
            by += 14
        text(d, (x, hy2 + 66), src, F(SANS, 9), GRAY)
        cw2 = d.textlength(chip, font=F(SANSB, 9)) + 10
        d.rectangle([x + hw - cw2, hy2 + 64, x + hw, hy2 + 78], fill=NAVY)
        text(d, (x + hw - cw2 + 5, hy2 + 66), chip, F(SANSB, 9), (255, 255, 255))

    # ---------- cards ----------
    cy0 = 420
    text(d, (M, 398), "MORE OF THE DAY  —  10 STORIES", F(SANSB, 14), INK)
    d.line([(X0, 414), (X1, 414)], fill=INK, width=2)
    cards = [
        ("AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury chief wants China answers.", "Reuters", "REPORTED", TEAL),
        ("FBI", "FBI PROBES NCIC HACK", "Hackers hit police NCIC database.", "AP", "REPORTED", PURPLE),
        ("WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "Strikes could resume in the New Year.", "Reuters", "REPORTED", BROWN),
        ("MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts Nasdaq futures 3%.", "Bloomberg", "REPORTED", TEAL),
        ("SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", RED),
        ("SPORT", "TOM JACKSON DIES AT 75", "Broncos LB turned ESPN voice dies.", "ESPN", "REPORTED", TEAL),
        ("LEGAL", "STATES SUE SPACEX", "Ten states challenge AI safety claims.", "AP", "REPORTED", PURPLE),
        ("TECH", "ANTHROPIC IPO: $107.3B", "Raised at $83; debut closes $97.17.", "WSJ", "REPORTED", NAVY),
        ("EUROPE", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed airspace.", "AP", "CLAIM", RED),
        ("SPACE", "RUSSIAN NUCLEAR SATELLITE", "Intel: satellite built to carry a nuke.", "Reuters", "CLAIM", GRAY),
    ]
    cwid = 193
    cgap = 8
    ch = 82
    for idx, (cat, head, body, src, chip, col) in enumerate(cards):
        row, c = divmod(idx, 5)
        x = X0 + c * (cwid + cgap)
        y = cy0 + row * (ch + 8)
        d.rectangle([x, y, x + cwid, y + ch], outline=(180, 180, 180), width=1)
        d.rectangle([x, y, x + cwid, y + 16], fill=col)
        text(d, (x + 5, y + 3), cat, F(SANSB, 9), (255, 255, 255))
        n = str(idx + 4)
        text(d, (x + cwid - 6 - d.textlength(n, font=F(SANSB, 10)), y + 3), n, F(SANSB, 10), (255, 255, 255))
        lines = wrap(d, head, F(SANSB, 12), cwid - 10)
        ly = y + 20
        for ln in lines[:2]:
            text(d, (x + 5, ly), ln, F(SANSB, 12), INK)
            ly += 14
        text(d, (x + 5, y + 50), body, F(SANS, 10), INK)
        text(d, (x + 5, y + 66), src, F(SANS, 9), GRAY)
        fill = NAVY if chip == "REPORTED" else RED
        cw3 = d.textlength(chip, font=F(SANSB, 8)) + 8
        d.rectangle([x + cwid - cw3 - 4, y + 65, x + cwid - 4, y + 77], fill=fill)
        text(d, (x + cwid - cw3, y + 67), chip, F(SANSB, 8), (255, 255, 255))

    # ---------- map + ALSO ----------
    my0 = 620
    text(d, (M, 600), "WHERE IT HAPPENED", F(SANSB, 14), INK)
    text(d, (452, 600), "ALSO ON MONDAY", F(SANSB, 14), INK)
    d.line([(X0, 616), (X1, 616)], fill=INK, width=2)
    mx0, my1, mx1 = M, my0, 440
    d.rectangle([mx0, my0, mx1, 830], fill=LIGHTBLUE)
    for gx in range(mx0, mx1 + 1, 16):
        d.line([(gx, my0), (gx, 830)], fill=(200, 220, 232), width=1)
    for gy in range(my0, 831, 16):
        d.line([(mx0, gy), (mx1, gy)], fill=(200, 220, 232), width=1)
    continents = [
        [(28, 628), (180, 622), (205, 668), (160, 726), (90, 726), (35, 676)],
        [(150, 742), (200, 740), (195, 800), (165, 820), (148, 782)],
        [(255, 622), (300, 618), (312, 644), (285, 668), (258, 656)],
        [(255, 676), (300, 674), (305, 738), (280, 776), (255, 732)],
        [(320, 622), (420, 618), (435, 658), (400, 714), (340, 704), (318, 666)],
        [(370, 780), (420, 778), (425, 804), (375, 808)],
    ]
    for poly in continents:
        d.polygon(poly, fill=GREEN, outline=(110, 150, 95))
    pins = [(1, 415, 655), (2, 170, 775), (3, 395, 635), (4, 120, 670), (5, 150, 655),
            (6, 330, 685), (7, 105, 645), (8, 60, 670), (9, 95, 690), (10, 115, 715),
            (11, 275, 635), (12, 295, 650), (13, 320, 625)]
    for n, px, py in pins:
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        s = str(n)
        text(d, (px - d.textlength(s, font=F(SANSB, 9)) / 2, py - 6), s, F(SANSB, 9), (255, 255, 255))
    legend = ("Pins 1–13: 1 Seoul · 2 Bridgetown · 3 Beijing · 4 Washington · 5 New York · 6 Tehran · "
              "7 Chicago · 8 San Francisco · 9 Denver · 10 Austin · 11 Warsaw · 12 Kyiv · 13 Moscow")
    ly = 834
    for ln in wrap(d, legend, F(SANS, 10), mx1 - mx0):
        text(d, (mx0, ly), ln, F(SANS, 10), GRAY)
        ly += 13

    also = [
        "14. Paris: 100+ back 2% billionaire tax", "15. Manchester: 12,000 cleared",
        "16. Zelenskyy: 165 missiles in a week", "17. COP31: the day after pact rejected",
        "18. Benghazi: UN demands port probe", "19. Israel unity talks resume",
        "20. Gaza: two killed in Israeli strike", "21. West Bank settler attacks",
        "22. Iran war: no deal in sight", "23. Lebanon seizes 264 kg explosives",
        "24. Bahrain: strike hits plant, 2 hurt", "25. Sudan: defences down drones",
        "26. DRC: fighting traps Ebola teams", "27. Bangladesh: Hasina jailed if she returns",
        "28. Seoul minister quits in exam row", "29. SK Telecom -7.3% as hype cools",
        "30. China eases margin rules", "31. Seoul readies 10T-won fund",
    ]
    ax = [452, 740]
    for i, item in enumerate(also):
        col, row = divmod(i, 9)
        text(d, (ax[col], my0 + 4 + row * 26), item, F(SANS, 12), INK)

    # ---------- DATE CHECK ----------
    d.rectangle([X0, 880, X1, 958], outline=RED, width=2)
    text(d, (M + 4, 884), "DATE CHECK", F(SANSB, 14), RED)
    rt = "READ 23 NOV 2026, 23:59 UTC — STORIES DATED 23 NOV ONLY"
    text(d, (X1 - 4 - d.textlength(rt, font=F(SANSB, 10)), 888), rt, F(SANSB, 10), INK)
    left = ("LEFT OUT — NOT 23 NOV: Democrats reach 258 seats (22 Nov) · Sparta II fire (22 Nov) · "
            "El Chapo Isidro captured (22 Nov) · EU-Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · "
            "ICJ Myanmar ruling (19 Nov)")
    ly = 906
    for ln in wrap(d, left, F(SANS, 11), X1 - X0 - 8):
        text(d, (M + 4, ly), ln, F(SANS, 11), INK)
        ly += 14
    ny = ("NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · "
          "COP32 venue not set · WHO evacuating trapped Ebola staff")
    text(d, (M + 4, ly + 2), ny, F(SANS, 11), INK)

    # ---------- footer ----------
    text(d, (M, 964), "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · NYT · ESPN · Lowy Institute (Asia Power Index 2026).", F(SANS, 10), GRAY)
    text(d, (M, 978), "CHIPS: REPORTED = confirmed by wires · CLAIM = one side's claim, not independently confirmed · ONGOING = still developing", F(SANS, 10), GRAY)

    # ---------- bottom bar ----------
    d.rectangle([0, 996, W, H], fill=INK)
    bot = "Scenes are drawn illustrations, not photographs.   ·   THE WORLD TODAY — Monday 23 November 2026   ·   31 stories   ·   6 regions"
    text(d, ((W - d.textlength(bot, font=F(SANSB, 11))) / 2, 1006), bot, F(SANSB, 11), GOLD)

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
    print("saved entry.png")
