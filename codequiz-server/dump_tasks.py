# -*- coding: utf-8 -*-

"""
This script is used for dumping all tasks from the sqlite database to a
json file.
Such a file can be imported by another script (future plan).

Aim: ease the processe of importing many tasks to the database

"""

import os, sys, time
import json
import pickle
from ipHelp import IPS, Tracer, ip_syshook, sys
# Tracer(colors='Linux')() # start debugging

dumpfilname = "quiz_tasks.json"

def get_field_names(model):
    """
    :returns: a list of field names for the given model
    """
    return [f.name for f in model._meta.fields]


def serialize_value(val):
    """
    background:
    helps to save complex objects  (such as datetime-instances)
    to a json file
    """
    return pickle.dumps(val)




uc_const1 = u'⌘' # temp for all '"'-chars in the source
uc_const2 = u'◆' # represents all '"'-chars introduced by json (in our file)

def repl_src_quotes(string):
    return unicode(string).replace('"', uc_const1)

def reinsert_src_quotes(string):
    return unicode(string).replace(uc_const1, '"')


def repl_json_quotes(string):
    return unicode(string).replace('"', uc_const2)


def model_instance_to_dict(instance, fieldnames):
    items = []
    for fname in fieldnames:
        value = getattr(instance, fname)
        if isinstance(value, basestring):
            value = repl_src_quotes(value)

        if isinstance(  value, ( basestring, int, long, float,
                                 bool, type(None) )  ):
            items.append( (fname, value) )
        else:
            # serialize the complex object
            items.append( ( fname+"_pickle", serialize_value(value) )  )

    return dict(items)

def model_to_json(model):

    assert issubclass(model, models.Model)
    fieldnames = get_field_names(model)
    instances = model.objects.all()

    dict_list = [model_instance_to_dict(mi, fieldnames) for mi in instances]


    jstring = json.dumps(dict_list, indent=4)
    jstring = repl_json_quotes(jstring)


    return jstring


if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codequiz.settings")

    import quiz.models as dm
    from django.db import models


    res = model_to_json(dm.Task)


    with open(dumpfilname, 'w') as dumpfile:
        if isinstance(res, unicode):
            res = res.encode('utf-8')
        dumpfile.write(res)
    print "%s written" % dumpfilname









