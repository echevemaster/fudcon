# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import (TextField)
from wtforms.validators import Required, Email


class UserForm(Form):
    username = None
    password = None
    name = TextField(u'Nombres:',
                     [Required(u'Debe ingresar su nombre')])
    email = TextField(u'Email:', 
                      [Email(u'Su email está mal formado')])
    active = None

