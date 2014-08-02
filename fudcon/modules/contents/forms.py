# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SelectField, BooleanField
from wtforms.validators import Required
from fudcon.modules.contents.models import PAGES, POSTS


class AddPage(Form):
    title = TextField(u'Title',
                      [Required(u'Add the title of the page')])
    description = TextAreaField(u'Description',
                                [Required(u'Add the description of the page')])
    content_type = SelectField(u'Content Type:', coerce=int, choices=
                               [(PAGES, u'Page'),
                               (POSTS, u'Post')])
    is_on_user_menu = BooleanField(u'Is on user menu?',
                                   [Required(u'Select the menu option or not')])
    tag = TextField(u'Tag:',
                    [Required(u'Add the tag for the main pages')])
    active = active = BooleanField(u'Active?',
                                   [Required(u'Select the status of the page')])
