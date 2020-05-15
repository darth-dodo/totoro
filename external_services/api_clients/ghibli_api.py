import logging
import os

import requests
from requests.exceptions import RequestException

from external_services.exceptions import ExternalAPIError

logger = logging.getLogger(__name__)


class GhibliAPIClient:

    """
    Application layer API client over the Ghibli API


    - Wrapping all the external errors under `ExternalAPIError` and logging the actual error
    - Providing query params using **kwargs
    - Max Page size is locked to 250

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
        """
        Method to construct the query params and make the requests for fetching Movies data from External API

        :param kwargs: query params
        :return list: External API response
        """
        self.url = f"{self.base_url}{self.FILMS_URL}"
        self.method = "get"
        self.params = self._prepare_query_params(kwargs)

        self._make_request()

        return self.response.json()

    def get_people(self, **kwargs):
        """
        Method to construct the query params and make the requests for fetching People data from External API

        :param kwargs: query params
        :return list: External API response
        """

        self.url = f"{self.base_url}{self.PEOPLE_URL}"
        self.method = "get"
        self.params = self._prepare_query_params(kwargs)

        self._make_request()

        return self.response.json()

    def _make_request(self):
        """
        Private method for make the request using `requests` library

        - Log errors and raise `ExternalAPIError` in case of exceptions
        - Set the response attribute in case of success

        """
        try:
            self.response = requests.request(
                method=self.method,
                url=self.url,
                params=self.params,
                data=self.data,
            )

            logger.debug(f"Request URL: {self.response.url}")

            self.response.raise_for_status()

        # wrap all `requests` library error and serve as custom application error
        except RequestException as e:
            logger.error(e.__str__(), exc_info=True)
            raise ExternalAPIError(
                "Error while communication with External API"
            )

    def _prepare_query_params(self, query_kwargs):
        """
        Query params constructor
        - Takes in a dict of kwargs and builds out the query params for the request
        - Sets the `limit` query param to the Max Page size in case `limit` is not specified

        :param query_kwargs: dict of query params
        :return dict: query params for the request
        """
        query_params = dict()
        if query_kwargs.get("fields"):
            query_params["fields"] = query_kwargs["fields"]

        if query_kwargs.get("limit"):
            query_params["limit"] = query_kwargs["limit"]
        else:
            query_params["limit"] = self.MAX_PAGE_SIZE

        return query_params
