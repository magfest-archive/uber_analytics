from uber.common import *
from collections import Counter
from uszipcode import ZipcodeSearchEngine
from geopy.distance import VincentyDistance


@JinjaEnv.jinja_filter()
def get_count(counter, key):
    return counter.get(key)


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

    @ajax
    def refresh(self, session, **params):
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
        return True

    @csv_file
    def radial_zip_data(self, out, session, **params):
        if params.get('radius'):
            res = ZipcodeSearchEngine().by_coordinate(self.center["Latitude"], self.center["Longitude"], radius=int(params['radius']), returns=0)
            out.writerow(['# of Attendees', 'City', 'State', 'Zipcode', 'Miles from Event', '% of Total Attendees'])
            if len(res) > 0:
                keys = self.zips.keys()
                center_coord = (self.center["Latitude"], self.center["Longitude"])
                filter = Attendee.badge_status.in_([c.NEW_STATUS, c.COMPLETED_STATUS])
                attendees = session.query(Attendee).filter(filter)
                total_count = attendees.count()
                for x in res:
                    if x['Zipcode'] in keys:
                        out.writerow([self.zips_counter[x['Zipcode']], x['City'], x['State'], x['Zipcode'],
                                      VincentyDistance((x["Latitude"], x["Longitude"]), center_coord).miles,
                                      "%.2f" % float(self.zips_counter[x['Zipcode']]/total_count * 100)])

    @ajax
    def set_center(self, session, **params):
        if params.get("zip"):
            self.center = ZipcodeSearchEngine().by_zipcode(params["zip"])
            return "Set to %s, %s - %s" % (self.center["City"], self.center["State"], self.center["Zipcode"])
        return False
