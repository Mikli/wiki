#!/usr/bin/env python
'''
Created on 11-05-2014

@author: Michal Klis
'''
from baseh import BaseHandler
from urls import url_list
import logging

class PageHandler(BaseHandler):
    def get(self, page_name):
        edit_url = url_list.get("edit") + page_name
        history_url = url_list.get("history") + page_name

        requested_version = self.request.get("version")
        logging.info("requested version %s"%requested_version)
        if requested_version:
            content = self._get_page_content_for_version(page_name, requested_version)
            logging.info(content)
            edit_url = edit_url + "?version=" + requested_version
        else:
            content = self._get_page_content(page_name)

        # TODO: shall redirect to edit only if logged in, otherwise just show
        # empty page with login/signup links
        if content:
            self.render("page.html",
                         content = content,
                         edit_link = edit_url,
                         history_link = history_url,
                         user = self.get_user())
        else:
            self.redirect(edit_url)


