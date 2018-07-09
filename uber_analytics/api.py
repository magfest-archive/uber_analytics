from uber.common import *

from .site_sections.graphs import RegistrationDataOneYear

class AnalyticsApi:
    def badge_sale_history(self):
        with Session() as session:
            reg_data = RegistrationDataOneYear()
            reg_data.query_current_year(session)

            return {
                'current_registrations': reg_data.dump_data(),
            }

    def badge_stats(self):
        return {
            'badges_sold': c.BADGES_SOLD,
            'remaining_badges': c.REMAINING_BADGES,
            'badges_price': c.BADGE_PRICE,
            'server_current_timestamp': int(datetime.utcnow().timestamp()),
            'warn_if_server_browser_time_mismatch': c.WARN_IF_SERVER_BROWSER_TIME_MISMATCH
        }

services.register(AnalyticsApi(),'analytics')