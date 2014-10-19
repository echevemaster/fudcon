# -*- coding: utf-8 -*-
import os
import json
import logging
from flask import (Blueprint,
                   redirect, render_template,
                   url_for, flash, request)
from werkzeug import secure_filename
from sqlalchemy.sql import func
from fudcon.app import is_fudcon_admin, app
from fudcon.database import db
from fudcon.modules.contents.forms import AddPage
from fudcon.modules.contents.models import Content
from fudcon.modules.speakers.models import Speaker
from fudcon.modules.users.models import User
from fudcon.modules.speakers.forms import AddSpeaker
from fudcon.modules.sessions.models import (Session, SessionVoted, TALKS,
                                            BARCAMPS, WORKSHOPS)
from fudcon.modules.sessions.forms import AddSession
from fudcon.modules.rooms.models import Room
from fudcon.modules.rooms.forms import AddRoom
from fudcon.app import app
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        speaker = Speaker(names=form.names.data,
                          fas=form.fas.data,
                          bio=form.bio.data,
                          active=form.active.data)
        db.session.add(speaker)
        db.session.commit()
        flash('Ponente creado')
        return redirect(url_for('admin.speakers'))
    return render_template('backend/speakers_actions.html',
                           form=form,
                           title=u"Añadir speaker",
                           action=action)


@bp.route('/speakers/edit/<int:speaker_id>',
          methods=['GET', 'POST'])
@is_fudcon_admin
def edit_speaker(speaker_id):
    query_edit_speaker = Speaker.query.filter(Speaker.id ==
                                              speaker_id).first()
    form = AddSpeaker(obj=query_edit_speaker)
    action = url_for('admin.edit_speaker', speaker_id=speaker_id)
    if form.validate_on_submit():
        form.populate_obj(query_edit_speaker)
        db.session.commit()
        flash('Ponente actualizado')
        return redirect(url_for('admin.speakers'))
    return render_template('backend/speakers_actions.html',
                           title=u'Editar ponente',
                           form=form,
                           action=action)


@bp.route('/speakers/delete/<int:speaker_id>',
          methods=['GET', 'POST'])
@is_fudcon_admin
def delete_speaker(speaker_id):
    query_delete_speaker = Speaker.query.filter(
        Speaker.id == speaker_id).first()
    db.session.delete(query_delete_speaker)
    db.session.commit()
    flash('Ponente borrado')
    return redirect(request.referrer)


@bp.route('/rooms', methods=['GET', 'POST'])
@bp.route('/rooms/<int:page>', methods=['GET', 'POST'])
@is_fudcon_admin
def rooms(page=1):
    paginate_params = (page, items_per_page, False)
    queryset = Room.query.paginate(*paginate_params)
    return render_template('backend/rooms.html',
                           title='Listar salas',
                           rooms=queryset)


@bp.route('/rooms/add', methods=['GET', 'POST'])
@is_fudcon_admin
def add_room():
    form = AddRoom()
    action = url_for('admin.add_room')
    if form.validate_on_submit():
        room = Room(name=form.name.data,
                    description=form.description.data,)
        db.session.add(room)
        db.session.commit()
        flash(u'Sala creada')
        return redirect(url_for('admin.rooms'))
    return render_template('backend/rooms_actions.html',
                           form=form,
                           title=u"Añadir sala",
                           action=action)


@bp.route('/rooms/delete/<int:room_id>',
          methods=['GET', 'POST'])
@is_fudcon_admin
def delete_room(room_id):
    query_delete_room = Room.query.filter(
        Room.id == room_id).first()
    db.session.delete(query_delete_room)
    db.session.commit()
    flash('Sala borrada')
    return redirect(request.referrer)


@bp.route('/rooms/edit/<int:room_id>',
          methods=['GET', 'POST'])
@is_fudcon_admin
def edit_room(room_id):
    query_edit_room = Room.query.filter(Room.id ==
                                        room_id).first()
    form = AddRoom(obj=query_edit_room)
    action = url_for('admin.edit_room', room_id=room_id)
    if form.validate_on_submit():
        form.populate_obj(query_edit_room)
        db.session.commit()
        flash('Sala actualizada')
        return redirect(url_for('admin.rooms'))
    return render_template('backend/rooms_actions.html',
                           title=u'Editar sala',
                           form=form,
                           action=action)


@bp.route('/sessions', methods=['GET', 'POST'])
@bp.route('/sessions/<int:page>', methods=['GET', 'POST'])
@is_fudcon_admin
def sessions(page=1):
    paginate_params = (page, items_per_page, False)
    queryset = Session.query.paginate(*paginate_params)
    return render_template('backend/sessions.html',
                           title='Listar sesiones',
                           sessions=queryset)


@bp.route('/sessions/add', methods=['GET', 'POST'])
@is_fudcon_admin
def add_session():
    form = AddSession()
    action = url_for('admin.add_session')
    choices_session = [(TALKS, 'Charlas'),
                      (BARCAMPS, 'Mesas de trabajo'),
                      (WORKSHOPS, 'Talleres')]
    form.session_type.choices = choices_session
    query_room = Room.query.all()
    choices_room = [(c.id, c.name) for c in query_room]
    form.room_id.choices = choices_room
    query_fas = Speaker.query.filter(Speaker.active == 1).all()
    choices_fas = [(c.fas, c.names) for c in query_fas]
    form.fas.choices = choices_fas
    if form.validate_on_submit():
        session = Session(name=form.name.data,
                          topic=form.topic.data,
                          description=form.description.data,
                          session_type=form.session_type.data,
                          fas=form.fas.data,
                          room_id=form.room_id.data,
                          day=form.day.data,
                          time_start=form.time_start.data,
                          time_end=form.time_end.data,
                          active=form.active.data)
        db.session.add(session)
        db.session.commit()
        flash(u'Sesión creada')
        return redirect(url_for('admin.sessions'))
    return render_template('backend/sessions_actions.html',
                           form=form,
                           title=u"Añadir sesión",
                           action=action)


@bp.route('/sessions/edit/<int:session_id>',
          methods=['GET', 'POST'])
@is_fudcon_admin
def edit_session(session_id):
    query_edit_session = Session.query.filter(Session.id ==
                                              session_id).first()
    form = AddSession(obj=query_edit_session)
    action = url_for('admin.edit_session', session_id=session_id)
    choices_session = [(TALKS, 'Charlas'),
                      (BARCAMPS, 'Mesas de trabajo'),
                      (WORKSHOPS, 'Talleres')]
    form.session_type.choices = choices_session
    query_room = Room.query.all()
    choices_room = [(c.id, c.name) for c in query_room]
    form.room_id.choices = choices_room
    query_fas = Speaker.query.filter(Speaker.active == 1).all()
    choices_fas = [(c.fas, c.names) for c in query_fas]
    form.fas.choices = choices_fas
    if form.validate_on_submit():
        form.populate_obj(query_edit_session)
        db.session.commit()
        flash('Sesion actualizada')
        return redirect(url_for('admin.sessions'))
    return render_template('backend/sessions_actions.html',
                           title=u'Editar sesión',
                           form=form,
                           action=action)


@bp.route('/sessions/delete/<int:session_id>',
          methods=['GET', 'POST'])
@is_fudcon_admin
def delete_session(session_id):
    query_delete_session = Session.query.filter(
        Session.id == session_id).first()
    db.session.delete(query_delete_session)
    db.session.commit()
    flash(u'Sesión Borrada')
    return redirect(request.referrer)


@bp.route('/votation_talks',
          methods=['GET', 'POST'])
@is_fudcon_admin
def votation_talks():
    query_votation_talks = Session.query.\
        with_entities(Session.name,
                      db.func.count(SessionVoted.value).label('count_talks')).\
        join(Session.votes).group_by(Session.id).\
        filter(Session.active == 1,
               Session.session_type == 1).all()
    query_users = User.query.count()

    return render_template('backend/votation_talks.html',
                           title=u'Ver votación',
                           talks=query_votation_talks,
                           count_users=query_users)

@bp.route('/uploads', methods=['GET', 'POST'])
@is_fudcon_admin
def upload():
    """Upload files from froala editor"""
    file = request.files['file']
    if file:
        if not os.path.exists(upload_folder):
            try:
                os.makedirs(upload_folder)
            except OSError as e:
                if e.eerno != e.EEXIST:
                    app.logger.debug('Error %s:%s',e.eerno, e.error)

        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        url = url_for('static', filename='uploads/' + filename)
        link = '%s' % (url)
        return json.dumps({'link': link})
