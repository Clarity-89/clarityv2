#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

if __name__ == "__main__":
    # load the environment variables containing the secrets/config
    dotenv_path = os.path.join(os.path.dirname(__file__), os.pardir, ".env")
    load_dotenv(dotenv_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv('DJANGO_SETTINGS_MODULE', "clarityv2.conf.dev"))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)