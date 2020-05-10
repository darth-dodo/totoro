import datetime
import logging

from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.viewsets import ViewSet

from external_services.api_clients.ghibli_api import ExternalAPIError
from movies.services import (
    MovieValueError,
    generate_list_movies_with_people,
    generate_movie_data_with_people,
)
from totoro_app import settings

logger = logging.getLogger(__name__)


class GhibliMovies(ViewSet):

    permission_classes = [AllowAny]

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request):

        try:
            api_data = generate_list_movies_with_people()
        except ValueError as e:
            bad_request_data = dict()
            bad_request_data["message"] = str(e)
            return Response(data=bad_request_data, status=HTTP_400_BAD_REQUEST)

        timestamp = datetime.datetime.isoformat(timezone.now())

        response_data = dict()
        response_data["api_data"] = api_data
        response_data["timestamp"] = timestamp

        return Response(response_data)

    @method_decorator(cache_page(settings.CACHE_TTL))
    def retrieve(self, request, pk=None):

        try:
            api_data = generate_movie_data_with_people(pk)

        except MovieValueError as e:
            data_not_found = dict()
            data_not_found["message"] = str(e)
            return Response(data=data_not_found, status=HTTP_404_NOT_FOUND)

        except ExternalAPIError as e:
            bad_request_data = dict()
            bad_request_data["message"] = str(e)
            return Response(data=bad_request_data, status=HTTP_400_BAD_REQUEST)

        timestamp = datetime.datetime.isoformat(timezone.now())

        response_data = dict()
        response_data["api_data"] = api_data
        response_data["timestamp"] = timestamp

        return Response(response_data)
