import pyshorteners

from botbuilder.core import TurnContext, CardFactory
from botbuilder.core.teams import TeamsInfo
from botbuilder.schema import Activity

from fyle_teams_app.models import User
from fyle_teams_app.libs import fyle_utils, team_utils
from fyle_teams_app.ui.cards import authorisation as authorisation_card


shortner = pyshorteners.Shortener()


class TeamAuthorisation:

    @staticmethod
    async def bot_installed(turn_context: TurnContext):

        user_conversation_reference = turn_context.get_conversation_reference(turn_context.activity)
        user_conversation_reference_dict = user_conversation_reference.as_dict()
        turn_context_dict = turn_context.activity.as_dict()
        team_id = turn_context_dict['channel_data']['tenant']['id']
        user_id = turn_context_dict['from_property']['id']

        # Check if user already exists
        user = await User.get_by_id(user_id)

        # If user exists -> user has already installed Fyle app
        if user is not None:
            return await turn_context.send_activity('Hey 👋, you\'ve already installed Fyle app!')

        # Create entry for user
        user = await User.create_user(team_id, user_id, user_conversation_reference_dict)

        FYLE_OAUTH_URL = fyle_utils.get_fyle_oauth_url(user_id, team_id)

        short_fyle_oauth_url = shortner.tinyurl.short(FYLE_OAUTH_URL)

        FYLE_OAUTH_URL = team_utils.get_teams_stage_view_url(short_fyle_oauth_url, 'Link Fyle Account')

        pre_auth_card = authorisation_card.get_pre_auth_card(FYLE_OAUTH_URL)

        user_details = await TeamsInfo.get_member(turn_context, user_id)

        User.track_bot_installed(user_details)

        return await turn_context.send_activity(
            Activity(
                attachments=[CardFactory.adaptive_card(pre_auth_card)]
            )
        )
