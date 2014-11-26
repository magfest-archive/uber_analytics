from uber.common import *
from uber_analytics._version import __version__
from uber_analytics import graphs

config = parse_config(__file__)
django.conf.settings.TEMPLATE_DIRS.insert(0, join(config['module_root'], 'templates'))

analytics_app_config = {
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(config['module_root'], 'static')
    }
}

cherrypy.tree.mount(Root(), PATH + '/analytics', analytics_app_config)