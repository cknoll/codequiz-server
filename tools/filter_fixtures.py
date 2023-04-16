import sys
import json
import demjson
import re
import os


"""
quick and dirty script to make old fixtures loadable

"""

from ipydex import IPS, activate_ips_on_exception
activate_ips_on_exception()

fname = sys.argv[1]

with open(fname, "r") as fp:

    jdata = json.load(fp)


new_data = []

for i in range(8, 46):
    break
    new_data.append({
        "fields" : {  },
        "model" : "quiz.taggedmodel",
        "pk" : i
    })


model_blacklist = [

    re.compile("^ratings.*"),
    re.compile("^feedback.*"),
    re.compile("^auth.*"),
    re.compile("^admin.*"),
    re.compile("^quiz\.quizresult*."),

]

c = 0
for d in jdata:
    mod = d["model"]
    for regex in model_blacklist:
        if regex.match(mod):
            c += 1
            break
    else:
        new_data.append(d)

base, ext = os.path.splitext(fname)
new_fname = f"{base}_stripped{ext}"

with open(new_fname, "w") as fp:
    fp.write(demjson.encode(new_data, compactly=False, indent_amount=2))


print("omitted:", c)

#IPS()
