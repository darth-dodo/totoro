from unittest import mock

import pytest

from movies.exceptions import MovieDoesNotExist, MultipleMoviesExist
from movies.services import (
    generate_list_movies_with_people,
    generate_movie_data_with_people,
)


class TestListMovieWithPeopleService:
    @pytest.fixture(autouse=True)
    def init_fixtures(self):
        pass

    @mock.patch(
        "external_services.api_clients.ghibli_api.GhibliAPIClient.get_movies",
        autospec=True,
    )
    @mock.patch(
        "external_services.api_clients.ghibli_api.GhibliAPIClient.get_people",
        autospec=True,
    )
    def test_generate_list_movies_with_people_success(
        self,
        mock_people_api_call,
        mock_movies_api_call,
        static_movies_data,
        static_people_data,
    ):
        mock_movies_api_call.return_value = static_movies_data
        mock_people_api_call.return_value = static_people_data

        service_response_data = generate_list_movies_with_people()

        assert len(service_response_data) == 1
        assert isinstance(service_response_data, list)
        response_data_element_keys = set(service_response_data[0].keys())
        ideal_response_keys = {
            "title",
            "release_date",
            "vehicles",
            "description",
            "producer",
            "locations",
            "rt_score",
            "species",
            "id",
            "people",
            "url",
            "director",
        }
        assert response_data_element_keys == ideal_response_keys

    @mock.patch(
        "external_services.api_clients.ghibli_api.GhibliAPIClient.get_movies",
        autospec=True,
    )
    @mock.patch(
        "external_services.api_clients.ghibli_api.GhibliAPIClient.get_people",
        autospec=True,
    )
    def test_generate_movie_data_with_people_success(
        self,
        mock_people_api_call,
        mock_movies_api_call,
        static_movies_data,
        static_people_data,
        static_data_movie_uuid,
    ):
        mock_movies_api_call.return_value = static_movies_data
        mock_people_api_call.return_value = static_people_data

        service_response = generate_movie_data_with_people(
            static_data_movie_uuid
        )
        assert isinstance(service_response, dict)

        ideal_response_keys = {
            "id",
            "title",
            "release_date",
            "url",
            "producer",
            "species",
            "locations",
            "vehicles",
            "people",
            "rt_score",
            "director",
            "description",
        }

        assert set(service_response.keys()) == ideal_response_keys

    @mock.patch(
        "external_services.api_clients.ghibli_api.GhibliAPIClient.get_movies",
        autospec=True,
    )
    @mock.patch(
        "external_services.api_clients.ghibli_api.GhibliAPIClient.get_people",
        autospec=True,
    )
    def test_generate_movie_data_with_people_fails_for_duplicate_uuid(
        self,
        mock_people_api_call,
        mock_movies_api_call,
        static_movies_data_with_duplicates,
        static_data_movie_uuid,
    ):

        mock_movies_api_call.return_value = static_movies_data_with_duplicates
        mock_people_api_call.return_value = []

        with pytest.raises(MultipleMoviesExist) as exc_info:
            generate_movie_data_with_people(static_data_movie_uuid)

        assert (
            str(exc_info.value)
            == "External API returned more than one movies for UUID 2baf70d1-42bb-4437-b551-e5fed5a87abe!"
        )

    @mock.patch(
        "external_services.api_clients.ghibli_api.GhibliAPIClient.get_movies",
        autospec=True,
    )
    @mock.patch(
        "external_services.api_clients.ghibli_api.GhibliAPIClient.get_people",
        autospec=True,
    )
    def test_generate_movie_data_with_people_fails_for_movie_uuid_does_exist(
        self,
        mock_people_api_call,
        mock_movies_api_call,
        static_data_movie_uuid,
    ):
        mock_movies_api_call.return_value = []
        mock_people_api_call.return_value = []

        with pytest.raises(MovieDoesNotExist) as exc_info:
            generate_movie_data_with_people(static_data_movie_uuid)

        assert (
            str(exc_info.value)
            == "Movie ID 2baf70d1-42bb-4437-b551-e5fed5a87abe not present in external API!"
        )
