import logging

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

logger = logging.getLogger(__name__)


class GhibliMovies(ViewSet):

    permission_classes = [AllowAny]

    def list(self, request):
        logger.info("Making the request!")
        response_data = {f"key_{i}": i * i for i in range(1, 10)}
        return Response(response_data)
