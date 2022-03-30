#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" configure.py


"""

from common import *


def main():
    setup()

    run_playbook("configure.yml")


if __name__ == "__main__":
    main()
