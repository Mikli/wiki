#!/usr/bin/env python
'''
Created on 11-05-2014

@author: Michal Klis
'''

from baseh import BaseHandler
from uservalidation import UserValidation
from user_model import User
from password_hash import PasswordHash
from table_connection import UserConnection
from urls import url_list
import logging

PREVIOUS_PAGE_COOKIE = "Previous_page"

class SignupHandler(BaseHandler):
    def get(self):

        referer = str(self.request.referer)
        logging.info(referer)
        if referer:
            self.setCookie(PREVIOUS_PAGE_COOKIE, referer)

        self.render("signup.html")

    def post(self):
        error = False
        template_params = {}
        template_params['username'] = self.request.get('username')
        template_params['pass'] = self.request.get('password')
        template_params['verify'] = self.request.get('verify')
        template_params['email'] = self.request.get('email')

        usr = UserValidation(False, False)
        usr.createUser(name = template_params['username'],
                            password = template_params['pass'],
                             password2 = template_params['verify'],
                              email = template_params['email'] )

        if not usr.validate_email():
            template_params['email_error'] = "That's not a valid email."
            error = True


        (matching, valid) = usr.validate_password()
        if not valid:
            template_params['password_error'] = "That wasn't a valid password."
            error = True
        elif not matching:
            template_params['verify_error'] = "Your passwords didn't match."
            error = True

        if not usr.validate_user_name():
            template_params['username_error'] = "That's not a valid username."
            error = True

        if not error:
            template_params['pass'] = self.hashPassword(**template_params)
            user_id = self.registerUser(**template_params)
            if user_id:
                user_id_str = str(user_id) + '|' + template_params['pass'].split('|')[0]
                self.setCookie("user_id", user_id_str)
                referer = "/"
                prev_r = str(self.request.cookies.get(PREVIOUS_PAGE_COOKIE))

                if(prev_r):
                    logging.info(prev_r)
                    referer = prev_r
                    self.delete_Cookie(PREVIOUS_PAGE_COOKIE)
                self.redirect(referer)

            else:
                template_params['username_error'] = "Username already registered."
                error = True

        if error:
            self.render("signup.html", **template_params)

    def hashPassword(self, **userparams):
        return PasswordHash().hash_password(userparams.get('username') +
                                            userparams.get('pass'))

    def registerUser(self, **userparams):
        uc = UserConnection()
        if uc.get_user_by_username(userparams.get('username')):
            return None
        else:
            return uc.add_entry(name = userparams.get('username'),
                                password = userparams.get('pass'),
                                email = userparams.get('email'))

