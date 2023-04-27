"""
This module contains some auxiliary funcitonality for the quiz app.
It should not be confunded with the aux package (which is not app-specific).
"""

from io import StringIO
import re
import json

from django.core.management import call_command
from django.conf import settings


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
    import demjson3
    res = demjson3.encode(keep_data, encoding="utf-8", compactly=False)

    # remove trailing spaces and ensure final linebreak:
    lb = b"\n"  # byte-linebreak
    res2 = lb.join([line.rstrip() for line in res.split(lb)] + [lb])

    return res2

def insert_settings_context_preprocessor(request):
    """This function is called for every request.

    see settings.TEMPLATES["OPTIONS"]["context_processors"] for details.
    Also see: https://docs.djangoproject.com/en/4.2/ref/templates/api/#writing-your-own-context-processors
    """

    # select some settings which should be availabe in all templates

    keys = ["DEVMODE"]

    partial_context = { (f"SETTINGS_{k}", getattr(settings, k, None)) for k in keys }

    print("called me")

    return partial_context
