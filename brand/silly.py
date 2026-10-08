# Silly the dachshund (TheSilliestGames Studio's CEO), belly-up, as pixel art.
# Shapes are painted onto a grid, then every empty pixel touching the dog becomes outline.
# Writes silly.svg (crisp pixel rects, transparent background).
import math
import sys

PAL = {
    "o": "#2a1a2e",  # outline
    "b": "#b8632c",  # coat
    "l": "#d98f55",  # belly / light coat
    "L": "#ecb684",  # belly highlight
    "d": "#8c461f",  # coat shadow
    "e": "#6a3118",  # ears
    "E": "#86431f",  # ear highlight
    "m": "#9a5226",  # muzzle
    "n": "#1c1418",  # nose
    "N": "#6a5a62",  # nose shine
    "k": "#1c1418",  # eye
    "w": "#ffffff",  # eye shine
    "c": "#2c56b8",  # collar
    "C": "#9cc8ff",  # collar beads
    "t": "#4fb8d0",  # bone tag
    "T": "#b8eef8",  # tag shine
    "p": "#3a2620",  # claws
    "r": "#c8c8d0",  # tag ring
}

W, H = 62, 30
g = [[None] * W for _ in range(H)]


def put(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        g[y][x] = c


def ellipse(cx, cy, rx, ry, c):
    for y in range(H):
        for x in range(W):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1.0:
                put(x, y, c(x, y) if callable(c) else c)


def rect(x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            put(x, y, c(x, y) if callable(c) else c)


# --- Body: a long sausage, belly up (light on top, shadow underneath)
BODY_TOP, BODY_BOT = 12, 22


def body_col(x, y):
    if y <= BODY_TOP + 1:
        return "L" if (x in range(24, 30) or x in range(42, 48)) and y == BODY_TOP else "l"
    if y <= BODY_TOP + 3:
        return "l"
    if y >= BODY_BOT - 1:
        return "d"
    return "b"


rect(23, BODY_TOP, 50, BODY_BOT, body_col)
ellipse(23.5, (BODY_TOP + BODY_BOT + 1) / 2, 5.0, 5.5, body_col)  # chest
ellipse(50.5, (BODY_TOP + BODY_BOT + 1) / 2, 5.0, 5.5, body_col)  # rump

# --- Short stubby legs up in the air, paws flopped over toward the head (like the photo)
def leg(x, top, flop):
    for y in range(top + 2, BODY_TOP + 1):
        put(x, y, "b")
        put(x + 1, y, "l")
        put(x + 2, y, "b")
    # paw: a rounded nub that tips over toward the head
    px = x - flop
    for xx in range(px, px + 4):
        put(xx, top + 1, "b")
    for xx in range(px + 1, px + 4):
        put(xx, top, "b")
    put(px + 1, top + 1, "l")
    put(px + 2, top + 1, "l")
    put(px - 1, top + 1, "p")  # claw tips peeking out
    put(px - 1, top + 2, "p") if flop else None


leg(26, 6, 1)    # front legs
leg(31, 7, 1)
leg(42, 6, 1)    # back legs
leg(47, 5, 0)

# --- Tail, curling up off the rump
for i, (x, y) in enumerate([(55, 15), (56, 14), (57, 13), (57, 12), (58, 11), (58, 10), (58, 9)]):
    put(x, y, "b")
    put(x - 1, y, "b" if i else "d")

# --- Collar between head and chest, with beads
for y in range(10, 22):
    put(19, y, "c")
    put(20, y, "C" if y % 2 == 0 else "c")

# --- Head: domed skull, long snout, nose
ellipse(13.0, 13.0, 6.5, 6.0, "b")
for x in range(3, 13):  # snout tapers toward the nose
    top = 12 + (12 - x) // 4
    for y in range(top, 18):
        put(x, y, "m" if y >= 15 or x < 8 else "b")
rect(2, 13, 4, 15, "n")
put(2, 13, "N")
put(3, 13, "N")
for x in range(5, 11):
    put(x, 17, "d")  # mouth line
# eye, brow
rect(12, 10, 13, 11, "k")
put(12, 10, "w")
put(14, 11, "L")  # a sliver of eye white: the side-eye from the photo
put(11, 9, "d")   # brow raised in the middle: a hopeful, slightly worried look
put(12, 8, "d")
put(13, 8, "d")

# --- Long floppy ear hanging over the neck
def ear(x, y):
    return "E" if x == 15 and y < 19 else "e"


ellipse(16.0, 15.5, 2.6, 6.5, ear)

# --- Bone tag on a ring, hanging from the collar
put(20, 22, "r")
put(20, 23, "r")
rect(19, 25, 24, 26, "t")
for x, y in [(18, 24), (18, 25), (18, 26), (18, 27), (25, 24), (25, 25), (25, 26), (25, 27)]:
    put(x, y, "t")
put(19, 25, "T")
put(20, 25, "T")
put(18, 24, "T")

# --- Outline: empty pixels touching the dog (4-neighbours) become outline
filled = [[g[y][x] is not None for x in range(W)] for y in range(H)]
for y in range(H):
    for x in range(W):
        if filled[y][x]:
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and filled[ny][nx]:
                g[y][x] = "o"
                break

# --- Trim to the drawing plus a 1-pixel margin, write SVG
ys = [y for y in range(H) if any(g[y])]
xs = [x for x in range(W) if any(g[y][x] for y in range(H))]
x0, x1, y0, y1 = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
w, h = x1 - x0 + 1, y1 - y0 + 1
scale = int(sys.argv[1]) if len(sys.argv) > 1 else 10
rects = []
for y in range(y0, y1 + 1):
    x = x0
    while x <= x1:
        ch = g[y][x] if 0 <= y < H and 0 <= x < W else None
        if ch:
            x2 = x
            while x2 + 1 <= x1 and g[y][x2 + 1] == ch:
                x2 += 1
            rects.append(f'<rect x="{x - x0}" y="{y - y0}" width="{x2 - x + 1}" height="1" fill="{PAL[ch]}"/>')
            x = x2 + 1
        else:
            x += 1
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w * scale}" height="{h * scale}" '
       f'shape-rendering="crispEdges">' + "".join(rects) + "</svg>")
open("silly.svg", "w").write(svg)
print(f"{w}x{h} pixels, {len(rects)} rects")
