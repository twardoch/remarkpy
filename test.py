#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

__version__ = '0.0.1'

import json
import quickjs

msg = {'amesg': {'bmesg': [1, 2, 3, 4]}}

with open('./bundle.js') as f:
    _fn = quickjs.Function('make_schema', f.read())
    print(json.dumps(_fn(msg), indent=2))
    