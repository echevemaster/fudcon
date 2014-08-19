# -*- coding: utf-8 -*-
from flask import (Blueprint,
                   redirect, render_template,
                   url_for, flash)
from fudcon.app import is_fudcon_admin
from fudcon.database import db
from fudcon.modules.contents.forms import AddPage
from fudcon.modules.contents.models import Content

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/', methods=['GET', 'POST'])
@is_fudcon_admin
def index():
    """ Admin blueprint for this application
    """
    return render_template('backend/index.html',
                           title='Administration')


@bp.route('/pages/add', methods=['GET', 'POST'])
def add_page():
    """ Add page to the application
    """
    form = AddPage()
    action = url_for('admin.add_page')
    if form.validate_on_submit():
        content = Content(title=form.title.data,
                          description=form.description.data,
                          content_type=form.content_type.data,
                          is_on_user_menu=form.is_on_user_menu.data,
                          tag=form.tag.data,
                          active=form.active.data)
        db.session.add(content)
        db.session.commit()
        flash('Page created')
        return redirect(url_for('admin.page'))
    return render_template('backend/pages_actions.html',
                           form=form,
                           title='Add page',
                           action=action)
