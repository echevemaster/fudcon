# -*- coding: utf-8 -*-
"""
fudcon.modules.speakers.models
~~~~~~~~~~~~~~~~~~~~~

Speakers models
"""

from fudcon.database import db


class Speaker(db.Model):
    """
    Model for listing all the attributes of
    the speakers
    """
    __tablename__ = 'speakers'

    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(255))
    fas = db.Column(db.String(255))
    bio = db.Column(db.Text())
    active = db.Column(db.Boolean())
