from uber.common import *
from sqlalchemy.sql.expression import literal

class RegistrationDataOneYear:
    def __init__(self):
        self.event_name = ""

        # what is the final day of this event (i.e. Sunday of a Fri->Sun festival)
        self.end_date = ""

        # this holds how many registrations were taken each day starting at 365 days from the end date of the event.
        # this array is in chronological order and does not skip days.
        #
        # examples:
        # registrations_per_day[0]   is the #regs that were taken on end_date-365 (1 year before the event)
        # .....
        # registrations_per_day[362] is the #regs that were taken on end_date-2 (2 days before the end date)
        # registrations_per_day[363] is the #regs that were taken on end_date-1 (the day before the end date)
        # registrations_per_day[364] is the #regs that were taken on end_date
        self.registrations_per_day = []

        # same as above, but, contains a cumulative sum of the same data
        self.registrations_per_day_cumulative_sum = []

        self.num_days_to_report = 365

    def query_current_year(self, session):
        self.event_name = EVENT_NAME_AND_YEAR

        # TODO: we're hacking the timezone info out of ESCHATON (final day of event). probably not the right thing to do
        self.end_date = DATES['ESCHATON'].replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)

        # return registrations where people actually paid money
        # exclude: dealers
        reg_per_day = session\
            .query(
                func.date_trunc(literal('day'),Attendee.registered),
                func.count( func.date_trunc(literal('day'),Attendee.registered))
            )\
            .outerjoin(Attendee.group)\
            .filter(
                (
                    (Attendee.group_id != None) &
                    (Attendee.paid == PAID_BY_GROUP) &          # if they're paid by group
                    (Group.tables == 0) &                       # make sure they aren't dealers
                    (Group.amount_paid > 0)                     # make sure they've paid something
                ) | (                                           # OR
                    (Attendee.paid == HAS_PAID)                 # if they're an attendee, make sure they're fully paid
                )
            )\
            .group_by(
                func.date_trunc(literal('day'), Attendee.registered)
            )\
            .order_by(
                func.date_trunc(literal('day'),Attendee.registered),
            )\
            .all()

        # now, convert the query's data into the format we need.
        # SQL will skip days without registrations
        # we need all self.num_days_to_report days to have data, even if it's zero

        # create 365 elements in the final array
        self.registrations_per_day = self.num_days_to_report * [0]

        for reg_data in reg_per_day:
            day = reg_data[0]
            reg_count = reg_data[1]

            day_offset = self.num_days_to_report - (self.end_date - day).days
            day_index = day_offset - 1

            if day_index < 0 or day_index >= self.num_days_to_report:
                raise 'Analytics data processing: dates are invalid (not within range of 1 year before ESCHATON). check that your ESCHATON config setting matches the data in the database.'

            self.registrations_per_day[day_index] = reg_count

        self.compute_cumulative_sum_from_registrations_per_day()

    # compute cumulative sum up until the last non-zero data point
    def compute_cumulative_sum_from_registrations_per_day(self):

        if len(self.registrations_per_day) != self.num_days_to_report:
            raise 'array validation error: array size should be the same as the report size'

        # figure out where the last non-zero data point is in the array
        last_useful_data_index = self.num_days_to_report - 1
        for regs in reversed(self.registrations_per_day):
            if regs != 0:
                break # found it, so we're done.
            last_useful_data_index -= 1

        # compute the cumulative sum, leaving all numbers past the last data point at zero
        self.registrations_per_day_cumulative_sum = self.num_days_to_report * [0]
        total_so_far = 0
        current_index = 0
        for regs_this_day in self.registrations_per_day:
            total_so_far += regs_this_day
            self.registrations_per_day_cumulative_sum[current_index] = total_so_far
            if current_index == last_useful_data_index:
                break
            current_index += 1


    def dump_data(self):
        return [
            {"registrations_per_day": self.registrations_per_day},
            {"registrations_per_day_cumulative_sum": self.registrations_per_day_cumulative_sum},
            {"event_name": self.event_name},
            {"event_end_date": self.end_date.strftime("%d-%m-%Y")},
        ]

    def to_JSON(self):
        return json.dumps(self.dump_data(), indent=4)


@all_renderable(STATS)
class Root:
    def index(self, session):
        graph_data_current_year = RegistrationDataOneYear()
        graph_data_current_year.query_current_year(session)

        return {
            'current_registrations': graph_data_current_year.to_JSON(),
        }

Uber.graphs = Root()