import jinja2
import webapp2
import os

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.write(render_str(template, **kw))
        pass

    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def setCookie(self, cookie_name, cookie_value, path = "/"):
        cookie_params = {'cookie_name':cookie_name,
                         'cookie_value':cookie_value,
                         'path':path}
        self.response.headers.add_header("Set-Cookie",
                                         "%(cookie_name)s=%(cookie_value)s;  Path=%(path)s"
                                         % cookie_params)

