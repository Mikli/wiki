#!/usr/bin/env python
'''
Created on Jan 6, 2013

@author: Michal Klis
'''
from baseh import BaseHandler
import urls

class LogoutHandler(BaseHandler):
    def get(self):
        self.response.headers.add_header("Set-Cookie",
                                         "user_id=;  Path=/")
        #self.write(self.request.referer)
        self.redirect(self.request.referer)