#!/usr/bin/env python


import base64
import sys
import urllib
from workflow import Workflow3

def main(wf):
    args = wf.args

    encoders = [(urllib.quote, "URL (Percent)"),
                (urllib.quote_plus, "URL (Plus)"),
                (base64.encodestring, "Base 64")]
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
