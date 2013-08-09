# -*- coding: utf-8 -*-

"""
This script is used for dumping all data from the sqlite database to a
text file such that it can be tracked by version control.
"""

import os, sys, time


dumpfilname = "quiz_data_dump.sql"

def get_field_names(model):
    return [f.name for f in model._meta.fields]


def gen_model_report(model):
    assert issubclass(model, models.Model)

    fieldnames = get_field_names(model)

    instances = model.objects.all()

    res = "-> Model: %s\n\n" % model.__name__
    for instance in instances:
        for f in fieldnames:
            res+="%s = %s\n\n" %(f, getattr(instance, f))
        res +="%s\n\n" %("- "*3)
    res +="%s\n\n""- "%("- "*7)
    return res


if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codequiz.settings")

    import quiz.models as dm
    from django.db import models



    model_list = [getattr(dm, a) for a in dir(dm)]
    model_list = filter(lambda x: isinstance(x, type), model_list)
    model_list = filter(lambda x: issubclass(x, models.Model), model_list)


    res = [gen_model_report(m) for m in model_list]
    res = "".join(res)


    with open(dumpfilname, 'w') as dumpfile:
        dumpfile.write(res)
    print "%s written" % dumpfilname









