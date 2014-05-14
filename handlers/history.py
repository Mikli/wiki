#!/usr/bin/env python
'''
Created on 12-05-2014

@author: Michal Klis
'''
from baseh import BaseHandler
from table_connection import WikiPageConnection
from urls import url_list
import logging

class HistoryHandler(BaseHandler):
    def get(self, page_name):
        pages = WikiPageConnection().get_all_versions_of_page_by_name(page_name)

        edit_url = url_list.get("edit") + page_name
        view_url = page_name

        logging.info(view_url)
        self.render("history.html", content = pages,
                         edit_link = edit_url,
                         view_link = view_url,
                         user = self.get_user())