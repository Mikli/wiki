#!/usr/bin/env python
'''
Created on Dec 27, 2012

@author: Michal Klis
'''
from user_model import User
from page_model import WikiPage
from google.appengine.api import memcache
import logging
from datetime import datetime
from compiler.ast import List

class ATableConnection(object):
    db_model_class = None

    def __init__(self):
        raise NotImplementedError

    def add_entry(self, **table_fields):
        b = self.db_model_class(**table_fields)
        b.put()
        return b.key().id_or_name()

    def get_all(self):
        return self.db_model_class.gql("")

    def get_all_sorted_by(self, key, direction = "desc"):
        logging.error("DB QUERY!")
        return self.db_model_class.gql("order by " + key + " " + direction)

    def delete_all(self):
        all_entries = self.get_all()
        for entry in all_entries:
            entry.delete()

    def get_entry_by_id(self, entry_id):
        return self.db_model_class.get_by_id(entry_id)

    def flush(self):
        cl = memcache.Client()
        cl.flush_all()
        logging.error("flushing")

class WikiPageConnection(ATableConnection):
    def __init__(self):
        self.db_model_class = WikiPage

#    def get_all_sorted_by(self, key, direction="desc", force_cache_reload = False):
#        k = self._make_key("Blog")#, key, direction)
#        cl = memcache.Client()
#        res = cl.get(k)
#        if (not res) or force_cache_reload or res["key"] != key or res["direction"] != direction:
#            res = {}
#            res["update_time"] =  datetime.now()
#            res["Blog"] = [entry for entry in ATableConnection.get_all_sorted_by(self, key, direction=direction)]
#            res["key"] = key
#            res["direction"] = direction
#            cl.set(k, res)
#
#        query_time = datetime.now() - res["update_time"]
#        return res["Blog"], query_time

#    def get_entry_by_id(self, entry_id):
#        k = self._make_key("Blog", entry_id)
#        cl = memcache.Client()
#        res = cl.get(k)
#        if not res:
#            res = {}
#            res["update_time"] = datetime.now()
#            res["Blog"] = ATableConnection.get_entry_by_id(self, entry_id)
#            cl.set(k, res)
#        query_time = datetime.now() - res["update_time"]
#        return res["Blog"], query_time

    def add_entry(self, **table_fields):
        pages = self.get_all_versions_of_page_by_name(table_fields["page_name"])
        #pn = pages.count()
        #logging.info("page entries %s" + str(pn))
        latest_version = 0
        latest_page = pages.get()
        if (latest_page):
            logging.info("the version is" + str(latest_page.version))
            latest_version = latest_page.version
        table_fields["version"] = latest_version + 1;
        entry_id = ATableConnection.add_entry(self, **table_fields)
        #self._cache_reload(self._make_key("Blog"))
        return entry_id

    def get_page_content_by_name(self, page_name):
        # TODO: memcache it!
        logging.info("get_page_content_by_name")
        page = self.get_page_by_name(page_name)
        if page:
            return page.content

    def get_page_content_by_name_and_version(self, page_name, version):
        logging.info("get_page_content_by_name_and_version, page_name %s, version %s", page_name, version)
        page = self.db_model_class.gql("where page_name=:1 and version=:2", page_name, long(version)).get()
        if page:
            return page.content

    def get_all_versions_of_page_by_name(self, page_name):
        pages = self.db_model_class.gql("where page_name=:1 order by version desc", page_name)
        for page in pages:
            logging.info(page)
        return pages

    def get_page_by_name(self, page_name):
        logging.info("getting page by name:%s"%page_name)
        return self.get_all_versions_of_page_by_name(page_name).get()

    def _cache_reload(self, key):
        if key == self._make_key("Blog"):
            cl = memcache.Client()
            res = cl.get(key)
            if res:
                self.get_all_sorted_by(res["key"], res["direction"], force_cache_reload = True)

    def _make_key(self, *args):
        key = ""
        for arg in args:
            key += repr(arg)
            logging.error(key)
        return key

class UserConnection(ATableConnection):
    def __init__(self):
        self.db_model_class = User

    def get_user_by_username(self, username):
        return self.db_model_class.gql("where name=:1", username).get()
