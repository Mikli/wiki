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
            db_content = WikiPageConnection().get_page_content_by_name(page_name)
            if db_content:
                content = db_content
            self.render("edit.html", content = content, user = user)
        else:
            self.redirect(url_list.get("login"))

    def post(self, page_name):
        content = self.request.get("content")

        if content:
            db_conn = WikiPageConnection()
            db_conn.add_entry(page_name = page_name, content = content)

        self.redirect(page_name)