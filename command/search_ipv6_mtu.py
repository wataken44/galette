#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" search_ipv6_mtu.py


"""

import subprocess
import sys


def main():

    mtu = 1500

    while mtu >= 1280:
        size = mtu - 40 - 8  # IPv6 header: 40Byte, ICMPv6 Header: 8Byte
        command = "ping -M do -c 1 -s %s -6 ipv6.google.com" % size

        proc = subprocess.run(command, shell=True, capture_output=True)
        if proc.returncode == 0:
            print(mtu)
            return
        mtu -= 2


if __name__ == "__main__":
    main()
