#!/usr/bin/env python
'''
Created on Dec 30, 2012

@author: Michal Klis
'''
from google.appengine.ext import db

class User(db.Model):
    name = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    email = db.StringProperty()