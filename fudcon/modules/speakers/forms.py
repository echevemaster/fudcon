# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import Required


class AddSpeaker(Form):
    names = TextField(u'Nombres:',
                      [Required(u'Ingrese el nombre del ponente')])
    fas = TextField(u'Cuenta FAS:')
    bio = TextAreaField(u'Bio:',
                        [Required(u'Ingrese la bio del ponente')])
    active = BooleanField(u'Activo?')
