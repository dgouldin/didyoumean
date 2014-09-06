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
                print('event=retweet id={0}'.format(tweet['id_str']))
                continue # don't reply to retweets

            print('event=received id={0}'.format(tweet['id_str']))
            tweet_lower = tweet['text'].lower()
            for k in keywords.keys():
                if k.lower() in tweet_lower:
                    keyword = k
                    break
            else:
                print('event=no_match id={0}'.format(tweet['id_str']))
                continue # no keyword match

            replacement = keywords[keyword]
            print('event=replacement id={0} "{1}" -> "{2}"'.format(
                tweet['id_str'], keyword, replacement))
            tweet_url = 'https://twitter.com/{}/status/{}'.format(
                tweet['user']['screen_name'],
                tweet['id_str'],
            )
            reply_body = 'Did you mean "{}"? {}'.format(
                replacement,
                tweet_url,
            )
            response = twitter.post(url, {
                'status': reply_body,
                'in_reply_to_status_id': tweet['id_str'],
                'trim_user': 'true',
            })
            if response.status_code == 200:
                print('event=publish tweet="{0}"'.format(reply_body))
            else:
                print('event=publish_error status_code={0}, content="{1}"'.format(
                    response.status_code, response.content))
