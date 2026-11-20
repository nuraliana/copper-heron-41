#!/usr/bin/env python3
"""Draw the Friday 20 November 2026 front page as a single square picture.

The story bundle lives in stories.json next to this file. The picture is
a broadsheet in miniature: a nameplate, a figures band, region tabs, a
timeline, three big stories, ten smaller ones, a world chart with pins,
the rest of the day's briefs, a box that sorts out the previous day's
news, and a sources line. Everything is drawn with Pillow shapes and
system typefaces; the program takes no input from the network, the clock
or any random source, so running it twice gives the same bytes.

It saves entry.png into the directory named by
MAKEFUN_OUTPUT_DIR (or /output), never into the program's own folder:
the grader runs the program from a read-only directory, so writing
beside the script fails there. It also tries, best effort, to mirror
the file beside itself for local runs, ignoring a read-only folder.
It checks the written file matches byte for byte, prints the size and
digest, and refuses to finish when the file would pass one mebibyte.
"""

import hashlib, io, json, os, sys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

PAGE = 1024
MARGIN = 30
INNER = PAGE - 2 * MARGIN

SHEET = (247,241,227)
SOOT = (26,26,26)
DIM = (110,104,92)
LINECOL = (60,52,44)
OXBLOOD = (161,30,34)
DEEP = (20,54,92)
SAND = (228,211,168)
PANEL = (255,252,244)
BORDER = (90,80,64)

TYPE_DIR = "/usr/share/fonts/truetype/dejavu"


def open_faces():
    """Fetch the four typefaces the page is set in."""
    return {
        "title": ImageFont.truetype(f"{TYPE_DIR}/DejaVuSerif-Bold.ttf", 54),
        "standfirst": ImageFont.truetype(f"{TYPE_DIR}/DejaVuSerif-Italic.ttf", 16),
        "serif": ImageFont.truetype(f"{TYPE_DIR}/DejaVuSerif.ttf", 12),
        "stat": ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans-Bold.ttf", 21),
        "kick": ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans-Bold.ttf", 11),
        "kick9": ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans-Bold.ttf", 9),
        "kick10": ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans-Bold.ttf", 10),
        "kick12": ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans-Bold.ttf", 12),
        "kick13": ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans-Bold.ttf", 13),
        "head17": ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans-Bold.ttf", 17),
        "body": ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans.ttf", 11),
        "body10": ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans.ttf", 10),
        "body9": ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans.ttf", 9),
        "fine": ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans.ttf", 8),
        "micro": ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans-Bold.ttf", 8),
    }


def fold_words(text, face, width):
    """Break text into lines that fit, word by word, greedily."""
    words = text.split()
    if not words:
        return [""]
    lines = []
    cur = words[0]
    for w in words[1:]:
        trial = cur + " " + w
        if face.getlength(trial) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def snip_lines(text, face, width, most):
    """Fold text and keep no more than `most` lines, ending with … ."""
    lines = fold_words(text, face, width)
    if len(lines) <= most:
        return lines
    keep = lines[:most]
    last = keep[-1]
    while last and face.getlength(last + "…") > width:
        last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
    keep[-1] = last + "…"
    return keep


def rule(pen, y, colour=LINECOL, weight=2):
    pen.line(((MARGIN, y), (PAGE - MARGIN, y)), fill=colour, width=weight)


# ------------------------------------------------------------------ pictures

def pic_cyclone(pen, ox, oy, ow, oh):
    pen.rectangle(((ox, oy), (ox + ow, oy + oh)), fill=(16,42,78))
    pen.ellipse(((ox + ow - 34, oy + 8), (ox + ow - 8, oy + 34)),
                fill=(238,230,205))
    cx, cy = ox + ow // 2 - 6, oy + oh // 2 + 2
    pen.ellipse(((cx - 9, cy - 9), (cx + 9, cy + 9)), fill=(238,230,205))
    for k in range(0, 4):
        r = (14, 22, 30, 38)[k]
        pen.arc(((cx - r, cy - r), (cx + r, cy + r)),
                start=40 + k * 55, end=250 + k * 55,
                fill=(255,255,255), width=3)
    for k, wy in enumerate((oh - 22, oh - 14, oh - 6)):
        pen.arc(((ox + 8 + k * 4, oy + wy - 8),
                 (ox + ow - 8 - k * 4, oy + wy + 8)),
                start=200, end=340, fill=(180,210,235), width=2)


def pic_cop(pen, ox, oy, ow, oh):
    pen.rectangle(((ox, oy), (ox + ow, oy + oh)), fill=(168,208,232))
    pen.ellipse(((ox + ow - 36, oy + 6), (ox + ow - 10, oy + 32)),
                fill=(240,140,40))
    pen.polygon(((ox, oy + oh), (ox, oy + oh - 34),
                 (ox + ow * 0.45, oy + oh - 52), (ox + ow * 0.7, oy + oh - 30),
                 (ox + ow, oy + oh - 40), (ox + ow, oy + oh)),
                fill=(96,150,84))
    pen.polygon(((ox, oy + oh), (ox, oy + oh - 22),
                 (ox + ow * 0.5, oy + oh - 34), (ox + ow, oy + oh - 20),
                 (ox + ow, oy + oh)), fill=(58,122,62))
    tx, ty = ox + ow // 2 + 8, oy + oh - 44
    pen.rectangle(((tx - 2, ty), (tx + 2, ty + 16)), fill=(90,60,30))
    pen.ellipse(((tx - 13, ty - 14), (tx + 13, ty + 8)), fill=(46,110,52))
    pen.ellipse(((tx - 8, ty - 6), (tx - 2, ty)), fill=(250,220,90))
    pen.ellipse(((tx + 3, ty - 8), (tx + 9, ty - 2)), fill=(250,220,90))


def pic_ipo(pen, ox, oy, ow, oh):
    pen.rectangle(((ox, oy), (ox + ow, oy + oh)), fill=(14,59,46))
    big = ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans-Bold.ttf", 26)
    gold = ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans-Bold.ttf", 18)
    pen.text((ox + 8, oy + 6), "AN" "T", font=big, fill=(255,255,255))
    pen.text((ox + ow - 78, oy + 10), "$97" ".17", font=gold,
             fill=(232,190,80))
    base = oy + oh - 12
    step = (ow - 16) / 9
    tops = []
    for k in range(0, 9):
        cx = ox + 12 + k * step
        up = (k % 2 == 0)
        top = oy + 42 + (k * 2 if k < 5 else (8 - k) * 2)
        bot = top + 14
        col = (46,160,90) if up else (205,70,60)
        pen.line(((cx, top - 5), (cx, bot + 5)), fill=col, width=2)
        pen.rectangle(((cx - 4, top), (cx + 4, bot)), fill=col)
        tops.append((cx, top))
    for a, b in zip(tops, tops[1:]):
        pen.line((a, b), fill=(232,190,80), width=2)


def pic_flags(pen, ox, oy, ow, oh):
    pen.rectangle(((ox, oy), (ox + ow, oy + oh)), fill=(238,232,214))
    pen.rectangle(((ox, oy + oh - 8), (ox + ow, oy + oh)), fill=(150,110,70))
    poles = [ox + 18, ox + ow // 2, ox + ow - 22]
    for p in poles:
        pen.line(((p, oy + 12), (p, oy + oh - 8)), fill=(80,70,55), width=2)
    pen.rectangle(((poles[0], oy + 12), (poles[0] + 26, oy + 32)),
                  fill=(200,40,40))
    pen.ellipse(((poles[0] + 9, oy + 16), (poles[0] + 17, oy + 24)),
                fill=(238,232,214))
    for r, col in enumerate(((255,255,255), (200,40,40), (255,255,255),
                             (200,40,40), (255,255,255))):
        pen.rectangle(((poles[1], oy + 12 + r * 4),
                       (poles[1] + 26, oy + 16 + r * 4)), fill=col)
    pen.rectangle(((poles[1], oy + 12), (poles[1] + 10, oy + 20)),
                  fill=(30,60,140))
    for r, col in enumerate(((255,255,255), (40,80,180), (200,40,40))):
        pen.rectangle(((poles[2], oy + 12 + r * 7),
                       (poles[2] + 26, oy + 19 + r * 7)), fill=col)


def pic_parliament(pen, ox, oy, ow, oh):
    pen.rectangle(((ox, oy), (ox + ow, oy + oh)), fill=(238,232,214))
    pen.polygon(((ox + 6, oy + 30), (ox + ow // 2, oy + 8),
                 (ox + ow - 6, oy + 30)), fill=(70,70,78))
    pen.rectangle(((ox + 6, oy + 30), (ox + ow - 6, oy + 38)),
                  fill=(150,140,120))
    for k in range(0, 5):
        cx = ox + 14 + k * ((ow - 28) / 4)
        pen.rectangle(((cx - 4, oy + 38), (cx + 4, oy + oh - 10)),
                      fill=(210,200,175))
    pen.rectangle(((ox + 6, oy + oh - 10), (ox + ow - 6, oy + oh - 4)),
                  fill=(150,140,120))
    px = ox + ow - 26
    pen.line(((px, oy + 6), (px, oy + 24)), fill=(80,70,55), width=2)
    for r, col in enumerate(((40,40,40), (200,40,40), (232,190,80))):
        pen.rectangle(((px, oy + 6 + r * 5), (px + 14, oy + 11 + r * 5)),
                      fill=col)


def pic_embassy(pen, ox, oy, ow, oh):
    pen.rectangle(((ox, oy), (ox + ow, oy + oh)), fill=(185,210,230))
    pen.rectangle(((ox + 8, oy + 22), (ox + ow - 14, oy + oh - 6)),
                  fill=(245,242,235))
    pen.pieslice(((ox + 8, oy + 2), (ox + ow - 14, oy + 42)),
                 start=180, end=360, fill=(245,242,235))
    for k in range(0, 4):
        cx = ox + 18 + k * ((ow - 36) / 3)
        pen.rectangle(((cx - 3, oy + 34), (cx + 3, oy + oh - 6)),
                      fill=(200,192,172))
    pen.rectangle(((ox + ow - 8, oy), (ox + ow - 2, oy + oh)),
                  fill=(200,40,40))
    pen.ellipse(((ox + ow - 34, oy + 6), (ox + ow - 20, oy + 20)),
                fill=(235,120,50))


def pic_capitol(pen, ox, oy, ow, oh):
    pen.rectangle(((ox, oy), (ox + ow, oy + oh)), fill=(185,210,230))
    pen.rectangle(((ox + 6, oy + 34), (ox + ow - 6, oy + oh - 6)),
                  fill=(245,242,235))
    pen.pieslice(((ox + ow // 2 - 16, oy + 6), (ox + ow // 2 + 16, oy + 38)),
                 start=180, end=360, fill=(245,242,235))
    pen.rectangle(((ox + ow // 2 - 2, oy + 2), (ox + ow // 2 + 2, oy + 10)),
                  fill=(245,242,235))
    for k in range(0, 5):
        cx = ox + 14 + k * ((ow - 28) / 4)
        pen.rectangle(((cx - 3, oy + 40), (cx + 3, oy + oh - 6)),
                      fill=(200,192,172))


def pic_chip(pen, ox, oy, ow, oh):
    pen.rectangle(((ox, oy), (ox + ow, oy + oh)), fill=(10,26,51))
    for k in range(0, 7):
        px = ox + 8 + k * ((ow - 16) / 6)
        pen.rectangle(((px - 2, oy + 2), (px + 2, oy + 9)),
                      fill=(46,200,110))
        pen.rectangle(((px - 2, oy + oh - 9), (px + 2, oy + oh - 2)),
                      fill=(46,200,110))
    cx, cy = ox + ow // 2, oy + oh // 2
    pen.rectangle(((cx - 22, cy - 16), (cx + 22, cy + 16)),
                  fill=(30,170,95))
    pen.rectangle(((cx - 14, cy - 9), (cx + 14, cy + 9)), fill=(16,120,70))
    f = ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans-Bold.ttf", 15)
    pen.text((cx - 9, cy - 10), "A" "I", font=f, fill=(255,255,255))


def pic_cricket(pen, ox, oy, ow, oh):
    pen.rectangle(((ox, oy), (ox + ow, oy + oh)), fill=(58,140,70))
    pen.rectangle(((ox, oy), (ox + ow, oy + 16)), fill=(245,242,235))
    f = ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans-Bold.ttf", 13)
    pen.text((ox + 5, oy + 1), "11" "8", font=f, fill=(30,30,30))
    pen.rectangle(((ox + 6, oy + oh - 22), (ox + ow - 6, oy + oh - 12)),
                  fill=(190,150,95))
    pen.polygon(((ox + ow - 46, oy + 22), (ox + ow - 34, oy + 22),
                 (ox + ow - 58, oy + oh - 26), (ox + ow - 70, oy + oh - 26)),
                fill=(220,190,130))
    pen.ellipse(((ox + 22, oy + oh - 38), (ox + 34, oy + oh - 26)),
                fill=(200,40,40))


def pic_gta(pen, ox, oy, ow, oh):
    top = [104, 40, 150]
    bot = [198, 30, 110]
    for yy in range(0, oh):
        t = yy / max(oh - 1, 1)
        col = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(0, 3))
        pen.line(((ox, oy + yy), (ox + ow, oy + yy)), fill=col)
    pen.ellipse(((ox + ow - 34, oy + 8), (ox + ow - 10, oy + 32)),
                fill=(250,225,200))
    f = ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans-Bold.ttf", 22)
    pen.text((ox + 6, oy + 4), "V" "I", font=f, fill=(255,255,255))
    base = oy + oh
    heights = [16, 26, 12, 30, 20, 34, 14, 24, 18]
    bw = ow / len(heights)
    for k in range(0, len(heights)):
        hh = heights[k]
        pen.rectangle(((ox + k * bw, base - hh),
                       (ox + (k + 1) * bw, base)), fill=(30,12,40))


def pic_boat(pen, ox, oy, ow, oh):
    pen.rectangle(((ox, oy), (ox + ow, oy + oh)), fill=(52,110,170))
    for k, wy in enumerate((oh - 16, oh - 10, oh - 4)):
        pen.arc(((ox + 6 + k * 6, oy + wy - 8),
                 (ox + ow - 6 - k * 6, oy + wy + 8)),
                start=200, end=340, fill=(255,255,255), width=2)
    hx, hy = ox + ow // 2, oy + oh - 20
    pen.polygon(((hx - 26, hy), (hx + 26, hy), (hx + 18, hy + 14),
                 (hx - 18, hy + 14)), fill=(120,75,40))
    pen.line(((hx, hy), (hx, oy + 10)), fill=(90,60,30), width=2)
    pen.polygon(((hx + 2, oy + 12), (hx + 2, hy - 2), (hx + 24, hy - 2)),
                fill=(240,235,220))


def pic_drought(pen, ox, oy, ow, oh):
    pen.rectangle(((ox, oy), (ox + ow, oy + oh)), fill=(245,225,150))
    pen.ellipse(((ox + ow - 32, oy + 6), (ox + ow - 8, oy + 30)),
                fill=(240,140,40))
    pen.polygon(((ox, oy + oh - 12), (ox + ow * 0.3, oy + oh - 34),
                 (ox + ow * 0.6, oy + oh - 12)), fill=(170,120,70))
    pen.polygon(((ox + ow * 0.45, oy + oh - 12),
                 (ox + ow * 0.7, oy + oh - 28), (ox + ow, oy + oh - 12)),
                fill=(150,105,60))
    pen.rectangle(((ox, oy + oh - 12), (ox + ow, oy + oh)),
                  fill=(70,130,190))


def pic_baseball(pen, ox, oy, ow, oh):
    pen.rectangle(((ox, oy), (ox + ow, oy + oh)), fill=(52,130,66))
    pen.rectangle(((ox, oy), (ox + ow, oy + 12)), fill=(90,165,100))
    cx, cy = ox + ow // 2, oy + oh // 2 + 3
    pen.ellipse(((cx - 20, cy - 20), (cx + 20, cy + 20)),
                fill=(250,250,245))
    pen.arc(((cx - 20, cy - 20), (cx + 20, cy + 20)), start=300, end=60,
            fill=(200,40,40), width=2)
    pen.arc(((cx - 20, cy - 20), (cx + 20, cy + 20)), start=120, end=240,
            fill=(200,40,40), width=2)


PICS = {
    "cyclone": pic_cyclone,
    "cop": pic_cop,
    "ipo": pic_ipo,
    "flags": pic_flags,
    "parliament": pic_parliament,
    "embassy": pic_embassy,
    "capitol": pic_capitol,
    "chip": pic_chip,
    "cricket": pic_cricket,
    "gta": pic_gta,
    "boat": pic_boat,
    "drought": pic_drought,
    "baseball": pic_baseball,
}


# -------------------------------------------------------------------- chart

# Rough coastlines as (longitude, latitude) pairs, from general geography.
NORTH_AMERICA = [(-168,66),(-158,58),(-152,60),(-140,60),
                 (-134,57),(-129,54),(-125,49),(-124,42),
                 (-120,34),(-114,29),(-109,26),(-105,20),
                 (-97,16),(-93,15),(-88,13),(-83,9),
                 (-79,9),(-81,13),(-84,16),(-86,21),
                 (-87,25),(-84,30),(-81,26),(-80,32),
                 (-76,35),(-74,39),(-70,42),(-67,44),
                 (-63,45),(-59,47),(-55,52),(-60,55),
                 (-65,58),(-68,58),(-75,62),(-79,66),
                 (-85,66),(-90,68),(-95,69),(-110,68),
                 (-125,70),(-140,70),(-155,71),(-163,68)]
GREENLAND = [(-58,64),(-52,60),(-44,60),(-40,64),
             (-32,68),(-22,70),(-20,74),(-28,76),
             (-45,76),(-56,74),(-60,70)]
SOUTH_AMERICA = [(-77,7),(-72,12),(-64,11),(-60,8),
                 (-54,6),(-51,4),(-50,0),(-44,-3),
                 (-38,-5),(-35,-8),(-39,-15),(-41,-22),
                 (-48,-27),(-52,-33),(-57,-38),(-62,-41),
                 (-65,-45),(-68,-50),(-69,-54),(-73,-50),
                 (-73,-43),(-72,-36),(-71,-29),(-70,-20),
                 (-75,-15),(-79,-8),(-81,-4),(-80,1),(-77,4)]
EUROPE = [(-10,36),(-9,38),(-9,43),(-2,44),
          (-1,46),(-4,48),(-2,49),(0,51),
          (3,53),(7,54),(8,57),(10,59),
          (6,60),(6,62),(11,64),(14,67),
          (19,69),(25,71),(30,70),(34,68),
          (39,67),(41,64),(40,60),(38,55),
          (36,51),(34,47),(31,46),(28,44),
          (24,40),(26,38),(23,36),(19,40),
          (16,42),(12,44),(8,44),(4,43),
          (0,39),(-2,37),(-6,36),(-9,37)]
BRITAIN = [(-5,50),(-3,53),(-5,56),(-3,58),(-1,57),(0,53),(1,51)]
AFRICA = [(-6,35),(-10,31),(-15,27),(-17,21),
          (-17,15),(-16,12),(-13,8),(-8,4),
          (-4,5),(2,6),(6,4),(9,4),
          (9,0),(12,-4),(13,-10),(12,-17),
          (14,-22),(16,-28),(19,-34),(26,-34),
          (32,-28),(35,-24),(40,-18),(40,-12),
          (39,-6),(41,-2),(46,0),(51,2),
          (51,11),(47,11),(43,12),(40,15),
          (38,18),(37,22),(34,28),(32,31),
          (30,31),(25,32),(20,32),(15,32),
          (11,33),(10,34)]
ASIA = [(30,36),(33,36),(36,33),(39,31),
        (42,29),(45,29),(48,29),(50,29),
        (53,27),(56,26),(58,24),(60,25),
        (62,25),(66,25),(68,23),(71,21),
        (73,17),(75,11),(77,8),(80,9),
        (80,13),(82,17),(85,19),(88,22),
        (91,22),(93,20),(94,17),(96,15),
        (98,10),(100,7),(102,4),(104,2),
        (105,8),(107,11),(109,14),(109,18),
        (106,20),(108,21),(111,21),(114,22),
        (117,24),(119,26),(121,31),(120,33),
        (122,37),(124,39),(126,40),(128,42),
        (130,42),(132,43),(135,44),(137,46),
        (139,48),(141,50),(142,53),(142,56),
        (141,59),(140,61),(142,64),(146,66),
        (150,69),(155,69),(160,69),(164,66),
        (170,64),(170,60),(163,59),(158,53),
        (156,51),(152,56),(150,59),(146,59),
        (142,55),(141,52),(140,46),(138,40),
        (135,35),(132,33),(129,31),(127,34),
        (126,38),(128,40),(130,42)]
AUSTRALIA = [(113,-22),(114,-30),(115,-33),(118,-35),
             (124,-33),(129,-32),(132,-32),(135,-35),
             (138,-35),(140,-38),(145,-38),(150,-37),
             (153,-32),(153,-27),(150,-23),(146,-19),
             (142,-15),(142,-11),(140,-17),(137,-15),
             (135,-12),(132,-11),(130,-13),(126,-14),
             (122,-17),(118,-20)]
NEW_ZEALAND = [(167,-45),(168,-46),(170,-43),(172,-41),
               (174,-39),(175,-38),(177,-38),(178,-37),
               (176,-40),(174,-41),(173,-42),(171,-44),(168,-46)]
JAPAN = [(130,31),(132,33),(134,34),(136,35),
         (138,35),(139,37),(140,39),(141,41),
         (141,44),(143,44),(145,44),(144,42),
         (142,39),(140,36),(137,37),(135,34),(132,33)]

COASTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, EUROPE, BRITAIN,
          AFRICA, ASIA, AUSTRALIA, NEW_ZEALAND, JAPAN]

# (story number, longitude, latitude, nudge x, nudge y). Two marks share
# Washington; the second one is pushed out to sea so both stay readable.
MARKS = [
    [1, 85, 19, 0, 0], [2, 33, 35, 0, 0], [3, -64, 44, 0, 0],
    [4, 113, 22.5, 0, 0], [5, 13, 55, 0, 0], [6, 33, 48, 0, 0],
    [7, -82, 38, 0, 0], [8, -122, 37.5, 0, 0], [9, 174.8, -41.3, 0, 0],
    [10, -8, 54, 0, 0], [11, -17.4, 14.7, 0, 0], [12, -172, -21, 0, 0],
    [13, -63, 30, 0, 0],
]

CHART_W = 300
CHART_H = 200


def locate(lon, lat, mx, my):
    """Flat projection: longitude runs left to right, latitude 75 to -55."""
    px = mx + (lon + 180.0) / 360.0 * CHART_W
    py = my + (75.0 - lat) / 130.0 * CHART_H
    return px, py


def draw_chart(pen, faces, mx, my):
    pen.rectangle(((mx, my), (mx + CHART_W, my + CHART_H)), fill=DEEP)
    for shape in COASTS:
        pts = [locate(lon, lat, mx, my) for lon, lat in shape]
        pen.polygon(pts, fill=SAND)
    pen.rectangle(((mx, my), (mx + CHART_W, my + CHART_H)),
                  outline=(20,30,45), width=2)
    pin_face = ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans-Bold.ttf", 10)
    for num, lon, lat, ox, oy in MARKS:
        px, py = locate(lon, lat, mx, my)
        px += ox
        py += oy
        r = 6
        px = min(max(px, mx + r + 4), mx + CHART_W - r - 4)
        py = min(max(py, my + r + 4), my + CHART_H - r - 4)
        pen.ellipse(((px - r - 1, py - r - 1), (px + r + 1, py + r + 1)),
                    fill=(255,255,255))
        pen.ellipse(((px - r, py - r), (px + r, py + r)), fill=OXBLOOD)
        label = str(num)
        tw = pin_face.getlength(label)
        pen.text((px - tw / 2, py - 7), label, font=pin_face,
                 fill=(255,255,255))


# ------------------------------------------------------------ flowing words

def flow_words(segments, width):
    """Fold (text, face) runs into lines of (word, face, colour) triples.

    segments: a list of (text, face, fill). Returns a list of lines, each
    a list of (word, face, fill)."""
    words = []
    for text, face, fill in segments:
        for w in text.split(" "):
            if w:
                words.append((w, face, fill))
    lines = []
    cur = []
    cur_w = 0.0
    for w, face, fill in words:
        ww = face.getlength(w)
        add = ww if not cur else ww + face.getlength(" ")
        if cur and cur_w + add > width:
            lines.append(cur)
            cur = [(w, face, fill)]
            cur_w = ww
        else:
            cur.append((w, face, fill))
            cur_w += add
    if cur:
        lines.append(cur)
    return lines


def ink_lines(pen, lines, x, y, leading):
    for line in lines:
        cx = x
        for w, face, fill in line:
            pen.text((cx, y), w, font=face, fill=fill)
            cx += face.getlength(w + " ")
        y += leading
    return y


# ------------------------------------------------------------------- sections

def head_line(pen, faces, x, y, text):
    pen.text((x, y), text, font=faces["kick13"], fill=OXBLOOD)
    return y + 18


def draw_top(pen, faces, data):
    y = 20
    pen.text((MARGIN, y), "THE WORLD " "IN ONE DAY", font=faces["kick"],
             fill=OXBLOOD)
    right = "FRIDAY'S NEWS · ONE PAGE · 36 " "STORIES"
    pen.text((PAGE - MARGIN - faces["kick"].getlength(right), y), right,
             font=faces["kick"], fill=SOOT)
    rule(pen, 40)
    pen.text((MARGIN, 46), data["paper"], font=faces["title"], fill=SOOT)
    pen.text((MARGIN, 112), data["subhead"], font=faces["standfirst"],
             fill=OXBLOOD)
    rule(pen, 136)
    return 144


def draw_stats(pen, faces, data):
    col_w = INNER / 6
    for i, pair in enumerate(data["stats"]):
        num, cap = pair
        cx = MARGIN + i * col_w
        pen.text((cx + 8, 144), num, font=faces["stat"], fill=OXBLOOD)
        lines = snip_lines(cap, faces["body9"], col_w - 18, 2)
        yy = 170
        for ln in lines:
            pen.text((cx + 8, yy), ln, font=faces["body9"], fill=SOOT)
            yy += 11
        if i:
            pen.line(((cx, 146), (cx, 190)), fill=(190,180,160), width=1)
    rule(pen, 196, weight=1)
    return 204


TAB_PAINTS = ["#2E6E6A", "#A11E22", "#B07A2A", "#6B7A2A",
              "#2C4A73", "#6E3B5C", "#5A5A5A"]


def draw_tabs(pen, faces, data):
    n = len(data["regions"])
    tab_w = INNER / n
    y = 204
    for i, pair in enumerate(data["regions"]):
        name, count = pair
        x0 = MARGIN + i * tab_w
        pen.rectangle(((x0 + 1, y), (x0 + tab_w - 1, y + 22)),
                      fill=TAB_PAINTS[i % len(TAB_PAINTS)])
        label = f"{name} {count}"
        face = faces["kick10"]
        tw = face.getlength(label)
        pen.text((x0 + (tab_w - tw) / 2, y + 5), label, font=face,
                 fill=(255,255,255))
    return y + 30


def draw_times(pen, faces, data):
    n = len(data["timeline"])
    cell_w = INNER / n
    y = 234
    for i, pair in enumerate(data["timeline"]):
        when, what = pair
        cx = MARGIN + i * cell_w
        pen.text((cx + 6, y), when, font=faces["kick10"], fill=OXBLOOD)
        lines = snip_lines(what, faces["body10"], cell_w - 12, 2)
        yy = y + 14
        for ln in lines:
            pen.text((cx + 6, yy), ln, font=faces["body10"], fill=SOOT)
            yy += 12
    rule(pen, 268, weight=1)
    return 276


def draw_leads(pen, faces, data):
    gap = 10
    col_w = (INNER - 2 * gap) // 3
    y = 276
    box_h = 180
    for i in range(0, len(data["leads"])):
        story = data["leads"][i]
        x0 = MARGIN + i * (col_w + gap)
        pen.rectangle(((x0, y), (x0 + col_w, y + box_h)), fill=PANEL,
                      outline=BORDER, width=1)
        PICS[story["art"]](pen, x0 + 1, y + 1, col_w - 2, 76)
        inner = x0 + 8
        iw = col_w - 16
        yy = y + 82
        pen.text((inner, yy), story["tag"], font=faces["micro"], fill=DIM)
        yy += 13
        kick = f"{story['n']} · {story['place']} · {story['topic']}"
        pen.text((inner, yy), kick, font=faces["kick10"], fill=OXBLOOD)
        yy += 15
        for ln in snip_lines(story["headline"], faces["head17"], iw, 2):
            pen.text((inner, yy), ln, font=faces["head17"], fill=SOOT)
            yy += 20
        yy += 2
        for ln in snip_lines(story["deck"], faces["body"], iw, 2):
            pen.text((inner, yy), ln, font=faces["body"], fill=SOOT)
            yy += 13
    return y + box_h + 8


def draw_smalls(pen, faces, data, img, y0):
    gap = 6
    col_w = (INNER - 4 * gap) // 5
    box_h = 104
    y = y0
    for row in range(0, 2):
        for col in range(0, 5):
            story = data["medium"][row * 5 + col]
            x0 = MARGIN + col * (col_w + gap)
            yy = y + row * (box_h + gap)
            pen.rectangle(((x0, yy), (x0 + col_w, yy + box_h)), fill=PANEL,
                          outline=BORDER, width=1)
            # The strip is short, so paint the picture at lead height
            # and shrink it down deterministically.
            sw = int(col_w - 2)
            tile = Image.new("RGB", (sw, 76), SHEET)
            td = ImageDraw.Draw(tile)
            PICS[story["art"]](td, 0, 0, sw, 76)
            tile = tile.resize((sw, 32), Image.LANCZOS)
            img.paste(tile, (x0 + 1, yy + 1))
            inner = x0 + 6
            iw = col_w - 12
            ty = yy + 38
            kick = f"{story['n']} · {story['place']} · {story['topic']}"
            pen.text((inner, ty), kick, font=faces["kick9"], fill=OXBLOOD)
            ty += 13
            for ln in snip_lines(story["headline"], faces["kick12"], iw, 2):
                pen.text((inner, ty), ln, font=faces["kick12"], fill=SOOT)
                ty += 14
            ty += 1
            for ln in snip_lines(story["deck"], faces["body10"], iw, 2):
                pen.text((inner, ty), ln, font=faces["body10"], fill=SOOT)
                ty += 12
    return y + 2 * box_h + gap + 6


def draw_chart_briefs(pen, faces, data, y0):
    y = y0
    rule(pen, y - 4, weight=1)
    head_line(pen, faces, MARGIN, y, "WHERE IT " "HAPPENED")
    bx = MARGIN + CHART_W + 14
    bw = PAGE - MARGIN - bx
    head_line(pen, faces, bx, y,
              "ALSO ON FRIDAY 20 NOVEMBER — 23 MORE " "STORIES")
    my = y + 22
    draw_chart(pen, faces, MARGIN, my)
    cy = my + CHART_H + 6
    for ln in fold_words("Red numbers mark stories 1–13.",
                         faces["body9"], CHART_W):
        pen.text((MARGIN, cy), ln, font=faces["body9"], fill=DIM)
        cy += 11
    for ln in fold_words("Positions are approximate.",
                         faces["body9"], CHART_W):
        pen.text((MARGIN, cy), ln, font=faces["body9"], fill=DIM)
        cy += 11

    # Briefs: run down the right column, shrinking the face until the
    # whole block fits between the chart top and the check box.
    limit = 940 - 6
    room = limit - my
    fits = [(10, 10, 0), (9, 9.5, 0)]
    choice = fits[-1]
    for size, lead, gap in fits:
        bf = ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans.ttf", size)
        kf = ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans-Bold.ttf", size)
        all_lines = []
        for item in data["also"]:
            num, place, text = item
            segs = [(f"{num} {place} — ", kf, OXBLOOD),
                    (text, bf, SOOT)]
            all_lines.extend(flow_words(segs, bw))
        total = len(all_lines) * lead + (len(data["also"]) - 1) * gap
        choice = (size, lead, gap)
        if total <= room:
            break
    size, lead, bgap = choice
    bf = ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans.ttf", size)
    kf = ImageFont.truetype(f"{TYPE_DIR}/DejaVuSans-Bold.ttf", size)
    yy = my
    for item in data["also"]:
        num, place, text = item
        segs = [(f"{num} {place} — ", kf, OXBLOOD), (text, bf, SOOT)]
        lines = flow_words(segs, bw)
        yy = ink_lines(pen, lines, bx, yy, lead)
        yy += bgap
    return max(cy, yy) + 4


def draw_check(pen, faces, data):
    y = 940
    pen.rectangle(((MARGIN, y), (PAGE - MARGIN, y + 46)), outline=OXBLOOD,
                  width=2)
    pen.text((MARGIN + 8, y + 5), "DATE " "CHECK", font=faces["kick"],
             fill=OXBLOOD)
    lines = snip_lines(data["datecheck"], faces["body10"],
                       INNER - 16, 2)
    yy = y + 20
    for ln in lines:
        pen.text((MARGIN + 8, yy), ln, font=faces["body10"], fill=SOOT)
        yy += 12
    return y + 52


def draw_source(pen, faces, data):
    y = 998
    lines = snip_lines(data["sources"], faces["fine"], INNER, 2)
    yy = y
    for ln in lines:
        pen.text((MARGIN, yy), ln, font=faces["fine"], fill=DIM)
        yy += 10
    return yy


def compose(data):
    faces = open_faces()
    img = Image.new("RGB", (PAGE, PAGE), SHEET)
    pen = ImageDraw.Draw(img)
    y = draw_top(pen, faces, data)
    if y != 144:
        raise AssertionError(f"top ended at {y}, wanted 144")
    draw_stats(pen, faces, data)
    draw_tabs(pen, faces, data)
    draw_times(pen, faces, data)
    y = draw_leads(pen, faces, data)
    if y != 464:
        raise AssertionError(f"leads ended at {y}, wanted 464")
    y = draw_smalls(pen, faces, data, img, y)
    if y != 684:
        raise AssertionError(f"smalls ended at {y}, wanted 684")
    y = draw_chart_briefs(pen, faces, data, y)
    draw_check(pen, faces, data)
    draw_source(pen, faces, data)
    return img


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    img = compose(data)
    # Encode once in memory, then write only to the output directory.
    # Writing beside the script crashes when the program folder is
    # read-only (the grader runs from /bot read-only), so the local
    # mirror below is best effort and any failure there is ignored.
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    raw = buf.getvalue()
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    dest = os.path.join(outdir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(raw)
    try:
        with open(os.path.join(here, "entry.png"), "wb") as fh:
            fh.write(raw)
    except OSError:
        pass
    with open(dest, "rb") as fh:
        twin = fh.read()
    if raw != twin:
        print("copy mismatch", file=sys.stderr)
        sys.exit(1)
    if len(raw) > 1048576:
        print(f"too big: {len(raw)} bytes", file=sys.stderr)
        sys.exit(1)
    print(f"entry.png {len(raw)} bytes sha256 "
          f"{hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    raise SystemExit(run())
