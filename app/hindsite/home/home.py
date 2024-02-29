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

    # return authorized(facilitator_route(selected), participant_route(selected))
    return authorized(participant_route(selected), facilitator_route(selected))

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
    boards = None
    # TODO: Get the boards for the group
    if 'groupid' in session and session['groupid'] is not None:
        # a group is selected, so we can populate the boards
        boards = get_boards(session.get('groupid'))
        if boards is None:
            #create the board defaults
            #add the boards to the board selector
            pass
        else:
            #populate the board selector
            #select the most recent board
            pass
        #render the page

    if request.method == 'POST':
        try:
            session['groupname'] = request.args['groupname']
            session['groupid'] = request.args['group_id']
        except GroupAddError as ex:
            flash(ex.message)
        if 'groupname' in session:
            selected = session['groupname']
        return render_template('facilitator-home.html', title='Facilitator Home', \
                               groups=groups, selected=selected, board=board)
    return render_template('facilitator-home.html', title='Facilitator Home', \
                           groups=groups, selected=selected, board=board)


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
            groupname = request.form['groupname']
            group = create_group(groupname, current_user.id)
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

@home.route('/facilitator-display', methods=['GET', 'POST'])
@login_required
def facilitator_display():
    """
        Route to retrieve the cards using HTMx polling
    """
    groupid = ''
    board = None
    if session.get('groupid') is not None:
        groupid = session.get('groupid')
        boards = get_boards(groupid, False)
        board = boards[0]
    return render_template('partials/facilitator-blob.html', title='Home', board=board)
