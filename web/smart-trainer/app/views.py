# views.py

import sys
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
from flask import session, Flask, url_for, redirect, render_template, request, flash, Markup
import flask
from flask_table import Table, Col
#from app import app
#from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from contextlib import closing
#import thread
import time
#import jsonify

node_1 = None
node_2 = None
node_3 = None
node_4 = None  
node_5 = None
# mysql = MySQL()
app = Flask(__name__)
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
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password')

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

def node_func():
    starttime=time.time()
    x = 0
    while x < 1:
        x += 1
        global node_1
        with open('TEST', 'r') as f:
            reader = f.read()
            #print repr(reader)
            if reader == "1\n":    
                node_1 = True
            if reader == "2\n":
                node_1 = False
        global node_2
        node_2 = True
        global node_3
        node_3 = True
        global node_4  
        node_4 = False
        global node_5  
        node_5 = False
        
        
        time.sleep(5.0 - ((time.time() - starttime) % 5.0))


@app.route('/home', methods=['GET','POST'])
@login_required
def home():
    form = LoginForm()
    if current_user.is_authenticated:   
        start = False
        start_2 = False
        player = None
        nodes = None
        rounds = None
        distance = None
        delay = None
        node_1 = True
        node_2 = True
        node_3 = True
        node_4 = True
        node_5 = True
        labels = []	
        labels_2 = settings2.get_times()
        labels_2 = labels_2[1]
        for i in range(0,labels_2):
            labels.append(i)
        values_2 = settings2.get_times()
        values_2 = values_2[3:]
        values = []
        for i in values_2:
            if i != "":
                values.append(i) 
        nodes_list = []
        nodes = settings2.get_values_int("nodes")
        rounds = settings2.get_values_int("rounds")
        delay = settings2.get_values_int("delay")
        distance = settings2.get_values_int("distance")
        if request.method == 'POST':
            player = request.form['player']
            nodes = request.form['nodes']
            rounds = request.form['duration']
            delay = request.form['time_sleep']
            distance = request.form['sensitivity']

            settings2.update_values("nodes",int(nodes))
            settings2.update_values("rounds",int(rounds))
            settings2.update_values("delay",int(delay)) 
            settings2.update_values("distance",int(distance)) 

            labels = []	
            labels_2 = settings2.get_times()
            labels_2 = labels_2[1]
            for i in range(1,labels_2+1):
            #for i in range(0,labels_2):
                labels.append(i)
            values_2 = settings2.get_times()
            values_2 = values_2[3:]
            values = []
            for i in values_2:
                if i != "":
                    values.append(i) 
            ish = "hejsan" 
            for x in range(1, int(nodes) + 1):
                nodes_list.append(x)
            
            if player != "":
                flash("Start")
                start = True
                trainer2.read_settings()
                t1 = threading.Thread(target=trainer2.main)
                t1.daemon = True
                t1.start()
                t1.join()
            else:
                start_2 = True
                flash("Incomplete form")

        split_time = times2.print_split_times()
        settings2.update_times(split_time)
        nodes = settings2.get_values_int("nodes")
        rounds = settings2.get_values_int("rounds")
        delay = settings2.get_values_int("delay")
        distance = settings2.get_values_int("distance")
	
            #return flask.render_template('makkan.html', form=form,start_2=start_2, start=start, nodes_list=nodes_list, player=player, nodes=nodes, time_sleep=delay, duration=rounds, sensitivity=distance\
                #, node_1=node_1, node_2=node_2, node_3=node_3, node_4=node_4, node_5=node_5)
        
        return flask.render_template('makkan.html',values=values, labels=labels, form=form,start_2=start_2, start=start, nodes_list=nodes_list, player=player, nodes=nodes, delay=delay, rounds=rounds, distance=distance\
            , node_1=node_1, node_2=node_2, node_3=node_3, node_4=node_4, node_5=node_5)
#     #print(request.method)
#     #print (times2.print_total_time())
    
#         # if request.method == 'POST':
#         #     status = request.form['start_button']

#         #     if status == 'Clear':
#         #         print ("Clearing")
#         #         total_time = ""
#         #         split_time = []
#         #         return render_template("index.html", time=total_time, split=split_time)

#         #     if status == 'Start':

#         #         t1 = threading.Thread(target=trainer2.main)
#         #         t1.daemon = True
#         #         t1.start()
#         #         t1.join()

#         #         total_time = times2.print_total_time()
#         #         split_time = times2.print_split_times()
#         return render_template("index.html")#, total_time=total_time, split=split_time)
    
#     #total_time = times2.print_total_time()
#     #split_time = times2.print_split_times()
#     #return render_template("index.html", time=total_time, split=split_time)
#         #return render_template("index.html")

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

# @app.route('/test', methods=['GET','POST'])
# def test():
#     #print(request.method)
#     #print (times2.print_total_time())
    
#     if request.method == 'POST':
#         nodes = int(request.form['nodes'])
#         rounds = int(request.form['rounds'])

#         if nodes > 0 and rounds >0:
#             t1 = threading.Thread(target=trainer2.main)
#             t1.daemon = True
#             t1.start()
#             t1.join()

#             total_time = times2.print_total_time()
#             split_time = times2.print_split_times()
#             return render_template("test.html", total_time = total_time, split=split_time)


#     return render_template("test.html")

# @app.route('/about')
# def about():
#     return render_template("about.html")

# @app.route('/settings')
# def settings():
#     return render_template("settings.html")

# @app.route('/highscore')
# def highscore():
#     return render_template("highscore.html")

# @app.route('/sign-up',methods=['POST','GET'])
# def signUp():
#     try:
#         _name = request.form['inputName']
#         _email = request.form['inputEmail']
#         _password = request.form['inputPassword']

#         # validate the received values
#         if _name and _email and _password:

#             # All Good, let's call the MySQL

#             with closing(mysql.connect()) as conn:
#                 with closing(conn.cursor()) as cursor:
#                     _hashed_password = generate_password_hash(_password)
#                     cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
#                     data = cursor.fetchall()

#                     if len(data) is 0:
#                         conn.commit()
#                         return json.dumps({'message':'User created successfully!'})
#                     else:
#                         return json.dumps({'error':str(data[0])})
#         else:
#             return json.dumps({'html':'<span>Enter the required fields</span>'})

#     except Exception as e:
#         return json.dumps({'error':str(e)})



if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='192.168.4.1')
