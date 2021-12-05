from typing import Dict

from asgiref.sync import sync_to_async

from django.db import models

from fyle_teams_app.libs import utils

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
    def get_by_id(user_id):
        return utils.get_or_none(User, team_user_id=user_id)


    @staticmethod
    @sync_to_async
    def create_user(team_id: str, user_id: str, conversation_reference: Dict):
        return User.objects.get_or_create(
            team_id=team_id,
            team_user_id=user_id,
            team_user_conversation_reference=conversation_reference
        )
