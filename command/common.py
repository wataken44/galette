#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" common.py


"""

import getpass
import os
import subprocess
import sys
import tempfile

BASE_DIR = os.path.abspath(os.path.dirname(__file__) + "/../") + "/"
COMMAND_DIR = BASE_DIR + "command/"
PLAYBOOK_DIR = BASE_DIR + "playbook/"


def run(playbook):
    debug = os.environ.get("GALETTE_DEBUG", "0")
    verbose = 0
    if debug in ["0", "1", "2", "3"]:
        verbose = int(debug)

    ask_become_pass = getpass.getuser() != "root"

    exec_dir = create_exec_dir()
    move_to_exec_dir(exec_dir)

    setup_hosts(exec_dir)

    run_playbook(playbook, ask_become_pass, verbose)

    if verbose == 0:
        cleanup_exec_dir(exec_dir)


def create_exec_dir():

    exec_dir = os.path.abspath(tempfile.mkdtemp(prefix="galette-")) + "/"
    print("mkdir %s" % exec_dir)

    cmd = "cp -r %s %s" % (PLAYBOOK_DIR, exec_dir)
    os.system(cmd)
    print(cmd)

    return exec_dir


def setup_hosts(exec_dir):
    body = """
[routers]
router ansible_host=localhost

[routers:vars]
ansible_python_interpreter=auto_silent
ansible_connection=local

"""
    cmd = "echo '%s' > %splaybook/hosts" % (body, exec_dir)
    print(cmd)
    os.system(cmd)


def move_to_exec_dir(exec_dir):
    print("cd %splaybook" % exec_dir)
    os.chdir(exec_dir + "playbook")


def cleanup_exec_dir(exec_dir):
    cmd = "rm -rf %s" % exec_dir
    os.system(cmd)


def run_playbook(playbook, ask_become_pass=True, verbose=0):
    cmd = ["ansible-playbook", "-i", "hosts"]
    if ask_become_pass:
        cmd.append("--ask-become-pass")

    if verbose > 0:
        cmd.append("-" + "v" * verbose)

    cmd.append(playbook)

    print(" ".join(cmd))
    subprocess.run(cmd, encoding="utf-8")
