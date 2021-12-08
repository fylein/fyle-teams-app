from typing import Dict, List

import enum
import uuid
import aiohttp
import asyncio


from asgiref.sync import sync_to_async

from django.db import models
from django.conf import settings

from fyle_teams_app.libs import fyle_utils, logger, assertions, http


class SubscriptionType(enum.Enum):
    SPENDER = 'SPENDER'
    APPROVER = 'APPROVER'


class UserSubscription(models.Model):
    class Meta:
        db_table = 'user_subscriptions'
        unique_together = ['team_user', 'subscription_type']

    team_user = models.ForeignKey('User', on_delete=models.CASCADE, to_field='team_user_id')
    subscription_type = models.CharField(max_length=120)
    fyle_subscription_id = models.CharField(max_length=120, unique=True)
    webhook_id = models.CharField(max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return '{} - {}'.format(self.team_user.team_user_id, self.subscription_type)


    @staticmethod
    @sync_to_async
    def bulk_create_subsctiption(subsctiptions: List):
        return UserSubscription.objects.bulk_create(subsctiptions)


    @staticmethod
    @sync_to_async
    def remove_user_subscriptions(team_user_id: str):
        UserSubscription.objects.filter(team_user_id=team_user_id).delete()


    @staticmethod
    async def create_notification_subscriptions(user, fyle_profile: Dict) -> None:
        access_token = await fyle_utils.get_fyle_access_token(user.fyle_refresh_token)
        cluster_domain = await fyle_utils.get_cluster_domain(access_token)

        SUBSCRIPTON_WEBHOOK_DETAILS_MAPPING = {
            SubscriptionType.SPENDER: {
                'role_required': 'FYLER',
                'webhook_url': '{}/fyle/spender/notifications'.format(settings.TEAMS_SERVICE_BASE_URL)
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

                # This will create async task an run in parallel and do another task
                subscription = await asyncio.create_task(
                    UserSubscription.upsert_fyle_subscription(cluster_domain, access_token, subscription_payload, subscription_type)
                )

                if subscription.status != 200:
                    logger.error('Error while creating %s subscription for user: %s ', subscription_role_required, fyle_user_id)
                    logger.error('%s Subscription error %s', subscription_role_required, subscription.content)
                    assertions.assert_good(False)

                subscription = await subscription.json()

                subscription_id = subscription['data']['id']

                subscription = UserSubscription(
                    team_user=user,
                    subscription_type=subscription_type.value,
                    fyle_subscription_id=subscription_id,
                    webhook_id=subscription_webhook_id
                )

                user_subscriptions.append(subscription)

        # Creating/Inserting subsctiptions in bulk
        await UserSubscription.bulk_create_subsctiption(user_subscriptions)


    @staticmethod
    async def upsert_fyle_subscription(cluster_domain: str, access_token: str, subscription_payload: Dict, subscription_type: SubscriptionType) -> aiohttp.ClientResponse:
        FYLE_PLATFORM_URL = '{}/platform/v1'.format(cluster_domain)

        SUBSCRIPTION_TYPE_URL_MAPPINGS = {
            SubscriptionType.SPENDER: '{}/spender/subscriptions'.format(FYLE_PLATFORM_URL),
            SubscriptionType.APPROVER: '{}/approver/subscriptions'.format(FYLE_PLATFORM_URL)
        }

        subscrition_url = SUBSCRIPTION_TYPE_URL_MAPPINGS[subscription_type]

        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        }

        subscription = await http.post(
            url=subscrition_url,
            json=subscription_payload,
            headers=headers
        )

        return subscription
