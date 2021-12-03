import enum
import uuid

from typing import Dict, List

from asgiref.sync import sync_to_async

from django.db import models
from django.conf import settings

# from fyle_teams_app.libs import fyle_utils, logger, assertions

from fyle_teams_app.models import User


class SubscriptionType(enum.Enum):
    SPENDER = 'SPENDER'
    APPROVER = 'APPROVER'


class UserSubscription(models.Model):
    class Meta:
        db_table = 'user_subscriptions'
        unique_together = ['team_user', 'subscription_type']

    team_user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='team_user_id')
    subscription_type = models.CharField(max_length=120)
    fyle_subscription_id = models.CharField(max_length=120, unique=True)
    webhook_id = models.CharField(max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return '{} - {}'.format(self.team_user.team_user_id, self.subscription_type)


    @staticmethod
    def bulk_create_subsctiption(subsctiptions: List):
        return UserSubscription.objects.bulk_create(subsctiptions)


    # @staticmethod
    # async def create_notification_subscriptions(user, fyle_profile: Dict) -> None:
    #     access_token = fyle_utils.get_fyle_access_token(user.fyle_refresh_token)
    #     cluster_domain = fyle_utils.get_cluster_domain(access_token)

    #     SUBSCRIPTON_WEBHOOK_DETAILS_MAPPING = {
    #         SubscriptionType.SPENDER: {
    #             'role_required': 'FYLER',
    #             'webhook_url': '{}/fyle/fyler/notifications'.format(settings.SLACK_SERVICE_BASE_URL)
    #         },
    #         SubscriptionType.APPROVER: {
    #             'role_required': 'APPROVER',
    #             'webhook_url': '{}/fyle/approver/notifications'.format(settings.SLACK_SERVICE_BASE_URL)
    #         }
    #     }

    #     user_subscriptions = []

    #     for subscription_type in SubscriptionType:
    #         subscription_webhook_details = SUBSCRIPTON_WEBHOOK_DETAILS_MAPPING[subscription_type]

    #         subscription_role_required = subscription_webhook_details['role_required']

    #         if subscription_role_required in fyle_profile['roles']:
    #             fyle_user_id = user.fyle_user_id

    #             subscription_webhook_id = str(uuid.uuid4())

    #             webhook_url = subscription_webhook_details['webhook_url']
    #             webhook_url = '{}/{}'.format(webhook_url, subscription_webhook_id)

    #             subscription_payload = {}
    #             subscription_payload['data'] = {
    #                 'webhook_url': webhook_url,
    #                 'is_enabled': True
    #             }

    #             subscription = fyle_utils.upsert_fyle_subscription(cluster_domain, access_token, subscription_payload, subscription_type)

    #             if subscription.status_code != 200:
    #                 logger.error('Error while creating %s subscription for user: %s ', subscription_role_required, fyle_user_id)
    #                 logger.error('%s Subscription error %s', subscription_role_required, subscription.content)
    #                 assertions.assert_good(False)

    #             subscription_id = subscription.json()['data']['id']

    #             subscription = UserSubscription(
    #                 slack_user=user,
    #                 subscription_type=subscription_type.value,
    #                 subscription_id=subscription_id,
    #                 webhook_id=subscription_webhook_id
    #             )

    #             user_subscriptions.append(subscription)

    #     # Creating/Inserting subsctiptions in bulk
    #     await sync_to_async(UserSubscription.bulk_create_subsctiption, thread_sensitive=True)(user_subscriptions)
