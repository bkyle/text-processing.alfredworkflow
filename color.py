#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), "lib"))

import re
import base64
import sys
import urllib

from typing import Optional

from workflow import Workflow3


wf = Workflow3()
logger = wf.logger

def color2rgb(s) -> Optional[tuple]:
    """Converts a named color, e.g. "cyan", to a tuple of integers representing the red, green,
    and blue channels of the color.
    
    Args:
      s: string containing the name of the color.

    Returns:
      A tuple containing integers representing the red, green, and blue channels of the color
      or `None` if the string does not name a known color.    
    """
    return None

def generate_icon(color: str) -> Optional[str]:
    """Generates an icon representing the passed color in the Alfred workflow cache and
    returns a string containing the path to the icon.  If an icon is not generated then
    `None` is returned.
    
    Args:
      color: string containing the name of the color.
    """
    return None


# The functions in this section require Pillow which may not be present.  If the package is not
# present then the default implementation (above) is used.
try:
    from PIL import Image, ImageColor

    def color2rgb(s):
        """See `color2rgb`."""
        if not s:
            return None
        if s.startswith("#"):
            # hex strings should be processed with hex2rgb
            return None
        try:
            rgb = ImageColor.getrgb(s)
            logger.debug("%s => %s" % (s, rgb))
            return (rgb[0], rgb[1], rgb[2])
        except ValueError:
            return None

    def generate_icon(color: tuple[int,int,int]) -> str:
        """See `generate_icon`."""
        if not color:
            return None

        image = Image.new('RGB', (128, 128), color)

        file_name = re.sub(r"[#:]", "", color)
        path = wf.cachefile(f"{file_name}.png")
        image.save(path)
        return path

except ModuleNotFoundError:
    logger.warning("PIL not found, no thumbnails will be generated")



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
    def __init__(self, rgb: tuple[int,int,int]):
        self.rgb = rgb
        self.hsl = rgb2hsl(rgb)

    def asRGB(self):
        return "%d %d %d" % self.rgb

    def asHex(self):
        return "#%02x%02x%02x" % self.rgb

    def asHSL(self):
        return "%d° %s%% %s%%" % (self.hsl[0], int(self.hsl[1] * 100), int(self.hsl[2] * 100))

def main(wf):
    query = wf.args[0]
    rgb = color2rgb(query)
    if rgb is None:
        rgb = hex2rgb(query)
    if rgb is None:
        return
    color = Color(rgb)
    values = [(color.asHex(), "HEX"),
              (color.asRGB(), "Red, Green, Blue"),
              (color.asHSL(), "Hue, Saturation, Lightness")]
    icon_path = generate_icon(color.asHex())
    for value, subtitle in values:
        wf.add_item(title=value,
                    subtitle=subtitle,
                    arg=value,
                    copytext=value,
                    valid=True,
                    icon=icon_path,
                    icontype="filepath")
        

    wf.send_feedback()

if __name__ == "__main__":
    sys.exit(wf.run(main))
