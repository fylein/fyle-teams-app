from typing import Dict
import analytics

from django.conf import settings

analytics.write_key = settings.FYLE_TEAMS_APP_SEGMENT_KEY


class Tracking:

    def __init__(self, user_email: str) -> None:
        analytics.identify(user_email, {})

    def track_event(self, user_email: str, event_name: str, event_data: Dict) -> bool:
        event_data['asset'] = 'TEAMS_APP'
        analytics.track(user_email, event_name, event_data)
