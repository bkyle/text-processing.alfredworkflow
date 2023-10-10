#!/usr/bin/env python3

import os
import sys

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), "lib"))

import base64
import sys
import urllib.parse
from workflow import Workflow3

def base64decode(s: str) -> str:
    try:
        return base64.b64decode(s.encode()).decode()
    except ValueError:
        return None

def main(wf):
    args = wf.args

    decoders = [(urllib.parse.unquote, "URL (Percent)"),
                (urllib.parse.unquote_plus, "URL (Plus)"),
                (lambda x: base64.b64decode(x.encode()).decode(), "Base 64")]
    for decoder, name in decoders:
        try:
            decoded = decoder(args[0])
            if decoded:
                wf.add_item(title=decoded,
                            subtitle=name,
                            arg=decoded,
                            copytext=decoded,
                            valid=True)
        except ValueError:

            pass
    wf.send_feedback()

if __name__ == "__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
