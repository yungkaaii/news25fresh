#!/usr/bin/env python3
"""THE WORLD TODAY - Wednesday 25 November 2026.

Draws a newspaper front page summing up 25 November 2026 world news
in one 1024x1024 PNG, using only the Python standard library.

No network, no randomness, no clock reads: the output is fully
deterministic. Writes exactly one file: $MAKEFUN_OUTPUT_DIR/entry.png
(default /output/entry.png).
"""

import hashlib
import os
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- font --
# A 5x7 bitmap font, defined fresh here. Each glyph is 7 rows of 5 cells.
# '#' is ink, '.' is blank. All poster text is uppercase.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
}
FONT.update({
    "0": (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    "1": ("..#..", ".##..", "#.#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "-": (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    "(": ("...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"),
    ")": ("##...", "..#..", "...#.", "...#.", "...#.", "..#..", "##..."),
    "/": ("....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."),
    "%": ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "|": ("..#..", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "&": (".##..", "#..#.", "#..#.", ".#...", "#.#.#", "#..#.", ".##.#"),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "+": (".....", "..#..", "..#..", ".###.", "..#..", "..#..", "....."),
    "=": (".....", ".....", ".###.", ".....", ".###.", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
    "E2": ("..###", ".#...", "#....", "###..", "#....", ".#...", "..###"),  # euro sign
})

EURO = "E2"  # placeholder key used in strings as \u0002


def glyph(ch):
    if ch == "\u20ac":
        return FONT["E2"]
    return FONT[ch]

# -------------------------------------------------------------- colours --
PAPER = (247, 243, 232)
INK = (17, 20, 24)
NAVY = (15, 42, 82)
RED = (176, 30, 36)
BLUE = (31, 90, 160)
DEEPBLUE = (10, 45, 110)
GREEN = (34, 120, 80)
ISLAND = (46, 125, 70)
GOLD = (212, 160, 40)
YELLOW = (235, 200, 60)
SKY = (178, 214, 235)
OCEAN = (18, 68, 130)
GREY = (120, 116, 108)
LIGHT = (232, 228, 216)
WHITE = (255, 255, 255)
CREAM = (255, 250, 238)


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.buf = bytearray(bytes(bg) * (w * h))

    def fill_rect(self, x0, y0, x1, y1, color):
        x0 = max(0, x0)
        y0 = max(0, y0)
        x1 = min(self.w, x1)
        y1 = min(self.h, y1)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(color) * (x1 - x0)
        for y in range(y0, y1):
            base = (y * self.w + x0) * 3
            self.buf[base:base + len(row)] = row

    def rect_border(self, x0, y0, x1, y1, color, t=2):
        self.fill_rect(x0, y0, x1, y0 + t, color)
        self.fill_rect(x0, y1 - t, x1, y1, color)
        self.fill_rect(x0, y0, x0 + t, y1, color)
        self.fill_rect(x1 - t, y0, x1, y1, color)

    def hline(self, x0, x1, y, color, t=1):
        self.fill_rect(x0, y, x1, y + t, color)

    def vline(self, x, y0, y1, color, t=1):
        self.fill_rect(x, y0, x + t, y1, color)

    def disc(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            half = int((r * r - dy * dy) ** 0.5)
            self.fill_rect(cx - half, cy + dy, cx + half + 1, cy + dy + 1, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        # Bresenham, with a square brush of width t.
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            self.fill_rect(x, y, x + t, y + t, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def triangle(self, p0, p1, p2, color):
        # Scanline fill of a triangle, integer math only.
        pts = sorted([p0, p1, p2], key=lambda p: p[1])
        (ax, ay), (bx, by), (cx, cy) = pts
        if ay == cy:
            return
        for y in range(ay, cy + 1):
            xs = []
            for (x0, y0), (x1, y1) in (((ax, ay), (bx, by)),
                                       ((bx, by), (cx, cy)),
                                       ((ax, ay), (cx, cy))):
                if y0 == y1:
                    continue
                if min(y0, y1) <= y <= max(y0, y1):
                    xs.append(x0 + (x1 - x0) * (y - y0) // (y1 - y0))
            if len(xs) >= 2:
                self.fill_rect(min(xs), y, max(xs) + 1, y + 1, color)


# ----------------------------------------------------------------- text --
def text_width(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(cv, x, y, s, scale, color):
    cx = x
    for ch in s:
        g = glyph(ch)
        for row_i, row in enumerate(g):
            for col_i, cell in enumerate(row):
                if cell == "#":
                    cv.fill_rect(cx + col_i * scale, y + row_i * scale,
                                 cx + (col_i + 1) * scale,
                                 y + (row_i + 1) * scale, color)
        cx += 6 * scale
    return cx


def draw_text_centered(cv, cx, y, s, scale, color):
    draw_text(cv, cx - text_width(s, scale) // 2, y, s, scale, color)


def wrap_text(s, scale, max_w):
    """Word wrap; for two lines, picks the split that best balances them."""
    words = s.split(" ")
    if text_width(s, scale) <= max_w:
        return [s]
    best = None
    for i in range(1, len(words)):
        l1 = " ".join(words[:i])
        l2 = " ".join(words[i:])
        if text_width(l1, scale) <= max_w and text_width(l2, scale) <= max_w:
            m = max(text_width(l1, scale), text_width(l2, scale))
            if best is None or m < best[0]:
                best = (m, [l1, l2])
    if best is not None:
        return best[1]
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

# -------------------------------------------------------------- stories --
# 30 stories, all reported on Wednesday 25 November 2026.
# (number, category, headline) -- headlines are short on purpose so each
# fits on two lines in the grid. Story 01 is the lead, drawn large.
STORIES = [
    ("01", "THE PACIFIC", "SOLOMON ISLANDS SIGNS LANDMARK TREATY WITH AUSTRALIA"),
    ("02", "SPACE", "SHENZHOU-24 CARRIES PAKISTAN'S FIRST ASTRONAUT"),
    ("03", "TECH", "US JURY CONVICTS HUAWEI OF STEALING TRADE SECRETS"),
    ("04", "WAR", "UKRAINE DRONES SINK RUSSIAN SHIP IN LIBYA"),
    ("05", "WAR", "ZELENSKY: UKRAINE NEEDS \u20ac115BN AID FOR 2027"),
    ("06", "MIDEAST", "FRESH ATTACKS ON SHIPPING IN STRAIT OF HORMUZ"),
    ("07", "MIDEAST", "ISRAELI STRIKES IN GAZA KILL 7, INCLUDING OFFICIAL"),
    ("08", "MIDEAST", "HOUTHI ATTACK IN RIYADH INJURES 11 PEOPLE"),
    ("09", "MIDEAST", "IRAN VOWS 'ALL MEANS' TO COUNTER US BLOCKADE"),
    ("10", "ECONOMY", "EUROZONE INFLATION RISES TO 4.0%"),
    ("11", "ECONOMY", "AUSTRALIAN INFLATION RISES TO 4.9%"),
    ("12", "ECONOMY", "UK ENERGY BILLS TO RISE 26% FROM JANUARY"),
    ("13", "MARKETS", "AI FEARS DRAG MARKETS LOWER ACROSS ASIA, WALL ST"),
    ("14", "MARKETS", "ANTHROPIC SHARES FALL BELOW IPO PRICE"),
    ("15", "TECH", "AMAZON BUYS DECART TO CHALLENGE NVIDIA"),
    ("16", "TECH", "HACKERS' AI AGENTS BREAK INTO UNIVERSITY SERVER"),
    ("17", "TECH", "TIDAL BANS AI MUSIC, DELETES 27M TRACKS"),
    ("18", "USA", "ABREGO GARCIA LEAVES US FOR SPAIN"),
    ("19", "LATAM", "COLOMBIA FREES HOSTAGES IN SUPERMARKET SIEGE"),
    ("20", "SPORT", "COURT RESTORES AFCON TITLE TO SENEGAL"),
    ("21", "HEALTH", "ROCHE BREAST CANCER PILL WINS 2ND FDA NOD"),
    ("22", "HEALTH", "UN: FUNDING CUTS THREATEN HIV PROGRESS"),
    ("23", "USA", "SIX KILLED IN PLANE CRASH OFF MISSISSIPPI"),
    ("24", "ASIA", "DOZENS TRAPPED IN FLOODED INDONESIA GOLD MINE"),
    ("25", "CHINA", "XI'S PURGE TAKES DOWN SHANGHAI CHIEF CHEN JINING"),
    ("26", "ASIA", "NORTH KOREA EXPELS SWISS DIPLOMAT"),
    ("27", "UK", "TWO HELD AFTER BREAK-IN AT PRINCE WILLIAM'S HOME"),
    ("28", "BUSINESS", "EASYJET PROFIT FALLS 89% AS FUEL COSTS SOAR"),
    ("29", "USA", "SAN FRANCISCO BAY BRACES FOR RECORD FLOODING"),
    ("30", "CLIMATE", "BOWEN: GEOPOLITICS HURT COP31 CONSENSUS"),
]

LEAD_SUMMARY = [
    "CANBERRA IS NAMED PRIMARY SECURITY PARTNER.",
    "NO FOREIGN MILITARY BASES ON THE ISLANDS.",
    "THE PACT REPLACES A 2022 DEAL WITH CHINA.",
]


# ------------------------------------------------------------- drawing --
def draw_masthead(cv):
    cv.fill_rect(0, 0, W, 88, NAVY)
    draw_text_centered(cv, W // 2, 20, "THE WORLD TODAY", 7, WHITE)
    cv.fill_rect(0, 92, W, 96, RED)
    draw_text_centered(cv, W // 2, 106, "WEDNESDAY 25 NOVEMBER 2026", 3, RED)
    draw_text_centered(cv, W // 2, 134,
                       "30 STORIES FROM ONE DAY | IN ONE IMAGE", 2, GREY)


def draw_lead_illustration(cv, x0, y0, x1, y1):
    """The Pacific: sun, ocean, islands and the two flags of the treaty."""
    cv.fill_rect(x0, y0, x1, y1, SKY)
    cv.disc(x1 - 42, y0 + 30, 24, GOLD)
    cv.fill_rect(x0, y0 + 118, x1, y1, OCEAN)
    # islands rising out of the sea
    cv.disc(x0 + 78, y0 + 128, 36, ISLAND)
    cv.disc(x0 + 228, y0 + 136, 48, ISLAND)
    cv.disc(x0 + 150, y0 + 142, 22, GREEN)
    # wave crests
    for wx in range(x0 + 12, x1 - 12, 34):
        cv.fill_rect(wx, y0 + 168, wx + 18, y0 + 172, WHITE)
    for wx in range(x0 + 28, x1 - 12, 34):
        cv.fill_rect(wx, y0 + 184, wx + 18, y0 + 188, WHITE)
    # flagpoles
    cv.fill_rect(x0 + 40, y0 + 12, x0 + 44, y0 + 128, INK)
    cv.fill_rect(x0 + 196, y0 + 12, x0 + 200, y0 + 136, INK)
    # Australian flag: blue field, Union Jack corner, southern cross
    fx, fy = x0 + 44, y0 + 12
    cv.fill_rect(fx, fy, fx + 64, fy + 36, DEEPBLUE)
    cv.fill_rect(fx, fy, fx + 32, fy + 18, WHITE)
    cv.fill_rect(fx + 14, fy, fx + 18, fy + 18, RED)
    cv.fill_rect(fx, fy + 7, fx + 32, fy + 11, RED)
    for sx, sy in ((50, 8), (56, 24), (44, 28), (58, 14)):
        cv.disc(fx + sx, fy + sy, 2, WHITE)
    cv.disc(fx + 16, fy + 28, 2, WHITE)
    # Solomon Islands flag: blue over green, yellow diagonal, stars
    gx, gy = x0 + 200, y0 + 12
    cv.fill_rect(gx, gy, gx + 64, gy + 36, BLUE)
    cv.triangle((gx, gy + 36), (gx + 64, gy + 36), (gx + 64, gy), GREEN)
    cv.line(gx, gy + 33, gx + 64, gy + 3, YELLOW, 6)
    for sx, sy in ((8, 6), (18, 6), (28, 6), (13, 14), (23, 14)):
        cv.disc(gx + sx, gy + sy, 2, WHITE)
    cv.rect_border(x0, y0, x1, y1, INK, 2)


def draw_lead(cv):
    cv.fill_rect(16, 164, 1008, 396, CREAM)
    cv.rect_border(16, 164, 1008, 396, NAVY, 3)
    draw_text(cv, 32, 180, "LEAD STORY | THE PACIFIC", 2, RED)
    hy = 206
    for line in ("SOLOMON ISLANDS SIGNS", "LANDMARK TREATY WITH", "AUSTRALIA"):
        draw_text(cv, 32, hy, line, 4, INK)
        hy += 34
    sy = 316
    for line in LEAD_SUMMARY:
        draw_text(cv, 32, sy, line, 2, INK)
        sy += 18
    draw_text(cv, 32, 376, "SIGNED IN CANBERRA | WEDNESDAY", 2, RED)
    draw_lead_illustration(cv, 664, 180, 992, 380)


def draw_grid(cv):
    gy0 = 448
    row_h = 56
    cols = (16, 352, 688)
    col_w = 328
    draw_text(cv, 16, 410, "THE DAY IN 30 STORIES", 3, NAVY)
    draw_text(cv, 1016 - text_width("02-30 BELOW", 2), 414,
              "02-30 BELOW", 2, RED)
    cv.fill_rect(16, 440, 1016, 443, NAVY)
    # separators
    for r in range(1, 10):
        cv.hline(16, 1016, gy0 + r * row_h, LIGHT, 1)
    for cx in (348, 684):
        cv.vline(cx, gy0, gy0 + 10 * row_h, LIGHT, 1)
    # stories 02..30 fill 29 of the 30 cells; the last cell is the sign-off
    cells = STORIES[1:]
    for idx, (num, cat, headline) in enumerate(cells):
        row, col = divmod(idx, 3)
        x = cols[col] + 8
        y = gy0 + row * row_h
        draw_text(cv, x, y + 4, num + " | " + cat, 2, RED)
        lines = wrap_text(headline, 2, col_w - 16)
        assert len(lines) <= 2, (num, headline, lines)
        ly = y + 22
        for line in lines:
            draw_text(cv, x, ly, line, 2, INK)
            ly += 18
    # sign-off cell: row 10, column 3
    fx, fy = cols[2], gy0 + 9 * row_h
    cv.fill_rect(fx + 4, fy + 2, fx + col_w, fy + row_h, NAVY)
    draw_text(cv, fx + 12, fy + 6, "30 STORIES.", 2, WHITE)
    draw_text(cv, fx + 12, fy + 24, "ONE DAY.", 2, WHITE)
    draw_text(cv, fx + 12, fy + 40, "25 NOV 2026.", 2, GOLD)


def build_image():
    cv = Canvas(W, H, PAPER)
    draw_masthead(cv)
    draw_lead(cv)
    draw_grid(cv)
    return cv.buf


# ------------------------------------------------------------------ png --
def png_bytes(rgb):
    def chunk(typ, data):
        return (struct.pack(">I", len(data)) + typ + data +
                struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += rgb[y * W * 3:(y + 1) * W * 3]
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
            chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = png_bytes(build_image())
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes) sha256=%s"
          % (path, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
