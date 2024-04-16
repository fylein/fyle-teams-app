import asyncio
import json

from django.http import HttpResponse, HttpRequest
from django.http.response import JsonResponse
from django.views import View
from django.conf import settings
from django.utils.decorators import classonlymethod

from botbuilder.schema import Activity

from fyle_teams_app.bot import FyleBot
from fyle_teams_app.libs import logger


logger = logger.get_logger(__name__)


TEAMS_BOT_ADAPTER = settings.TEAMS_BOT_ADAPTER


class TeamsView(View):

    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        # pylint: disable=protected-access
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    async def post(self, request: HttpRequest) -> HttpResponse:
        """ Main request handler which handles all the request coming from Teams """

        if 'application/json' in request.headers['Content-Type']:
            body = json.loads(request.body.decode('utf-8'))
        else:
            return JsonResponse({}, status=415)

        logger.info('Request received from Teams -> %s', body)

        activity = Activity().deserialize(body)
        logger.info('Activity received from Teams -> %s', activity)

        auth_header = (
            request.headers['Authorization'] if 'Authorization' in request.headers else ''
        )
        logger.info('Auth header received from Teams -> %s', auth_header)

        try:
            response = await TEAMS_BOT_ADAPTER.process_activity(activity, auth_header, FyleBot().on_turn)
            logger.info('Response from Teams -> %s', response)

            if response:
                return JsonResponse(response.body, status=response.status)

            return JsonResponse({}, status=201)
        except Exception as exception:
            logger.error('Error occured while handling request')
            logger.error(exception)
            raise exception

        return JsonResponse({}, status=400)


class KubernetesView(View):

    def get(self, request: HttpRequest) -> HttpResponse:

        return JsonResponse({'message': 'teams service is ready'}, status=200)
