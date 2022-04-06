from typing import Dict

from fyle_teams_app.libs import fyle_utils

FYLE_APP_DOMAIN = fyle_utils.get_fyle_app_domain()


def get_pre_auth_card(fyle_oauth_url) -> Dict:
    pre_auth_card = {
        'type': 'AdaptiveCard',
        'body': [
            {
                'type': 'TextBlock',
                'size': 'Medium',
                'weight': 'Bolder',
                'text': 'Hey there 👋'
            },
            {
                'type': 'Container',
                'items': [
                    {
                        'type': 'TextBlock',
                        'text': '• The Fyle app for Microsoft Teams brings all the important expense reporting action to right where work happens. No more switching between multiple tabs!\n\n• Once you link your Fyle account, you can use this app to receive real-time notifications on the status of your expense reports after you\'ve submitted them.\n\n• And if you\'re an approver, you\'ll be notified on Microsoft Teams whenever a teammate submits an expense report to you. Not just that, you can even approve it right from this app. \n\nYour teammates are going to love you for your speed! ⚡\n\nWhat are you waiting for?\nLink your Fyle account now',
                        'color': 'Default',
                        'fontType': 'Default',
                        'wrap': True
                    }
                ],
                'style': 'emphasis'
            },
            {
                'type': 'Container',
                'items': [
                    {
                        'type': 'ActionSet',
                        'actions': [
                            {
                                'type': 'Action.OpenUrl',
                                'title': 'Link Your Fyle Account in {}'.format(FYLE_APP_DOMAIN),
                                'url': fyle_oauth_url,
                                'style': 'positive'
                            }
                        ]
                    }
                ]
            }
        ],
        '$schema': 'http://adaptivecards.io/schemas/adaptive-card.json',
        'version': '1.4'
    }
    return pre_auth_card


def get_post_auth_card() -> Dict:
    post_auth_card = {
        "type": "AdaptiveCard",
        "body": [
            {
                "type": "Container",
                "style": "emphasis",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": "**Yaay 🎊. you've successfully linked Fyle to Microsoft Teams 🎊**\n\nWhat's next?\n\nIf you've submitted an expense report for approval, you'll receive real-time notifications on the Fyle Teams app whenever:\n\n• Your report gets approved ✅ \n\n• You receive your reimbursement 💰\n\n• A comment is made on the report 💬 \n\n• The report is sent back to you for further inquiry 🚫\n\nIf you're an approver, you'll see a direct message like below whenever your teammate submits a report to you for approval.\n",
                        "wrap": True
                    }
                ]
            },
            {
                "type": "Container",
                "items": [
                    {
                        "type": "Container",
                        "style": "emphasis",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "You can even approve the report from within this app as soon as you're notified. Your teammates are going to love you for your speed! ⚡\n\nTo see the official documentation, visit https://www.fylehq.com/help/en/?q=microsoft-teams\n\nIf you're running into any trouble, please send us a note at support@fylehq.com",
                                "wrap": True
                            }
                        ]
                    }
                ]
            }
        ],
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.4"
    }
    return post_auth_card
