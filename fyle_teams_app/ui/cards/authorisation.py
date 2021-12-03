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
                        "text": "**Yaay 🎊. you've successfully linked Fyle to Microsoft Teams 🎊**\n\nWhat's next?\n\nIf you've submitted an expense report for approval, you'll receive real-time notifications on the Fyle Slack app whenever:\n\n• Your report gets approved ✅ \n\n• You receive your reimbursement 💰\n\n• A comment is made on the report 💬 \n\n• The report is sent back to you for further inquiry 🚫\n\nIf you're an approver, you'll see a direct message like below whenever your teammate submits a report to you for approval.\n",
                        "wrap": True
                    }
                ]
            },
            {
                "type": "Container",
                "items": [
                    {
                        "type": "ActionSet",
                        "actions": [
                            {
                                "type": "Action.ShowCard",
                                "title": "Report Approval Notification",
                                "card": {
                                    "type": "AdaptiveCard",
                                    "body": [
                                        {
                                            "type": "Container",
                                            "style": "emphasis",
                                            "items": [
                                                {
                                                    "type": "ColumnSet",
                                                    "columns": [
                                                        {
                                                            "type": "Column",
                                                            "items": [
                                                                {
                                                                    "type": "TextBlock",
                                                                    "size": "Large",
                                                                    "weight": "Bolder",
                                                                    "text": "**Expense report submitted for approval**",
                                                                    "wrap": True
                                                                }
                                                            ],
                                                            "width": "stretch"
                                                        }
                                                    ]
                                                }
                                            ],
                                            "bleed": True
                                        },
                                        {
                                            "type": "Container",
                                            "items": [
                                                {
                                                    "type": "ColumnSet",
                                                    "columns": [
                                                        {
                                                            "type": "Column",
                                                            "items": [
                                                                {
                                                                    "type": "TextBlock",
                                                                    "size": "ExtraLarge",
                                                                    "text": "Internet Spend ",
                                                                    "wrap": True
                                                                }
                                                            ],
                                                            "width": "stretch"
                                                        }
                                                    ]
                                                },
                                                {
                                                    "type": "TextBlock",
                                                    "spacing": "Small",
                                                    "size": "Small",
                                                    "weight": "Bolder",
                                                    "text": "[C/2021/05/R/34](https://fylehq.com)",
                                                    "wrap": True
                                                },
                                                {
                                                    "type": "FactSet",
                                                    "spacing": "Large",
                                                    "facts": [
                                                        {
                                                            "title": "Amount",
                                                            "value": "INR 1234.45"
                                                        },
                                                        {
                                                            "title": "Number of expenses",
                                                            "value": "2"
                                                        },
                                                        {
                                                            "title": "Submitted By",
                                                            "value": "**John Doe** (john.doe@gmail.com)"
                                                        },
                                                        {
                                                            "title": "Submitted On",
                                                            "value": "July 01, 2021"
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "type": "Container",
                                            "spacing": "Large",
                                            "style": "emphasis",
                                            "items": [
                                                {
                                                    "type": "Container",
                                                    "items": [
                                                        {
                                                            "type": "ColumnSet",
                                                            "columns": [
                                                                {
                                                                    "type": "Column",
                                                                    "width": "stretch",
                                                                    "items": [
                                                                        {
                                                                            "type": "TextBlock",
                                                                            "text": "**View Report Expenses**",
                                                                            "wrap": True
                                                                        },
                                                                        {
                                                                            "type": "ColumnSet",
                                                                            "id": "vrd",
                                                                            "isVisible": False,
                                                                            "columns": [
                                                                                {
                                                                                    "type": "Column",
                                                                                    "width": "stretch",
                                                                                    "items": [
                                                                                        {
                                                                                            "type": "TextBlock",
                                                                                            "text": "**Amount**",
                                                                                            "wrap": True
                                                                                        }
                                                                                    ]
                                                                                },
                                                                                {
                                                                                    "type": "Column",
                                                                                    "width": "stretch",
                                                                                    "items": [
                                                                                        {
                                                                                            "type": "TextBlock",
                                                                                            "text": "**Category**",
                                                                                            "wrap": True
                                                                                        }
                                                                                    ]
                                                                                },
                                                                                {
                                                                                    "type": "Column",
                                                                                    "width": "stretch",
                                                                                    "items": [
                                                                                        {
                                                                                            "type": "TextBlock",
                                                                                            "text": "**Merchant**",
                                                                                            "wrap": True
                                                                                        }
                                                                                    ]
                                                                                },
                                                                                {
                                                                                    "type": "Column",
                                                                                    "width": "stretch",
                                                                                    "items": [
                                                                                        {
                                                                                            "type": "TextBlock",
                                                                                            "text": "**Expense ID**",
                                                                                            "wrap": True
                                                                                        }
                                                                                    ]
                                                                                }
                                                                            ]
                                                                        },
                                                                        {
                                                                            "type": "ColumnSet",
                                                                            "id": "vrd1",
                                                                            "isVisible": False,
                                                                            "columns": [
                                                                                {
                                                                                    "type": "Column",
                                                                                    "width": "stretch",
                                                                                    "items": [
                                                                                        {
                                                                                            "type": "TextBlock",
                                                                                            "text": "INR 1200.00",
                                                                                            "wrap": True
                                                                                        }
                                                                                    ]
                                                                                },
                                                                                {
                                                                                    "type": "Column",
                                                                                    "width": "stretch",
                                                                                    "items": [
                                                                                        {
                                                                                            "type": "TextBlock",
                                                                                            "text": "Internet",
                                                                                            "wrap": True
                                                                                        }
                                                                                    ]
                                                                                },
                                                                                {
                                                                                    "type": "Column",
                                                                                    "width": "stretch",
                                                                                    "items": [
                                                                                        {
                                                                                            "type": "TextBlock",
                                                                                            "text": "Jio",
                                                                                            "wrap": True
                                                                                        }
                                                                                    ]
                                                                                },
                                                                                {
                                                                                    "type": "Column",
                                                                                    "width": "stretch",
                                                                                    "items": [
                                                                                        {
                                                                                            "type": "TextBlock",
                                                                                            "text": "[E/2021/11/T/14](https://fylehq.com)",
                                                                                            "wrap": True
                                                                                        }
                                                                                    ]
                                                                                }
                                                                            ]
                                                                        },
                                                                        {
                                                                            "type": "ColumnSet",
                                                                            "id": "vrd2",
                                                                            "isVisible": False,
                                                                            "columns": [
                                                                                {
                                                                                    "type": "Column",
                                                                                    "width": "stretch",
                                                                                    "items": [
                                                                                        {
                                                                                            "type": "TextBlock",
                                                                                            "text": "INR 134.45",
                                                                                            "wrap": True
                                                                                        }
                                                                                    ]
                                                                                },
                                                                                {
                                                                                    "type": "Column",
                                                                                    "width": "stretch",
                                                                                    "items": [
                                                                                        {
                                                                                            "type": "TextBlock",
                                                                                            "text": "Taxi",
                                                                                            "wrap": True
                                                                                        }
                                                                                    ]
                                                                                },
                                                                                {
                                                                                    "type": "Column",
                                                                                    "width": "stretch",
                                                                                    "items": [
                                                                                        {
                                                                                            "type": "TextBlock",
                                                                                            "text": "Uber",
                                                                                            "wrap": True
                                                                                        }
                                                                                    ]
                                                                                },
                                                                                {
                                                                                    "type": "Column",
                                                                                    "width": "stretch",
                                                                                    "items": [
                                                                                        {
                                                                                            "type": "TextBlock",
                                                                                            "text": "[E/2021/11/T/14](https://fylehq.com)",
                                                                                            "wrap": True
                                                                                        }
                                                                                    ]
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "type": "Column",
                                                                    "spacing": "Small",
                                                                    "selectAction": {
                                                                        "type": "Action.ToggleVisibility",
                                                                        "targetElements": [
                                                                            "vrd",
                                                                            "vrd1",
                                                                            "vrd2",
                                                                            "ChevronUp",
                                                                            "ChevronDown"
                                                                        ]
                                                                    },
                                                                    "verticalContentAlignment": "Center",
                                                                    "items": [
                                                                        {
                                                                            "type": "Image",
                                                                            "id": "ChevronDown",
                                                                            "url": "https://adaptivecards.io/content/down.png",
                                                                            "width": "20px"
                                                                        },
                                                                        {
                                                                            "type": "Image",
                                                                            "id": "ChevronUp",
                                                                            "url": "https://adaptivecards.io/content/up.png",
                                                                            "width": "20px",
                                                                            "isVisible": False
                                                                        }
                                                                    ],
                                                                    "width": "auto"
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ],
                                            "bleed": True
                                        },
                                        {
                                            "type": "Container",
                                            "items": [
                                                {
                                                    "type": "ActionSet",
                                                    "actions": [
                                                        {
                                                            "type": "Action.Execute",
                                                            "title": "Approve",
                                                            "data": {
                                                                "id": "_qkQW8dJlUeLVi7ZMEzYVw",
                                                                "action": "mock_report_approve"
                                                            },
                                                            "style": "positive"
                                                        },
                                                        {
                                                            "type": "Action.OpenUrl",
                                                            "title": "View in Fyle",
                                                            "url": "https://fylehq.com"
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ],
                                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                                    "version": "1.4",
                                    "fallbackText": "This card requires Adaptive Cards v1.2 support to be rendered properly."
                                }
                            }
                        ]
                    },
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
