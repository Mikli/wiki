#!/usr/bin/env python
'''
Created on 11-05-2014

@author: Michal Klis
'''
from baseh import BaseHandler
from table_connection import WikiPageConnection
from urls import url_list

class EditHandler(BaseHandler):
    def get(self, page_name):
        user = self.get_user()

        if user:
            content = ''

            requested_version = self.request.get("version")

            if requested_version:
                db_content = self._get_page_content_for_version(page_name, requested_version)
            else:
                db_content = self._get_page_content(page_name)

            if db_content:
                content = db_content
            self.render("edit.html", content = content, history_link = (url_list.get("history") + page_name), user = user)
        else:
            self.redirect(url_list.get("login"))

    def post(self, page_name):
        content = self.request.get("content")

        if content:
            db_conn = WikiPageConnection()
            db_conn.add_entry(page_name = page_name, content = content)

        self.redirect(page_name)