from typing import Dict

from botbuilder.schema import ConversationReference
from botbuilder.core import CardFactory

from django.http import JsonResponse

from fyle_teams_app.models import User
from fyle_teams_app.views.notifications.base import FyleNotificationView, NotificationType
from fyle_teams_app.libs import team_utils
from fyle_teams_app.libs.fyle_utils import ReportState, FyleResourceType
from fyle_teams_app.ui.cards import notifications as notification_cards


class FyleApproverNotification(FyleNotificationView):

    def initialize_notification_handlers(self) -> None:
        self.notification_handlers = {
            NotificationType.REPORT_SUBMITTED.value: self.handle_report_submitted
        }


    async def handle_report_submitted(self, webhook_data: Dict, user: User, user_conversation_reference: ConversationReference) -> JsonResponse:

        report = webhook_data['data']

        if report['state'] == ReportState.APPROVER_PENDING.value:

            report_approval_card = notification_cards.get_report_approval_card(report)

            await team_utils.send_message_to_user(
                conversation_reference=user_conversation_reference,
                attachments=[CardFactory.adaptive_card(report_approval_card)]
            )

            self.track_notification('Report Approval Notification Received', user, FyleResourceType.REPORT, report)

        return JsonResponse({}, status=200)
