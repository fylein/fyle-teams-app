from typing import Dict

from fyle.platform import exceptions as platform_exceptions

from botbuilder.core import TurnContext, CardFactory, MessageFactory
from botbuilder.schema import AdaptiveCardInvokeValue

from django.http.response import JsonResponse

from fyle_teams_app.models import User
from fyle_teams_app.libs import logger, fyle_utils, assertions
from fyle_teams_app.ui.cards import notifications as notification_cards
from fyle_teams_app.libs.tracking import Tracking



logger = logger.get_logger(__name__)


class ActionHandler:

    action_handlers: Dict = {}

    def initialize_action_handlers(self):
        self.action_handlers = {
            'approve_report': self.handle_approve_report
        }


    async def handle_actions(self, turn_context: TurnContext, action_details: AdaptiveCardInvokeValue) -> JsonResponse:

        # Initialising action handlers
        self.initialize_action_handlers()

        action_details = action_details.as_dict()
        action = action_details['action']['data']['action']

        action_handler = self.action_handlers.get(action)

        if action_handler is None:
            logger.error('Invalid action -> %s', action)
        else:
            return await action_handler(turn_context, action_details)

        return JsonResponse({})


    async def handle_approve_report(self, turn_context: TurnContext, action_details: Dict):

        report_id = action_details['action']['data']['id']
        team_user_id = turn_context.activity.from_property.id

        user = await User.get_by_id(team_user_id)
        assertions.assert_found(user, 'user not found')

        platform = await fyle_utils.get_fyle_sdk_connection(user.fyle_refresh_token)

        try:
            report = platform.v1beta.approver.reports.get_by_id(report_id)
            report = report['data']
        except platform_exceptions.NotFoundItemError as e:
            logger.error('Report not found with id -> %s', report_id)
            logger.error('Error -> %s', e)
            # None here means report is deleted/doesn't exist
            report = None
            report_message = 'Looks like you no longer have access to this expense report  🤕 '

        if report is not None:
            can_approve_report, report_message = fyle_utils.can_approve_report(report, user.fyle_user_id)

            if can_approve_report is True:
                try:
                    report = platform.v1beta.approver.reports.approve(report_id)
                    report = report['data']
                    report_message = '**Expense Report Approved** 🚀 '

                    # Track report approved
                    self.track_report_approved(user, report)

                except platform_exceptions.PlatformError as e:
                    logger.error('Error while processing report approve -> %s', e)

                    report_message = 'Seems like an error occured while approving this report 🤕  \n' \
                        'Please try approving again or `Review in Fyle` to approve directly from Fyle ⚡'

            report_card = notification_cards.get_report_approval_card(report, report_message, can_approve_report=False)

            update_activity = MessageFactory.attachment(CardFactory.adaptive_card(report_card))
            update_activity.id = turn_context.activity.reply_to_id

        else:
            update_activity = MessageFactory.text(report_message)
            update_activity.id = turn_context.activity.reply_to_id

        return await turn_context.update_activity(update_activity)


    def track_report_approved(self, user: User, report: Dict):
        event_data = {
            'team_user_id': user.team_user_id,
            'fyle_user_id': user.fyle_user_id,
            'email': user.email,
            'team_id': user.team_id,
            'report_id': report['id'],
            'org_id': report['org_id']
        }

        tracking = Tracking(user.email)
        tracking.track_event(user.email, 'Report Approved From Teams', event_data)
