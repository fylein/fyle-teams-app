from typing import Dict

from botbuilder.core import TurnContext, CardFactory
from botbuilder.schema import Activity

from django.http import JsonResponse

from fyle_teams_app.libs import fyle_utils, logger
from fyle_teams_app.models import User, UserSubscription
from fyle_teams_app.ui.cards import authorisation as authorisation_card


logger = logger.get_logger(__name__)


class CommandHandler:

    command_handlers: Dict = {}

    def initialize_command_handlers(self):
        self.command_handlers = {
            'UNLINK_FYLE_ACCOUNT': self.handle_unlink_fyle_account,
            'LINK_FYLE_ACCOUNT': self.handle_link_fyle_account,
            'HI': self.handle_welcome_command,
            'HELLO': self.handle_welcome_command,
            'HELP': self.handle_help_command
        }


    async def handle_commands(self, turn_context: TurnContext) -> JsonResponse:

        # Initialising command handlers
        self.initialize_command_handlers()

        logger.info('Received message: %s', turn_context)

        command = turn_context.activity.text

        # Converting message command to a consistent format
        # Ex: 'Fyle Unlink Account' -> 'FYLE_UNLINK_ACCOUNT'
        command = command.strip().upper().replace(' ', '_')

        logger.info('Command received: %s', command)

        command_handler = self.command_handlers.get(command)

        turn_context_dict = turn_context.activity.as_dict()

        user_id = turn_context_dict['from_property']['id']
        team_id = turn_context_dict['channel_data']['tenant']['id']

        if command_handler is not None:
            return await command_handler(turn_context, user_id, team_id)
        else:
            message = 'Hey we couldn\'t understand that message  🤕, try `Hi`, `Hello` or `Help` to get started ⚡'
            return await turn_context.send_activity(message)


    async def handle_unlink_fyle_account(self, turn_context: TurnContext, user_id: str, team_id: str) -> JsonResponse:

        user = await User.get_by_id(user_id)

        fyle_user_id = user.fyle_user_id

        if fyle_user_id is None:
            message = 'You have not linked your Fyle account 🤕 '
        else:
            user_details_to_track = {
                'user_id': user_id,
                'team_id': team_id,
                'fyle_user_id': fyle_user_id,
                'email': user.email
            }

            processing_message = 'We are unlinking your Fyle account with Microsft Teams, we will send a message once it is done'
            await turn_context.send_activity(processing_message)

            await UserSubscription.disable_notification_subscriptions(user)
            await UserSubscription.remove_user_subscriptions(user_id)
            await User.clear_user_details(user_id)

            message = 'You have successfully unlinked your Fyle account  🎊'

        await turn_context.send_activity(message)

        User.track_fyle_account_unlinked(user_details_to_track)

        return JsonResponse({})


    async def handle_link_fyle_account(self, turn_context: TurnContext, user_id: str, team_id: str) -> JsonResponse:
        user = await User.get_by_id(user_id)

        if user.fyle_user_id is not None:
            message = 'You have already linked your Fyle account 🎊'
        else:
            FYLE_OAUTH_URL = fyle_utils.get_fyle_oauth_url(user_id, team_id)
            pre_auth_card = authorisation_card.get_pre_auth_card(FYLE_OAUTH_URL)

            message = Activity(
                attachments=[CardFactory.adaptive_card(pre_auth_card)]
            )
        await turn_context.send_activity(
            message
        )
        return JsonResponse({})


    async def handle_welcome_command(self, turn_context: TurnContext, user_id: str, team_id: str) -> JsonResponse:
        user = await User.get_by_id(user_id)

        if user.fyle_user_id is None:
            message = 'Hey there, seems like you have not linked your Fyle account 🤕, we\'ll send you a message with which you can link your Fyle account 🎊'
            await turn_context.send_activity(message)

            FYLE_OAUTH_URL = fyle_utils.get_fyle_oauth_url(user_id, team_id)
            pre_auth_card = authorisation_card.get_pre_auth_card(FYLE_OAUTH_URL)
            message_activity = Activity(
                attachments=[CardFactory.adaptive_card(pre_auth_card)]
            )
        else:
            post_auth_card = authorisation_card.get_post_auth_card()
            message_activity = Activity(
                attachments=[CardFactory.adaptive_card(post_auth_card)]
            )

        await turn_context.send_activity(
            message_activity
        )
        return JsonResponse({})


    async def handle_help_command(self, turn_context: TurnContext, user_id: str, team_id: str) -> JsonResponse:
        user = await User.get_by_id(user_id)

        if user.fyle_user_id is None:
            message = 'Hey there, seems like you have not linked your Fyle account 🤕, we\'ll send you a message with which you can link your Fyle account 🎊'
            await turn_context.send_activity(message)

            FYLE_OAUTH_URL = fyle_utils.get_fyle_oauth_url(user_id, team_id)
            pre_auth_card = authorisation_card.get_pre_auth_card(FYLE_OAUTH_URL)
            message_activity = Activity(
                attachments=[CardFactory.adaptive_card(pre_auth_card)]
            )
            await turn_context.send_activity(message_activity)
        else:
            message = 'To unlink your Fyle account, type `Unlink Fyle Account`'
            await turn_context.send_activity(message)
            message = 'Sit back and relax, You\'ll be notified whenever any action happens on your expense reports ⚡'
            await turn_context.send_activity(message)

        return JsonResponse({})
