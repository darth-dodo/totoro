from unittest import mock

import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK


class TestMoviesViewSet:
    @pytest.fixture(autouse=True)
    def init_fixtures(self, db, api_client, static_data_movie_uuid):
        self.api_client = api_client
        self.list_url = reverse("movies:movies-list")
        self.retrieve_url = reverse(
            "movies:movies-detail", kwargs={"pk": static_data_movie_uuid}
        )

    @mock.patch(
        "external_services.api_clients.ghibli_api.GhibliAPIClient.get_movies",
        autospec=True,
    )
    @mock.patch(
        "external_services.api_clients.ghibli_api.GhibliAPIClient.get_people",
        autospec=True,
    )
    def test_list_page_successful_response(
        self,
        mock_people_api_call,
        mock_movies_api_call,
        static_movies_data,
        static_people_data,
    ):

        mock_movies_api_call.return_value = static_movies_data
        mock_people_api_call.return_value = static_people_data

        response = self.api_client.get(self.list_url)

        response_json = response.json()

        response_api_data = response_json["api_data"]

        assert isinstance(response_api_data, list)
        assert len(response_api_data) == 1

        assert response.status_code == HTTP_200_OK

    @mock.patch(
        "external_services.api_clients.ghibli_api.GhibliAPIClient.get_movies",
    )
    @mock.patch(
        "external_services.api_clients.ghibli_api.GhibliAPIClient.get_people",
    )
    def test_detail_page_successful_response(
        self,
        mock_people_api_call,
        mock_movies_api_call,
        static_movies_data,
        static_people_data,
        static_data_movie_uuid,
    ):

        mock_movies_api_call.return_value = static_movies_data
        mock_people_api_call.return_value = static_people_data

        response = self.api_client.get(self.retrieve_url)

        response_json = response.json()

        response_api_data = response_json["api_data"]
        assert response_api_data["id"] == static_data_movie_uuid

        assert isinstance(response_api_data, dict)
        assert response.status_code == HTTP_200_OK
