#!/usr/bin/env python3

import os
import sys

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), "lib"))

import base64
import sys
import urllib.parse
from workflow import Workflow3

def main(wf):
    args = wf.args

    decoders = [(urllib.parse.unquote, "URL (Percent)"),
                (urllib.parse.unquote_plus, "URL (Plus)"),
                (lambda x: base64.b64decode(x.encode()).decode(), "Base 64")]
    for decoder, name in decoders:
        decoded = decoder(args[0])
        wf.add_item(title=decoded,
                    subtitle=name,
                    arg=decoded,
                    copytext=decoded,
                    valid=True)
    wf.send_feedback()

if __name__ == "__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
