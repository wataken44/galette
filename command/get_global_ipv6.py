#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" get_global_ipv6.py


"""

import ipaddress
import json
import re
import subprocess
import sys

IP_ROUTE_COMMAND = "ip -6 route get $(dig www.google.com AAAA +short)"
IP_ADDR_COMMAND = "ip -6 addr show dev "


def main():

    output_json = False
    if len(sys.argv) == 2 and sys.argv[1] == "--json":
        output_json = True

    dev, src = get_route_src()
    addr = None
    if src is not None:
        addr = get_nic_address(dev, src)

    if output_json:
        if addr is None:
            print(json.dumps(None))
        else:
            arr = addr.split("/")
            print(json.dumps({"interface": dev, "address": arr[0], "netmask": arr[1]}))
    else:
        if addr is not None:
            print(addr)


def get_route_src():
    proc = subprocess.run(IP_ROUTE_COMMAND, shell=True, capture_output=True)

    ptn = re.compile(r"dev ([^ ]+).*src ([^ ]+) ")
    mo = ptn.search(proc.stdout.decode("utf-8"))

    dev = None
    src = None
    if mo:
        try:
            ipaddress.IPv6Address(mo[2])
            dev = mo[1]
            src = mo[2]
        except Exception:
            pass

    return dev, src


def get_nic_address(dev, src):
    proc = subprocess.run(IP_ADDR_COMMAND + dev, shell=True, capture_output=True)

    for line in proc.stdout.decode("utf-8").splitlines():
        if line.find(src) < 0:
            continue

        ptn = re.compile(r"inet6 ([^ ]+)")
        mo = ptn.search(line)

        if mo is None:
            continue

        try:
            ipaddress.IPv6Network(mo[1], strict=False)
            return mo[1]
        except Exception:
            pass

    return None


if __name__ == "__main__":
    main()
