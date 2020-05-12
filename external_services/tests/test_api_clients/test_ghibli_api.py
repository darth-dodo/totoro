import pytest

from external_services.exceptions import ExternalAPIError


class TestGhibliAPI:
    @pytest.fixture(autouse=True)
    def init_fixtures(self, ghibli_api_client):
        self.client = ghibli_api_client

    def test_get_movies_success(self):
        movies_response = self.client.get_movies()
        assert len(movies_response) == 20
        assert isinstance(movies_response, list)
        first_movie = movies_response[0]
        assert isinstance(first_movie, dict)

    def test_get_movies_response_keys(self):
        movies_response = self.client.get_movies()
        first_movie = movies_response[0]

        ideal_response_keys_set = {
            "director",
            "rt_score",
            "title",
            "people",
            "locations",
            "vehicles",
            "url",
            "id",
            "producer",
            "description",
            "release_date",
            "species",
        }

        assert set(first_movie.keys()) == ideal_response_keys_set

    def test_max_limit_query_param_for_movies(self):
        query_params = dict()
        query_params["limit"] = 1

        movies_response = self.client.get_movies(**query_params)

        assert len(movies_response) == 1

    def test_response_keys_query_param_for_movies(self):
        query_params = dict()
        query_params["fields"] = "id,url,title"

        movies_response = self.client.get_movies(**query_params)
        first_movie = movies_response[0]

        ideal_response_keys_set = {"id", "url", "title"}
        assert set(first_movie.keys()) == ideal_response_keys_set

    def test_external_api_error_due_to_invalid_request_for_get_movies(
        self, monkeypatched_bad_url_client
    ):

        with pytest.raises(ExternalAPIError):
            monkeypatched_bad_url_client.get_movies()

    def test_get_people_success(self):
        people_response = self.client.get_people()
        assert len(people_response) == 31
        assert isinstance(people_response, list)
        first_person = people_response[0]
        assert isinstance(first_person, dict)

    def test_get_people_response_keys(self):
        people_response = self.client.get_people()
        first_person = people_response[0]

        ideal_response_keys_set = {
            "eye_color",
            "gender",
            "films",
            "age",
            "id",
            "url",
            "hair_color",
            "name",
            "species",
        }

        assert set(first_person.keys()) == ideal_response_keys_set

    def test_max_limit_query_param_for_people(self):
        query_params = dict()
        query_params["limit"] = 1

        people_response = self.client.get_people(**query_params)

        assert len(people_response) == 1

    def test_response_keys_query_param_for_people(self):
        query_params = dict()
        query_params["fields"] = "id,url,name"

        people_response = self.client.get_people(**query_params)
        first_person = people_response[0]

        ideal_response_keys_set = {"id", "url", "name"}
        assert set(first_person.keys()) == ideal_response_keys_set

    def test_external_api_error_due_to_invalid_request_for_get_people(
        self, monkeypatched_bad_url_client
    ):
        with pytest.raises(ExternalAPIError):
            monkeypatched_bad_url_client.get_people()
