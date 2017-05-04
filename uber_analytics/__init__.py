from uber.common import *
from uber_analytics._version import __version__

from uber_analytics import api

config = parse_config(__file__)
mount_site_sections(config['module_root'])
static_overrides(join(config['module_root'], 'static'))
template_overrides(join(config['module_root'], 'templates'))

c.MENU['Statistics'].append_menu_item(
    MenuItem(name='Graphs', href='../graphs/')
)
