# Critter Card
# Doggy Docs

# Importing the core building blocks from the Flask library that we'll need to create pages,
# show HTML, handle forms, and redirect users
# Flask: class for creating the application instance
# render_template: Generates HTML pages. Takes in the name of an HTML file from template and
# combines it w python variables (like name or icon) and produces a final HTML page based on those
# two.
# request: Object that holds all the info about an incoming request. (i.e. User clicks save on pet
# name)
# redirect: Sends users to a diff URL. Used for redirecting users to the new homepage w their
# pets name shown.
# url_for: Builds URLs for you (i.e. you can type your url like url_for('pet profile', pet_id = 1)).
# This ensures that you dont have any broken links anywhere.
from flask import Flask, render_template, request, redirect, url_for
# SQLAlchemy: Designed for database interactions on flask
# This will use a database connection object that will be a point of contact for all operations
# (i.e. defining models, adding data, and saving data).
# Model: blueprint for the database
from flask_sqlalchemy import SQLAlchemy
# Provies tools to interact w the operating system. Specifically, for determining the location
# of app.py for the database. 
import os

app = Flask(__name__)

# This initializes basedir to the absolute path of the directory in which our running Python file is
# which in this case is app.py. This ensures the data is saved properly from this file.
basedir = os.path.abspath(os.path.dirname(__file__))
# Tells Flask exactly where to find the database and what kind of database it is.
# app.config: Adjusting the settings for app
# ['SQLALCHEMY_DATABASE_URI"]: The specific setting being changed. SQLAlchemy is programmed to look
# for this exact key to know where the database is. URI (Uniform Resource Identifier).
# 'sqlite:///': The type of database. SQLite stores everything in a single file. /// means its on
# your local computer.
# os.path.join(basedir, 'data.sqlite'): This part builds the rest of the address. Takes the basedir
# from earlire w/ the desired file name of data.sqlite. This makes a reliable path to the database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# Another setting, specifically for turning off the ability to see old modifications since it takes
# up extra memory.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Officially creating the database connection object
# SQLAlchemy(app): Creates the main SQLAlchemy service object, passing in app to hand over all the
# config details (database address stuff).
# db saves it as this variable name. Now we can edit this variable to adjust the database itself.
db = SQLAlchemy(app)

# DB Model
# User Blueprint, constructs the user table in the database. It's going to store information about
# each person who signs up.
# Declares a new Python class that inherits db.Model, which tells SQLAlchemy that this is a db model
# and should be turned into a table.
class User(db.Model):
    # id defines this specific column.
    # db.Column: Creating a column in the table
    # db.Integer: The data in this column is gonna be an int
    # primary_key=True: Designates that this column is the key, meaning that every user will get a
    # unique number that automatically increments. It also determines that the user will be defined
    # by this int (their user id for our website)
    # *Must be unique, cannot be empty, is autoincrementing
    id = db.Column(db.Integer, primary_key=True)

    # Defines the auth0_sub column. This will store the unique ID that Auth0 provides.
    # db.String(200): The max string length will be 200 chars.
    # unique=True: No two users can have the same Auth0 ID.
    # nullable=False: This field cannot be empty, every user must have a Auth0 ID.
    # Auth0 is going to give us this ID
    auth0_sub = db.Column(db.String(200), unique=True, nullable=False)

    # The reason we use both id & auth0_sub is that Auth0 will give us a user's ID, given that, we
    # can look for that auth0 ID in the table, which will be paired to a user ID, this tells us that
    # this signed in person is attached to this account. Primary key will also focus on using that
    # to identify things like pets, settings, etc. for a specific account.

    # db.relationship('Pet',...):
    # Rather than creating a column, this links our user to the pet, allowing you to use a command
    # like my_user.pets to get a list of all pets owned by that specific user.
    # backref='owner': This is a shortcut that adds the owner property to the Pet model, meaning that
    # you can reversely find the user's name using my_pet.owner.
    # lazy=True: Only loads the user's pets when requested to do so.
    pets = db.relationship('Pet', backref='owner', lazy=True)

# Declares model for pets. New pet table in database
class Pet(db.Model):
    # Just like users, creates an auto-incrementing ID number for every pet
    id = db.Column(db.Integer, primary_key=True)
    # Defines the name of the pet, which can be up to 80 chars long
    name = db.Column(db.String(80), nullable=False)
    # Defines the filename of the pet's icon
    # default='dog_icon.png': If there isn't an icon yet, it'll automatically be given a default
    # icon image.
    icon_url = db.Column(db.String(200), nullable=False, default='dog_icon.png')

    # db.ForeignKey: This is the key that links the tables. The number in this column MUST
    # match a number that exists in the id column of the user table.
    # nullable=False: Every pet must have an owner
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# This line is called a decorated. The @ symbol means that its a special instruction that modifies
# the function below it.
# app.cli: Flask's built-in Command Line Interface tools
# .command('init-db'): Tells Flask to create a new terminal command and name it init-db.
#* You can run this by typing flask init_db after this.
@app.cli.command('init-db')
# Container for the code that will be run when we call flask init_db
def init_db_command():
    # Creates the database tables
    # Tells SQLAlchemy to look at all the classes in your code that inherit db.Model (atm this is
    # User and Pet)
    # It connects the database file to our configuration, data.sqlite (line 36)
    # Creates the tables of user and pet inside that database file, complete w/ every column we
    # defined before.
    db.create_all()
    # Simple user feedback to know the tables are created within the terminal so that we know it
    # was done correctly.
    print('Initialized the dataase.')

# The homepage of the website "website.com/"
@app.route("/")
def home():
    return 

@app.route("/pet/<int:pet_id>") # Change pet_id later
def pet(pet_id):


# This conditional is only true if you run Python on your on computer
if __name__ == "__main__":
    app.run(debug=True)