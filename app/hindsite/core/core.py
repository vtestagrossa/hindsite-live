"""
Template route testing for development
"""
import os
from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_required

import app.hindsite.auth.authenticate as auth

static_dir = os.path.abspath('static')
core = Blueprint('core',
                   __name__,
                   template_folder='templates',    # relative route to templates dir
                   static_folder=static_dir)

@core.route('/')
@login_required
def index():
    """
        Loads index.html, sets the title
    """
    title = 'Index'
    return render_template('index.html', title=title)


@core.route('/retrospective')
@login_required
def retrospective():
    """
        Loads retrospective.html, sets the title
    """
    title = 'Retrospective'
    return render_template('retrospective.html', title=title)


@core.route('/history')
@login_required
def history():
    """
        Loads history.html, sets the title
    """
    title = 'History'
    return render_template('history.html', title=title)


@core.route('/settings')
@login_required
def settings():
    """
        Loads settings.html, sets the title
    """
    title = 'Settings'
    return render_template('settings.html', title=title)
