"""
This module contains some auxiliary funcitonality for the quiz app.
It should not be confunded with the aux package (which is not app-specific).
"""

from io import StringIO
import re
import json

from django.core.management import call_command


def make_backup() -> bytes:

    model_blacklist = [
        "contenttypes*", "sessions*", r"admin\.logentry", r"auth\.permission"
    ]


    buf = StringIO()
    call_command("dumpdata", stdout=buf)
    buf.seek(0)
    data = json.loads(buf.read())

    blacklist_re = re.compile("|".join(model_blacklist))


    keep_data = []
    bad_data = []
    for d in data:
        model = d.get("model")
        if model is None:
            continue
        if blacklist_re.match(model):
            # just for debugging
            bad_data.append(model)
            continue
        else:
            keep_data.append(d)

    # dependency only needed here
    # todo: properly handle optional dependencies (Milestone 1.0)
    # noinspection PyPackageRequirements
    import demjson
    res = demjson.encode(keep_data, encoding="utf-8", compactly=False)

    # remove trailing spaces and ensure final linebreak:
    lb = b"\n"  # byte-linebreak
    res2 = lb.join([line.rstrip() for line in res.split(lb)] + [lb])

    return res2
