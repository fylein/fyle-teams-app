from typing import Dict

from botbuilder.core import TurnContext

from django.http import JsonResponse

from fyle_teams_app.models import User, UserSubscription


class CommandHandler:

    command_handlers: Dict = {}

    def initialize_command_handlers(self):
        self.command_handlers = {
            'FYLE_UNLINK_ACCOUNT': self.handle_fyle_unlink_account
        }


    async def handle_commands(self, turn_context: TurnContext) -> JsonResponse:

        # Initialising command handlers
        self.initialize_command_handlers()

        command = turn_context.activity.text

        # Converting message command to a consistent format
        # Ex: 'Fyle Unlink Account' -> 'FYLE_UNLINK_ACCOUNT'
        command = command.strip().upper().replace(' ', '_')

        command_handler = self.command_handlers.get(command)

        if command_handler is not None:
            return await command_handler(turn_context)

        return JsonResponse({})


    async def handle_fyle_unlink_account(self, turn_context: TurnContext) -> JsonResponse:

        turn_context_dict = turn_context.activity.as_dict()

        user_id = turn_context_dict['from_property']['id']

        user = await User.get_by_id(user_id)

        if user.fyle_user_id is None:

            message = 'You have not linked your Fyle account 🤕 '

        else:
            await UserSubscription.disable_notification_subscriptions(user)

            await UserSubscription.remove_user_subscriptions(user_id)

            await User.clear_user_details(user_id)

            message = 'You have successfully unlinked your Fyle account  🎊'

        await turn_context.send_activity(message)

        return JsonResponse({})
