# coding:utf-8
import redis
import json
import random
import time

import settings

img_keys_name = "pw:captcha:keys"

qiniu_temp_keys = "pw:qiniu:keys"

r = redis.StrictRedis.from_url(settings.redis_url)

img_keys = json.loads(r.get(img_keys_name))
img_keys_length = len(img_keys)


def rand_captcha():
    rand_value = random.randint(0, img_keys_length)
    img_chars = img_keys[rand_value]
    return img_chars, r.get("pw:captcha:" + img_chars)


def register_qiniu_key(key, register_time=time.time()):
    r.zadd(qiniu_temp_keys, int(register_time), key)
