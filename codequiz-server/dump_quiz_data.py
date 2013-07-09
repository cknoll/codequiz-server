# -*- coding: utf-8 -*-

"""
This script is used for dumping all data from the sqlite database to a
text file such that it can be tracked by version control.
"""

import os, sys, time
import StringIO

# this copied from manage.py

new_argv = [sys.argv[0], 'dumpdata', "quiz"]


dumpfilname = "quiz_data_dump.sql"
stdout = sys.stdout

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codequiz.settings")

    from django.core.management import execute_from_command_line

    sys.stdout = StringIO.StringIO()
    sys.stdout.write(time.ctime()+"\n")
    execute_from_command_line(new_argv) # writes to stdout

    dump_string = sys.stdout.get_value()

    sys.stdout.close()
    sys.stdout = stdout

    dump_string.replace('\n')

    # unvollständig