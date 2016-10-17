# coding: utf-8

from .utils import get_identity_attributes, string_types


class Datastore(object):
    def __init__(self, db):
        self.db = db

    def commit(self):
        pass

    def put(self, model):
        raise NotImplementedError

    def delete(self, model):
        raise NotImplementedError


class SQLAlchemyDatastore(Datastore):
    def commit(self):
        self.db.session.commit()

    def put(self, model):
        self.db.session.add(model)
        return model

    def delete(self, model):
        self.db.session.delete(model)

    def merge(self, model):
        return self.db.session.merge(model)


class UserDatastore(object):
    def __init__(self, user_model, role_model):
        self.user_model = user_model
        self.role_model = role_model

    def _prepare_role_modify_args(self, user, role):
        if isinstance(user, string_types):
            user = self.find_user(email=user)
        if isinstance(role, string_types):
            role = self.find_role(role)
        return user, role

    def _prepare_create_user_args(self, **kwargs):
        kwargs.setdefault('active', False)
        roles = kwargs.get('roles', [])
        for i, role in enumerate(roles):
            rn = role.name if isinstance(role, self.role_model) else role
            roles[i] = self.find_role(rn)

        kwargs['roles'] = roles
        return kwargs

    def get_user(self, id_or_email):
        raise NotImplementedError

    def find_user(self, *args, **kwargs):
        raise NotImplementedError

    def find_role(self, *args, **kwargs):
        raise NotImplementedError

    def add_role_to_user(self, user, role):
        user, role = self._prepare_create_user_args(user, role)
        if role not in user._roles:
            user.add_role(role)
            self.put(user)
            return True
        return False

    def remove_role_from_user(self, user, role):
        rv = False
        user, role = self._prepare_role_modify_args(user, role)
        if role in user.roles:
            rv = True
            user.remove_role(role)
        return rv

    def toggle_active(self, user):
        """Toggles a user's active status. Always returns True."""
        user.active = not user.active
        return True

    def deactivate_user(self, user):
        """Deactivates a specified user. Returns `True` if a change was made.

        :param user: The user to deactivate
        """
        if user.active:
            user.active = False
            return True
        return False

    def activate_user(self, user):
        """Activates a specified user. Returns `True` if a change was made.

        :param user: The user to activate
        """
        if not user.active:
            user.active = True
            return True
        return False

    def create_role(self, **kwargs):
        """Creates and returns a new role from the given parameters"""
        role = self.role_model(**kwargs)
        return self.put(role)

    def find_or_create_role(self, name, **kwargs):
        """Returns a role matching the given name or creates it with any
        additionally provided parameters
        """
        kwargs["name"] = name
        return self.find_role(name) or self.create_role(**kwargs)

    def create_user(self, **kwargs):
        """Creates and returns a new user from the given parameters."""
        kwargs = self._prepare_create_user_args(**kwargs)
        user = self.user_model(**kwargs)
        return self.put(user)

    def delete_user(self, user):
        """ Delete the specified user """
        self.delete(user)

    def load_user_from_dict(self, user_dict):
        model = self.user_model()
        for (key, value) in user_dict.iteritems():
            setattr(model, key, value)
        return model


class SQLAlchemyUserDatastore(SQLAlchemyDatastore, UserDatastore):
    """A SQLAlchemy datastore implementation for Flask-Security that assumes the
    use of the Flask-SQLAlchemy extension."""

    def __init__(self, db, user_model, role_model):
        SQLAlchemyDatastore.__init__(self, db)
        UserDatastore.__init__(self, user_model, role_model)

    def get_user(self, identifier):
        for attr in get_identity_attributes():
            query = getattr(self.user_model, attr) == identifier
            rv = self.user_model.query.filter(query).first()
            if rv is not None:
                return rv


    def find_user(self, **kwargs):
        return self.user_model.query.filter_by(**kwargs).first()

    def find_role(self, role):
        return self.role_model.query.filter_by(name=role).first()
