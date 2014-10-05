# -*- coding: utf-8 -*-
"""
fudcon.modules.rooms.models
~~~~~~~~~~~~~~~~~~~~~

Rooms models
"""

from fudcon.database import db

class Room(db.Model):
    """
    Model for the session rooms
    """
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text())
