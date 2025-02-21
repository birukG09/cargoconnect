import os  # Importing the OS module to access environment variables
import logging  # Importing logging module for debugging
from flask import Flask, redirect, url_for  # Importing Flask and helper functions
from flask_sqlalchemy import SQLAlchemy  # Importing SQLAlchemy for database handling
from flask_login import LoginManager, current_user  # Importing Flask-Login for user authentication
from sqlalchemy.orm import DeclarativeBase  # Importing base class for SQLAlchemy ORM

# Setting up logging to show debug messages
logging.basicConfig(level=logging.DEBUG)

# Creating a base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initializing the database object with a custom base model
db = SQLAlchemy(model_class=Base)

# Creating the Flask application instance
app = Flask(__name__)

# Configuring the Flask app with secret key and database URL
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key")  # Getting secret key from environment variables
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")  # Getting database URL from environment
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {  # Setting database connection options
    "pool_recycle": 300,  # Recycle connections every 300 seconds
    "pool_pre_ping": True,  # Check if connection is alive before using it
}

# Initializing database with Flask app
db.init_app(app)

# Initializing Flask-Login manager
login_manager = LoginManager()
login_manager.init_app(app)  # Connecting login manager to Flask app
login_manager.login_view = 'auth.login'  # Setting default login route

# Function to load user from database using Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models import User  # Importing User model
    return User.query.get(int(user_id))  # Fetching user by ID from database

# Defining the root route of the application
@app.route('/')
def index():
    if current_user.is_authenticated:  # Checking if user is logged in
        return redirect(url_for('booking.dashboard'))  # Redirecting to dashboard if authenticated
    return redirect(url_for('auth.login'))  # Redirecting to login page if not authenticated

# Importing and registering blueprints (modularizing the app)
from routes.auth import auth_bp  # Import authentication routes
from routes.booking import booking_bp  # Import booking routes
from routes.admin import admin_bp  # Import admin routes
from routes.payment import payment_bp  # Import payment routes

# Registering blueprints with the Flask app
app.register_blueprint(auth_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(payment_bp)

# Creating database tables within the application context
with app.app_context():
    import models  # Import models to create tables
    db.create_all()  # Create all tables in the database if they don't exist
