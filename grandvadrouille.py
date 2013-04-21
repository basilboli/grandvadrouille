# -*- coding: utf-8 -*-
"""
    Grandvadrouille
    ~~~~~~

    A cleaning management example application written using Flask and mongodb

    :copyright: (c) 2013 by basilboli
"""
from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
from flask.ext.pymongo import PyMongo
import datetime

# configuration
DATABASE = 'grandvadrouille'
DEBUG = True
USERNAME = 'admin'
PASSWORD = 'admin'

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/test')
def test():
    """ printing all items"""
    users = mongo.db.users.find()
    for user in users:
        print user['name']
    print 'mongo : ', users
    return render_template('index.html')

@app.route('/')
def home():
    users = mongo.db.users.find()
    return render_template('index.html',users=users)

@app.route('/add',methods=['POST'])
def addnewcleaning():

    team = request.form.getlist('team')
    print 'team : ', team

    count = len(team)
    if (count!=0):
        contribution  = 2.0 / count
        print 'team count',count
        print 'contribution : ',contribution

        #updating scores
        for user_name in team:
            user = mongo.db.users.find_one({'name':user_name})
            new_score = user['score'] + contribution
            mongo.db.users.update({'name':user['name']},{'$set':{"score":new_score}})
            print 'adding controbution {0} to user {1}: '.format(contribution,user['name'])

        #updating history
        now = datetime.datetime.now()
        new_history_item = dict (date=now,team=','.join(team))
        mongo.db.history.insert(new_history_item)
        print 'addnewcleaning {0}+{1}'.format(now,team)


    return redirect("/")


@app.route('/viz')
def viz():
    users = mongo.db.users.find()
    return render_template('dataviz.html',users=users)


@app.route('/history')
def history():
    history_items = mongo.db.history.find()
    return render_template('history.html',history_items=history_items)

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)
