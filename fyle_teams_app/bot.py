from botbuilder.core import TurnContext
from botbuilder.core.teams import TeamsActivityHandler

from fyle_teams_app.libs import logger

from fyle_teams_app.views.authorisation.team import TeamAuthorisation


logger = logger.get_logger(__name__)


class FyleBot(TeamsActivityHandler):

    # Catch-all for errors.
    async def on_error(self, error: Exception):

        logger.error('\n [on_turn_error] unhandled error: %s', error)


    async def on_message_activity(self, turn_context: TurnContext):
        return await turn_context.send_activity('Hello this is a Fyle bot')


    async def on_installation_update_add(self, turn_context: TurnContext):
        return await TeamAuthorisation.bot_installed(turn_context)
