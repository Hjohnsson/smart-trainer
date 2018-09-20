# app/__init__.py

from flask import Flask
from flaskext.mysql import MySQL
import os

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

app.secret_key = os.urandom(12)

# Load the views
from app import views

# Load the config file
app.config.from_object('config')
