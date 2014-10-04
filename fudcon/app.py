# -*- coding: utf-8 -*-
import urlparse
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, g, redirect, url_for, flash
from flask.ext.fas_openid import FAS
from flask.ext import login
from fudcon.database import db
from fudcon.ui.frontend.utils import avatar_url
from functools import wraps
from fudcon.modules.users.models import User
from social.apps.flask_app.routes import social_auth
from social.apps.flask_app.template_filters import backends
from social.apps.flask_app.default.models import init_social

# Instantiate application.
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Instantiate database object
db.init_app(app)

init_social(app, db)


# Set up FAS
FAS = FAS(app)

login_manager = login.LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = ''
login_manager.init_app(app)

app.context_processor(backends)

# Set OpenID

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except (TypeError, ValueError):
        pass

@app.before_request
def global_user():
    g.user = login.current_user

@app.teardown_appcontext
def commit_on_success(error=None):
    if error is None:
        db.session.commit()

@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

@app.context_processor
def inject_user():
    try:
        return {'user': g._user}
    except AttributeError:
        return {'user': None}


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


def create_logger():
    if not app.debug:
        formatter = logging.Formatter(
            "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        handler = RotatingFileHandler('fudconlatam.log', maxBytes=10000000, backupCount=5)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

from fudcon.ui.frontend.views import bp as frontend_bp
from fudcon.ui.backend.views import bp as backend_bp
from fudcon.modules.auth.views import bp as auth_bp


# Register blueprints.
app.register_blueprint(frontend_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(backend_bp)
app.register_blueprint(social_auth)
