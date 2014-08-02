# -*- coding: utf-8 -*-
"""
fudcon.modules.contents.models
~~~~~~~~~~~~~~~~~~~~~

Contents models
"""

from fudcon.database import db

POSTS = 1
PAGES = 2


class Content(db.Model):
    """
    Model for entries of posts and pages of the
    webpage
    """
    __tablename__ = 'contents'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    slug = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text())
    content_type = db.Column(db.SmallInteger(), default=POSTS)
    is_on_user_menu = db.Column(db.Boolean())
    tag = db.Column(db.String(255))
    active = db.Column(db.Boolean())
