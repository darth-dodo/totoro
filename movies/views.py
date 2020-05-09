import datetime
import logging

from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from movies.services import generate_list_of_films_with_people
from totoro_app import settings

logger = logging.getLogger(__name__)


class GhibliMovies(ViewSet):

    permission_classes = [AllowAny]

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request):
        api_data = generate_list_of_films_with_people()
        timestamp = datetime.datetime.isoformat(timezone.now())
        response_data = dict()
        response_data["api_data"] = api_data
        response_data["timestamp"] = timestamp
        return Response(response_data)

    @method_decorator(cache_page(settings.CACHE_TTL))
    def retrieve(self, request, pk=None):
        api_data = generate_list_of_films_with_people(filter_movies_uuid=pk)
        timestamp = datetime.datetime.isoformat(timezone.now())
        response_data = dict()
        response_data["api_data"] = api_data
        response_data["timestamp"] = timestamp
        return Response(response_data)
