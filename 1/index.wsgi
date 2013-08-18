# -*- coding:utf-8 -*- 
from bottle import Bottle, run

import sae
import urllib2
import urllib
import cookielib
import re
import os
import sys
import weibo
import json

app = Bottle()
os.environ['disable_fetchurl'] = True

@app.route('/')
def hello():
    print '1111111111'
    return "done"

@app.route('/xiamicheckin' , method='GET')
def xiami():
    print '1111'
    os.environ['REMOTE_ADDR'] = '211.67.16.50'
    APP_KEY = 'xxxxxx'
    MY_APP_SECRET = 'xxxxxxxxxxxxxxx'
    REDIRECT_URL = 'https://api.weibo.com/oauth2/default.html'
#这个是设置回调地址，必须与那个”高级信息“里的一致

#请求用户授权的过程
    AUTH_URL = 'https://api.weibo.com/oauth2/authorize'
    USERID = 'xxxxxxxx'
    PASSWD ='xxxxxxxxxxxxxxx'
    client = weibo.APIClient(APP_KEY, MY_APP_SECRET, redirect_uri=REDIRECT_URL)
    referer_url = client.get_authorize_url()
  
    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    urllib2.install_opener(opener)
    postdata = {"client_id": APP_KEY,
             "redirect_uri": REDIRECT_URL,
             "userId": USERID,
             "passwd": PASSWD,
             "isLoginSina": "0",
             "action": "submit",
             "response_type": "code",
             }
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0",
               "Host": "api.weibo.com",
               "Referer": referer_url
             }
    req  = urllib2.Request(
                           url = AUTH_URL,
                           data = urllib.urlencode(postdata),
                           headers = headers)
    try:
        resp = urllib2.urlopen(req)
        print "callback url is : %s" % resp.geturl()
        #print "code is : %s" % resp.geturl()[-32:]
    except Exception, e:
        print e
    code=resp.geturl()[-32:]
#获得用户授权
    print code
    request = client.request_access_token(code, REDIRECT_URL)

#保存access_token ,exires_in, uid
    access_token = request.access_token
    #print access_token
    expires_in = request.expires_in
    uid = request.uid
    #print uid
    client.set_access_token(access_token, expires_in)
    print '72'
    
    #print '74'
    r = client.post.statuses__update(status=u'测试')
    print 'done'
    return "done"
application = sae.create_wsgi_app(app)