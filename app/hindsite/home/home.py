"""
Template route testing for development
"""
import datetime
import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from app.hindsite.home.home_model import accept_invitation, create_group, \
    GroupAddError, get_invitation, get_invitations
from app.hindsite.common_model import add_card, add_field, create_board, get_boards, get_groups, authorized, get_most_recent_board, get_user, set_start_date_for_board

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
        Checks the authorization state and returns the correct
        function depending on what the facilitator session variable
        value is.
    """
    if 'groupname' not in session or session['groupname'] is None:
        #Ensures session contains groupname and sets a default value
        session['groupname'] = "Select a Group"
    selected = session['groupname']

    #TODO: The first version below is the correct route. Uncomment it to enable 
    # proper routing.
    #
    # The second version below is to test/develop facilitator_route()

    return authorized(facilitator_route(selected), participant_route(selected))
    # return authorized(participant_route(selected), facilitator_route(selected)) #TODO: Testing Facilitator mode

def participant_route(selected: str):
    """
        Loads home.html, sets the title and loads in the group
        selection dropdown. Periodically checks for invites sent
        from other users to their groups and loads them.
    """
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

def facilitator_route(selected: str):
    """
        Route for Facilitator mode
    """
    groups = get_groups(current_user.id)
    board = None
    if 'groupid' in session and session['groupid'] is not None:
            board = create_board(session['groupid'])
            field = add_field(board, "Test Field")
            add_card(field, get_user(current_user.id), "Test Card")
            add_card(field, get_user(current_user.id), "Test Card2")
            add_card(field, get_user(current_user.id), "Test Card3")
            add_card(field, get_user(current_user.id), "Test Card4")
            add_card(field, get_user(current_user.id), "Test Card5")
            add_card(field, get_user(current_user.id), "Test Card6")

    if request.method == 'POST':
        try:
            session['groupname'] = request.args['groupname']
            session['groupid'] = request.args['group_id']
        except GroupAddError as ex:
            flash(ex.message)
        if 'groupname' in session:
            selected = session['groupname']
        return render_template('partials/facilitator-blob.html', title='Home', \
                               groups=groups, selected=selected, boards=board)
    return render_template('facilitator-home.html', title='Home', groups=groups, selected=selected, boards=board)

@home.route('/invites', methods=['POST', 'GET'])
@login_required
def invites():
    """
        Loads all the invite codes to be accepted or rejected
    TODO: Put the invite codes into a modal, add decline button, create
    notification bell to open the modal.
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
            #TODO: Create a default board
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
