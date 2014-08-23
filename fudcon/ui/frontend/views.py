# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, url_for
from fudcon.modules.contents.models import Content

bp = Blueprint('frontend', __name__,
               template_folder='templates')


@bp.route('/', methods=['GET', 'POST'])
def index():
    queryset = Content.query.filter(Content.is_on_user_menu == 1,
                                    Content.tag == 'home',
                                    Content.active == 1).first()  
    return render_template('frontend/index.html',
                           title="Home",
                           detail=queryset)
