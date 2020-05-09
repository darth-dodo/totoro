import datetime
import logging

import pytz
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from totoro_app import settings

logger = logging.getLogger(__name__)


class GhibliMovies(ViewSet):

    permission_classes = [AllowAny]

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request):
        logger.info("Making the request!")
        response_data = {f"key_{i}": i * i for i in range(1, 10)}
        response_data["timestamp"] = datetime.datetime.isoformat(
            datetime.datetime.now(tz=pytz.timezone("Europe/Berlin")))
        return Response(response_data)
