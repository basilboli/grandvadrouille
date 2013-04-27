grandvadrouille
===============

# What is it ?
Super simple and intuitive service to manage and visualize roommates contribution to cleaning.

**Choose*** a team, **confirm*** and **see*** actual cleaning contribution by roommate.

# What is it not ?
cleaning planning using calendars.

# How to deploy?
You should have mongodb installed. See also requirements.txt for more details.

    
0. Go to mongodb shell and add as many users as you want by executing the following command.
    
    db.users.insert({"name":"ROOMATE_NAME","score":0})
for ex. 
    db.users.insert({"name":"John","score":0})
    db.users.insert({"name":"Samantha","score":0})
    db.users.insert({"name":"Bob","score":0})        

property score is actual roommate total contribution and is used for ranking roommates.

1. Launch service using built-in server: 
    python grandvadrouille.py

2. Go to [http://127.0.0.1:500](http://127.0.0.1:500) and enjoy!

You can also deploy using smth. like gunicorn etc. To be covered later.    


