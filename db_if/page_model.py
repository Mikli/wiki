#!/usr/bin/env python
'''
Created on 11-05-2014

@author: Michal Klis
'''
from google.appengine.ext import db

class WikiPage(db.Model):
    page_name = db.StringProperty(required = True)
    content = db.TextProperty()
    version = db.IntegerProperty(required = True)
    creation_time = db.DateTimeProperty(auto_now_add = True)