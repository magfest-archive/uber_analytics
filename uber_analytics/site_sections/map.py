from uber.common import *
from collections import Counter
from uszipcode import ZipcodeSearchEngine
from django.template.defaulttags import register
from geopy.distance import vicenty


@register.filter
def get_count(counter, key):
    return counter.get(key)

@all_renderable(c.STATS)
class Root:
    zips_counter = Counter()
    zips = {}
    center = ZipcodeSearchEngine().by_zipcode("20745")

    def index(self):
        if len(self.zips) == 0:
            raise HTTPRedirect("refresh")
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

    @csv_file
    def radial_zip_data(self, out, session, **params):
        out.writerow(['# of Attendees', 'City', 'State', 'Zipcode', 'Miles from Event'])
        if params.get('radius'):
            res = ZipcodeSearchEngine().by_coordinate(self.center["Latitude"], self.center["Longitude"], radius=int(params['radius']), returns=0)
            if len(res) > 0:
                keys = self.zips.keys()
                center_coord = (self.center["Latitude"], self.center["Longitude"])
                for x in res:
                    if x['Zipcode'] in keys:
                        out.writerow([self.zips_counter[x['Zipcode']], x['City'], x['State'], x['Zipcode'], vincenty((x["Latitude"], x["Longitude"]), center_coord).miles])


