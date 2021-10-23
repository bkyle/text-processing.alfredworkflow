#!/usr/bin/env python

import re
import sys
from workflow import Workflow3

def snake_case(s):
    return re.sub(" ", "_", s)

def camelCase(s):
    def camelize(i, word):
        if i == 0:
            return word
        else:
            return word.capitalize()

    return "".join([camelize(i, word) for i, word in enumerate(re.split(" ", s))])

def ProperCase(s):
    return "".join([word.capitalize() for word in re.split(" ", s)])

def h4ck3rC453(s):
    subs = {"a": "4",
            "e": "3",
            "l": "1",
            "o": "0",
            "s": "5"}
    def h4ck3r1ze(c):
        if c.lower() in subs.keys():
            return subs[c.lower()]
        else:
            return c

    return "".join([h4ck3r1ze(c) for c in s])

def main(wf):

    s = wf.args[0]

    numeric_transformers = [(str, "Integer"),
                            (hex, "Hexadecimal"),
                            (oct, "Octal"),
                            (bin, "Binary")]
    radix = 10
    if re.match(r"^0[0-8]*$", s):
        radix = 8
    elif re.match(r"^0[xX]([0-9a-fA-F]*)?$", s):
        radix = 16

    try:
        x = int(wf.args[0], radix)
        for transformer, name in numeric_transformers:
            transformed = transformer(x)
            wf.add_item(title=transformed,
                        subtitle=name,
                        copytext=transformed)
    except ValueError as e:
        pass

    text_transformers = [(unicode.upper, "UPPER"),
                         (unicode.lower, "lower"),
                         (unicode.title, "Title Case"),
                         (unicode.capitalize, "Capitalize"),
                         (unicode.swapcase, "sWAP cASE"),
                         (snake_case, "snake_case"),
                         (camelCase, "camelCase"),
                         (ProperCase, "ProperCase"),
                         (h4ck3rC453, "h4ck3rc453")]

    for transformer, name in text_transformers:
       transformed = transformer(s)
       wf.add_item(title=transformed,
                   subtitle=name,
                   copytext=transformed)

    wf.send_feedback()

if __name__ == "__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
