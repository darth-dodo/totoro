from unittest import mock

import pytest

from movies.services import generate_list_movies_with_people


class TestListMovieWithPeopleService:
    @pytest.fixture(autouse=True)
    def init_fixtures(self):
        pass

    @mock.patch(
        "external_services.api_clients.ghibli_api.GhibliAPIClient.get_movies"
    )
    @mock.patch(
        "external_services.api_clients.ghibli_api.GhibliAPIClient.get_people"
    )
    def test_list_service(
        self,
        mocked_people,
        mocked_movies,
        static_people_data,
        static_movies_data,
    ):
        mocked_movies.return_value = static_movies_data

        mocked_people.return_value = static_people_data

        response_data = generate_list_movies_with_people()

        assert len(response_data) == 1
        response_data_element_keys = set(response_data[0].keys())
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
