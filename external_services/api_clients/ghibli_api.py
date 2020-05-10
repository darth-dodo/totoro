import logging
import os

import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


class GhibliAPIClient:

    """

    Sample Usage:

    client = GhibliAPIClient()
    movies_fields = {"fields": "id,title,director,producer,release_date,url"}
    movies_data = client.get_movies(**movies_fields)

    people_fields = {"fields": "id,name,films"}
    people_data = client.get_people(**people_fields)
    """

    FILMS_URL = "films/"
    PEOPLE_URL = "people/"
    MAX_PAGE_SIZE = 250

    def __init__(self):
        self.base_url = os.getenv("GHIBLI_API_BASE_URL")

        self.url = None
        self.params = None
        self.data = None
        self.method = "head"

    def get_movies(self, **kwargs):
        self.url = f"{self.base_url}{self.FILMS_URL}"
        self.method = "get"
        self.params = self._prepare_query_params(kwargs)

        self._make_request()

        return self.response.json()

    def get_people(self, **kwargs):
        self.url = f"{self.base_url}{self.PEOPLE_URL}"
        self.method = "get"
        self.params = self._prepare_query_params(kwargs)

        self._make_request()

        return self.response.json()

    def _make_request(self):
        try:
            self.response = requests.request(
                method=self.method,
                url=self.url,
                params=self.params,
                data=self.data,
            )
            print(f"Request {self.response.url}")
            self.response.raise_for_status()

        # wrap all `requests` library error and server as custom application error
        except RequestException as e:
            logger.error(e.__str__(), exc_info=True)
            raise ValueError("Error while communication with external API")

    def _prepare_query_params(self, query_kwargs):
        query_params = dict()
        if query_kwargs.get("fields"):
            query_params["fields"] = query_kwargs["fields"]

        if query_kwargs.get("limit"):
            query_params["limit"] = query_kwargs["limit"]
        else:
            query_params["limit"] = self.MAX_PAGE_SIZE

        return query_params
