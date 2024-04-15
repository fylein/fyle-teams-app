import logging
from botbuilder.core import TurnContext, CardFactory
from botbuilder.core.teams import TeamsInfo
from botbuilder.schema import Activity
from django.http.response import JsonResponse

from fyle_teams_app.models import User
from fyle_teams_app.libs import fyle_utils
from fyle_teams_app.ui.cards import authorisation as authorisation_card

logger = logging.getLogger(__name__)


class TeamAuthorisation:

    @staticmethod
    async def bot_installed(turn_context: TurnContext):

        user_conversation_reference = turn_context.get_conversation_reference(turn_context.activity)
        user_conversation_reference_dict = user_conversation_reference.as_dict()
        turn_context_dict = turn_context.activity.as_dict()
        team_id = turn_context_dict['channel_data']['tenant']['id']
        user_id = turn_context_dict['from_property']['id']

        logger.error(f"User conversation reference: {user_conversation_reference_dict}")
        logger.error(f"User id: {user_id}")
        logger.error(f"Team id: {team_id}")

        # Check if user already exists
        user = await User.get_by_id(user_id)

        # If user exists -> user has already installed Fyle app
        if user is not None:
            logger.error(f"User {user_id} has already installed Fyle app")
            return await turn_context.send_activity('Hey 👋, you\'ve already installed Fyle app!')

        # Create entry for user
        user = await User.create_user(team_id, user_id, user_conversation_reference_dict)
        logger.error(f"User {user_id} created successfully")

        FYLE_OAUTH_URL = fyle_utils.get_fyle_oauth_url(user_id, team_id)
        logger.error(f"Fyle OAuth URL: {FYLE_OAUTH_URL}")
        pre_auth_card = authorisation_card.get_pre_auth_card(FYLE_OAUTH_URL)

        user_details = await TeamsInfo.get_member(turn_context, user_id)
        logger.error(f"User details: {user_details.as_dict()}")
        User.track_bot_installation_status(user_details, 'Teams Bot Installed')

        return await turn_context.send_activity(
            Activity(
                attachments=[CardFactory.adaptive_card(pre_auth_card)]
            )
        )


    @staticmethod
    async def bot_uninstalled(turn_context: TurnContext):

        turn_context_dict = turn_context.activity.as_dict()
        logger.info(f"Turn context from bot_uninstalled: {turn_context_dict}")

        user_id = turn_context_dict['from_property']['id']
        logger.info(f"User id from bot_uninstalled: {user_id}")
        # Check if user already exists
        user = await User.get_by_id(user_id)
        logger.info(f"User from bot_uninstalled: {user}")
        # Remove user
        await User.remove_user(user)

        user_details = await TeamsInfo.get_member(turn_context, user_id)
        logger.info(f"User details: {user_details.as_dict()}")
        User.track_bot_installation_status(user_details, 'Teams Bot Uninstalled')

        return JsonResponse({})
