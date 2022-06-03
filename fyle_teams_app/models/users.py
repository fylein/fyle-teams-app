from typing import Dict

from asgiref.sync import sync_to_async

from botbuilder.schema.teams import TeamsChannelAccount

from django.db import models

from fyle_teams_app.libs import utils, fyle_utils, logger
from fyle_teams_app.libs.tracking import Tracking
from fyle_teams_app.models.user_subscriptions import UserSubscription


logger = logger.get_logger(__name__)


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
    fyle_org_name = models.CharField(max_length=120, blank=True, null=True)
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
    def get_by_fyle_user_id(fyle_user_id: str):
        return utils.get_or_none(User, fyle_user_id=fyle_user_id)

    @staticmethod
    @sync_to_async
    def delete_user(user):
        user.delete()

    @staticmethod
    async def remove_user(user):
        if user.fyle_user_id is not None:
            await UserSubscription.disable_notification_subscriptions(user)
            await UserSubscription.remove_user_subscriptions(user.team_user_id)
        await User.delete_user(user)


    @staticmethod
    @sync_to_async
    def create_user(team_id: str, user_id: str, conversation_reference: Dict):
        return User.objects.create(
            team_id=team_id,
            team_user_id=user_id,
            team_user_conversation_reference=conversation_reference
        )


    @staticmethod
    @sync_to_async
    def set_user_details(team_user_id: str, fyle_profile: Dict, fyle_refresh_token: str):
        User.objects.filter(team_user_id=team_user_id).update(
            fyle_user_id=fyle_profile['user_id'],
            fyle_refresh_token=fyle_refresh_token,
            fyle_org_id=fyle_profile['org_id'],
            fyle_org_name=fyle_profile['org']['name'],
            email=fyle_profile['user']['email']
        )


    @staticmethod
    @sync_to_async
    def clear_user_details(team_user_id: str):
        User.objects.filter(team_user_id=team_user_id).update(
            fyle_user_id=None,
            fyle_refresh_token=None,
            fyle_org_id=None,
            email=None
        )


    @staticmethod
    async def link_fyle_account(code: str, team_user_id: str):
        # Since transaction block cannot be used in async world with our use case
        # Using try catch block here, if any error occurs while linking Fyle account
        # Clear fyle acccount details and remove subscriptions
        error_occured = False
        user = None
        error_message = None
        try:
            fyle_refresh_token = await fyle_utils.get_fyle_refresh_token(code)

            fyle_profile = await fyle_utils.get_fyle_profile(fyle_refresh_token)

            user = await User.get_by_fyle_user_id(fyle_profile['user_id'])

            if user is not None:
                error_occured = True
                error_message = 'Hey buddy you\'ve already linked your *Fyle* account in another teams workspace. Please unlink account from there first and link here again.'
            else:
                await User.set_user_details(team_user_id, fyle_profile, fyle_refresh_token)

                user = await User.get_by_id(team_user_id)

                await UserSubscription.create_notification_subscriptions(user, fyle_profile)

                User.track_fyle_account_linked(user, fyle_profile)

        except Exception as e:
            logger.error('Error while linking Fyle account %s', str(e))
            # Clear fyle acccount details if created
            await User.clear_user_details(team_user_id)

            error_message = 'Hey seems like an error occured while linking your *Fyle* account 🤕   Please try again in a while \n If the issues still persists, please contact support@fylehq.com'
            error_occured = True

        return user, error_occured, error_message


    @staticmethod
    def track_fyle_account_linked(user, fyle_profile: Dict) -> None:
        event_data = {
            'teams_user_id': user.team_user_id,
            'fyle_user_id': user.fyle_user_id,
            'email': user.email,
            'team_id': user.team_id,
            'fyle_org_id': user.fyle_org_id,
            'fyle_org_name': fyle_profile['org']['name'],
            'fyle_roles': fyle_profile['roles']
        }

        tracking = Tracking(user.email)
        tracking.track_event(user.email, 'Fyle Account Linked To Teams', event_data)

    @staticmethod
    def track_fyle_account_unlinked(event_data) -> None:
        email = event_data['email']
        tracking = Tracking(email)
        tracking.track_event(email, 'Fyle Account Unlinked From Teams', event_data)


    @staticmethod
    def track_bot_installation_status(user_details: TeamsChannelAccount, event_name: str):
        user_email = user_details.email if user_details.email is not None else user_details.user_principal_name
        event_data = {
            'user_id': user_details.id,
            'team_id': user_details.tenant_id,
            'email': user_email,
            'name': user_details.name
        }

        tracking = Tracking(user_email)
        tracking.track_event(user_email, event_name, event_data)
