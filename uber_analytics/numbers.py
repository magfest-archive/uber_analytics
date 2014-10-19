from uber.common import *

@all_renderable(STATS)
class Root:
    def index(self, session):
        return {
            'count': session.query(Attendee).count()
        }

Uber.numbers = Root()
