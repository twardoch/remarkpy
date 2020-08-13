#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

__version__ = '0.0.1'

import json
import quickjs

with open('./test.md') as mdf:
    md = mdf.read()

with open('./remarkpy.js') as f:
#with open('../remarkpyjs/index.js') as f:
    js = f.read()

parseMd = quickjs.Function('parseMd', js)
print(parseMd('## H1'))
#parseHtml = quickjs.Function('parseHtml', js)

#print(parseHtml('<h1>hello</h1>'))
#print(parseHtml)
#help(parseHtml)
