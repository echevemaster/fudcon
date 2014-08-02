# -*- coding: utf-8 -*-
from flask import request, Blueprint, redirect
from flask import url_for, g, current_app
from fudcon.app import is_safe_url, FAS

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def auth_login():
    """ Login mechanism for this application
    """
    next_url = url_for('frontend.index')
    if 'next' in request.values:
        if is_safe_url(request.values['next']):
            next_url = request.values['next']

    if next_url == url_for('frontend.index'):
        next_url = url_for('frontend.index')

    if hasattr(g, 'fas_user') and g.fas_user is not None:
        return redirect(next_url)
    else:
        return FAS.login(return_url=next_url)


@bp.route('/logout', methods=['GET', 'POST'])
def auth_logout():
    if g.fas_user:
        FAS.logout()
    return redirect(url_for('frontend.index'))
