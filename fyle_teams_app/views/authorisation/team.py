from asgiref.sync import sync_to_async

from django.conf import settings

from botbuilder.core import TurnContext, CardFactory
from botbuilder.schema import Activity

from fyle_teams_app.models import User
from fyle_teams_app.libs import utils
from fyle_teams_app.ui.cards import authorisation as authorisation_card

class TeamAuthorisation:

    @staticmethod
    async def bot_installed(turn_context: TurnContext):

        user_conversation_reference = turn_context.get_conversation_reference(turn_context.activity)
        user_conversation_reference_dict = user_conversation_reference.as_dict()
        turn_context_dict = turn_context.activity.as_dict()
        team_id = turn_context_dict['channel_data']['tenant']['id']
        user_id = turn_context_dict['from_property']['id']

        # Check if user already exists
        user = await sync_to_async(User.get_by_id, thread_sensitive=True)(user_id)

        # If user exists -> user has already installed Fyle app
        if user is not None:
            return await turn_context.send_activity('Hey 👋, you\'ve already installed Fyle app!')

        # Create entry for user
        user = await sync_to_async(User.create_user, thread_sensitive=True)(team_id, user_id, user_conversation_reference_dict)

        # State object to be used to identify which user is performing Fyle authorisation
        state = {
            'user_id': user_id,
            'team_id': team_id
        }

        # Encoding state to be passed in FYLE_OAUTH_URL
        encoded_state = utils.encode_state(state)

        # This url redirects request to our server when Fyle authorisation is done
        redirect_uri = '{}/fyle/authorisation'.format(settings.TEAMS_SERVICE_BASE_URL)

        FYLE_OAUTH_URL = '{}/app/developers/#/oauth/authorize?client_id={}&response_type=code&state={}&redirect_uri={}'.format(
            settings.FYLE_ACCOUNTS_URL,
            settings.FYLE_CLIENT_ID,
            encoded_state,
            redirect_uri
        )

        pre_auth_card = authorisation_card.get_pre_auth_card(FYLE_OAUTH_URL)

        return await turn_context.send_activity(
            Activity(
                attachments=[CardFactory.adaptive_card(pre_auth_card)]
            )
        )
