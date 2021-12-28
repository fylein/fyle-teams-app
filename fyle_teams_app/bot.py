from botbuilder.core import TurnContext
from botbuilder.core import CardFactory
from botbuilder.core.teams import TeamsActivityHandler
from botbuilder.schema import AdaptiveCardInvokeValue, AdaptiveCardInvokeResponse, Activity
from django.conf import settings

from fyle_teams_app.libs import logger

from fyle_teams_app.views.authorisation.team import TeamAuthorisation
from fyle_teams_app.views.handlers.action_handlers import ActionHandler

logger = logger.get_logger(__name__)

from botbuilder.schema.teams import (
    TaskModuleMessageResponse,
    TaskModuleContinueResponse,
    TaskModuleRequest,
    TaskModuleResponse,
    TaskModuleTaskInfo,
)

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


    async def on_teams_task_module_fetch(self, turn_context: TurnContext, task_module_request: TaskModuleRequest) -> TaskModuleResponse:
        task_info = TaskModuleTaskInfo()
        task_info.url = task_info.fallback_url = 'https://app.fyle.tech'
        task_info.height = 'medium'
        task_info.width = 'medium'
        task_info.title = 'Link Fyle Account'
        return TaskModuleResponse(task=TaskModuleContinueResponse(value=task_info))


    async def on_message_activity(self, turn_context: TurnContext):
        url = "https://teams.microsoft.com/l/stage/"+ settings.TEAMS_APP_ID +"/0?context={\"contentUrl\":\"https://tinyurl.com/y5qd7o5a\",\"websiteUrl\":\"https://tinyurl.com/y5qd7o5a\",\"name\":\"Link Fyle Account\"}"
        print('URL -> ', url)
        task_module_url = 'https://teams.microsoft.com/l/task/'+settings.TEAMS_APP_ID+'?url=https://tinyurl.com/y5qd7o5a&height=large&width=large&title=Link Fyle Account&completionBotId='+ settings.TEAMS_BOT_ID
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
                    "type": "Action.OpenUrl",
                    "title": 'Task Module Deep Link',
                    "url": task_module_url
                    # "data": {"msteams": {"type": "task/fetch"}, "data": 'task_module'},
                },
                {
                   "type": "Action.OpenUrl",
                   "title": "Stage View via Deep Link",
                    "url": url
                }
            ]
        }
        # adaptive_card = {
        #     "type": "AdaptiveCard",
        #     "version": "1.4",
        #     "authentication": {
        #         "connectionName": "myConnection",
        #         "text": "Please Authenticate your account",
        #         "tokenExchangeResource": {
        #         "id": "myTokenId",
        #         "providerId": "myProviderId",
        #         "uri": "https: //mytoken.exchange/resource"
        #         },
        #         "buttons": [
        #             {
        #                 "type": "signin",
        #                 "title": "Click here to Sign In!"
        #             }
        #         ]
        #     },
        #     "body": [
        #         {
        #         "type": "TextBlock",
        #         "text": "This is a card that has authentication"
        #         }
        #     ]
        # }
        card = CardFactory.adaptive_card(adaptive_card)
        return await turn_context.send_activity(
            Activity(
                attachments=[card]
            )
        )


    # async def on_message_activity(self, turn_context: TurnContext):
    #     return await super().on_message_activity(turn_context)
