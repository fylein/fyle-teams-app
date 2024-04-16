import enum
import logging

from typing import Dict, Tuple

from fyle.platform import Platform

from django.conf import settings

from fyle_teams_app.libs import http, assertions, utils, logger


logger = logger.get_logger(__name__)
logger.level = logging.INFO


FYLE_TOKEN_URL = '{}/oauth/token'.format(settings.FYLE_ACCOUNTS_URL)

class ReportState(enum.Enum):
    DRAFT = 'DRAFT'
    APPROVER_PENDING = 'APPROVER_PENDING'
    PAYMENT_PROCESSING = 'PAYMENT_PROCESSING'
    APPROVER_INQUIRY = 'APPROVER_INQUIRY'
    APPROVED = 'APPROVED'
    APPROVAL_DONE = 'APPROVAL_DONE'
    APPROVAL_DISABLED = 'APPROVAL_DISABLED'
    PAYMENT_PENDING = 'PAYMENT_PENDING'
    PAID = 'PAID'


class FyleResourceType(enum.Enum):
    REPORT = 'REPORT'
    EXPENSE = 'EXPENSE'


async def get_fyle_sdk_connection(refresh_token: str) -> Platform:
    access_token = await get_fyle_access_token(refresh_token)
    logger.info('Fetched Fyle access token %s', access_token)
    cluster_domain = await get_cluster_domain(access_token)
    logger.info('Fetched cluster domain %s', cluster_domain)

    FYLE_PLATFORM_URL = '{}/platform/v1'.format(cluster_domain)

    return Platform(
        server_url=FYLE_PLATFORM_URL,
        token_url=FYLE_TOKEN_URL,
        client_id=settings.FYLE_CLIENT_ID,
        client_secret=settings.FYLE_CLIENT_SECRET,
        refresh_token=refresh_token
    )


async def get_cluster_domain(access_token: str) -> str:
    cluster_domain_url = '{}/oauth/cluster'.format(settings.FYLE_ACCOUNTS_URL)
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token)
    }

    response = await http.post(url=cluster_domain_url, headers=headers)
    logger.info('Fetched cluster domain response %s', response.json())
    assertions.assert_valid(response.status == 200, 'Error fetching cluster domain')

    response = await response.json()

    return response['cluster_domain']


async def get_fyle_access_token(fyle_refresh_token: str) -> str:
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': fyle_refresh_token,
        'client_id': settings.FYLE_CLIENT_ID,
        'client_secret': settings.FYLE_CLIENT_SECRET
    }

    headers = {
        'Content-Type': 'application/json'
    }

    oauth_response = await http.post('{}/oauth/token'.format(settings.FYLE_ACCOUNTS_URL), json=payload, headers=headers)
    assertions.assert_good(oauth_response.status == 200, 'Error fetching fyle token details')

    oauth_response = await oauth_response.json()

    return oauth_response['access_token']


async def get_fyle_refresh_token(code: str) -> str:
    FYLE_OAUTH_TOKEN_URL = '{}/oauth/token'.format(settings.FYLE_ACCOUNTS_URL)

    oauth_payload = {
        'grant_type': 'authorization_code',
        'client_id': settings.FYLE_CLIENT_ID,
        'client_secret': settings.FYLE_CLIENT_SECRET,
        'code': code
    }

    oauth_response = await http.post(FYLE_OAUTH_TOKEN_URL, oauth_payload)
    assertions.assert_good(oauth_response.status == 200, 'Error fetching fyle token details')

    oauth_response = await oauth_response.json()

    return oauth_response['refresh_token']


async def get_fyle_profile(refresh_token: str) -> Dict:
    connection = await get_fyle_sdk_connection(refresh_token)
    fyle_profile_response = connection.v1beta.spender.my_profile.get()
    return fyle_profile_response['data']


def get_fyle_resource_url(resource: Dict, resource_type: str) -> str:

    RESOURCE_URL_MAPPING = {
        FyleResourceType.REPORT.value: '{}/app/main/#/reports'.format(settings.FYLE_APP_URL),
        FyleResourceType.EXPENSE.value: '{}/app/main/#/view_expense'.format(settings.FYLE_APP_URL)
    }

    resource_base_url = RESOURCE_URL_MAPPING[resource_type]
    resource_base_url = '{}/{}'.format(resource_base_url, resource['id'])

    resource_query_params = {
        'org_id': resource['org_id']
    }

    resource_url = utils.convert_to_branchio_url(resource_base_url, resource_query_params)

    return resource_url


def get_fyle_oauth_url(user_id: str, team_id: str) -> str:

    # State object to be used to identify which user is performing Fyle authorisation
    state_params = {
        'user_id': user_id,
        'team_id': team_id
    }

    # Encoding state to be passed in FYLE_OAUTH_URL
    base64_encoded_state = utils.encode_state(state_params)

    # This url redirects request to our server when Fyle authorisation is done
    redirect_uri = '{}/fyle/authorisation'.format(settings.TEAMS_SERVICE_BASE_URL)

    FYLE_OAUTH_URL = '{}/app/developers/#/oauth/authorize?client_id={}&response_type=code&state={}&redirect_uri={}'.format(
        settings.FYLE_APP_URL,
        settings.FYLE_CLIENT_ID,
        base64_encoded_state,
        redirect_uri
    )

    return FYLE_OAUTH_URL


def can_approve_report(report: Dict, approver_user_id: str) -> Tuple[bool, str]:

    report_approved_states = [
        ReportState.APPROVED.value,
        ReportState.PAYMENT_PENDING.value,
        ReportState.PAYMENT_PROCESSING.value,
        ReportState.PAID.value
    ]

    report_message = None
    can_approve_report = True

    if report['state'] == ReportState.APPROVER_INQUIRY.value:
        can_approve_report = False
        report_message = 'This expense report has been sent back to the employee'

    elif report['state'] in report_approved_states:
        can_approve_report = False
        report_message = 'This expense report has already been approved ✅ '

    elif can_approve_report is True:

        for approver in report['approvals']:

            if approver['approver_user_id'] == approver_user_id:

                if approver['state'] == ReportState.APPROVAL_DONE.value:
                    can_approve_report = False
                    report_message = 'Looks like you\'ve already approved this expense report 🙈'
                    break

                if approver['state'] == ReportState.APPROVAL_DISABLED.value:
                    can_approve_report = False
                    report_message = 'Looks like you no longer have permission to approve this expense report 🙈'
                    break

    return can_approve_report, report_message


def get_fyle_app_domain():
    fyle_app_url = settings.FYLE_APP_URL
    hostname = fyle_app_url.split('//')[1]
    domain = '.'.join(hostname.split('.')[1:])
    return domain
