#!/usr/bin/env python

import json

try:
    from tornado.escape import json_encode
except ImportError:
    json_encode = lambda value: json.dumps(value).replace("</", "<\\/")
