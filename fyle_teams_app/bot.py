from botbuilder.core import TurnContext
from botbuilder.core.teams import TeamsActivityHandler

from fyle_teams_app.libs import logger


logger = logger.get_logger(__name__)


class FyleBot(TeamsActivityHandler):

    # Catch-all for errors.
    async def on_error(self, context: TurnContext, error: Exception):

        logger.error('\n [on_turn_error] unhandled error: %s', error)


    async def on_message_activity(self, turn_context: TurnContext):
        return await turn_context.send_activity('Hello this is a Fyle bot')
