'''
Created on 11-05-2014

@author: Michal Klis
'''
from google.appengine.ext import db

class WikiPage(db.Model):
    page_name = db.StringProperty(required = True)
    content = db.TextProperty()
    history = db.StringProperty()