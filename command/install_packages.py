#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" install_packages.py


"""

from common import *


def main():
    setup()

    run_playbook("install_packages.yml")


if __name__ == "__main__":
    main()
