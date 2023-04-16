#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codequiz-server-project.settings.production")

    current_dir = os.path.dirname(os.path.abspath(sys.modules.get(__name__).__file__))
    apps_dir = os.path.join(current_dir, "apps")
    sys.path.insert(0, apps_dir)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
