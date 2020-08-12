#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

__version__ = '0.0.1'

import json
import quickjs

with open('./test.md') as mdf:
    md = mdf.read()

ctx = quickjs.Context()

with open('./remarkpy.js') as f:
    rjs = ctx.module(f.read())

print(rjs)
#print(parseMD(md))
