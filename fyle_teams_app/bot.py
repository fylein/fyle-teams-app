import json
from botbuilder.core import TurnContext
from botbuilder.core.card_factory import CardFactory
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.schema import AdaptiveCardInvokeValue, AdaptiveCardInvokeResponse, Activity, HeroCard, CardAction
from botbuilder.schema.teams import (
    TaskModuleMessageResponse,
    TaskModuleContinueResponse,
    TaskModuleRequest,
    TaskModuleResponse,
    TaskModuleTaskInfo,
)

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


    async def on_message_activity(self, turn_context: TurnContext):
        adaptive_card = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.0",
            "type": "AdaptiveCard",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Task Module from adaptive card",
                    "weight": "bolder",
                    "size": "medium"
                }
            ],
            "actions": [
                {
                    "id": "btnBuy",
                    "type": "Action.Submit",
                    "title": "Hello",
                    "data": {"msteams": {"type": "task/fetch"}, "data": "task_module_abcd"}
                }
            ]
        }
        card = CardFactory.adaptive_card(adaptive_card)
        return await turn_context.send_activity(
            Activity(
                attachments=[card]
            )
        )

        # buttons = [
        #     CardAction(
        #         type="invoke",
        #         title="Hello",
        #         value=json.dumps({"type": "task/fetch", "data": "hero_vard"})
        #     )
        # ]

        # card = HeroCard(title="Task Module Invocation from Hero Card", buttons=buttons)
        # card = CardFactory.hero_card(card)
        # return await turn_context.send_activity(
        #     Activity(
        #         attachments=[card]
        #     )
        # )


    async def on_teams_task_module_fetch(self, turn_context: TurnContext, task_module_request: TaskModuleRequest) -> TaskModuleResponse:
        task_info = TaskModuleTaskInfo()
        task_info.url = task_info.fallback_url = "https://www.fylehq.com"
        task_info.height = "large"
        task_info.width = "large"
        task_info.title = "Task Module Test"
        return TaskModuleResponse(task=TaskModuleContinueResponse(value=task_info))
