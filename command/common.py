#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" common.py


"""

import os
import subprocess

import constants


def setup():
    os.chdir(constants.PLAYBOOK_DIR)


def run_playbook(playbook, ask_become_pass=True, debug=False):
    cmd = ["ansible-playbook", "-i", "hosts"]
    if ask_become_pass:
        cmd.append("--ask-become-pass")

    if debug:
        cmd.append("-vvv")
    else:
        d = int(os.environ.get("GALETTE_DEBUG", "0"))
        if d > 0:
            cmd.append("-" + "v" * d)

    cmd.append(playbook)

    print(" ".join(cmd))
    subprocess.run(cmd, encoding="utf-8")
