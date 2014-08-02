# -*- coding: utf-8 -*-
"""
fudcon.modules.users.models
~~~~~~~~~~~~~~~~~~~~~

Users models
"""

from fudcon.database import db


class User(db.Model):
    """
    Model for users of the applications
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(255))
    fas = db.Column(db.String(255))
    email = db.Column(db.String(255))
    active = db.Column(db.Boolean())
