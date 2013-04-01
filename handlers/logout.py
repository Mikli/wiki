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
        self.redirect(urls["goodbye"])