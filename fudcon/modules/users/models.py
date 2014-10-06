# -*- coding: utf-8 -*-
"""
fudcon.modules.users.models
~~~~~~~~~~~~~~~~~~~~~

Users models
"""

from flask.ext.login import UserMixin
from fudcon.database import db


class User(db.Model, UserMixin):
    """
    Model for users of the applications
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    name  = db.Column(db.String(255))
    email = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)

    def is_active(self):
        return self.active

