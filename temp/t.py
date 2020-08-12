import json
import quickjs

msg = {'amesg': {'bmesg': [1, 2, 3, 4]}}

with open('./bundle.js') as f:
    _fn = quickjs.Function('make_schema', f.read())
    print(json.dumps(_fn(msg), indent=2))
