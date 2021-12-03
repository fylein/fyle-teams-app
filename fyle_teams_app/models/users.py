from typing import Dict


from django.db import models, transaction

from fyle_teams_app.libs import utils
# from fyle_teams_app.models import UserSubscription


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
    def get_by_id(user_id: str):
        return utils.get_or_none(User, team_user_id=user_id)


    @staticmethod
    def create_user(team_id: str, user_id: str, conversation_reference: Dict):
        return User.objects.get_or_create(
            team_id=team_id,
            team_user_id=user_id,
            team_user_conversation_reference=conversation_reference
        )


    @staticmethod
    def link_fyle_account(team_user_id: str, fyle_profile: Dict, fyle_refresh_token: str):

        User.objects.filter(team_user_id=team_user_id).update(
            fyle_user_id=fyle_profile['user_id'],
            fyle_refresh_token=fyle_refresh_token,
            fyle_org_id=fyle_profile['org_id'],
            email=fyle_profile['user']['email']
        )

        return User.get_by_id(team_user_id)

    # @staticmethod
    # def link_fyle_account(code: str, team_user_id: str):

    #     user = None

    #     with transaction.atomic():

    #         fyle_refresh_token = fyle_utils.get_fyle_refresh_token(code)

    #         fyle_profile = fyle_utils.get_fyle_profile(fyle_refresh_token)

    #         user = User.objects.get(team_user_id=team_user_id).update(
    #             fyle_user_id=fyle_profile['user_id'],
    #             fyle_refresh_token=fyle_refresh_token,
    #             fyle_org_id=fyle_profile['org_id'],
    #             email=fyle_profile['user']['email']
    #         )

    #         UserSubscription.create_notification_subscriptions(user, fyle_profile)

    #     return user
