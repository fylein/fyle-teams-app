from typing import Dict


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
            }
        ],
        'actions': [
            {
                'type': 'Action.OpenUrl',
                'title': 'Link Your Fyle Account',
                'url': fyle_oauth_url,
                'style': 'positive'
            }
        ],
        '$schema': 'http://adaptivecards.io/schemas/adaptive-card.json',
        'version': '1.4',
        'selectAction': {
            'type': 'Action.OpenUrl'
        }
    }
    return pre_auth_card
