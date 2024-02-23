"""
Template route testing for development
"""
import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from app.hindsite.home.home_model import accept_invitation, create_group, \
    GroupAddError, get_invitation, get_invitations
from app.hindsite.common_model import get_groups

static_dir = os.path.abspath('static')
home = Blueprint('home',
                   __name__,
                   template_folder='templates',    # relative route to templates dir
                   static_folder=static_dir)

@home.route('/')
def index():
    """
        Just redirects to home at the root of the page.
    """
    return redirect(url_for('home.homepage'))

@home.route('/home', methods=['GET', 'POST'])
@login_required
def homepage():
    """
        Loads home.html, sets the title
    """
    if not 'groupname' in session or session['groupname'] is None:
        #Ensures session contains groupname and sets a default value
        session['groupname'] = "Select a Group"
    selected = session['groupname']

    groups = get_groups(current_user.id)
    if request.method == 'POST':
        try:
            session['groupname'] = request.args['groupname']
            session['groupid'] = request.args['group_id']
        except GroupAddError as ex:
            flash(ex.message)
        if 'groupname' in session:
            selected = session['groupname']
        return render_template('partials/dropdown.html', title='Home', \
                               groups=groups, selected=selected)
    return render_template('home.html', title='Home', groups=groups, selected=selected)

@home.route('/invites', methods=['POST', 'GET'])
@login_required
def invites():
    """
        Loads all the invite codes to be accepted or rejected
    """
    error = None
    if request.method == 'GET':
        invitations = get_invitations(current_user.id)
        return render_template('partials/invites.html', invitations=invitations)
    if request.method == 'POST':
        try:
            group = request.args['group']

            membership = get_invitation(group, current_user.id)
            accept_invitation(membership)
        except GroupAddError as e:
            error = e.message
            flash(error)
    return render_template('partials/accepted.html')

@home.route('/add-group', methods=['GET', 'POST'])
@login_required
def group_add():
    """
        The route for the add group dropdown item.
    """
    error = None
    if request.method == 'POST':
        try:
            create_group(request.form['groupname'], current_user.id)
        except GroupAddError as e:
            error = e.message
    if error is not None:
        flash(error)
    return redirect(url_for('home.homepage'))

@home.route('/modal')
@login_required
def modal():
    """
        Route to retrieve the modal using HTMx
    """
    groups = get_groups(current_user.id)
    return render_template('partials/modal.html', groups=groups)