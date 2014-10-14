# -*- coding: utf-8 -*-
import os
import datetime
from flask import (Blueprint, render_template, g,
                   url_for, redirect, flash, request)
from sqlalchemy import or_
from flask.ext.login import login_required, logout_user
from fudcon.database import db
from fudcon.modules.contents.models import Content
from fudcon.modules.speakers.models import Speaker
from fudcon.modules.sessions.models import Session, SessionVoted
from fudcon.modules.users.models import User
from fudcon.modules.users.forms import UserForm
from fudcon.modules.sessions.forms import AddBarcamp
from fudcon.app import app
# from fudcon.app import login_manager

bp = Blueprint('frontend', __name__,
               template_folder='templates')

items_per_page = app.config['ITEMS_PER_PAGE']
upload_folder = app.config['TALKS_FOLDER']


@bp.route('/', methods=['GET', 'POST'])
def index():
    queryset = Content.query.filter(Content.is_on_user_menu == 1,
                                    Content.tag == 'home',
                                    Content.active == 1).first()
    return render_template('frontend/index.html',
                           title="Home",
                           detail=queryset)


@bp.route('/venue', methods=['GET', 'POST'])
def venue():
    queryset = Content.query.filter(Content.is_on_user_menu == 1,
                                    Content.tag == 'venue',
                                    Content.active == 1).first()
    return render_template('frontend/index.html',
                           title='Venue',
                           detail=queryset)


@bp.route('/accomodation', methods=['GET', 'POST'])
def accomodation():
    queryset = Content.query.filter(Content.is_on_user_menu == 1,
                                    Content.tag == 'accomodation',
                                    Content.active == 1).first()
    return render_template('frontend/index.html',
                           title='Alojamiento',
                           detail=queryset)


@bp.route('/sponsors', methods=['GET', 'POST'])
def sponsors():
    queryset = Content.query.filter(Content.is_on_user_menu == 1,
                                    Content.tag == 'sponsors',
                                    Content.active == 1).first()
    return render_template('frontend/index.html',
                           title='Sponsors',
                           detail=queryset)


@bp.route('/speakers', methods=['GET', 'POST'])
@bp.route('/speakers/<int:page>', methods=['GET', 'POST'])
def speakers(page=1):
    paginate_params = (page, items_per_page, False)
    queryset = Speaker.query.paginate(*paginate_params)
    return render_template('frontend/speakers.html',
                           title=u'Ponentes',
                           speakers=queryset)


@bp.route('/sessions', methods=['GET', 'POST'])
@bp.route('/sessions/<int:page>', methods=['GET', 'POST'])
def sessions(page=1):
    """Ui for session.

    :page: parameter for pagination
    :returns: a template for session

    """
    # paginate_params = (page, items_per_page, False)
    # queryset = Session.query.paginate(*paginate_params)
    talks = Session.query.filter(Session.active == 1,
                                 Session.session_type == 1).all()
    barcamps = Session.query.filter(Session.active == 1,
                                    Session.session_type == 2).all()
    workshops = Session.query.filter(Session.active == 1,
                                     Session.session_type == 3).all()
    return render_template('frontend/sessions.html',
                           title=u'Sesiones',
                           talks=talks,
                           barcamps=barcamps,
                           workshops=workshops)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    print g.user
    return render_template('frontend/login.html')


@login_required
@bp.route('/done', methods=['GET', 'POST'])
def done():
    queryset = User.query.filter(User.username == g.user.username).first()
    form = UserForm(obj=queryset)
    # action = url_for('frontend.done')
    if form.validate_on_submit():
        form.populate_obj(queryset)
        db.session.commit()
        flash('Registro actualizado')
        return redirect(url_for('frontend.done'))

    return render_template('frontend/done.html',
                           title=u'Actualizado con éxito',
                           form=form)


@login_required
@bp.route('/votation-talks', methods=['GET', 'POST'])
def votation_talks():
    user_vote = g.user.username
    session_type = 1
    queryset = Session.query.filter(Session.active == 1,
                                    Session.session_type == 1).all()
    has_voted = SessionVoted.query.filter(SessionVoted.voter ==
                                          user_vote).count()
    if request.method == 'POST':
        for item in queryset:
            session_id = 'session_id_{}'.format(item.id)
            value = 'vote_{}'.format(item.id)
            args_id = request.form.get(session_id)
            args_value = request.form.get(value)
            votes = SessionVoted(session_type=session_type,
                                 session_id=args_id,
                                 voter=user_vote,
                                 value=args_value)
            db.session.add(votes)
        db.session.commit()
        flash(u'Ud ha votado con éxito')
        return redirect(url_for('frontend.done'))

    return render_template('frontend/votation_talks.html',
                           title=u'Elige tus charlas favoritas',
                           votes=queryset,
                           user_vote=user_vote,
                           session_type=session_type,
                           has_voted=has_voted)


@login_required
@bp.route('/votation-barcamps', methods=['GET', 'POST'])
def votation_barcamps():
    if datetime.datetime.utcnow() >= app.config['OPEN_WORKSHOP_AND_BARCAMPS']:
        opened = True
    else:
        opened = False

    user_vote = g.user.username
    session_type = 2
    queryset = Session.query.\
        filter(Session.active == 1,
               Session.session_type ==
               session_type).all()
    has_voted = SessionVoted.query.\
        filter(SessionVoted.voter == user_vote,
               or_(SessionVoted.session_type == 2,
                   SessionVoted.session_type == 3)).count()
    form = AddBarcamp()
    choices_sessions = [(c.id, c.name) for c in queryset]
    form.session_id.choices = choices_sessions
    action = url_for('frontend.votation_barcamps')
    if request.method == 'POST':
        barcamp = SessionVoted(session_type=session_type,
                               session_id=form.session_id.data,
                               voter=user_vote,
                               value=1)
        db.session.add(barcamp)
        db.session.commit()
        flash(u'Ud ha asegurado su asistencia \
              a la mesa de trabajo seleccionada')
        return redirect(url_for('frontend.done'))
    return render_template('frontend/votation_barcamps.html',
                           form=form,
                           title="Elige tu mesa de trabajo",
                           action=action,
                           has_voted=has_voted,
                           opened=opened)


@login_required
@bp.route('/votation-workshops', methods=['GET', 'POST'])
def votation_workshops():
    if datetime.datetime.utcnow() >= app.config['OPEN_WORKSHOP_AND_BARCAMPS']:
        opened = True
    else:
        opened = False

    user_vote = g.user.username
    session_type = 3
    queryset = Session.query.\
        filter(Session.active == 1,
               Session.session_type ==
               session_type).all()
    has_voted = SessionVoted.query.\
        filter(SessionVoted.voter == user_vote,
               or_(SessionVoted.session_type == 2,
                   SessionVoted.session_type == 3)).count()
    form = AddBarcamp()
    choices_sessions = [(c.id, c.name) for c in queryset]
    form.session_id.choices = choices_sessions
    action = url_for('frontend.votation_workshops')
    if request.method == 'POST':
        workshop = SessionVoted(session_type=session_type,
                                session_id=form.session_id.data,
                                voter=user_vote,
                                value=1)
        db.session.add(workshop)
        db.session.commit()
        flash(u'Ud ha asegurado su asistencia \
              al taller seleccionado')
        return redirect(url_for('frontend.done'))
    return render_template('frontend/votation_workshops.html',
                           form=form,
                           title="Elige tu taller",
                           action=action,
                           has_voted=has_voted,
                           opened=opened)


def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try:
        lst = os.listdir(path)
    except OSError:
        pass  # ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree


@bp.route('/download_slides')
def dirtree():
    path = os.path.expanduser(upload_folder)
    return render_template('frontend/dirtree.html',
                           tree=make_tree(path),
                           path_file=path)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect('/')
