#!/usr/bin/python
# coding=UTF-8

# import datetime
import schedule
import time
from weibo import APIClient

APP_KEY = '<app key>' # app key
APP_SECRET = '<app secret>' # app secret
CALLBACK_URL = '<callback url>' # callback url
tokenFilePath = 'access_token_'+APP_KEY

client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

def init():
    try:
        with open(tokenFilePath) as f:
            access_token = f.readline().strip('\n')
            expires_in = int(f.readline())
    except IOError:
        print 'access_token not exist, re-authorize ...'
        
        url = client.get_authorize_url()
        print 'Get auth code from this URL: ', url

        code = raw_input('Input code: ')
        r = client.request_access_token(code)
        access_token = r.access_token
        expires_in = r.expires_in

        with open(tokenFilePath, 'w') as f:
            f.writelines([access_token, '\n', str(expires_in)])

    client.set_access_token(access_token, expires_in)

    return True

def run():
    print 'Post a weibo.'
    client.statuses.share.post(status=u'This is a test. https://github.com/TomDu/WeiboBot')

if init():
    schedule.every().day.at("15:30").do(run)

    while True:
        schedule.run_pending()
        time.sleep(1)
