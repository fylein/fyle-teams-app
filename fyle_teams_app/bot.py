from botbuilder.core import TurnContext
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.schema import AdaptiveCardInvokeValue, AdaptiveCardInvokeResponse

from fyle_teams_app.libs import logger

from fyle_teams_app.views.authorisation.team import TeamAuthorisation
from fyle_teams_app.views.handlers.action_handlers import ActionHandler

logger = logger.get_logger(__name__)


class FyleBot(TeamsActivityHandler):

    # Catches all errors and logs at ERROR level
    async def on_error(self, error: Exception):
        logger.error('\n [on_turn_error] unhandled error: %s', error)


    async def on_installation_update_add(self, turn_context: TurnContext):
        # On bot installation pass control to TeamAuthorisation module
        return await TeamAuthorisation.bot_installed(turn_context)


    async def on_adaptive_card_invoke(self, turn_context: TurnContext, invoke_value: AdaptiveCardInvokeValue) -> AdaptiveCardInvokeResponse:
        # On button interaction on cards pass control to Action handler module
        return await ActionHandler().handle_actions(turn_context, invoke_value)
