#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Snyph Flask App
from flask import *
from subprocess import Popen, PIPE
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/<what>/<randomizer>/<freq>/<input>")
def api(what, randomizer, freq, input):
    if what in ["encrypt", "decrypt"]:
        if randomizer == "default":
            randomizer = "0102030405060708091011121314151617181920" \
                         "2122232425262728293031323334353637383940" \
                         "4142434445464748495051525354555657585960"
        stuff = ["python", "api.py", "-H", randomizer, "-f", freq]
        stuff += ["-e"*(what == "encrypt") + "-d"*(what == "decrypt"),
                  input]
    else:
        return "no"
    output = Popen(stuff, stdout = PIPE).stdout.read().strip('\n')
    return Response(output, mimetype = "text/plain")

app.debug = False
if __name__ == '__main__':
    app.run()