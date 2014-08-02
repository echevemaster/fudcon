# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, url_for

bp = Blueprint('frontend', __name__,
               template_folder='templates')


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('frontend/index.html',
                           title="Home")
