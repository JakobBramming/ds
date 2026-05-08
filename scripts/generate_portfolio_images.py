from math import cos, pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


COLORS = {
    "bg": (234, 234, 234),
    "panel": (248, 248, 248),
    "ink": (54, 58, 61),
    "muted": (118, 119, 116),
    "blue": (68, 124, 179),
    "teal": (12, 125, 121),
    "green": (139, 209, 175),
    "cyan": (117, 208, 207),
    "gold": (227, 173, 118),
    "brown": (122, 65, 12),
    "olive": (168, 168, 60),
    "lightblue": (173, 216, 228),
}


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


FONT_SM = font(15)
FONT_MD = font(20)
FONT_LG = font(30)
FONT_BOLD = font(18, True)
FONT_TITLE = font(34)


def rounded(draw, box, fill, outline=None, radius=8, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, fill=None, fnt=None, anchor=None):
    draw.text(xy, value, fill=fill or COLORS["ink"], font=fnt or FONT_SM, anchor=anchor)


def pie(draw, center, radius, values, colors):
    total = sum(values)
    start = -90
    for value, color in zip(values, colors):
        angle = value / total * 360
        draw.pieslice(
            (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius),
            start,
            start + angle,
            fill=color,
        )
        start += angle


def line_chart(draw, box, series, colors, labels):
    x0, y0, x1, y1 = box
    draw.line((x0, y1, x1, y1), fill=(190, 190, 190), width=2)
    draw.line((x0, y0, x0, y1), fill=(190, 190, 190), width=2)
    for i in range(5):
        y = y0 + i * (y1 - y0) / 4
        draw.line((x0, y, x1, y), fill=(218, 218, 218), width=1)
    max_value = max(max(values) for values in series)
    for values, color in zip(series, colors):
        pts = []
        for idx, value in enumerate(values):
            x = x0 + idx * (x1 - x0) / (len(values) - 1)
            y = y1 - value / max_value * (y1 - y0)
            pts.append((x, y))
        draw.line(pts, fill=color, width=3, joint="curve")
        for point in pts:
            draw.ellipse((point[0] - 4, point[1] - 4, point[0] + 4, point[1] + 4), fill=color)
    for idx, label in enumerate(labels):
        x = x0 + idx * (x1 - x0) / (len(labels) - 1)
        text(draw, (x, y1 + 18), label, COLORS["muted"], FONT_SM, "mm")


def dashboard_base(width=1380, height=1120, title="Car Accidents"):
    img = Image.new("RGB", (width, height), COLORS["bg"])
    draw = ImageDraw.Draw(img)
    text(draw, (18, 12), title, COLORS["ink"], FONT_TITLE)
    filters = ["Accident Type", "Road Conditions", "Fatal or Injury", "Road Category"]
    for idx, label in enumerate(filters):
        x = 18 + idx * 335
        text(draw, (x, 58), label, COLORS["ink"], FONT_BOLD)
        rounded(draw, (x, 78, x + 310, 116), (250, 250, 250), (196, 196, 196), 4)
        text(draw, (x + 14, 97), "All", COLORS["muted"], FONT_SM, "lm")
        draw.polygon([(x + 285, 94), (x + 296, 94), (x + 290, 101)], fill=(150, 150, 150))
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    for idx, month in enumerate(months):
        x = 276 + idx * 68
        rounded(draw, (x, 126, x + 60, 170), COLORS["lightblue"], None, 9)
        text(draw, (x + 30, 148), month, (0, 0, 0), FONT_SM, "mm")
    return img, draw


def draw_synthetic_map(draw, box, points=False):
    x0, y0, x1, y1 = box
    rounded(draw, box, (222, 229, 231), (40, 115, 215), 0)
    shapes = [
        [(70, 70), (160, 42), (244, 110), (210, 210), (276, 324), (178, 462), (88, 390), (44, 240)],
        [(308, 70), (444, 112), (426, 250), (354, 278), (338, 408), (270, 432), (256, 302), (292, 188)],
        [(80, 382), (166, 400), (142, 492), (54, 472)],
    ]
    for shape in shapes:
        pts = [(x0 + px * (x1 - x0) / 520, y0 + py * (y1 - y0) / 520) for px, py in shape]
        draw.polygon(pts, fill=(249, 240, 198), outline=(70, 70, 70))
    if points:
        for i in range(160):
            sx = (i * 73 % 500) + 10
            sy = (i * 131 % 500) + 10
            color = [COLORS["gold"], COLORS["teal"], COLORS["brown"], COLORS["blue"]][i % 4]
            px = x0 + sx * (x1 - x0) / 520
            py = y0 + sy * (y1 - y0) / 520
            draw.ellipse((px - 3, py - 3, px + 3, py + 3), fill=color)
    else:
        for i in range(22):
            sx = (i * 113 % 430) + 45
            sy = (i * 79 % 410) + 58
            intensity = 90 + (i * 31 % 120)
            px = x0 + sx * (x1 - x0) / 520
            py = y0 + sy * (y1 - y0) / 520
            draw.ellipse((px - 9, py - 9, px + 9, py + 9), fill=(170, 100, 35 + intensity // 6))


def make_dashboard_municipality():
    img, draw = dashboard_base()
    rounded(draw, (20, 206, 160, 252), COLORS["lightblue"], None, 8)
    text(draw, (90, 230), "Municipality Map", (0, 0, 0), FONT_SM, "mm")
    rounded(draw, (190, 206, 310, 252), (240, 240, 240), (190, 190, 190), 8)
    text(draw, (250, 230), "Incident Map", COLORS["ink"], FONT_SM, "mm")
    draw_synthetic_map(draw, (28, 300, 578, 830), points=False)
    text(draw, (742, 306), "Road Conditions in Slagelse", COLORS["ink"], FONT_MD)
    pie(draw, (880, 420), 86, [64, 24, 7, 3, 2], [COLORS["gold"], COLORS["blue"], COLORS["olive"], COLORS["cyan"], COLORS["teal"]])
    text(draw, (1048, 306), "Accident Types in Slagelse", COLORS["ink"], FONT_MD)
    pie(draw, (1170, 420), 82, [31, 22, 18, 13, 10, 6], [COLORS["blue"], COLORS["brown"], COLORS["teal"], COLORS["green"], COLORS["cyan"], COLORS["olive"]])
    rounded(draw, (690, 570, 1320, 832), COLORS["panel"], None, 0)
    text(draw, (980, 602), "Road condition comparison", COLORS["ink"], FONT_MD, "mm")
    labels = ["Turning", "Straight", "Single", "Pedestrian", "Head-on", "Parked"]
    for idx, label in enumerate(labels):
        y = 650 + idx * 30
        text(draw, (875, y + 8), label, COLORS["ink"], FONT_SM, "ra")
        draw.rectangle((925, y, 925 + [120, 180, 220, 250, 132, 92][idx], y + 18), fill=COLORS["gold"])
        draw.rectangle((925 - [45, 84, 72, 110, 38, 24][idx], y, 925, y + 18), fill=COLORS["blue"])
    rounded(draw, (20, 860, 1330, 900), (250, 250, 250), (196, 196, 196), 4)
    text(draw, (34, 880), "Accident Type", COLORS["ink"], FONT_SM, "lm")
    text(draw, (88, 942), "Accidents over Months by Accident Type in Slagelse", COLORS["ink"], FONT_MD)
    line_chart(
        draw,
        (86, 982, 1270, 1090),
        [[5, 4, 2, 6, 1, 5, 3, 4, 2, 1, 6, 2], [3, 1, 4, 2, 5, 1, 2, 3, 5, 2, 1, 4], [2, 3, 2, 1, 4, 2, 1, 2, 1, 3, 2, 1]],
        [COLORS["blue"], COLORS["teal"], COLORS["brown"]],
        ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"],
    )
    img.save(ASSETS / "dashboard-municipality.png", quality=92)


def make_dashboard_incident():
    img, draw = dashboard_base(height=720, title="Car Accidents - Incident View")
    draw_synthetic_map(draw, (0, 0, 480, 720), points=True)
    text(draw, (505, 24), "road_type", COLORS["ink"], FONT_SM)
    for idx, label in enumerate(["Municipal Road", "State road", "Private Shared Road", "Other State Road"]):
        y = 44 + idx * 22
        draw.ellipse((506, y - 5, 516, y + 5), fill=[COLORS["gold"], (125, 45, 150), COLORS["teal"], COLORS["olive"]][idx])
        text(draw, (530, y), label, COLORS["ink"], FONT_SM, "lm")
    text(draw, (720, 24), "Road Conditions", COLORS["ink"], FONT_MD)
    pie(draw, (860, 122), 76, [70, 21, 4, 3, 2], [COLORS["gold"], COLORS["blue"], COLORS["olive"], COLORS["cyan"], COLORS["teal"]])
    text(draw, (1020, 24), "Accident Types", COLORS["ink"], FONT_MD)
    pie(draw, (1140, 122), 76, [28, 21, 19, 15, 11, 6], [COLORS["blue"], COLORS["brown"], COLORS["teal"], COLORS["green"], COLORS["cyan"], COLORS["olive"]])
    rounded(draw, (665, 350, 1310, 680), COLORS["panel"], None, 0)
    text(draw, (988, 392), "Accident Details", COLORS["ink"], FONT_LG, "mm")
    details = [
        ("Month:", "oct"),
        ("Road Type:", "Municipal Road"),
        ("Accident Type:", "Single vehicle accident"),
        ("Road Conditions:", "Dry"),
        ("Fatal Accident:", "No"),
        ("Municipality:", "Faaborg-Midtfyn"),
    ]
    for idx, (key, value) in enumerate(details):
        y = 442 + idx * 28
        text(draw, (688, y), key, COLORS["ink"], FONT_BOLD)
        text(draw, (955, y), value, COLORS["ink"], FONT_SM)
    img.save(ASSETS / "dashboard-incident-map.png", quality=92)


def make_project_images():
    for name, mode in [("project-thesis.png", "optimization"), ("project-dashboard.png", "dashboard")]:
        img = Image.new("RGB", (900, 420), (231, 238, 233) if mode == "optimization" else (236, 235, 233))
        draw = ImageDraw.Draw(img)
        if mode == "optimization":
            for i in range(5):
                draw.line((80 + i * 160, 40, 40 + i * 180, 380), fill=(210, 220, 214), width=2)
            route = [(120, 220), (250, 90), (410, 120), (520, 260), (700, 150), (780, 255)]
            draw.line(route, fill=COLORS["teal"], width=8, joint="curve")
            draw.line([(120, 220), (330, 300), (520, 260), (650, 330), (780, 255)], fill=COLORS["gold"], width=8)
            for x, y in route:
                draw.ellipse((x - 18, y - 18, x + 18, y + 18), fill=(255, 253, 247), outline=COLORS["teal"], width=5)
            draw.ellipse((92, 192, 148, 248), fill=(23, 32, 27))
            text(draw, (56, 318), "routing scenarios", COLORS["muted"], FONT_LG)
        else:
            rounded(draw, (58, 48, 418, 344), (247, 247, 247), (215, 215, 215), 8)
            draw_synthetic_map(draw, (82, 80, 392, 320), points=False)
            rounded(draw, (460, 48, 825, 182), (247, 247, 247), (215, 215, 215), 8)
            pie(draw, (550, 114), 50, [31, 26, 21, 14, 8], [COLORS["blue"], COLORS["gold"], COLORS["teal"], COLORS["green"], COLORS["brown"]])
            rounded(draw, (460, 210, 825, 344), (247, 247, 247), (215, 215, 215), 8)
            for i, h in enumerate([46, 72, 94, 56, 82]):
                draw.rectangle((500 + i * 54, 318 - h, 532 + i * 54, 318), fill=[COLORS["blue"], COLORS["teal"], COLORS["gold"], COLORS["brown"], COLORS["green"]][i])
            text(draw, (58, 386), "interactive dashboard", COLORS["muted"], FONT_LG)
        img.save(ASSETS / name, quality=92)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    make_dashboard_municipality()
    make_dashboard_incident()
    make_project_images()
