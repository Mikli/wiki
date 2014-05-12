import jinja2
import webapp2
import os
from urls import url_list

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True,
                               extensions=['jinja2.ext.autoescape'])

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        kw.update(url_list)
        #kw.update(self._get_user())
        self.response.write(render_str(template, **kw))
        pass

    def get_user(self):
        user_id = self.request.cookies.get('user_id')
        if user_id:
            from table_connection import UserConnection
            u = UserConnection().get_entry_by_id(int(user_id.split('|')[0]))
            if u and user_id.split('|')[1] == u.password.split('|')[0]:
                return u

    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def setCookie(self, cookie_name, cookie_value, path = "/"):
        cookie_params = {'cookie_name':cookie_name,
                         'cookie_value':cookie_value,
                         'path':path}
        self.response.headers.add_header("Set-Cookie",
                                         "%(cookie_name)s=%(cookie_value)s;  Path=%(path)s"
                                         % cookie_params)

    def delete_Cookie(self, cookie_name):
        self.setCookie(cookie_name, '')
