import enum

from django.db import models

from fyle_teams_app.models.users import User


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
