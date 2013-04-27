# -*- coding: utf-8 -*-
"""
    Grandvadrouille
    ~~~~~~

    A cleaning management example application written using Flask and mongodb

    :copyright: (c) 2013 by basilboli
"""
from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,session
from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId
import datetime

# configuration
DATABASE = 'grandvadrouille'
DEBUG = True
USERNAME = 'admin'
PASSWORD = 'admin'

app = Flask(__name__)
app.secret_key = 'ababagalamaga'
mongo = PyMongo(app)

@app.route('/test')
def test():
    """ printing all items"""
    users = mongo.db.users.find()
    for user in users:
        print user['name']
    print 'mongo : ', users
    return render_template('poc.html')

@app.route('/')
def home():
    print 'Current session : ', session
    users = mongo.db.users.find()
    return render_template('index.html',users=users)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        del session['user_id']
    return redirect("/")

@app.route('/auth',methods=['POST'])
def auth():
    email = request.form["email"]
    password = request.form['password']
    if password == 'ababagalamaga':
        session['user_id'] = email
        users = mongo.db.users.find()
        return render_template('index.html',users=users)
    else:
        return redirect('/login')



@app.route('/add',methods=['POST'])
def addnewcleaning():

    team = request.form.getlist('team')
    print 'team : ', team

    count = len(team)
    if (count!=0):
        #adding new item
        now = datetime.datetime.now()
        new_history_item = dict (date=now,team=team,status='pending')
        mongo.db.history.insert(new_history_item)
        print 'add new cleaning {0}+{1}'.format(now,team)

    return redirect("/viz")


@app.route('/viz')
def viz():
    users = mongo.db.users.find()
    return render_template('dataviz.html',users=users)


@app.route('/history')
def history():
    history_items = mongo.db.history.find({'status':'confirmed'})#requesting only confirmed items
    return render_template('history.html',history_items=history_items)

@app.route('/pending')
def pending():
    """ view cleanings in pending status"""
    print 'session : ', session
    if session['admin']==True:
        pending_items = mongo.db.history.find({'status':'pending'})#requesting only pending items
        return render_template('pending.html',history_items=pending_items)
    else:
        abort(404)


@app.route('/confirm',methods=['POST'])
def confirm():
    """confirm cleaning"""
    id  = request.form ['id']
    if id is None:
        abort(404)

    cleaning = mongo.db.history.find_one({'_id': ObjectId(id)})

    count = len(cleaning['team'])
    contribution  = 2.0 / count
    print 'team count',count
    print 'contribution : ',contribution

    #updating users scores
    for user_name in cleaning['team']:
        user = mongo.db.users.find_one({'name':user_name})
        new_score = user['score'] + contribution
        mongo.db.users.update({'name':user['name']},{'$set':{"score":new_score}})
        print 'adding contribution {0} to user {1}: '.format(contribution,user['name'])

    #pending status -> confirmed
    cleaning = mongo.db.history.update({'_id': ObjectId(id)},{'$set':{"status":'confirmed'}})
    return redirect('/pending')


if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)
