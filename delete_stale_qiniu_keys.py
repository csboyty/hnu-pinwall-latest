
import redis
import datetime
import time

import qiniu.conf
import qiniu.rs
from qiniu.auth.digest import Client, Mac
from qiniu.rs import EntryPath

interval = 24 * 60 * 60
redis_url = "redis://localhost:6379/10"
redis_key = "pw:qiniu:keys"

qiniu.conf.ACCESS_KEY = "Q-DeiayZfPqA0WDSOGSf-ekk345VrzuZa_6oBrX_"
qiniu.conf.SECRET_KEY = "fIiGiRr3pFmHOmBDR2Md1hTCqpMMBcE_gvZYMzwD"
qiniu_bucket = "design-pinwall"

_mac = Mac(access=qiniu.conf.ACCESS_KEY, secret=qiniu.conf.SECRET_KEY)

r = redis.StrictRedis.from_url(redis_url, max_connections=1)


def _time():
    utc_now = datetime.datetime.utcnow()
    utc_today = datetime.date(utc_now.year, utc_now.month, utc_now.day)
    utc_yesterday = utc_today - datetime.timedelta(days=1)
    return time.mktime(utc_yesterday.timetuple())


def do_delete_qiniu_keys():
    max_value = _time()
    keys = r.zrangebyscore(redis_key, 0, max_value)
    start, end = 0, 100
    client = qiniu.rs.Client(mac=_mac)
    while keys:
        part_keys = keys[start:end]
        if part_keys:
  #          entries = []
    #        for key in part_keys:
     #           entries.append(EntryPath(qiniu_bucket, key))

 #           client.batch_delete(entries)
            start, end = end, end + 100
        else:
            break

    if keys:
        r.zremrangebyscore(redis_key, 0, max_value)


def cron_delete():
    try:
        while 1:
            try:
                do_delete_qiniu_keys()
            except Exception:
                pass

            print "delete stale keys"
            time.sleep(interval)
    except KeyboardInterrupt:
        pass
    finally:
        r.connection_pool.disconnect()


if __name__ == "__main__":
    cron_delete()


