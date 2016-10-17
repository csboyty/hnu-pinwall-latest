# coding:utf-8
import os
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.contrib.fixers import ProxyFix
from pinwall import api, frontend,weixin
from pinwall.redis_tool import rand_captcha


frontend_setting_override = {
    'SECURITY_LOGINABLE': True,
    'SECURITY_LOGOUTABLE': True,
    'SECURITY_CONFIRMABLE': True,
    'SECURITY_REGISTERABLE': True,
    'SECURITY_RECOVERABLE': True,
    'SECURITY_TRACKABLE': False,
    'SECURITY_CHANGEABLE': True,
    'SECURITY_IDENTIFIABLE': True,
    'SECURITY_CAPTCHABLE': True,
    'SECURITY_CAPTCHA_FUNC': rand_captcha,
    'SECURITY_POST_LOGIN_VIEW': 'http://design.hnu.edu.cn/pinwall',
    'SECURITY_POST_LOGOUT_VIEW': 'http://design.hnu.edu.cn/pinwall',
    'SECURITY_POST_REGISTER_VIEW': 'http://design.hnu.edu.cn/pinwall',
    'SECURITY_POST_CONFIRM_VIEW': 'http://design.hnu.edu.cn/pinwall',
    'SECURITY_POST_RESET_VIEW': 'http://design.hnu.edu.cn/pinwall',
    'SECURITY_POST_CHANGE_VIEW': 'http://design.hnu.edu.cn/pinwall',
}

api_setting_override = {
    'SECURITY_LOGINABLE': False,
    'SECURITY_LOGOUTABLE': False,
    'SECURITY_CONFIRMABLE': False,
    'SECURITY_REGISTERABLE': False,
    'SECURITY_RECOVERABLE': False,
    'SECURITY_TRACKABLE': False,
    'SECURITY_CHANGEABLE': False,
}


application = ProxyFix(
    DispatcherMiddleware(
        frontend.create_app(settings_override=frontend_setting_override),
        {
            '/api': api.create_app(register_security_blueprint=False),
            '/weixin': weixin.create_app()
        }
    )
)

if __name__ == "__main__":
    # run_simple('0.0.0.0', 80, application, use_reloader=True, use_debugger=True)
    run_simple('0.0.0.0', 80, application)
