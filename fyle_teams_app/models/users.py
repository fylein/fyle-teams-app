from typing import Dict

from asgiref.sync import sync_to_async

from django.db import models

from fyle_teams_app.libs import utils, fyle_utils
from fyle_teams_app.models.user_subscriptions import UserSubscription


class User(models.Model):

    class Meta:
        db_table = 'users'

    team_user_id = models.CharField(max_length=255, unique=True)
    team_id = models.CharField(max_length=255)
    team_user_conversation_reference = models.JSONField()
    email = models.EmailField(blank=True, null=True)
    fyle_user_id = models.CharField(max_length=120, unique=True, blank=True, null=True)
    fyle_refresh_token = models.TextField(blank=True, null=True)
    fyle_org_id = models.CharField(max_length=120, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "{} - {}".format(self.team_user_id, self.email)


    @staticmethod
    @sync_to_async
    def get_by_id(user_id: str):
        return utils.get_or_none(User, team_user_id=user_id)


    @staticmethod
    @sync_to_async
    def create_user(team_id: str, user_id: str, conversation_reference: Dict):
        return User.objects.get_or_create(
            team_id=team_id,
            team_user_id=user_id,
            team_user_conversation_reference=conversation_reference
        )


    @staticmethod
    @sync_to_async
    def set_fyle_account_details(team_user_id: str, fyle_profile: Dict, fyle_refresh_token: str):

        User.objects.filter(team_user_id=team_user_id).update(
            fyle_user_id=fyle_profile['user_id'],
            fyle_refresh_token=fyle_refresh_token,
            fyle_org_id=fyle_profile['org_id'],
            email=fyle_profile['user']['email']
        )


    @staticmethod
    async def link_fyle_account(code: str, team_user_id: str):

        fyle_refresh_token = await fyle_utils.get_fyle_refresh_token(code)

        fyle_profile = await fyle_utils.get_fyle_profile(fyle_refresh_token)

        await User.set_fyle_account_details(team_user_id, fyle_profile, fyle_refresh_token)

        user = await User.get_by_id(team_user_id)

        await UserSubscription.create_notification_subscriptions(user, fyle_profile)

        return user
