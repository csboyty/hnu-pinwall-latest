# coding:utf-8

import os

basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

DEBUG = False
SECRET_KEY = 'pinwall-2014-secret-key'
# SERVER_NAME = "192.168.2.104:8000"

WTF_CSRF_ENABLED = False

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://dbuser:dbpassword@127.0.0.1:6432/design_pinwall'
SQLALCHEMY_POOL_SIZE = 20
SQLALCHEMY_ECHO = False

MAIL_DEFAULT_SENDER = "design@hnu.edu.cn"
MAIL_SERVER = "smtp.hnu.edu.cn"
MAIL_PORT = 25
MAIL_USE_TLS = True

SECURITY_POST_LOGIN_VIEW = "/"
SECURITY_POST_LOGOUT_VIEW = "/"
SECURITY_CONFIRM_SALT = "pinwall:confirm:salt"
SECURITY_REMEMBER_SALT = "pinall:remember:salt"
SECURITY_RESET_SALT = "pinwall:reset:salt"
SECURITY_PASSWORD_PREFIX = "13640661"
SECURITY_EMAIL_SENDER = "design@hnu.edu.cn"

CACHE_TYPE = "redis"
CACHE_REDIS_HOST = "localhost"
CACHE_REDIS_PORT = 6379
CACHE_KEY_PREFIX = "pw:"
CACHE_REDIS_DB = 11

CELERY_BROKER_URL = "redis://localhost:6379/12"
#CELERY_BACKEND_URL = "redis://localhost:6379/12"
CELERY_DEFAULT_QUEUE= "pinwall"
#CELERY_TASK_SERIALIZER = "json"
#CELERY_ACCEPT_CONTENT = ["json"]
#CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True

BOXVIEW_TOKEN = "ifv4pgix1qgghjjinibe91bygak4nteq"
BOXVIEW_BASE_URL = 'https://view-api.box.com'
BOXVIEW_UPLOAD_BASE_URL = 'https://upload.view-api.box.com'
BOXVIEW_API_VERSION = '/1'
BOXVIEW_VIEW_API_URL = '{}{}'.format(BOXVIEW_BASE_URL, BOXVIEW_API_VERSION)
BOXVIEW_UPLOAD_VIEW_API_URL = '{}{}'.format(BOXVIEW_UPLOAD_BASE_URL, BOXVIEW_API_VERSION)
BOXVIEW_SESSION_BASE_URL = '{}/view/'.format(BOXVIEW_BASE_URL)

WEROBOT_TOKEN = "pinwall"
WEROBOT_ROLE = "/"

domain_name = "http://design.hnu.edu.cn/pinwall"
default_user_profile = "http://design.hnu.edu.cn/pinwall/images/default_profile.jpg"

redis_url = "redis://localhost:6379/10"
tmp_dir = u"/var/app/pinwall/tmp"
qiniu_sync_dir = "/var/app/pinwall/qiniu-files/"
qiniu_baseurl = "http://design-pinwall.qiniudn.com/"
qiniu_html5_prefix = "http://design-pinwall.qiniudn.com/html5/"
qiniu_bucket = "design-pinwall"
qiniu_ak = "Q-DeiayZfPqA0WDSOGSf-ekk345VrzuZa_6oBrX_"
qiniu_sk = "fIiGiRr3pFmHOmBDR2Md1hTCqpMMBcE_gvZYMzwD"

show_boxview_uri = domain_name + "/boxview"

cache_timeout = 24 * 60 * 60

es_hosts = [("http", "localhost", "19200"), ]
es_timeout = 5
es_index = "pinwall"
