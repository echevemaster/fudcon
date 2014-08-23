# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SelectField, BooleanField
from wtforms.validators import Required
from fudcon.modules.contents.models import PAGES, POSTS


class AddPage(Form):
    title = TextField(u'Título',
                      [Required(u'Agregue el título de la página')])
    description = TextAreaField(u'Descripción',
                                [Required(u'Agregue la descripción de la pagina')])
    content_type = SelectField(u'Tipo de contenido:', coerce=int, choices=
                               [(PAGES, u'Página'),
                               (POSTS, u'Post')])
    is_on_user_menu = BooleanField(u'Está en el menú de usuario?')
    tag = TextField(u'Tag:',
                    [Required(u'Agregue un tag')])
    active = active = BooleanField(u'Activo?')
