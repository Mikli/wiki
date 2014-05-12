import fix_path
import webapp2
import login, logout, signup, page, edit
from urls import url_list

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, this is final!')


PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

url_map = [
    (url_list.get("index") , MainPage),
    (url_list.get("signup"), signup.SignupHandler),
    (url_list.get("login"), login.LoginHandler),
    (url_list.get("logout"), logout.LogoutHandler),
    (url_list.get("edit")  + PAGE_RE, edit.EditHandler),
    (url_list.get("page")  + PAGE_RE, page.PageHandler),
]

app = webapp2.WSGIApplication(url_map, debug=True)

