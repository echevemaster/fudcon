# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import (TextField, BooleanField,
                     TextAreaField, SelectField)
from wtforms_components import TimeField
from wtforms.validators import Required


class AddSession(Form):
    name = TextField(u'Nombre de la sesión:',
                     [Required(u'Ingrese el nombre de la sesión')])
    topic = TextField(u'Tópico de la sesión:',
                      [Required(u'Ingrese el nombre del tópico')])
    description = TextAreaField(u'Descripción de la sesión:')
    session_type = SelectField(u'Tipo de sesión', coerce=int,
                               choices=[])
    fas = SelectField(u'Ponente',
                      choices=[])
    room_id = SelectField(u'Sala', coerce=int,
                               choices=[])
    time_start = TimeField(u'Hora de inicio')
    time_end = TimeField(u'Hora de fin')
    active = BooleanField(u'Activo?:')
