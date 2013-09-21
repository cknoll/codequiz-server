#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Intention: go through all html files in the working dir
and add comment lines at the beginning and end containing the name of the
(template) file
"""

import os

files  = os.listdir('.')
files = filter(lambda x: x.endswith('.html'), files)

def add_comments(fname):
    with open(fname, 'r') as myfile:
        lines = myfile.readlines()

    c1 = "<!-- ==> start: %s -->\n" % (fname)
    c2 = "<!-- ==> end: %s -->\n" % (fname)

    if not lines[0] == c1:
        lines.insert(0,c1)
    if not lines[-1] == c2:
        lines.append(c2)

    if 0:
        print lines[0]
        print lines[-1]
        return
    with open(fname, 'w') as myfile:
        myfile.writelines(lines)

for f in files:
    print f
    add_comments(f)

print "done"
