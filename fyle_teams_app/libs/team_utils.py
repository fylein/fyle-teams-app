from typing import List

from botbuilder.schema import ConversationReference, Attachment, Activity

from django.conf import settings


TEAMS_BOT_ADAPTER = settings.TEAMS_BOT_ADAPTER


async def send_message_to_user(conversation_reference: ConversationReference, message: str = None, attachments: List[Attachment] = None):

    # If message is passed send only message to user
    if message is not None:
        activity = message

    # If attachment is passed send only attachment to user
    if attachments is not None:
        activity = Activity(
            attachments=attachments
        )

    return await TEAMS_BOT_ADAPTER.continue_conversation(
        conversation_reference,
        lambda turn_context: turn_context.send_activity(
            activity
        ),
        settings.TEAMS_BOT_ID
    )

def get_teams_stage_view_url(url: str, view_name: str) -> str:
    stage_view_url = "https://teams.microsoft.com/l/stage/"+ settings.TEAMS_APP_ID +"/0?context={\"contentUrl\":\""+ url +"\",\"websiteUrl\":\"" + url +"\",\"name\":\""+ view_name +"\"}"
    return stage_view_url


def get_teams_task_module_url(url: str, view_name: str) -> str:
    task_module_url = 'https://teams.microsoft.com/l/task/{}?url={}&height=large&width=large&title={}&completionBotId={}'.format(
        settings.TEAMS_APP_ID,
        url,
        view_name,
        settings.TEAMS_BOT_ID
    )
    return task_module_url
