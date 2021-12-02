import asyncio
import json

from django.http import HttpResponse, HttpRequest
from django.http.response import JsonResponse
from django.views import View
from django.conf import settings
from django.utils.decorators import classonlymethod

from botbuilder.schema import Activity
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    BotFrameworkAdapter,
)

from fyle_teams_app.bot import FyleBot
from fyle_teams_app.libs import logger


logger = logger.get_logger(__name__)


SETTINGS = BotFrameworkAdapterSettings(app_id=settings.TEAMS_APP_ID, app_password=settings.TEAMS_APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)


ADAPTER.on_turn_error = FyleBot.on_error


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
            print('BODY -> ', body)
        else:
            return JsonResponse({}, status=415)

        activity = Activity().deserialize(body)
        auth_header = (
            request.headers['Authorization'] if 'Authorization' in request.headers else ''
        )


        try:
            response = await ADAPTER.process_activity(activity, auth_header, FyleBot().on_turn)

            if response:
                return JsonResponse(response.body, status=response.status)

            return JsonResponse({}, status=201)
        except Exception as exception:
            logger.error('Error occured while handling request')
            logger.error(exception)
            raise exception

        return JsonResponse({}, status=400)
