import pytest

from external_services.api_clients.ghibli_api import GhibliAPIClient


@pytest.fixture
def ghibli_api_client():
    return GhibliAPIClient()


@pytest.fixture
def monkeypatched_bad_url_client(monkeypatch):
    monkeypatch.setenv("GHIBLI_API_BASE_URL", "")
    return GhibliAPIClient()
