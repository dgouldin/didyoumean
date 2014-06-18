#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib

from common import filename, twitter, keywords

url = 'https://stream.twitter.com/1.1/statuses/filter.json?track={0}'.format(
    urllib.quote(','.join(keywords.keys()))
)
r = twitter.post(url, stream=True)

with open(filename, 'w') as f:
    for line in r.iter_lines():
        if line:
            f.write(line + '\n')
            f.flush()
            print('event=received')
