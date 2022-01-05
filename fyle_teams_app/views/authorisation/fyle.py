import asyncio

from botbuilder.schema import ConversationReference
from botbuilder.core import CardFactory

from django.http import HttpRequest
from django.http.response import HttpResponseRedirect
from django.utils.decorators import classonlymethod
from django.views import View
from django.conf import settings

from fyle_teams_app.models import User
from fyle_teams_app.libs import utils, assertions, logger, team_utils
from fyle_teams_app.ui.cards import authorisation as authorisation_card


logger = logger.get_logger(__name__)


class FyleAuthorisation(View):

    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        # pylint: disable=protected-access
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view


    async def get(self, request: HttpRequest):

        error = request.GET.get('error')
        state = request.GET.get('state')

        state_params = utils.decode_state(state)

        user_id = state_params['user_id']

        # Fetch the user
        user = await User.get_by_id(user_id)
        assertions.assert_found(user, 'user not found')

        user_conversation_reference = ConversationReference().from_dict(user.team_user_conversation_reference)

        if error:
            logger.info('Fyle authorization error: %s', error)

            error_message = 'Seems like something went wrong 🤕 \n' \
                        'If the issues still persists, please contact support@fylehq.com'

            # Error when user declines Fyle authorization
            if error == 'access_denied':
                error_message = 'Well.. if you do change your mind link your Fyle account to Teams to stay up to date on all your expense reports.'

            return await team_utils.send_message_to_user(
                user_conversation_reference,
                error_message
            )

        else:
            code = request.GET.get('code')

            if user.fyle_user_id is not None:
                # If the user already exists send a message to user indicating they've already linked Fyle account
                message = 'Hey buddy you\'ve already linked your *Fyle* account 🌈'

                await team_utils.send_message_to_user(
                    user_conversation_reference,
                    message
                )

            else:

                user, error_occured = await User.link_fyle_account(code, user_id)

                if error_occured is True:
                    message = 'Hey seems like an error occured while linking your *Fyle* account 🤕   Please try again in a while \n If the issues still persists, please contact support@fylehq.com'

                    await team_utils.send_message_to_user(
                        user_conversation_reference,
                        message
                    )
                else:
                    post_auth_card = authorisation_card.get_post_auth_card()

                    await team_utils.send_message_to_user(
                        user_conversation_reference,
                        attachments=[CardFactory.adaptive_card(post_auth_card)]
                    )

        redirect_url = 'https://teams.microsoft.com/l/chat/0/0?users=28:{}'.format(settings.TEAMS_BOT_ID)

        return HttpResponseRedirect(redirect_url)
