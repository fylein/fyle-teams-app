from typing import Dict

from fyle_teams_app.libs import utils, fyle_utils


expenses = [
    {
        'amount': '123.45',
        'currency': 'INR',
        'seq_num': 'E/2021/11/T/15',
        'id': 'tx4whV8C1GGo',
        'org_id': 'abcd234',
        'spent_at': '2020-06-01T13:14:54.804+00:00',
        'category': {
            'name': 'Internet'
        },
        'merchant': 'Jio'
    },
    {
        'amount': '32.12',
        'currency': 'INR',
        'seq_num': 'E/2021/11/T/15',
        'id': 'tx4whV8C1GG1',
        'org_id': 'abcd234',
        'spent_at': '2020-06-01T13:14:54.804+00:00',
        'category': {
            'name': 'Taxi'
        },
        'merchant': 'Uber'
    }
]


def get_report_approval_card(report: Dict, message: str = None, can_approve_report: bool = True) -> Dict:
    view_report_expenses_view = [
        {
            'type': 'TextBlock',
            'text': '**View Report Expenses**',
            'wrap': True
        },
        {
            'type': 'ColumnSet',
            'id': 'expense_details_heading',
            'isVisible': False,
            'columns': [
                {
                    'type': 'Column',
                    'width': 'stretch',
                    'items': [
                        {
                            'type': 'TextBlock',
                            'text': '**Date of Spend**',
                            'wrap': True
                        }
                    ]
                },
                {
                    'type': 'Column',
                    'width': 'stretch',
                    'items': [
                        {
                            'type': 'TextBlock',
                            'text': '**Category**',
                            'wrap': True
                        }
                    ]
                },
                {
                    'type': 'Column',
                    'width': 'stretch',
                    'items': [
                        {
                            'type': 'TextBlock',
                            'text': '**Merchant**',
                            'wrap': True
                        }
                    ]
                },
                {
                    'type': 'Column',
                    'width': 'stretch',
                    'items': [
                        {
                            'type': 'TextBlock',
                            'text': '**Amount**',
                            'wrap': True
                        }
                    ]
                },
            ]
        }
    ]
    view_report_expenses_target_elements = [
        'expense_details_heading',
        'chevronUp',
        'chevronDown'
    ]

    for expense in expenses:
        view_report_expenses_target_elements.append(expense['id'])
        expense_view = {
            'type': 'ColumnSet',
            'id': '{}'.format(expense['id']),
            'isVisible': False,
            'columns': [
                {
                    'type': 'Column',
                    'width': 'stretch',
                    'items': [
                        {
                            'type': 'TextBlock',
                            'text': '{}'.format(utils.get_formatted_datetime(expense['spent_at'], '%B %d, %Y')),
                            'wrap': True
                        }
                    ]
                },
                {
                    'type': 'Column',
                    'width': 'stretch',
                    'items': [
                        {
                            'type': 'TextBlock',
                            'text': '{}'.format(expense['category']['name']),
                            'wrap': True
                        }
                    ]
                },
                {
                    'type': 'Column',
                    'width': 'stretch',
                    'items': [
                        {
                            'type': 'TextBlock',
                            'text': '{}'.format(expense['merchant']),
                            'wrap': True
                        }
                    ]
                },
                {
                    'type': 'Column',
                    'width': 'stretch',
                    'items': [
                        {
                            'type': 'TextBlock',
                            'text': '{} {}'.format(expense['currency'], expense['amount']),
                            'wrap': True
                        }
                    ]
                }
            ]
        }
        view_report_expenses_view.append(expense_view)

    report_approval_card = {
        'type': 'AdaptiveCard',
        '$schema': 'http://adaptivecards.io/schemas/adaptive-card.json',
        'version': '1.4',
        'body': [
            {
                'type': 'Container',
                'style': 'emphasis',
                'items': [
                    {
                        'type': 'ColumnSet',
                        'columns': [
                            {
                                'type': 'Column',
                                'items': [
                                    {
                                        'type': 'TextBlock',
                                        'size': 'large',
                                        'weight': 'bolder',
                                        'text': '📩 **Expense report submitted for approval**',
                                        'wrap': True
                                    }
                                ],
                                'width': 'stretch'
                            }
                        ]
                    }
                ],
                'bleed': True
            },
            {
                'type': 'Container',
                'items': [
                    {
                        'type': 'ColumnSet',
                        'columns': [
                            {
                                'type': 'Column',
                                'items': [
                                    {
                                        'type': 'TextBlock',
                                        'size': 'ExtraLarge',
                                        'text': '{}'.format(report['purpose']),
                                        'wrap': True
                                    }
                                ],
                                'width': 'stretch'
                            }
                        ]
                    },
                    {
                        'type': 'TextBlock',
                        'spacing': 'Small',
                        'size': 'Small',
                        'weight': 'Bolder',
                        'text': '[[{}]]({})'.format(report['seq_num'], fyle_utils.get_fyle_resource_url(report, 'REPORT')),
                        'wrap': True
                    },
                    {
                        'type': 'FactSet',
                        'spacing': 'Large',
                        'facts': [
                            {
                                'title': 'Amount',
                                'value': '{} {}'.format(report['currency'], report['amount'])
                            },
                            {
                                'title': 'No. of Expenses',
                                'value': '{}'.format(report['num_expenses'])
                            },
                            {
                                'title': 'Submitted By',
                                'value': '**{}**  ({})'.format(report['user']['full_name'], report['user']['email'])
                            },
                            {
                                'title': 'Submitted On',
                                'value': '{}'.format(utils.get_formatted_datetime(report['last_submitted_at'], '%B %d, %Y'))
                            }
                        ]
                    }
                ]
            },
            {
                'type': 'Container',
                'spacing': 'Large',
                'style': 'emphasis',
                'items': [
                    {
                        'type': 'Container',
                        'items': [
                            {
                                'type': 'ColumnSet',
                                'columns': [
                                    {
                                        'type': 'Column',
                                        'width': 'stretch',
                                        'items': view_report_expenses_view
                                    },
                                    {
                                        'type': 'Column',
                                        'spacing': 'Small',
                                        'selectAction': {
                                            'type': 'Action.ToggleVisibility',
                                            'targetElements': view_report_expenses_target_elements
                                        },
                                        'verticalContentAlignment': 'Center',
                                        'items': [
                                            {
                                                'type': 'Image',
                                                'id': 'chevronDown',
                                                'url': 'https://adaptivecards.io/content/down.png',
                                                'width': '20px',
                                            },
                                            {
                                                'type': 'Image',
                                                'id': 'chevronUp',
                                                'url': 'https://adaptivecards.io/content/up.png',
                                                'width': '20px',
                                                'isVisible': False
                                            }
                                        ],
                                        'width': 'auto'
                                    }
                                ]
                            }
                        ]
                    }
                ],
                'bleed': True
            },
            {
                'type': 'Container',
                'items': [
                    {
                        'type': 'ActionSet',
                        'actions': [
                            {
                                'type': 'Action.OpenUrl',
                                'title': 'View in Fyle',
                                'url': '{}'.format(fyle_utils.get_fyle_resource_url(report, 'REPORT'))
                            }
                        ]
                    }
                ]
            }
        ]
    }

    if message is not None and can_approve_report is False:
        report_message_view = {
            'type': 'TextBlock',
            'text': message,
            'wrap': True,
            'fontType': 'Default',
            'size': 'Medium',
            'weight': 'Bolder'
        }
        report_approval_card['body'][-1]['items'].insert(0, report_message_view)

    elif report['state'] == 'APPROVER_PENDING':
        approve_action = {
            'type': 'Action.Execute',
            'title': 'Approve',
            'style': 'positive',
            'data': {
                'id': '{}'.format(report['id']),
                'action': 'approve_report'
            }
        }
        report_approval_card['body'][-1]['items'][0]['actions'].insert(0, approve_action)

    return report_approval_card


def get_report_details_card(report: Dict, headline_text: str) -> Dict:

    report_details_card = {
        'type': 'AdaptiveCard',
        'body': [
            {
                'type': 'Container',
                'style': 'emphasis',
                'items': [
                    {
                        'type': 'ColumnSet',
                        'columns': [
                            {
                                'type': 'Column',
                                'items': [
                                    {
                                        'type': 'TextBlock',
                                        'size': 'medium',
                                        'weight': 'bolder',
                                        'text': headline_text,
                                        'wrap': True
                                    }
                                ],
                                'width': 'stretch'
                            }
                        ]
                    }
                ],
                'bleed': True
            },
            {
                'type': 'Container',
                'items': [
                    {
                        'type': 'FactSet',
                        'spacing': 'Large',
                        'facts': [
                            {
                                'title': 'Report Name',
                                'value': '{}'.format(report['purpose'])
                            },
                            {
                                'title': 'Amount',
                                'value': '{} {}'.format(report['currency'], report['amount'])
                            },
                            {
                                'title': 'Number of expenses',
                                'value': '{}'.format(report['num_expenses'])
                            },
                            {
                                'title': 'Submitted On',
                                'value': '{}'.format(utils.get_formatted_datetime(report['last_submitted_at'], '%B %d, %Y'))
                            }
                        ]
                    }
                ]
            },
            {
                'type': 'Container',
                'items': [
                    {
                        'type': 'ActionSet',
                        'actions': [
                            {
                                'type': 'Action.OpenUrl',
                                'title': 'View in Fyle',
                                'url': '{}'.format(fyle_utils.get_fyle_resource_url(report, 'REPORT'))
                            }
                        ]
                    }
                ]
            }
        ],
        '$schema': 'http://adaptivecards.io/schemas/adaptive-card.json',
        'version': '1.4',
        'fallbackText': 'This card requires Adaptive Cards v1.2 support to be rendered properly.',
        'verticalContentAlignment': 'Center'
    }

    return report_details_card


def get_expense_details_card(expense: Dict, headline_text: str) -> Dict:

    category = expense['category']['name']
    sub_category = expense['category']['sub_category']

    if sub_category is not None and category != sub_category:
        category = '{} / {}'.format(category, sub_category)

    currency = expense['currency']
    amount =  expense['amount']

    amount_details = '*Amount:*\n {} {}'.format(currency, amount)

    # If foreign currency exists, then show foreign amount and currency
    if expense['foreign_currency'] is not None:
        foreign_currency = expense['foreign_currency']
        foreign_amount =  expense['foreign_amount']

        amount_details = '{} \n ({} {})'.format(amount_details, foreign_currency, foreign_amount)

    expense_details_card = {
        'type': 'AdaptiveCard',
        'body': [
            {
                'type': 'Container',
                'style': 'emphasis',
                'items': [
                    {
                        'type': 'ColumnSet',
                        'columns': [
                            {
                                'type': 'Column',
                                'items': [
                                    {
                                        'type': 'TextBlock',
                                        'size': 'medium',
                                        'weight': 'bolder',
                                        'text': headline_text,
                                        'wrap': True
                                    }
                                ],
                                'width': 'stretch'
                            }
                        ]
                    }
                ],
                'bleed': True
            },
            {
                'type': 'Container',
                'items': [
                    {
                        'type': 'FactSet',
                        'spacing': 'Large',
                        'facts': [
                            {
                                'title': 'Amount',
                                'value': '{}'.format(amount_details)
                            },
                            {
                                'title': 'Category',
                                'value': '{}'.format(category)
                            },
                            {
                                'title': 'Spent at',
                                'value': '{}'.format(utils.get_formatted_datetime(expense['spent_at'], '%B %d, %Y'))
                            },
                            {
                                'title': 'Purpose',
                                'value': '{}'.format(expense['purpose'])
                            },
                            {
                                'title': 'Merchant',
                                'value': '{}'.format(expense['merchant'])
                            }
                        ]
                    }
                ]
            },
            {
                'type': 'Container',
                'items': [
                    {
                        'type': 'ActionSet',
                        'actions': [
                            {
                                'type': 'Action.OpenUrl',
                                'title': 'View in Fyle',
                                'url': '{}'.format(fyle_utils.get_fyle_resource_url(expense, 'EXPENSE'))
                            }
                        ]
                    }
                ],
                'style': 'default'
            }
        ],
        '$schema': 'http://adaptivecards.io/schemas/adaptive-card.json',
        'version': '1.4',
        'fallbackText': 'This card requires Adaptive Cards v1.2 support to be rendered properly.',
        'verticalContentAlignment': 'Center'
    }

    project = expense['project']

    if project is not None:
        project = expense['project']['name']
        sub_project = expense['project']['sub_project']

        if sub_project is not None:
            project = '{} / {}'.format(project, sub_project)

        project_section = {
            'title': 'Project',
            'value': project
        }

        expense_details_card['body'][1]['items'][0]['facts'].insert(1, project_section)

    return expense_details_card


def get_report_approval_state_section(report: Dict) -> Dict:
    is_report_fully_approved = True

    report_approved_by_section = []
    report_approved_by_section.append(
        {
            'type': 'TextBlock',
            'text': '**Approved by:**',
            'wrap': True
        }
    )

    report_approval_pending_from_section = []
    report_approval_pending_from_section.append(
        {
            'type': 'TextBlock',
            'text': '**Approval pending from:**',
            'wrap': True
        }
    )

    for approval in report['approvals']:
        approver_full_name = approval['approver_user']['full_name']
        approver_email = approval['approver_user']['email']

        if approval['state'] == 'APPROVAL_DONE':
            report_approved_by_section.append(
                {
                    'type': 'TextBlock',
                    'text': '{} ({})'.format(approver_full_name, approver_email),
                    'wrap': True
                }
            )

        if approval['state'] == 'APPROVAL_PENDING':
            report_approval_pending_from_section.append(
                {
                    'type': 'TextBlock',
                    'text': '{} ({})'.format(approver_full_name, approver_email),
                    'wrap': True
                }
            )
            is_report_fully_approved = False

    report_approval_state_section = {
        'type': 'Container',
        'items': [
            {
                'type': 'ColumnSet',
                'columns': [
                    {
                        'type': 'Column',
                        'width': 'stretch',
                        'items': report_approved_by_section
                    }
                ]
            }
        ],
        'style': 'emphasis',
        'bleed': True
    }

    if is_report_fully_approved is False:
        report_approval_state_section['items'][0]['columns'].append(report_approval_pending_from_section)


    return report_approval_state_section



def get_report_approved_card(report: Dict) -> Dict:

    headline_text = '✅   Your expense report [[{}]]({}) has been approved'.format(
        report['seq_num'],
        fyle_utils.get_fyle_resource_url(report, 'REPORT')
    )
    report_approved_card = get_report_details_card(report, headline_text)
    report_approval_state_section = get_report_approval_state_section(report)

    report_approved_card['body'][1]['items'].append(report_approval_state_section)

    return report_approved_card


def get_report_payment_processing_card(report: Dict) -> Dict:

    headline_text = '💰  Payment is being processed for your expense report [[{}]]({})'.format(
        report['seq_num'],
        fyle_utils.get_fyle_resource_url(report, 'REPORT')
    )
    report_payment_processing_card = get_report_details_card(report, headline_text)

    return report_payment_processing_card


def get_report_paid_card(report: Dict) -> Dict:

    headline_text = '💵  Reimbursement for your expense report [[{}]]({}) is here!'.format(
        report['seq_num'],
        fyle_utils.get_fyle_resource_url(report, 'REPORT')
    )
    report_paid_card = get_report_details_card(report, headline_text)

    return report_paid_card


def get_report_send_back_card(report: Dict, report_sendback_reason: str) -> Dict:

    headline_text = '🚫     {} ({}) sent back your expense report [[{}]]({})'.format(
        report['updated_by_user']['full_name'],
        report['updated_by_user']['email'],
        report['seq_num'],
        fyle_utils.get_fyle_resource_url(report, 'REPORT')
    )
    report_send_back_card = get_report_details_card(report, headline_text)

    report_sendback_reason = report_sendback_reason.replace('reason for sending back report: ', '')

    report_reason_section = {
        'type': 'Container',
        'style': 'warning',
        'bleed': True,
        'items': [
            {
                'type': 'TextBlock',
                'text': '**Reason for sending back report:**',
                'wrap': True
            },
            {
                'type': 'TextBlock',
                'text': report_sendback_reason,
                'wrap': True
            }
        ]
    }

    report_send_back_card['body'][1]['items'].insert(0, report_reason_section)

    return report_send_back_card


def get_report_commented_card(report: Dict, report_comment: str) -> Dict:

    headline_text = '💬  {} ({}) commented on your expense report [[{}]]({})'.format(
        report['updated_by_user']['full_name'],
        report['updated_by_user']['email'],
        report['seq_num'],
        fyle_utils.get_fyle_resource_url(report, 'REPORT')
    )
    report_commented_card = get_report_details_card(report, headline_text)

    report_reason_section = {
        'type': 'Container',
        'style': 'accent',
        'bleed': True,
        'items': [
            {
                'type': 'TextBlock',
                'text': '**Comment:**',
                'wrap': True
            },
            {
                'type': 'TextBlock',
                'text': report_comment,
                'wrap': True
            }
        ]
    }

    report_commented_card['body'][1]['items'].insert(0, report_reason_section)

    return report_commented_card


def get_expense_commented_card(expense: Dict, expense_comment: str) -> Dict:

    headline_text = '💬  {} ({}) commented on your expense [[{}]]({})'.format(
        expense['updated_by_user']['full_name'],
        expense['updated_by_user']['email'],
        expense['seq_num'],
        fyle_utils.get_fyle_resource_url(expense, 'EXPENSE')
    )

    expense_comment_card = get_expense_details_card(expense, headline_text)

    expense_comment_section = {
        'type': 'Container',
        'style': 'accent',
        'bleed': True,
        'separator': True,
        'items': [
            {
                'type': 'TextBlock',
                'text': '**Comment:**',
                'wrap': True
            },
            {
                'type': 'TextBlock',
                'text': expense_comment,
                'wrap': True
            }
        ]
    }

    expense_comment_card['body'][1]['items'].insert(0, expense_comment_section)

    return expense_comment_card
