#!/usr/bin/python
# -*- coding: utf-8 -*-
import httplib
import time
import random
import string
import hmac
import hashlib
import base64
import json
import urllib
import sys

def get_oauth_nonce():
    char_set = string.ascii_uppercase + string.digits
    return ''.join(random.sample(char_set,32))

def get_oauth_timestamp():
    return str(int(time.time()))

OAUTH_CONSUMER_KEY = 'yqBZgUWAFanrUI3PbA5A'
OAUTH_CONSUMER_SECRET = 'W4yD1N1FplIszcdFwBJ6H8lD348gW4yjdRu0NC0Axxw'
OAUTH_TOKEN = '193722284-w4gGHyNIn98nddzwaSpzGAGUTsfGCLZlNbxnh0o0'
OAUTH_TOKEN_SECRET = 'NjXXlbWWGHmsqeIyeABBbLKkMcRWwNInfqDHt4JiA'
OAUTH_SIGNATURE_METHOD = 'HMAC-SHA1'
OAUTH_VERSION = '1.0'
SIGNING_KEY = urllib.quote_plus(OAUTH_CONSUMER_SECRET) + '&' + urllib.quote_plus(OAUTH_TOKEN_SECRET)

def get_base_string(api_name, oauth_nonce, oauth_timestamp, **kwargs):
    params = {
             'oauth_consumer_key': OAUTH_CONSUMER_KEY,
             'oauth_nonce': oauth_nonce,
             'oauth_signature_method': 'HMAC-SHA1',
             'oauth_timestamp': oauth_timestamp,
             'oauth_token': OAUTH_TOKEN,
             'oauth_version': '1.0',
    }
    params.update(kwargs)
    param_string = '&'.join([key + '=' + params[key] for key in sorted(params.iterkeys())])
    http_method = 'GET'
    base_url = 'https://api.twitter.com/1.1/statuses/%(api_name)s.json' % locals()
    base_string = http_method + '&' + urllib.quote_plus(base_url) + '&' + urllib.quote_plus(param_string)
    return base_string

def get_OAuth_signature(api_name, oauth_nonce, oauth_timestamp, **kwargs):
    return urllib.quote_plus(base64.b64encode(hmac.new(SIGNING_KEY, get_base_string(api_name, oauth_nonce, oauth_timestamp, **kwargs), hashlib.sha1).digest()))

def get_request_url(api_name, **kwargs):
    args = '&'.join([key + '=' + kwargs[key] for key in kwargs])
    return "/1.1/statuses/%(api_name)s.json?%(args)s" % locals()

def get_api(api_name, **kwargs):
    oauth_nonce = get_oauth_nonce()
    oauth_timestamp = get_oauth_timestamp()
    oauth_consumer_key = OAUTH_CONSUMER_KEY
    oauth_token = OAUTH_TOKEN
    oauth_signature = get_OAuth_signature(api_name, oauth_nonce, oauth_timestamp, **kwargs)
    oauth_signature_method = OAUTH_SIGNATURE_METHOD
    oauth_version = OAUTH_VERSION
    long_str = 'OAuth oauth_consumer_key="%(oauth_consumer_key)s", oauth_nonce="%(oauth_nonce)s", oauth_signature="%(oauth_signature)s", oauth_signature_method="%(oauth_signature_method)s", oauth_timestamp="%(oauth_timestamp)s", oauth_token="%(oauth_token)s", oauth_version="%(oauth_version)s"' % locals()
    headers = {"Authorization": long_str,}
    conn = httplib.HTTPSConnection("api.twitter.com")
    conn.request("GET", get_request_url(api_name, **kwargs), headers=headers)
    res = conn.getresponse()
    output = res.read()
    assert res.status == 200 and res.reason == 'OK', 'Twitter API %(api_name)s GET FAILED!!! Result: %(output)s' % locals()
    conn.close()
    return json.loads(output)

def main():
    screen_name = sys.argv[1]
    output = get_api('user_timeline', screen_name=screen_name)
    for row in output:
        print row['text']
    print '------------------------------'
    output = get_api('home_timeline', count='3')
    for row in output:
        print row['user']['screen_name'] + ': ' + row['text']

if __name__ == '__main__':
    main()
