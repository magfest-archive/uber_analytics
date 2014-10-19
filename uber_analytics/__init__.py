from uber.common import *
from uber_analytics._version import __version__
from uber_analytics import numbers, graphing

config = parse_config(__file__)
django.conf.settings.TEMPLATE_DIRS.insert(0, join(config['module_root'], 'templates'))
