# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, url_for, redirect, flash
from flask.ext.login import login_required, logout_user
from fudcon.database import db
from fudcon.modules.contents.models import Content
from fudcon.modules.speakers.models import Speaker
from fudcon.modules.sessions.models import Session
from fudcon.modules.users.models import User
from fudcon.modules.users.forms import UserForm
from fudcon.app import app
# from fudcon.app import login_manager

bp = Blueprint('frontend', __name__,
               template_folder='templates')

items_per_page = app.config['ITEMS_PER_PAGE']


# app.context_processor(backends)
                            

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
                           ##aion=action,
                           form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect('/')

