from botbuilder.core import TurnContext
from botbuilder.core.teams import TeamsActivityHandler

from fyle_teams_app.libs import logger

from fyle_teams_app.views.authorisation.team import TeamAuthorisation
from fyle_teams_app.views.handlers.command_handlers import CommandHandler


logger = logger.get_logger(__name__)


class FyleBot(TeamsActivityHandler):

    # Catches all errors and logs at ERROR level
    async def on_error(self, error: Exception):
        logger.error('\n [on_turn_error] unhandled error: %s', error)


    async def on_installation_update_add(self, turn_context: TurnContext):
        # On bot installation pass control to TeamAuthorisation module
        return await TeamAuthorisation.bot_installed(turn_context)


    async def on_installation_update_remove(self, turn_context: TurnContext):
        # On bot uninstallation pass control to TeamAuthorisation module
        return await TeamAuthorisation.bot_uninstalled(turn_context)


    async def on_message_activity(self, turn_context: TurnContext):
        return await CommandHandler().handle_commands(turn_context)
