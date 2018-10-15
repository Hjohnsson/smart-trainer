# views.py

import sys
import time
sys.path.append('/home/pi/smart-trainer/raspberry/')
import times2
import trainer2
import settings2
import subprocess
import os
import threading
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from flask_sqlalchemy  import SQLAlchemy
from flask import session, Flask, url_for, redirect, render_template, request, flash, json
import flask
from flask_table import Table, Col
from app import app
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from contextlib import closing

# mysql = MySQL()

# # MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'pi'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'herman93'
# app.config['MYSQL_DATABASE_DB'] = 'SmartTrainer'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    roles = db.Column(db.String())
    phone = db.Column(db.String(15))
    ip_address = db.Column(db.String(25))
    user_id = db.Column(db.String(25))

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
            login_user(user)
            session['logged_in'] = True
            #flask.flash('Logged in successfully.')
        
            next = flask.request.args.get('next')

            return flask.redirect(next or flask.url_for('home'))
   

    return flask.render_template('login.html', form=form)


@app.route('/home', methods=['GET','POST'])
@login_required
def home():
    if current_user.is_authenticated:
    #print(request.method)
    #print (times2.print_total_time())

        nodes = settings2.get_values_int("nodes")
        rounds = settings2.get_values_int("rounds")
        delay = settings2.get_values_int("delay")
    
        if request.method == 'POST':
            status = request.form['start_button']

            if status == 'Clear':
                print ("Clearing")
                total_time = ""
                split_time = []
                return render_template("index.html", time=total_time, split=split_time)

            if status == 'Start':

                t1 = threading.Thread(target=trainer2.main)
                t1.daemon = True
                t1.start()
                t1.join()

                total_time = times2.print_total_time()
                split_time = times2.print_split_times()
                return render_template("index.html", total_time=total_time, split=split_time, nodes=nodes, rounds=rounds, delay=delay)
    
    #total_time = times2.print_total_time()
    #split_time = times2.print_split_times()
    #return render_template("index.html", time=total_time, split=split_time)
        nodes = settings2.get_values_int("nodes")
        rounds = settings2.get_values_int("rounds")
        delay = settings2.get_values_int("delay")
        return render_template("index.html",nodes=nodes, rounds=rounds, delay=delay)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/settings', methods=['GET','POST'])
@login_required
def settings():
    if current_user.is_authenticated:
        nodes = settings2.get_values_int("nodes")
        rounds = settings2.get_values_int("rounds")
        delay = settings2.get_values_int("delay")
        distance = settings2.get_values_int("distance")

        if request.method == 'POST':
            rounds_input = request.form['rounds']
            nodes_input = request.form['nodes']
            delay_input = request.form['delay']
            distance_input = request.form['distance']

            # Update sql database
            settings2.update_values("nodes",int(nodes_input))
            settings2.update_values("rounds",int(rounds_input))
            settings2.update_values("delay",int(delay_input))
            #settings2.update_values("distance",int(distance_input))

            # Read new values from sql database
            nodes = settings2.get_values_int("nodes")
            rounds = settings2.get_values_int("rounds")
            delay = settings2.get_values_int("delay")
            distance = settings2.get_values_int("distance")

        return render_template("settings.html", nodes=nodes, rounds=rounds, delay=delay, distance=distance)
    return render_template("index.html")

@app.route('/highscore')
@login_required
def highscore():
    return render_template("highscore.html")

@app.route('/sign-up',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call the MySQL

            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    _hashed_password = generate_password_hash(_password)
                    cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
                    data = cursor.fetchall()

                    if len(data) is 0:
                        conn.commit()
                        return json.dumps({'message':'User created successfully!'})
                    else:
                        return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})


