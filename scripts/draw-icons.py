#!/usr/bin/env python3
"""Draw native 512px Hyrule pixel icons with Pillow; no bitmap upscaling.

Each geometric primitive is rasterized directly on the 512px output canvas.
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / "icons/Hyrule-Icons/512x512"
S = 512
GRID = 16

class PixelDraw:
    """Map the original 32-unit design grid onto the native 512px canvas."""
    def __init__(self, draw):
        self.draw = draw

    @staticmethod
    def point(value):
        return tuple(int(v * GRID) for v in value)

    def rectangle(self, xy, **kwargs):
        if kwargs.get("outline") is not None:
            kwargs["width"] = GRID
        self.draw.rectangle(self.point(xy), **kwargs)

    def ellipse(self, xy, **kwargs):
        if kwargs.get("outline") is not None:
            kwargs["width"] = GRID
        self.draw.ellipse(self.point(xy), **kwargs)

    def polygon(self, xy, **kwargs):
        if kwargs.get("outline") is not None:
            kwargs["width"] = GRID
        self.draw.polygon([self.point(p) for p in xy], **kwargs)

    def line(self, xy, **kwargs):
        self.draw.line([self.point(p) for p in xy], width=kwargs.pop("width", 1) * GRID, **kwargs)

    def arc(self, xy, start, end, **kwargs):
        self.draw.arc(self.point(xy), start, end, width=kwargs.pop("width", 1) * GRID, **kwargs)
P = {
    "ink": "#241B12", "deep": "#09291D", "forest": "#123F2B",
    "green": "#28783C", "light_green": "#70A85A", "gold": "#E5B83E",
    "gold_dark": "#9A6724", "paper": "#F2D49A", "cream": "#FFF3D2",
    "blue": "#4D91A5", "red": "#A94332", "shadow": "#171B18",
    "white": "#FFF8E8", "grey": "#77766A",
}

def canvas():
    return Image.new("RGBA", (S, S), (0, 0, 0, 0))

def rect(d, xy, color, outline=None):
    d.rectangle(xy, fill=color, outline=outline)

def outline(d, xy, color="ink", width=1):
    d.rectangle(xy, outline=P[color], width=width)

def frame(d, x1=5, y1=4, x2=26, y2=27, fill="paper"):
    rect(d, (x1, y1, x2, y2), P[fill], P["ink"])
    rect(d, (x1+2, y1+2, x2-2, y1+2), P["cream"])

def draw_icon(name):
    im, d = canvas(), None
    d = PixelDraw(ImageDraw.Draw(im))
    # Consistent ground shadow and 32-bit JRPG palette.
    rect(d, (7, 27, 24, 28), P["shadow"])
    if name == "org.gnome.Nautilus":
        # Hylian treasure chest / file manager
        rect(d, (5, 10, 26, 26), P["gold_dark"], P["ink"])
        rect(d, (6, 8, 25, 16), P["gold"], P["ink"])
        rect(d, (8, 10, 23, 14), P["cream"])
        rect(d, (6, 17, 25, 24), P["forest"])
        rect(d, (14, 15, 17, 21), P["gold"], P["ink"])
        rect(d, (15, 17, 16, 19), P["ink"])
        rect(d, (9, 20, 12, 22), P["light_green"])
    elif name == "org.gnome.Settings":
        # Gear with a Triforce-like center
        d.ellipse((8, 7, 23, 22), fill=P["gold"], outline=P["ink"])
        for x,y in [(14,4),(14,22),(4,14),(22,14),(7,7),(20,7),(7,20),(20,20)]:
            rect(d, (x,y,x+3,y+3), P["gold"], P["ink"])
        d.ellipse((12, 11, 19, 18), fill=P["forest"], outline=P["ink"])
        d.polygon([(15,12),(12,17),(18,17)], fill=P["cream"], outline=P["ink"])
    elif name == "org.gnome.Software":
        # Potion shop bag with rupee
        rect(d, (7, 9, 24, 25), P["forest"], P["ink"])
        d.arc((11, 3, 21, 15), 180, 360, fill=P["gold"], width=2)
        d.polygon([(16,11),(20,17),(16,23),(12,17)], fill=P["blue"], outline=P["cream"])
        rect(d, (15, 15, 17, 18), P["white"])
    elif name == "org.gnome.Calculator":
        frame(d, 7, 4, 24, 27, "forest")
        rect(d, (10,7,21,11), P["paper"], P["ink"])
        for x,y in [(10,14),(15,14),(20,14),(10,19),(15,19),(20,19)]:
            rect(d, (x,y,x+2,y+2), P["gold"] if (x+y)%2 else P["cream"], P["ink"])
        rect(d, (10,24,21,25), P["blue"])
    elif name == "org.gnome.Calendar":
        frame(d, 5, 6, 26, 26, "paper")
        rect(d, (5,6,26,12), P["red"], P["ink"])
        rect(d, (10,3,12,9), P["gold"], P["ink"])
        rect(d, (20,3,22,9), P["gold"], P["ink"])
        for x,y in [(9,15),(15,15),(21,15),(9,20),(15,20),(21,20)]:
            rect(d, (x,y,x+2,y+2), P["forest"] if y==15 else P["gold_dark"])
        rect(d, (14,19,17,22), P["red"])
    elif name == "utilities-terminal":
        frame(d, 4, 6, 27, 25, "forest")
        rect(d, (6,8,25,11), P["gold_dark"])
        d.polygon([(9,14),(13,17),(9,20),(11,21),(16,17),(11,13)], fill=P["cream"])
        rect(d, (17,20,22,21), P["gold"])
    elif name == "org.gnome.TextEditor":
        frame(d, 7, 4, 24, 27, "paper")
        d.polygon([(18,4),(24,10),(18,10)], fill=P["gold"], outline=P["ink"])
        rect(d, (11,13,20,15), P["forest"])
        rect(d, (11,17,21,18), P["forest"])
        rect(d, (11,20,18,21), P["forest"])
        rect(d, (18,22,23,24), P["gold_dark"], P["ink"])
    elif name == "org.gnome.Loupe":
        d.ellipse((5,5,21,21), fill=P["blue"], outline=P["ink"])
        d.ellipse((9,9,17,17), fill=P["cream"], outline=P["gold_dark"])
        rect(d, (19,19,25,25), P["gold_dark"], P["ink"])
        rect(d, (21,21,24,24), P["gold"])
        rect(d, (10,8,14,9), P["white"])
    elif name == "org.gnome.clocks":
        d.ellipse((5,5,26,26), fill=P["paper"], outline=P["ink"])
        d.ellipse((8,8,23,23), outline=P["gold_dark"])
        rect(d, (15,10,16,16), P["forest"])
        rect(d, (15,15,21,16), P["red"])
        rect(d, (10,3,12,6), P["gold"], P["ink"])
        rect(d, (20,3,22,6), P["gold"], P["ink"])
    elif name == "org.gnome.Music":
        rect(d, (7,6,24,25), P["forest"], P["ink"])
        rect(d, (10,9,21,18), P["gold_dark"], P["ink"])
        d.polygon([(12,17),(16,12),(20,17)], fill=P["cream"])
        d.ellipse((10,19,15,24), fill=P["gold"], outline=P["ink"])
        d.ellipse((18,19,23,24), fill=P["gold"], outline=P["ink"])
    elif name == "org.gnome.Maps":
        d.polygon([(4,9),(11,6),(20,9),(27,6),(27,23),(20,26),(11,23),(4,26)], fill=P["blue"], outline=P["ink"])
        rect(d, (10,8,11,22), P["cream"])
        rect(d, (19,10,20,24), P["cream"])
        d.polygon([(16,9),(20,14),(16,20),(12,14)], fill=P["red"], outline=P["cream"])
        rect(d, (15,13,17,15), P["cream"])
    elif name == "org.gnome.SystemMonitor":
        frame(d, 5, 5, 26, 26, "forest")
        rect(d, (8,9,23,22), P["deep"], P["gold"])
        d.line([(9,18),(12,18),(14,12),(17,20),(20,14),(23,14)], fill=P["light_green"], width=2)
        rect(d, (9,24,22,25), P["gold"])
    elif name == "org.gnome.Screenshot":
        rect(d, (5,9,26,24), P["grey"], P["ink"])
        rect(d, (10,7,16,10), P["gold_dark"], P["ink"])
        d.ellipse((10,11,21,22), fill=P["blue"], outline=P["ink"])
        d.ellipse((13,14,18,19), fill=P["cream"], outline=P["gold"])
        rect(d, (7,11,9,13), P["red"])
    elif name == "org.gnome.DiskUtility":
        d.ellipse((5,7,26,16), fill=P["gold"], outline=P["ink"])
        rect(d, (5,11,26,22), P["gold_dark"], P["ink"])
        d.ellipse((5,17,26,26), fill=P["gold"], outline=P["ink"])
        d.ellipse((11,18,20,23), fill=P["forest"], outline=P["ink"])
        rect(d, (14,19,17,22), P["cream"])
    elif name == "drive-harddisk":
        rect(d, (7,11,24,23), P["grey"], P["ink"])
        rect(d, (9,13,22,15), P["white"])
        rect(d, (9,17,22,20), P["gold_dark"])
        d.ellipse((19,18,22,21), fill=P["green"], outline=P["ink"])
    elif name.startswith("folder"):
        rect(d, (4,10,27,25), P["gold_dark"], P["ink"])
        rect(d, (5,8,15,13), P["gold"], P["ink"])
        rect(d, (5,13,26,23), P["paper"], P["ink"])
        rect(d, (7,15,24,21), P["gold"])
        if name == "folder-documents":
            rect(d, (11,13,21,22), P["cream"], P["ink"])
            for y in (16,18,20): rect(d, (13,y,19,y), P["gold_dark"])
        elif name == "folder-download":
            d.polygon([(14,14),(18,14),(18,18),(21,18),(16,23),(11,18),(14,18)], fill=P["green"], outline=P["ink"])
        elif name == "folder-pictures":
            rect(d, (9,14,22,22), P["blue"], P["ink"])
            d.ellipse((17,15,20,18), fill=P["gold"])
            d.polygon([(10,21),(15,16),(19,21)], fill=P["light_green"])
        elif name == "folder-music":
            rect(d, (10,14,20,21), P["forest"], P["ink"])
            rect(d, (16,13,18,19), P["gold"], P["ink"])
            d.ellipse((12,18,16,22), fill=P["gold"], outline=P["ink"])
            rect(d, (17,12,20,13), P["cream"])
        elif name == "folder-videos":
            rect(d, (9,14,22,22), P["red"], P["ink"])
            d.polygon([(13,15),(13,21),(19,18)], fill=P["cream"], outline=P["ink"])
        elif name == "drive-harddisk":
            rect(d, (7,11,24,23), P["grey"], P["ink"])
            rect(d, (9,13,22,15), P["white"])
            rect(d, (9,17,22,20), P["gold_dark"])
            d.ellipse((19,18,22,21), fill=P["green"], outline=P["ink"])
    elif name.endswith("-x-generic") or name == "application-x-executable":
        frame(d, 7, 4, 24, 27, "paper")
        d.polygon([(18,4),(24,10),(18,10)], fill=P["gold"], outline=P["ink"])
        if name.startswith("text"):
            for y,w in [(14,10),(17,12),(20,9),(23,11)]: rect(d, (10,y,10+w//2,y+1), P["forest"])
        elif name.startswith("image"):
            rect(d, (10,13,21,22), P["blue"], P["ink"])
            d.ellipse((17,14,19,16), fill=P["gold"])
            d.polygon([(11,21),(15,16),(18,20),(20,18),(21,21)], fill=P["light_green"])
        elif name.startswith("audio"):
            rect(d, (10,16,14,20), P["gold_dark"])
            d.polygon([(14,14),(22,11),(22,21),(14,23)], fill=P["gold"])
            d.ellipse((18,20,22,24), fill=P["forest"], outline=P["ink"])
        elif name.startswith("application-x-executable"):
            rect(d, (10,13,21,22), P["forest"], P["ink"])
            d.polygon([(14,15),(14,20),(19,17)], fill=P["cream"])
            rect(d, (12,11,19,12), P["gold"])
        elif name.startswith("package-x-generic"):
            d.polygon([(10,14),(16,11),(22,14),(22,21),(16,24),(10,21)], fill=P["gold_dark"], outline=P["ink"])
            d.polygon([(10,14),(16,17),(22,14),(16,11)], fill=P["cream"], outline=P["ink"])
            rect(d, (15,17,17,22), P["gold"])
        else:
            rect(d, (10,13,21,22), P["forest"], P["ink"])
            d.polygon([(14,15),(14,20),(19,17)], fill=P["cream"])
    elif name == "network-wired":
        rect(d, (10,7,21,17), P["blue"], P["ink"])
        rect(d, (12,9,19,14), P["cream"])
        rect(d, (14,17,17,23), P["gold"], P["ink"])
        rect(d, (8,23,23,25), P["gold_dark"], P["ink"])
        for x in (11,15,19): rect(d, (x,24,x+1,26), P["ink"])
    elif name == "user-trash-full":
        rect(d, (8,10,23,25), P["grey"], P["ink"])
        rect(d, (7,8,24,10), P["gold"], P["ink"])
        rect(d, (12,5,19,7), P["gold_dark"], P["ink"])
        for x in (12,17): rect(d, (x,13,x+1,22), P["cream"])
        d.ellipse((10,17,14,21), fill=P["red"], outline=P["ink"])
        d.ellipse((17,16,21,20), fill=P["red"], outline=P["ink"])
    elif name == "network-wireless":
        d.arc((5,7,27,27), 220, 320, fill=P["gold"], width=3)
        d.arc((9,11,23,25), 220, 320, fill=P["cream"], width=3)
        d.arc((13,15,19,21), 220, 320, fill=P["green"], width=2)
        rect(d, (14,23,17,26), P["gold"], P["ink"])
    elif name == "battery-full":
        rect(d, (5,10,26,23), P["paper"], P["ink"])
        rect(d, (26,14,28,19), P["gold"], P["ink"])
        rect(d, (8,13,23,20), P["green"])
        rect(d, (10,15,12,18), P["light_green"])
        rect(d, (15,15,17,18), P["light_green"])
    elif name == "bluetooth-active":
        d.polygon([(15,4),(22,10),(18,15),(23,20),(15,27),(15,18),(10,22),(8,20),(14,15),(9,10),(11,8),(15,12)], fill=P["blue"], outline=P["ink"])
        rect(d, (14,7,16,24), P["cream"])
    elif name == "user-trash":
        rect(d, (8,10,23,25), P["grey"], P["ink"])
        rect(d, (7,8,24,10), P["gold"], P["ink"])
        rect(d, (12,5,19,7), P["gold_dark"], P["ink"])
        for x in (12,17): rect(d, (x,13,x+1,22), P["cream"])
    else:
        raise ValueError(f"Unknown icon: {name}")
    # Fine pixel details: material texture, edge lighting, and readable symbols.
    if name == "org.gnome.Nautilus":
        rect(d, (8, 12, 11, 13), P["gold_dark"])
        rect(d, (20, 12, 23, 13), P["gold_dark"])
        rect(d, (8, 18, 10, 19), P["light_green"])
        rect(d, (21, 18, 23, 19), P["light_green"])
        rect(d, (7, 22, 24, 23), P["deep"])
        for x in (8, 23): rect(d, (x, 9, x+1, 10), P["white"])
    elif name == "org.gnome.Settings":
        d.ellipse((14, 13, 17, 16), fill=P["gold"], outline=P["ink"])
        for x,y in ((10,9),(20,9),(10,19),(20,19)):
            rect(d, (x,y,x+1,y+1), P["cream"])
        rect(d, (14, 5, 17, 6), P["cream"])
    elif name == "org.gnome.Software":
        rect(d, (10, 10, 21, 12), P["green"])
        rect(d, (9, 20, 11, 22), P["light_green"])
        rect(d, (21, 20, 23, 22), P["deep"])
        d.polygon([(16,12),(18,16),(16,20),(14,16)], fill=P["blue"], outline=P["white"])
        rect(d, (15, 14, 16, 16), P["white"])
    elif name == "org.gnome.Calculator":
        rect(d, (11, 8, 13, 9), P["white"])
        rect(d, (18, 8, 20, 9), P["light_green"])
        for x,y in ((10,14),(15,14),(20,14),(10,19),(15,19),(20,19)):
            rect(d, (x, y, x, y), P["white"])
        rect(d, (12, 24, 19, 24), P["light_green"])
    elif name == "org.gnome.Calendar":
        rect(d, (7, 8, 24, 9), P["red"])
        for x in (10, 20): rect(d, (x, 4, x+1, 5), P["cream"])
        for x,y in ((9,15),(15,15),(21,15),(9,20),(15,20),(21,20)):
            rect(d, (x, y, x, y), P["cream"])
        rect(d, (14, 23, 17, 24), P["gold_dark"])
    elif name == "utilities-terminal":
        for x in (8, 12, 16): d.ellipse((x, 9, x+1, 10), fill=P["cream"])
        rect(d, (7, 12, 24, 13), P["green"])
        rect(d, (18, 20, 21, 20), P["cream"])
    elif name == "org.gnome.TextEditor":
        rect(d, (9, 12, 11, 24), P["gold_dark"])
        rect(d, (12, 13, 20, 13), P["light_green"])
        rect(d, (12, 17, 21, 17), P["gold_dark"])
        rect(d, (12, 20, 18, 20), P["gold_dark"])
        rect(d, (19, 22, 22, 22), P["cream"])
    elif name == "org.gnome.Loupe":
        d.ellipse((7, 7, 19, 19), outline=P["white"])
        rect(d, (9, 8, 12, 9), P["white"])
        rect(d, (20, 20, 23, 23), P["gold"])
        rect(d, (22, 23, 26, 26), P["ink"])
    elif name == "org.gnome.clocks":
        for x,y in ((15,8),(15,22),(8,15),(22,15)):
            rect(d, (x,y,x+1,y+1), P["gold_dark"])
        rect(d, (14, 11, 15, 15), P["cream"])
        rect(d, (16, 15, 20, 16), P["red"])
        d.ellipse((14, 14, 17, 17), fill=P["gold"], outline=P["ink"])
    elif name == "org.gnome.Music":
        rect(d, (8, 7, 23, 8), P["light_green"])
        rect(d, (11, 10, 20, 11), P["gold"])
        d.line([(12, 16), (16, 13), (20, 16)], fill=P["white"], width=1)
        rect(d, (11, 20, 12, 21), P["cream"])
        rect(d, (19, 20, 20, 21), P["cream"])
    elif name == "org.gnome.Maps":
        d.line([(5, 11),(10, 9),(10, 21)], fill=P["cream"], width=1)
        d.line([(21, 10),(25, 8),(25, 21)], fill=P["gold"], width=1)
        d.polygon([(16, 10),(18, 14),(16, 18),(14, 14)], fill=P["gold"], outline=P["ink"])
        rect(d, (15, 13, 16, 14), P["white"])
    elif name == "org.gnome.SystemMonitor":
        for y in (11, 14, 17, 20):
            rect(d, (9, y, 10, y), P["gold_dark"])
        d.line([(10, 19),(12, 19),(14, 13),(17, 21),(19, 15),(22, 15)], fill=P["cream"], width=1)
        rect(d, (7, 7, 11, 8), P["light_green"])
    elif name == "org.gnome.Screenshot":
        rect(d, (7, 10, 9, 11), P["white"])
        d.ellipse((12, 13, 19, 20), outline=P["white"])
        rect(d, (15, 14, 17, 15), P["light_green"])
        rect(d, (22, 11, 24, 12), P["gold"])
    elif name == "org.gnome.DiskUtility":
        d.arc((7, 8, 24, 15), 180, 360, fill=P["cream"], width=1)
        rect(d, (8, 12, 10, 17), P["gold"])
        rect(d, (21, 12, 23, 17), P["gold_dark"])
        d.ellipse((13, 19, 18, 22), outline=P["cream"])
    elif name.startswith("folder"):
        rect(d, (6, 14, 24, 15), P["cream"])
        rect(d, (7, 22, 23, 23), P["gold_dark"])
        rect(d, (6, 10, 13, 11), P["white"])
        if name == "folder-documents":
            rect(d, (13, 14, 19, 14), P["white"])
            rect(d, (13, 18, 18, 18), P["gold"])
        elif name == "folder-download":
            rect(d, (15, 14, 16, 17), P["cream"])
            rect(d, (13, 19, 18, 20), P["light_green"])
        elif name == "folder-pictures":
            rect(d, (11, 15, 12, 16), P["white"])
            rect(d, (16, 19, 20, 20), P["green"])
    elif name.endswith("-x-generic") or name == "application-x-executable":
        rect(d, (9, 6, 10, 8), P["white"])
        rect(d, (11, 11, 20, 11), P["gold"])
        if name.startswith("text"):
            for y in (15,18,21,24): rect(d, (11, y, 19, y), P["gold_dark"])
        elif name.startswith("image"):
            rect(d, (11, 14, 12, 15), P["white"])
            rect(d, (18, 14, 19, 15), P["cream"])
        elif name.startswith("audio"):
            rect(d, (12, 17, 13, 21), P["cream"])
            rect(d, (20, 13, 21, 19), P["white"])
        elif name.startswith("application-x-executable"):
            rect(d, (11, 14, 20, 14), P["light_green"])
            rect(d, (13, 16, 18, 19), P["cream"])
        elif name.startswith("package-x-generic"):
            rect(d, (12, 14, 14, 15), P["white"])
            rect(d, (18, 14, 20, 15), P["gold"])
            rect(d, (15, 18, 16, 22), P["cream"])
        else:
            rect(d, (11, 14, 20, 14), P["light_green"])
            rect(d, (11, 21, 20, 21), P["gold"])
    elif name == "network-wired":
        rect(d, (11, 8, 20, 9), P["white"])
        rect(d, (13, 17, 14, 22), P["cream"])
        rect(d, (18, 17, 19, 22), P["cream"])
    elif name == "user-trash-full":
        d.ellipse((11,18,13,20), fill=P["red"])
        d.ellipse((18,17,20,19), fill=P["red"])
        rect(d, (9, 11, 22, 12), P["white"])
    elif name == "network-wireless":
        d.arc((7, 8, 25, 26), 220, 320, fill=P["white"], width=1)
        d.arc((11, 12, 21, 23), 220, 320, fill=P["gold"], width=1)
        rect(d, (15, 24, 16, 25), P["white"])
    elif name == "battery-full":
        rect(d, (7, 12, 24, 13), P["white"])
        rect(d, (8, 20, 23, 21), P["gold_dark"])
        rect(d, (12, 14, 13, 19), P["light_green"])
        rect(d, (19, 14, 20, 19), P["light_green"])
    elif name == "bluetooth-active":
        d.line([(16, 5),(16, 26)], fill=P["white"], width=1)
        d.line([(10, 10),(22, 20)], fill=P["cream"], width=1)
        d.line([(10, 21),(22, 10)], fill=P["cream"], width=1)
    elif name == "user-trash":
        rect(d, (9, 11, 22, 12), P["grey"])
        rect(d, (10, 23, 21, 24), P["shadow"])
        for x in (12, 17): rect(d, (x, 14, x, 21), P["white"])
        rect(d, (8, 8, 23, 8), P["cream"])
    # Restrained bevel highlights make the tiny art read clearly.
    rect(d, (6, 5, 8, 6), P["cream"])
    return im

ICONS = {
    "apps": ["org.gnome.Nautilus", "org.gnome.Settings", "org.gnome.Software",
             "org.gnome.Calculator", "org.gnome.Calendar", "utilities-terminal",
             "org.gnome.TextEditor", "org.gnome.Loupe", "org.gnome.clocks",
             "org.gnome.Music", "org.gnome.Maps", "org.gnome.SystemMonitor",
             "org.gnome.Screenshot", "org.gnome.DiskUtility"],
    "places": ["folder", "folder-documents", "folder-download", "folder-pictures",
               "folder-music", "folder-videos", "drive-harddisk"],
    "mimetypes": ["text-x-generic", "image-x-generic", "audio-x-generic", "video-x-generic",
                  "application-x-executable", "package-x-generic"],
    "status": ["network-wireless", "network-wired", "battery-full", "bluetooth-active",
               "user-trash", "user-trash-full"],
}

def main():
    count = 0
    for category, names in ICONS.items():
        target = ROOT / category
        target.mkdir(parents=True, exist_ok=True)
        for name in names:
            draw_icon(name).save(target / f"{name}.png", optimize=True)
            count += 1
    print(f"Generated {count} native 512x512 Hyrule pixel icons (no bitmap upscaling).")

if __name__ == "__main__":
    main()
