#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" generate_vars.py


"""

import codecs
import sys
import yaml


def main():
    fp = open(sys.argv[1])
    data = yaml.safe_load(fp)
    fp.close()

    fp = codecs.open(sys.argv[2], "w", "utf-8")
    yaml.dump(data, fp, encoding="utf-8", allow_unicode=True)
    fp.close()


if __name__ == "__main__":
    main()
