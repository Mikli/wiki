#!/usr/bin/env python
'''
Created on Jan 3, 2013

@author: Michal Klis
'''
from baseh import BaseHandler
from password_hash import PasswordHash
from table_connection import UserConnection
from urls import url_list
import logging

PREVIOUS_PAGE_COOKIE = "Previous_page"

class LoginHandler(BaseHandler):

    def get(self):
        #logging.info(self.request.referer)
        referer = str(self.request.referer)

        self.setCookie(PREVIOUS_PAGE_COOKIE, referer)
        self.render("login.html")

    def post(self):
        error = False
        template_params = {}
        template_params['username'] = self.request.get('username')
        template_params['pass'] = self.request.get('password')

        if template_params['username'] and template_params['pass']:
            u = UserConnection().get_user_by_username(template_params['username'])
            if u and PasswordHash().validate_password(template_params['username'] +
                                                template_params['pass'],
                                                u.password):
                # make string like 84|938487394879fa3434
                user_id_str = str(u.key().id()) + '|' + str(u.password.split('|')[0])
                self.setCookie("user_id", user_id_str)
                referer = "/"
                prev_r = str(self.request.cookies.get(PREVIOUS_PAGE_COOKIE))
                #logging.info(prev_r)
                if(prev_r):
                    referer = prev_r
                    self.delete_Cookie(PREVIOUS_PAGE_COOKIE)
                self.redirect(referer)
            else:
                error = True
        else:
            error = True

        if error:
            self.render("login.html", error = "Wrong login or password!")

#        PasswordHash().validate_password(password, hash_with_salt)
