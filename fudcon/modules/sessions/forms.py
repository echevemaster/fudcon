# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import (TextField, BooleanField,
                     TextAreaField, SelectField)
from wtforms.validators import Required


class AddSession(Form):
    name = TextField(u'Nombre de la sesión:',
                     [Required(u'Ingrese el nombre de la sesión')])
    topic = TextField(u'Tópico de la sesión:',
                      [Required(u'Ingrese el nombre del tópico')])
    description = TextAreaField(u'Descripción de la sesión',
                                [Required(u'Ingrese la descripción')])
    session_type = SelectField(u'Tipo de sesión',
                               [Required(u'Ingrese el tipo de sesión')])
    active = BooleanField(u'Activo?:')
