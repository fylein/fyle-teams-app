from botbuilder.core import TurnContext
from botbuilder.core.teams import TeamsActivityHandler

from fyle_teams_app.libs import logger

from fyle_teams_app.views.authorisation.team import TeamAuthorisation


logger = logger.get_logger(__name__)


class FyleBot(TeamsActivityHandler):

    # Catches all errors and logs at ERROR level
    async def on_error(self, error: Exception):
        logger.error('\n [on_turn_error] unhandled error: %s', error)


    async def on_installation_update_add(self, turn_context: TurnContext):
        # On bot installation pass control to TeamAuthorisation modile
        return await TeamAuthorisation.bot_installed(turn_context)
