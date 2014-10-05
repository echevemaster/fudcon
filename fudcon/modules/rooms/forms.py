# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import (TextField, BooleanField,
                     TextAreaField, SelectField)
from wtforms.validators import Required


class AddRoom(Form):
    name = TextField(u'Nombre del salón:',
                     [Required(u'Ingrese el nombre o número del salón')])
    description = TextAreaField(u'Descripción de la sala:')
