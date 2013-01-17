#-*- coding:utf-8 -*-
from weibo import APIClient
import datetime
import time

APP_KEY = '' #Your app key
APP_SECRET = '' #Your app secret

CALLBACK_URL = '' # call back url

client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
url = client.get_authorize_url()
print url
code = raw_input()
r = client.request_access_token(code)
access_token = r.access_token
expires_in = r.expires_in
client.set_access_token(access_token, expires_in)
#print client.get.statuses__user_timeline(access_token=access_token, count=1)
#print client.get.statuses__user_timeline(access_token=access_token, count=1)

uid = client.get.account__get_uid()
uid = uid['uid']
total_statuses_count = client.get.users__show(uid=uid)
total_statuses_count = total_statuses_count['statuses_count']

now_count = 0
now_datetime = None
page = 1
f = None
if total_statuses_count % 45 != 0:
    total_statuses_count = (total_statuses_count / 45 + 1) * 45

while now_count <=total_statuses_count:
    mytimeline = client.get.statuses__user_timeline(count=45, page=page)
    if now_datetime == None:
        init_create = mytimeline['statuses'][0]['created_at']
        t = time.strptime(init_create, "%a %b %d %H:%M:%S +0800 %Y")
        status_date = datetime.date(t.tm_year, t.tm_mon, t.tm_mday)
        now_datetime = status_date.isoformat()
        filename = "my/%s.md" %  now_datetime
        print "begin to write %s" % now_datetime
        f = open(filename, "w+")
        #f.write("#%s\n" % now_datetime)
        f.write("Date: %s\n" % now_datetime)
        f.write("Title: %s my weibo day\n" % now_datetime)
        f.write("\n\n")

    for status in mytimeline['statuses']:
        created_date = status['created_at']
        t = time.strptime(created_date, "%a %b %d %H:%M:%S +0800 %Y")
        status_date = datetime.date(t.tm_year, t.tm_mon, t.tm_mday)
        date = status_date.isoformat()
        if date != now_datetime:
            f.close()
            print "write over %s" % now_datetime
            now_datetime = date
            filename = "my/%s.md" % now_datetime
            print "begin to write %s" % now_datetime
            f = open(filename, "w+")
            #f.write("#%s\n" % now_datetime)
            f.write("Date: %s\n" % now_datetime)
            f.write("Title: %s my weibo day\n" % now_datetime)
            f.write("\n\n")
        if "retweeted_status" in status:
            f.write(" ")
            f.write(status['text'].encode("utf-8"))
            f.write("\n")
            if 'user' in status['retweeted_status']:
                f.write(">@")
                f.write(status['retweeted_status']['user']['screen_name'].encode("utf-8") + ":")
                f.write(status['retweeted_status']['text'].encode("utf-8"))
                if 'original_pic' in status['retweeted_status']:
                    url = status['retweeted_status']['original_pic']
                    f.write("\n\n")
                    f.write("![pic](%s)" % url)
                f.write("\n\n")
            else:
                f.write(">微博被删除\n\n")
        else:
            f.write(" ")
            f.write(status['text'].encode("utf-8"))
            if 'original_pic' in status:
                url = status['original_pic']
                f.write("\n\n")
                f.write("![pic](%s)" % url)
            f.write("\n\n")

    page += 1
    now_count += 45







