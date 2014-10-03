from uber.common import *

@all_renderable(STATS)
class Root:
    def index(self):
        return {
            'what': 'just a silly example without any database stuff'
        }

Uber.graphing = Root()
