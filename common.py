import os
import csv
from requests_oauthlib import OAuth1Session

filename = os.environ['TWITTER_NAMED_PIPE_PATH']
if not os.path.exists(filename):
    os.mkfifo(filename)

twitter = OAuth1Session(os.environ['TWITTER_API_KEY'],
                        client_secret=os.environ['TWITTER_API_SECRET'],
                        resource_owner_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                        resource_owner_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

with open('keywords.csv', 'r') as f:
    keywords = {row[0]: row[1] for row in csv.reader(f)}

