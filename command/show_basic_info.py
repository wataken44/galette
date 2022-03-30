#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" show_basic_info.py


"""


import sys
import os

from constants import *


def main():
    os.chdir(PLAYBOOK_DIR)

    os.system("ansible-playbook -i hosts --ask-become-pass -vv show_basic_info.yml")


if __name__ == "__main__":
    main()
