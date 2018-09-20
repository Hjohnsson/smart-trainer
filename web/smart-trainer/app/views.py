# views.py

import sys
sys.path.append('/home/pi/smart-trainer/raspberry/')
import times2
import trainer2
import subprocess
import os
import threading

from flask import render_template, request, flash, json
from flask_table import Table, Col
from app import app
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from contextlib import closing

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'pi'
app.config['MYSQL_DATABASE_PASSWORD'] = 'herman93'
app.config['MYSQL_DATABASE_DB'] = 'SmartTrainer'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/', methods=['GET','POST'])
def index():
    #print(request.method)
    #print (times2.print_total_time())
    
    if request.method == 'POST':
        status = request.form['knappen']

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
            total_time = times2.print_total_time()
            split_time = times2.print_split_times()
            return render_template("index.html", time=total_time, split=split_time)
    
    #total_time = times2.print_total_time()
    #split_time = times2.print_split_times()
    #return render_template("index.html", time=total_time, split=split_time)
    return render_template("index.html")


@app.route('/test', methods=['GET','POST'])
def test():
    #print(request.method)
    #print (times2.print_total_time())
    
    if request.method == 'POST':
        nodes = int(request.form['nodes'])
        rounds = int(request.form['rounds'])

        if nodes > 0 and rounds >0:
            t1 = threading.Thread(target=trainer2.main)
            t1.daemon = True
            t1.start()
            t1.join()

            total_time = times2.print_total_time()
            split_time = times2.print_split_times()
            return render_template("test.html", total_time = total_time, split=split_time)


    return render_template("test.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/times')
def times(time="0", split = []):
    total_time = times2.print_total_time()
    split_time = times2.print_split_times()
    return render_template("times.html", time=total_time, split=split_time)

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showHome')
def showHome():
    return render_template('index.html')


@app.route('/signUp',methods=['POST','GET'])
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
                        return json.dumps({'message':'User created successfully !'})
                    else:
                        return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})


