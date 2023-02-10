#!/usr/bin/env python3

import os
import sys

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), "lib"))

import re
from workflow import Workflow3

wf = Workflow3()
logger = wf.logger

def word_count(s):
    return len(re.sub(r"[\s\r\n]+", " ", s, re.MULTILINE).split())

def char_count(s):
    return len(s)

def main(wf):

    s = wf.args[0]

    transformers = [(word_count, "Words"),
                    (char_count, "Characters")]
    try:
        for transformer, name in transformers:
            value = transformer(s)
            wf.add_item(title=f"{value} {name}",
                        subtitle=name,
                        arg=value,
                        copytext=value,
                        valid=True)
    except ValueError as e:
        pass

    wf.send_feedback()

if __name__ == "__main__":
    sys.exit(wf.run(main))
