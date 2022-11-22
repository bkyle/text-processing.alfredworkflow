#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), "lib"))

import base64
import sys
import urllib
import re
from workflow import Workflow3


def hex2rgb(s):
    """Converts an HTML-style color code, e.g. ``#DECAFE`` into a tuple of integers
    representing the red, green, and blue values of the color."""
    m = re.match(r"#?([A-Z0-9]{2,2})([A-Z0-9]{2,2})([A-Z0-9]{2,2})", s.upper())
    if m is None:
        return None

    r, g, b = m.group(1), m.group(2), m.group(3)
    r, g, b = int(r, 16), int(g, 16), int(b, 16)
    return (r, g, b)

def rgb2hsl(rgb):
    """Converts a tuple of integers representing red, green, and blue color values
into a tuple of integers representing hue, saturation, and lightness values."""
    r, g, b = rgb
    logger.info("r = %d, g = %d, b = %d", r, g, b)

    R = r / 255.0
    G = g / 255.0
    B = b / 255.0

    logger.info("R = %f, G = %f, B = %f", R, G, B)

    Cmax = max([R, G, B])
    Cmin = min([R, G, B])

    delta = Cmax - Cmin

    if delta == 0:
        h = 0
    elif Cmax == R:
        h = 60 * (((G - B) / delta) % 6)
    elif Cmax == G:
        h = 60 * (((B - R) / delta) + 2)
    elif Cmax == B:
        h = 60 * (((R - G) / delta) + 4)

    l = (Cmax + Cmin) / 2

    if delta == 0:
        s = 0
    else:
        s = delta / (1 - abs((2 * l) - 1))

    return (h, s, l)


class Color:
    def __init__(self, rgb):
        self.rgb = rgb
        self.hsl = rgb2hsl(rgb)

    def asRGB(self):
        return "%d %d %d" % self.rgb

    def asHex(self):
        return "#%02x%02x%02x" % self.rgb

    def asHSL(self):
        return "%d° %s%% %s%%" % (self.hsl[0], int(self.hsl[1] * 100), int(self.hsl[2] * 100))

def main(wf):
    args = wf.args
    args = ["78a9ff"]

    color = Color(hex2rgb(args[0]))
    values = [(color.asHex(), "HEX"),
              (color.asRGB(), "Red, Green, Blue"),
              (color.asHSL(), "Hue, Saturation, Lightness")]
    for value, subtitle in values:
        wf.add_item(title=value,
                    subtitle=subtitle,
                    arg=value,
                    copytext=value,
                    valid=True)

    wf.send_feedback()

logger = None

if __name__ == "__main__":
    wf = Workflow3()
    logger = wf.logger
    sys.exit(wf.run(main))
