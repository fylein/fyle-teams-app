import uuid
import asyncio

from typing import Dict

from asgiref.sync import sync_to_async

from botbuilder.schema import ConversationReference

from django.http import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.utils.decorators import classonlymethod
from django.views import View
from django.db import transaction
from django.conf import settings

from fyle_teams_app.models import User, UserSubscription
from fyle_teams_app.libs import utils, assertions, logger, team_utils, fyle_utils
from fyle_teams_app.models.user_subscriptions import SubscriptionType


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
        user = await sync_to_async(User.get_by_id, thread_sensitive=True)(user_id)
        assertions.assert_found(user, 'user not found')


        user_conversation_reference = ConversationReference().from_dict(user.team_user_conversation_reference)

        if error:
            logger.info('Fyle authorization error: %s', error)

            error_message = 'Seems like something went wrong 🤕 \n' \
                        'If the issues still persists, please contact support@fylehq.com'

            # Error when user declines Fyle authorization
            if error == 'access_denied':
                error_message = 'Well.. if you do change your mind, visit the home tab and link your Fyle account to Teams to stay up to date on all your expense reports.'

            return await team_utils.send_message_to_user(
                user_conversation_reference,
                error_message
            )

        else:
            code = request.GET.get('code')

            if user.fyle_user_id is not None:
                # If the user already exists send a message to user indicating they've already linked Fyle account
                message = 'Hey buddy you\'ve already linked your *Fyle* account 🌈'

                return await team_utils.send_message_to_user(
                    user_conversation_reference,
                    message
                )

            else:
                # Putting below logic inside a transaction block to prevent bad data
                # If any error occurs in any of the below step, Fyle account link to Slack should not happen
                # with transaction.atomic():

                # user = await sync_to_async(User.link_fyle_account, thread_sensitive=True)(code, user_id)

                fyle_refresh_token = await fyle_utils.get_fyle_refresh_token(code)

                fyle_profile = await fyle_utils.get_fyle_profile(fyle_refresh_token)

                user = await sync_to_async(User.link_fyle_account, thread_sensitive=True)(
                    user_id,
                    fyle_profile,
                    fyle_refresh_token
                )

                await self.create_notification_subscriptions(user, fyle_profile)

        return HttpResponse('Your Fyle account is successfully linked with Microsoft Teams')


    async def create_notification_subscriptions(self, user: User, fyle_profile: Dict) -> None:
        access_token = fyle_utils.get_fyle_access_token(user.fyle_refresh_token)
        cluster_domain = await fyle_utils.get_cluster_domain(access_token)

        SUBSCRIPTON_WEBHOOK_DETAILS_MAPPING = {
            SubscriptionType.SPENDER: {
                'role_required': 'FYLER',
                'webhook_url': '{}/fyle/fyler/notifications'.format(settings.TEAMS_SERVICE_BASE_URL)
            },
            SubscriptionType.APPROVER: {
                'role_required': 'APPROVER',
                'webhook_url': '{}/fyle/approver/notifications'.format(settings.TEAMS_SERVICE_BASE_URL)
            }
        }

        user_subscriptions = []

        for subscription_type in SubscriptionType:
            subscription_webhook_details = SUBSCRIPTON_WEBHOOK_DETAILS_MAPPING[subscription_type]

            subscription_role_required = subscription_webhook_details['role_required']

            if subscription_role_required in fyle_profile['roles']:
                fyle_user_id = user.fyle_user_id

                subscription_webhook_id = str(uuid.uuid4())

                webhook_url = subscription_webhook_details['webhook_url']
                webhook_url = '{}/{}'.format(webhook_url, subscription_webhook_id)

                subscription_payload = {}
                subscription_payload['data'] = {
                    'webhook_url': webhook_url,
                    'is_enabled': True
                }

                subscription = await fyle_utils.upsert_fyle_subscription(cluster_domain, access_token, subscription_payload, subscription_type)

                if subscription.status_code != 200:
                    logger.error('Error while creating %s subscription for user: %s ', subscription_role_required, fyle_user_id)
                    logger.error('%s Subscription error %s', subscription_role_required, subscription.content)
                    assertions.assert_good(False)

                subscription_id = subscription.json()['data']['id']

                subscription = UserSubscription(
                    team_user=user,
                    subscription_type=subscription_type.value,
                    fyle_subscription_id=subscription_id,
                    webhook_id=subscription_webhook_id
                )

                user_subscriptions.append(subscription)

        # Creating/Inserting subsctiptions in bulk
        await sync_to_async(UserSubscription.bulk_create_subsctiption, thread_sensitive=True)(user_subscriptions)
