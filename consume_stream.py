#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from common import filename, twitter, keywords

url = 'https://api.twitter.com/1.1/statuses/update.json'
while True:
    with open(filename, 'r') as pipe:
        while True:
            line = pipe.readline()
            if line == '':
                break
            elif line == '\n':
                continue

            try:
                tweet = json.loads(line.decode('utf-8'))
            except ValueError:
                print('event=malformed tweet="{0}"'.format(line))
                continue # malformed tweet payload

            if 'retweeted_status' in tweet:
                print('event=retweet')
                continue # don't reply to retweets

            print('event=received')
            tweet_lower = tweet['text'].lower()
            for k in keywords.keys():
                if k.lower() in tweet_lower:
                    keyword = k
                    break
            else:
                print('event=no_match')
                continue # no keyword match

            replacement = keywords[keyword]
            print('event=replacement "{0}" -> "{1}"'.format(
                keyword, replacement))
            reply_body = '@{0} did you mean "{1}"?'.format(
                tweet['user']['screen_name'],
                replacement,
            )
            twitter.post(url, {
                'status': reply_body,
                'in_reply_to_status_id': tweet['id_str'],
                'trim_user': 'true',
            })
            print('event=publish tweet="{0}"'.format(reply_body))
