# coding:utf-8

from flask import current_app
from flask.ext.script import Command, prompt, prompt_pass
from ..security.forms import RegisterForm
from ..security.registerable import register_user
from werkzeug.datastructures import MultiDict

from ..services import userService, roleService


class CreateUserCommand(Command):
    def run(self):
        email = prompt('Email')
        password = prompt_pass('Password')
        fullname = prompt('Fullname')
        data = MultiDict(dict(email=email, password=password, fullname=fullname))
        form = RegisterForm(data, csrf_enabled=False)
        if form.validate():
            user = register_user(email=email, password=password, fullname=fullname)
            print '\nUser created successfully'
            print 'User(id=%s email=%s)' % (user.id, user.email)
            return
        print '\nError creating user:'
        for errors in form.errors.values():
            print '\n'.join(errors)


class DeleteUserCommand(Command):
    def run(self):
        email = prompt("Email")
        user = userService.first(email=email)
        if not user:
            print 'Invalid user'
            return
        userService.delete(user)
        print 'User deleted successfully'


class CreateRoleCommand(Command):
    def run(self):
        name = prompt("Role name")
        description = prompt("Role description")
        role = roleService.create(name=name, description=description)
        print '\nRole created successfully'
        print 'Role(id=%s name=%s)' % (role.id, role.name)
        return


class DeleteRoleCommand(Command):
    def run(self):
        name = prompt("Role name")
        role = roleService.first(name=name)
        if not role:
            print 'Invalid role'
            return
        roleService.delete(role)
        print 'Role deleted successfully'

