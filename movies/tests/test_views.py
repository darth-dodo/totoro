import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK


class TestMoviesViewSet:
    @pytest.fixture(autouse=True)
    def init_fixtures(self, db, api_client, settings):
        self.api_client = api_client
        self.list_url = reverse("movies:movies-list")

    def test_list_page_successful_response(self):

        response = self.api_client.get(self.list_url)

        response_json = response.json()
        test_data = {f"key_{i}": i * i for i in range(1, 10)}
        del response_json["timestamp"]

        assert set(response_json.keys()) == set(test_data.keys())
        assert set(response_json.values()) == set(test_data.values())
        assert response.status_code == HTTP_200_OK
