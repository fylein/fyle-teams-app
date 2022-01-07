from typing import Dict

import json
import enum
import asyncio

from botbuilder.schema import ConversationReference

from django.views import View
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import classonlymethod

from fyle_teams_app.models import User, UserSubscription
from fyle_teams_app.libs import assertions, logger
from fyle_teams_app.libs.fyle_utils import FyleResourceType
from fyle_teams_app.libs.tracking import Tracking


logger = logger.get_logger(__name__)


# Defining notification types in <resource>_<resource_action> format
# Similar to payload received in webhook to keep it consistent
class NotificationType(enum.Enum):

    # Report notification types
    REPORT_SUBMITTED = 'REPORT_SUBMITTED'
    REPORT_COMMENTED = 'REPORT_COMMENTED'
    REPORT_APPROVED = 'REPORT_APPROVED'
    REPORT_PARTIALLY_APPROVED = 'REPORT_PARTIALLY_APPROVED'
    REPORT_APPROVER_SENDBACK = 'REPORT_APPROVER_SENDBACK'
    REPORT_PAYMENT_PROCESSING = 'REPORT_PAYMENT_PROCESSING'
    REPORT_PAID = 'REPORT_PAID'

    # Expense notification types
    EXPENSE_COMMENTED = 'EXPENSE_COMMENTED'


class FyleNotificationView(View):

    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        # pylint: disable=protected-access
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view


    notification_handlers: Dict = {}


    async def post(self, request: HttpRequest, webhook_id: str) -> JsonResponse:
        webhook_data = json.loads(request.body)

        resource = webhook_data['resource']
        action = webhook_data['action']

        # Constructing notification type in `<resource>_<action>` format
        # This is equivalent to the notification types defined
        notification_type = '{}_{}'.format(resource, action)

        logger.info('Notification type received -> %s',  notification_type)

        self.initialize_notification_handlers()

        notification_handler = self.notification_handlers.get(notification_type)

        if notification_handler is not None:

            user_subscription = await UserSubscription.get_by_webhook_id(webhook_id)
            assertions.assert_found(user_subscription, 'User subscription not found with webhook id: {}'.format(webhook_id))

            teams_user_id = user_subscription.team_user_id

            user = await User.get_by_id(teams_user_id)

            user_conversation_reference = ConversationReference().from_dict(user.team_user_conversation_reference)

            return await notification_handler(webhook_data, user, user_conversation_reference)

        return JsonResponse({}, status=200)


    @staticmethod
    def get_event_data(user: User) -> Dict:
        event_data = {
            'asset': 'TEAMS_APP',
            'team_user_id': user.team_user_id,
            'fyle_user_id': user.fyle_user_id,
            'email': user.email
        }
        return event_data


    @staticmethod
    def get_report_tracking_data(user: User, report: Dict) -> Dict:
        event_data = FyleNotificationView.get_event_data(user)

        event_data['report_id'] = report['id']
        event_data['org_id'] = report['org_id']

        return event_data


    @staticmethod
    def get_expense_tracking_data(user: User, expense: Dict) -> Dict:
        event_data = FyleNotificationView.get_event_data(user)

        event_data['expense_id'] = expense['id']
        event_data['org_id'] = expense['org_id']

        return event_data


    @staticmethod
    def track_notification(event_name: str, user: User, resource_type: str, resource: Dict) -> None:

        if resource_type == FyleResourceType.REPORT:
            event_data = FyleNotificationView.get_report_tracking_data(user, resource)
        elif resource_type == FyleResourceType.EXPENSE:
            event_data = FyleNotificationView.get_expense_tracking_data(user, resource)

        tracking = Tracking(user.email)

        tracking.track_event(user.email, event_name, event_data)