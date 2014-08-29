# -*- coding: utf-8 -*-
import os
import json
from flask import (Blueprint,
                   redirect, render_template,
                   url_for, flash, request)
from werkzeug import secure_filename
from fudcon.app import is_fudcon_admin, app
from fudcon.database import db
from fudcon.modules.contents.forms import AddPage
from fudcon.modules.contents.models import Content
from fudcon.modules.speakers.models import Speaker
from fudcon.modules.speakers.forms import AddSpeaker


bp = Blueprint('admin', __name__, url_prefix='/admin')

items_per_page = app.config['ITEMS_PER_PAGE']
upload_folder = app.config['UPLOADS_FOLDER']


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
    upload_url = url_for('admin.upload')
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
                           title=u'Añadir página',
                           action=action,
                           upload_url=upload_url)


@bp.route('/pages/edit/<int:page_id>', methods=['GET', 'POST'])
@is_fudcon_admin
def edit_page(page_id):
    upload_url = url_for('admin.upload')
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
                           title=u'Editar página',
                           form=form,
                           action=action,
                           upload_url=upload_url)


@bp.route('/pages/delete/<int:page_id>', methods=['GET', 'POST'])
@is_fudcon_admin
def delete_page(page_id):
    """Delete pages given their id
    :param page_id: integer argument for delete pages.
    :returns: A redirection to the referrer page
    """
    query_delete_page = Content.query.filter(
        Content.id == page_id).first_or_404()
    db.session.delete(query_delete_page)
    db.session.commit()
    flash('Record deleted')
    return redirect(request.referrer)


@bp.route('/speakers', methods=['GET', 'POST'])
@bp.route('/speakers/<int:page>', methods=['GET', 'POST'])
@is_fudcon_admin
def speakers(page=1):
    paginate_params = (page, items_per_page, False)
    queryset = Speaker.query.paginate(*paginate_params)
    return render_template('backend/speakers.html',
                            title='Listar ponentes',
                            speakers=queryset)

@bp.route('/speakers/add', methods=['GET', 'POST'])
@is_fudcon_admin
def add_speaker():
    """ Add speakers to the application
    """
    form = AddSpeaker()
    action = url_for('admin.add_speaker')
    if form.validate_on_submit():
        speaker = Speaker()



@bp.route('/uploads', methods=['GET', 'POST'])
@is_fudcon_admin
def upload():
    """Upload files from froala editor"""
    file = request.files['file']
    if file:
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        url = url_for('static', filename='uploads/' + filename)
        link = '%s' % (url)
        return json.dumps({'link': link})
