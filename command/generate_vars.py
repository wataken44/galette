#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" generate_vars.py


"""

import codecs
import ipaddress
import json
import os
import subprocess
import sys
import yaml

COMMAND_DIR = os.path.abspath(os.path.dirname(__file__)) + "/"


def main():
    fp = open(sys.argv[1])
    data = yaml.safe_load(fp)
    fp.close()

    interface, address, netmask = get_global_ipv6()
    if address is not None:
        print("external ipv6 address: %s %s/%s" % (interface, address, netmask))
        add_ipv6(data, interface, address, netmask)
    else:
        print("no external ipv6 address. configuration skipped.")

    fp = codecs.open(sys.argv[2], "w", "utf-8")
    yaml.dump(data, fp, encoding="utf-8", allow_unicode=True)
    fp.close()


def get_global_ipv6():
    proc = subprocess.run(
        COMMAND_DIR + "get_global_ipv6.py --json", shell=True, capture_output=True
    )

    d = json.loads(proc.stdout.decode("utf-8").strip())

    if d is None:
        return None, None, None

    interface = d.get("interface")
    address = d.get("address")
    netmask = d.get("netmask")

    return interface, address, netmask


def add_ipv6(data, external_interface, external_address, global_netmask):
    info = GlobalNetworkInfo(external_address, global_netmask)

    data["ipv6"] = {
        "external-interface": external_interface,
        "external-address": external_address,
        "netmask": global_netmask,
        "network": str(info.network_address),
    }

    # add_ipv6_interface(data, info)


def add_ipv6_interface(data, info):

    for idx, iface in enumerate(data["interfaces"]):
        if iface["lan"] == True:
            if "ipv6" not in data["interfaces"][idx]:
                data["interfaces"][idx]["ipv6"] = []

            name = data["interfaces"][idx]["name"]
            addr = genarete_modified_eui64_address(name, info)

            up_command = "ip route add %s/%s dev %s metric 128" % (
                info.network_address,
                info.prefixlen,
                name,
            )
            down_command = (
                "ip route del %s/%s dev %s metric 128 2>/dev/null || echo -n ''"
                % (info.network_address, info.prefixlen, name)
            )

            data["interfaces"][idx]["ipv6"].append(
                {
                    "method": "static",
                    "address": addr,
                    "netmask": info.prefixlen,
                    "up": up_command,
                    "down": down_command,
                }
            )

            data["ipv6"]["internal-address"] = addr
            data["ipv6"]["internal-interface"] = name

            print("%s add ipv6 address %s" % (name, addr))

            # TODO: split segment when multiple lan interface...
            break


def genarete_modified_eui64_address(nic, info):
    fp = open("/sys/class/net/%s/address" % nic)
    mac = fp.readline().strip()
    fp.close()

    arr = []
    for b in mac.split(":"):
        arr.append(int(b, 16))

    arr = arr[:3] + [0xFF, 0xFE] + arr[3:]
    arr[0] = arr[0] ^ 0x02

    suffix = arr[0]
    for b in arr[1:]:
        suffix = (suffix << 8) + b

    prefix = int(info.network_address)

    return str(ipaddress.IPv6Address(prefix + suffix))


class GlobalNetworkInfo:
    def __init__(self, external_address, netmask):
        network = ipaddress.IPv6Network(
            "%s/%s" % (external_address, netmask), strict=False
        )

        self._external = external_address
        self._network = network

    def get_external(self):
        return self._external

    external = property(get_external)

    def get_network_address(self):
        return self._network.network_address

    network_address = property(get_network_address)

    def get_netmask(self):
        return self._network.netmask

    def get_prefixlen(self):
        return self._network.prefixlen

    prefixlen = property(get_prefixlen)


if __name__ == "__main__":
    main()
