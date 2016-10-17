# coding:utf-8

import json
from base64 import urlsafe_b64encode
import urllib
import datetime
import qiniu.conf
import qiniu.rs
from qiniu.auth.digest import Client, Mac

from errors import PinwallError
import settings

qiniu.conf.ACCESS_KEY = settings.qiniu_ak
qiniu.conf.SECRET_KEY = settings.qiniu_sk

qiniu_baseurl = settings.qiniu_baseurl
qiniu_bucket = settings.qiniu_bucket

_mac = Mac(access=qiniu.conf.ACCESS_KEY, secret=qiniu.conf.SECRET_KEY)


def upload_token(bucket=qiniu_bucket, key=None, expires=datetime.timedelta(days=1), **kwargs):
    scope = bucket if not key else "%s:%s" % (bucket, key)
    policy = qiniu.rs.PutPolicy(scope)
    policy.expires = int(expires.total_seconds())
    for key, val in kwargs.iteritems():
        setattr(policy, key, val)
    return policy.token()


def delete_by_key(bucket=qiniu_bucket, key_or_url=None):
    if key_or_url:
        key = key_from_url(key_or_url)
        ret, err = qiniu.rs.Client().delete(bucket, key)
        if err is not None:
            raise PinwallError("delete <%s>:<%s> error" % (bucket, key), "QINIU_ERROR")


def key_from_url(key_or_url):
    if key_or_url.startswith(qiniu_baseurl):
        key = urllib.unquote(key_or_url)[len(qiniu_baseurl):]
        return key.encode("UTF-8")
    else:
        return key_or_url


def mk_image_thumbnail(bucket=qiniu_bucket, key_or_url=None, image_sizes=None, save_bucket=qiniu_bucket):
    if key_or_url and image_sizes:
        key = key_from_url(key_or_url)
        if "." in key:
            last_dot = key.rindex('.')
        else:
            last_dot = len(key)
        entry_format = "%(save_bucket)s:%(prefix)s-%(image_size)s%(suffix)s"
        fops = ["imageMogr2/thumbnail/%(image_size)s|saveas/%(encoded_entry)s"
                % {"image_size": image_size if image_size.split('x')[0] == image_size.split('x')[1] else '!%sr' % image_size,
                   "encoded_entry": urlsafe_b64encode(
                       entry_format % {"save_bucket": save_bucket, "prefix": key[:last_dot],
                                       "image_size": image_size,
                                       "suffix": key[last_dot:]})}
                for image_size in image_sizes]
        data = dict([("bucket", bucket), ("key", key), ("fops", ";".join(fops))])

        client = Client("api.qiniu.com", mac=_mac)
        client.set_header("Content-Type", "application/x-www-form-urlencoded")
        resp = client.round_tripper(method="POST", path="/pfop", body=urllib.urlencode(data),header={"Content-Type":"application/x-www-form-urlencoded"})
        #result = json.loads(resp.read())
        #print result
        #return result


def rm_image_thumbnail(bucket=qiniu_bucket, key_or_url=None, image_sizes=None):
    #print "qiniu rm_image_thumbnail"
    if key_or_url:
        key = key_from_url(key_or_url)
        if "." in key:
            last_dot = key.rindex('.')
        else:
            last_dot = len(key)
        key_format = "%(prefix)s-%(image_size)s%(suffix)s"
        keys = [qiniu.rs.EntryPath(bucket, key_format % {"prefix": key[:last_dot], "image_size": image_size,
                                                         "suffix": key[last_dot:]}) for image_size in image_sizes]
        keys.append(qiniu.rs.EntryPath(bucket, key))
        qiniu.rs.Client(mac=_mac).batch_delete(keys)


def rm_key(bucket=qiniu_bucket, key_or_url=None):
    #print "qiniu rm_key"
    if key_or_url:
        key = key_from_url(key_or_url)
        qiniu.rs.Client(mac=_mac).delete(bucket, key)


if __name__ == "__main__":
    rm_image_thumbnail(key_or_url="11271644574208-4a1.jpg", image_sizes=["200x200", "400x400", "800x800"])
    # from qiniu import io
    #
    # uptoken = upload_token()
    # ret, err = io.put(uptoken, "1.txt", "abcabc")
    # if err:
    # print err
    # else:
    # print ret






