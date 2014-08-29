# -*- coding: utf-8 -*-
import urlparse
from flask import Flask, request, g, redirect, url_for, flash
from flask.ext.fas_openid import FAS
from fudcon.database import db
from fudcon.ui.frontend.utils import avatar_url
from functools import wraps
# Instantiate application.
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Instantiate database object
db.init_app(app)

# Set up FAS
FAS = FAS(app)


def is_safe_url(target):
    ref_url = urlparse.urlparse(request.host_url)
    test_url = urlparse.urlparse(
        urlparse.urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def authenticated():
    return hasattr(g, 'fas_user') and g.fas_user


def is_admin(app):
    if not authenticated() \
            or not g.fas_user.cla_done \
            or len(g.fas_user.groups) < 1:
        return False

    admins = app.config['ADMIN_GROUP']

    if isinstance(admins, basestring):
        admins = set([admins])
    else:
        admins = set(admins)
    groups = set(g.fas_user.groups)
    return not groups.isdisjoint(admins)


# Inject variable to the all templates
@app.context_processor
def inject_variables():
    """ This context processor will pass
    variables in a dict to the all templates
    of the application
    :var str title: Title of the application
    :return: A dict with the title of the application
    """
    title = app.config['FUDCON_NAME']
    user_admin = is_admin(app)
    return dict(title_site=title,
                is_admin=user_admin)


def is_fudcon_admin(function):
    """ Decorator used to check if the loged in user
     is a fudcon admin or not.
    """
    @wraps(function)
    def decorated_function(*args, **kwargs):
        """ Do the actual work of the decorator. """
        if not authenticated():
            return redirect(url_for('auth.auth_login',
                                    next=request.url))
        elif not g.fas_user.cla_done:
            flash('You must sign the CLA (Contributor License '
                  'Agreement to use pkgdb', 'errors')
            return redirect(url_for('frontend.index'))
        elif not is_admin(app):
            flash('You are not an administrator of fudcon', 'errors')
            redirect(url_for('frontend.foo'))
        else:
            return function(*args, **kwargs)
    return decorated_function


@app.template_filter('avatar')
def avatar(fas, size=64):
    output = '<img class="avatar circle" src="%s"/>' % (
        avatar_url(fas, size)
    )
    return output

from fudcon.ui.frontend.views import bp as frontend_bp
from fudcon.ui.backend.views import bp as backend_bp
from fudcon.modules.auth.views import bp as auth_bp


# Register blueprints.
app.register_blueprint(frontend_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(backend_bp)
