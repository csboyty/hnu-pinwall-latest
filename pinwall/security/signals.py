# coding: utf-8

import blinker

signals = blinker.Namespace()

user_registered = signals.signal("user-registered")

user_confirmed = signals.signal("user-confirmed")

confirm_instructions_sent = signals.signal("confirm-instructions-sent")

password_changed = signals.signal("password-changed")

password_reset = signals.signal("password-reset")

reset_password_instructions_sent = signals.signal("password-reset-instructions-sent")