# -*- coding: utf-8 -*-
import httplib
import time
import httplib
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

def get_base_string(screen_name, oauth_nonce, oauth_timestamp):
    param = {'screen_name': screen_name,
             'oauth_consumer_key': OAUTH_CONSUMER_KEY,
             'oauth_nonce': oauth_nonce,
             'oauth_signature_method': 'HMAC-SHA1',
             'oauth_timestamp': oauth_timestamp,
             'oauth_token': OAUTH_TOKEN,
             'oauth_version': '1.0',
    }
    param_string = ''
    i = 0
    for key in sorted(param.iterkeys()):
        param_string += key + '=' + urllib.quote_plus(param[key])
        i = i + 1
        if i < len(param):
            param_string += '&'
    http_method = 'GET'
    base_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    base_string = http_method + '&' + urllib.quote_plus(base_url) + '&' + urllib.quote_plus(param_string)
    return base_string

def get_OAuth_signature(screen_name, oauth_nonce, oauth_timestamp):
    return urllib.quote_plus(base64.b64encode(hmac.new(SIGNING_KEY, get_base_string(screen_name, oauth_nonce, oauth_timestamp), hashlib.sha1).digest()))

def main():
    screen_name = sys.argv[1]
    oauth_nonce = get_oauth_nonce()
    oauth_timestamp = get_oauth_timestamp()
    oauth_consumer_key = OAUTH_CONSUMER_KEY
    oauth_token = OAUTH_TOKEN
    oauth_signature = get_OAuth_signature(screen_name, oauth_nonce, oauth_timestamp)
    oauth_signature_method = OAUTH_SIGNATURE_METHOD
    oauth_version = OAUTH_VERSION
    long_str = 'OAuth oauth_consumer_key="%(oauth_consumer_key)s", oauth_nonce="%(oauth_nonce)s", oauth_signature="%(oauth_signature)s", oauth_signature_method="%(oauth_signature_method)s", oauth_timestamp="%(oauth_timestamp)s", oauth_token="%(oauth_token)s", oauth_version="%(oauth_version)s"' % locals()
    headers = {"Authorization": long_str,}
    conn = httplib.HTTPSConnection("api.twitter.com")
    conn.request("GET", "/1.1/statuses/user_timeline.json?screen_name=%s" % screen_name, headers=headers)
    res = conn.getresponse()
    print res.status, res.reason
    result = res.read()
    result = json.loads(result)
    for row in result:
        print row['text']
    print "你好世界！"

if __name__ == '__main__':
    main()
