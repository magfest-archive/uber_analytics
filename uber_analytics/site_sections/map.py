from uber.common import *
from collections import Counter
from uszipcode import ZipcodeSearchEngine

@all_renderable(c.STATS)
class Root:
    zips_counter = Counter()
    zips = {}
    center = ZipcodeSearchEngine().by_zipcode("20745")

    def index(self):
        return {
            'zip_counts': self.zips_counter,
            'center': self.center,
            'zips': self.zips
        }

    def refresh(self, session):
        zips = {}
        self.zips_counter = Counter()
        attendees = session.query(Attendee).all()
        for person in attendees:
            if person.zip_code:
                self.zips_counter[person.zip_code] += 1

        for z in self.zips_counter.keys():
            found = ZipcodeSearchEngine().by_zipcode(z)
            if found.Zipcode:
                zips[z] = found

        self.zips = zips
        raise HTTPRedirect("index")