from typing import Dict

from botbuilder.core import TurnContext

from django.http import JsonResponse


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
        return JsonResponse({})
