#!/usr/bin/env python3

import sys
import os

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), "lib"))

import base64
import sys
import urllib.parse
from workflow import Workflow3

def main(wf):
    args = wf.args

    encoders = [(urllib.parse.quote, "URL (Percent)"),
                (urllib.parse.quote_plus, "URL (Plus)"),
                (lambda x: base64.b64encode(x.encode()).decode(), "Base 64")]
    for encoder, name in encoders:
        encoded = encoder(args[0])
        wf.add_item(title=encoded,
                    subtitle=name,
                    arg=encoded,
                    copytext=encoded,
                    valid=True)
    wf.send_feedback()

if __name__ == "__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))
