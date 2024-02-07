"""
Test
"""
import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Included to load .env environment variables for local dev
load_dotenv()

# Location agnostic URI that loads either the .env file, or if
# it's not included loads the variables set by the OS. In the
# case of Railway.app, the variables set by the database and
# linked to the app.
database_uri = ("mysql+pymysql://"
                + os.environ['MYSQLUSER'] + ":"
                + os.environ['MYSQL_ROOT_PASSWORD'] + "@"
                + os.environ['MYSQLHOST'] + ":"
                + os.environ['MYSQLPORT'] + "/"
                + os.environ['MYSQL_DATABASE'])

# Needed to redirect default paths to maintain the proposed folder structure
# since Flask looks for static and templates in the root folder of the app
template_dir = os.path.abspath('src/app/templates')
static_dir = os.path.abspath('src/app/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Sets the database URI to match whatever environment it's in
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

db = SQLAlchemy(app)


class Users(db.Model):
    """
    Sets up the database model
    """
    __tablename__ = 'users'
    id = db.Column('user_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    def __init__(self, name):
        self.name = name


@app.route('/')
def index():
    """
    Loads index.html, sets the title and users
    """
    title = 'Deployment Test'
    return render_template('index.html', title=title, users=Users.query.all())


with app.app_context():
    db.drop_all()
    db.create_all()
    ollanius = Users('Ollanius Pius')
    fabius = Users('Fabius Bile')
    db.session.add(ollanius)
    db.session.add(fabius)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default="80"))
