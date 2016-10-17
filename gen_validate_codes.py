# coding=utf-8

import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cStringIO as StringIO
import string
import redis
import json


redis_url = "redis://localhost:6379/10"

r = redis.StrictRedis.from_url(redis_url, max_connections=1)





chars = string.digits + string.ascii_lowercase


def create_validate_code(size=(140, 40), chars=chars, mode="RGB", bg_color=(255, 255, 255), fg_color=(255, 0, 0),
                         font_size=18, font_type="/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf", length=6,
                         draw_points=False,
                         point_chance=2):
    """

    :param size: 图片的大小，格式（宽，高），默认为(140, 40)
    :param chars: 允许的字符集合，格式字符串
    :param mode: 图片模式，默认为RGB
    :param bg_color: 背景颜色，默认为白色
    :param fg_color: 前景色，验证码字符颜色
    :param font_size: 验证码字体大小
    :param font_type: 验证码字体
    :param length: 验证码字符个数
    :param draw_points: 是否画干扰点
    :param point_chance: 干扰点出现的概率，大小范围[0, 50]
    :return:
    """
    width, height = size
    img = Image.new(mode, size, bg_color)
    # 创建图形
    draw = ImageDraw.Draw(img)
    # 创建画笔

    def get_chars():
        # 生成给定长度的字符串，返回列表格式
        return random.sample(chars, length)

    def create_points():
        chance = min(50, max(0, int(point_chance)))
        for w in xrange(width):
            for h in xrange(height):
                tmp = random.randint(0, 50)
                if tmp > 50 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        c_chars = get_chars()
        strs = '%s' % ''.join(c_chars)
        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)
        draw.text(((width - font_width) / 3, (height - font_height) / 4),
                  strs, font=font, fill=fg_color)
        return strs

    if draw_points:
        create_points()
    strs = create_strs()
    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
    ]
    img = img.transform(size, Image.PERSPECTIVE, params)
    # 创建扭曲
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, strs


image_keys = set()
for i in xrange(200):
    img, img_chars = create_validate_code()
    buf = StringIO.StringIO()
    img.save(buf, 'JPEG', quality=70)
    img_buf = buf.getvalue()
    image_keys.add(img_chars)
    r.set("pw:captcha:" + img_chars, img_buf)

r.set("pw:captcha:keys", json.dumps(list(image_keys)))

