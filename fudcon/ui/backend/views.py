# -*- coding: utf-8 -*-
from flask import (Blueprint,
                   redirect, render_template,
                   url_for, flash, request)
from fudcon.app import is_fudcon_admin, app
from fudcon.database import db
from fudcon.modules.contents.forms import AddPage
from fudcon.modules.contents.models import Content

bp = Blueprint('admin', __name__, url_prefix='/admin')

items_per_page = app.config['ITEMS_PER_PAGE']


@bp.route('/', methods=['GET', 'POST'])
@is_fudcon_admin
def index():
    """ Admin blueprint for this application
    """
    return render_template('backend/index.html',
                           title='Administration')


@bp.route('/pages', methods=['GET', 'POST'])
@bp.route('pages/<int:page>', methods=['GET', 'POST'])
@is_fudcon_admin
def pages(page=1):
    paginate_params = (page, items_per_page, False)
    queryset = Content.query.paginate(*paginate_params)
    return render_template('backend/pages.html',
                           title='List pages',
                           pages=queryset)


@bp.route('/pages/add', methods=['GET', 'POST'])
@is_fudcon_admin
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
        return redirect(url_for('admin.pages'))
    return render_template('backend/pages_actions.html',
                           form=form,
                           title='Add page',
                           action=action)


@bp.route('/pages/edit/<int:page_id>', methods=['GET', 'POST'])
@is_fudcon_admin
def edit_page(page_id):
    query_edit_page = Content.query.filter(Content.id ==
                                           page_id).first_or_404()
    form = AddPage(obj=query_edit_page)
    action = url_for('admin.edit_page', page_id=page_id)
    if form.validate_on_submit():
        form.populate_obj(query_edit_page)
        db.session.commit()
        flash('Page edited')
        return redirect(url_for('admin.pages'))
    return render_template('backend/pages_actions.html',
                           form=form,
                           action=action)


@bp.route('/pages/delete/<int:page_id>', methods=['GET', 'POST'])
@is_fudcon_admin
def delete_page(page_id):
    query_delete_page = Content.query.filter(
        Content.id == page_id).first_or_404()
    db.session.delete(query_delete_page)
    db.session.commit()
    flash('Record deleted')
    return redirect(request.referrer)
