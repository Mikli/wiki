import fix_path
import webapp2
import login, logout
from urls import url_list

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')

url_map = [
    (url_list.get("index") , MainPage),
    (url_list.get("login"), login.LoginHandler),
    (url_list.get("logout"), logout.LogoutHandler)
]

app = webapp2.WSGIApplication(url_map, debug=True)

