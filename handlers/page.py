'''
Created on 11-05-2014

@author: Michal Klis
'''
from baseh import BaseHandler
from urls import url_list

class PageHandler(BaseHandler):
    def get(self, page_name):
        edit_url = url_list.get("edit") + page_name

        content = self._get_page_content(page_name)

        if content:
            self.render("page.html", content = content, edit_link = edit_url, user = self.get_user())
        else:
            self.redirect(edit_url)

    def _get_page_content(self, page_name):
        from table_connection import WikiPageConnection
        return WikiPageConnection().get_page_content_by_name(page_name)
