# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import (TextField, BooleanField,
                     TextAreaField, SelectField)
from wtforms_components import TimeField
from wtforms.validators import Required, Optional


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
    day = SelectField(u'Ingrese el día', coerce=int, choices=[
                      (23, '23'),
                      (24, '24'),
                      (25, '25')])
    time_start = TimeField(u'Hora de inicio', [Optional()])
    time_end = TimeField(u'Hora de fin', [Optional()])

    active = BooleanField(u'Activo?:')


class AddBarcamp(Form):
    session_id = SelectField(u'Elija su sesión preferida',
                             coerce=int,
                             choices=[])
