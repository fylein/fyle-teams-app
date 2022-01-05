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
