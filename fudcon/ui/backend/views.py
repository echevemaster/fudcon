# -*- coding: utf-8 -*-
from flask import request, Blueprint, redirect, render_template
from flask import url_for, g, current_app
from fudcon.app import is_fudcon_admin
from fudcon.modules.contents.forms import AddPage

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
        return redirect(url_for('admin.page'))
    return render_template('backend/pages_actions.html',
                           form=form,
                           title='Add page',
                           action=action)
