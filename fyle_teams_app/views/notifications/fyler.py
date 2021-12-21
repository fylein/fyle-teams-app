from typing import Dict

from botbuilder.schema import ConversationReference
from botbuilder.core import CardFactory

from django.http import JsonResponse

from fyle_teams_app.models import User
from fyle_teams_app.views.notifications.base import FyleNotificationView, NotificationType
from fyle_teams_app.libs import team_utils
from fyle_teams_app.ui.cards import notifications as notification_cards


class FyleFylerNotification(FyleNotificationView):

    def initialize_notification_handlers(self) -> None:
        self.notification_handlers = {
            NotificationType.REPORT_PARTIALLY_APPROVED.value: self.handle_report_partially_approved,
            NotificationType.REPORT_PAYMENT_PROCESSING.value: self.handle_report_payment_processing,
            NotificationType.REPORT_APPROVER_SENDBACK.value: self.handle_report_approver_sendback,
            NotificationType.REPORT_COMMENTED.value: self.handle_report_commented,
            NotificationType.EXPENSE_COMMENTED.value: self.handle_expense_commented,
            NotificationType.REPORT_PAID.value: self.handle_report_paid
        }


    async def handle_report_partially_approved(self, webhook_data: Dict, user: User, user_conversation_reference: ConversationReference) -> JsonResponse:

        report = webhook_data['data']

        report_approved_card = notification_cards.get_report_approved_card(report)

        await team_utils.send_message_to_user(
            conversation_reference=user_conversation_reference,
            attachments=[CardFactory.adaptive_card(report_approved_card)]
        )

        return JsonResponse({}, status=200)


    async def handle_report_payment_processing(self, webhook_data: Dict, user: User, user_conversation_reference: ConversationReference) -> JsonResponse:

        report = webhook_data['data']

        report_payment_processing_card = notification_cards.get_report_payment_processing_card(report)

        await team_utils.send_message_to_user(
            conversation_reference=user_conversation_reference,
            attachments=[CardFactory.adaptive_card(report_payment_processing_card)]
        )

        return JsonResponse({}, status=200)


    async def handle_report_approver_sendback(self, webhook_data: Dict, user: User, user_conversation_reference: ConversationReference) -> JsonResponse:

        report = webhook_data['data']

        report_sendback_reason = webhook_data['reason']

        report_sendback_card = notification_cards.get_report_send_back_card(report, report_sendback_reason)

        await team_utils.send_message_to_user(
            conversation_reference=user_conversation_reference,
            attachments=[CardFactory.adaptive_card(report_sendback_card)]
        )

        return JsonResponse({}, status=200)


    async def handle_report_commented(self, webhook_data: Dict, user: User, user_conversation_reference: ConversationReference) -> JsonResponse:

        report = webhook_data['data']

        # Send comment notification only if the commenter is not SYSTEM and not the user itself
        if report['updated_by_user']['id'] not in ['SYSTEM', report['user']['id']]:

            report_comment = webhook_data['reason']

            report_commented_card = notification_cards.get_report_commented_card(report, report_comment)

            await team_utils.send_message_to_user(
                conversation_reference=user_conversation_reference,
                attachments=[CardFactory.adaptive_card(report_commented_card)]
            )

        return JsonResponse({}, status=200)


    async def handle_expense_commented(self, webhook_data: Dict, user: User, user_conversation_reference: ConversationReference) -> JsonResponse:

        expense = webhook_data['data']

        # Send comment notification only if the commenter is not SYSTEM and not the user itself
        if expense['updated_by_user']['id'] not in ['SYSTEM', expense['employee']['user']['id']]:

            expense_comment = webhook_data['reason']

            expense_commented_card = notification_cards.get_expense_commented_card(expense, expense_comment)

            await team_utils.send_message_to_user(
                conversation_reference=user_conversation_reference,
                attachments=[CardFactory.adaptive_card(expense_commented_card)]
            )

        return JsonResponse({}, status=200)


    async def handle_report_paid(self, webhook_data: Dict, user: User, user_conversation_reference: ConversationReference) -> JsonResponse:

        report = webhook_data['data']

        report_paid_card = notification_cards.get_report_paid_card(report)

        await team_utils.send_message_to_user(
            conversation_reference=user_conversation_reference,
            attachments=[CardFactory.adaptive_card(report_paid_card)]
        )

        return JsonResponse({}, status=200)
