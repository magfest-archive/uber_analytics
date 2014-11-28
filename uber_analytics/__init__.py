from uber.common import *
from uber_analytics._version import __version__
from uber_analytics import graphs

config = parse_config(__file__)
django.conf.settings.TEMPLATE_DIRS.insert(0, join(config['module_root'], 'templates'))

# this class exists solely to have a mount point for the /static config section below
#
# TODO: maybe there's a better way to do this? I don't want to attach the analytics_app_config
# to the graphs.Root() because it will create a new directory level which will mess with
# relative paths included in base.html -Dom
# idea: look at app.merge() or cherrypy.config.update()
class AnalyticsStatic:
    def index(self, session):
        return None

analytics_app_config = {
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(config['module_root'], 'static')
    }
}

cherrypy.tree.mount(AnalyticsStatic(), PATH + '/analytics', analytics_app_config)