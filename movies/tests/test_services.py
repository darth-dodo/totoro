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
    def test_list_service(self, mocked_people, mocked_films):
        mocked_films.return_value = [
            {
                "id": "2baf70d1-42bb-4437-b551-e5fed5a87abe",
                "title": "Castle in the Sky",
                "description": "The orphan Sheeta inherited a mysterious crystal that links her to the mythical sky-kingdom of Laputa. With the help of resourceful Pazu and a rollicking band of sky pirates, she makes her way to the ruins of the once-great civilization. Sheeta and Pazu must outwit the evil Muska, who plans to use Laputa's science to make himself ruler of the world.",
                "director": "Hayao Miyazaki",
                "producer": "Isao Takahata",
                "release_date": "1986",
                "rt_score": "95",
                "people": ["https://ghibliapi.herokuapp.com/people/"],
                "species": [
                    "https://ghibliapi.herokuapp.com/species/af3910a6-429f-4c74-9ad5-dfe1c4aa04f2"
                ],
                "locations": ["https://ghibliapi.herokuapp.com/locations/"],
                "vehicles": ["https://ghibliapi.herokuapp.com/vehicles/"],
                "url": "https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe",
            }
        ]

        mocked_people.return_value = [
            {
                "id": "40c005ce-3725-4f15-8409-3e1b1b14b583",
                "name": "Colonel Muska",
                "gender": "Male",
                "age": "33",
                "eye_color": "Grey",
                "hair_color": "Brown",
                "films": [
                    "https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe"
                ],
                "species": "https://ghibliapi.herokuapp.com/species/af3910a6-429f-4c74-9ad5-dfe1c4aa04f2",
                "url": "https://ghibliapi.herokuapp.com/people/40c005ce-3725-4f15-8409-3e1b1b14b583",
                "length": None,
            }
        ]

        data = generate_list_movies_with_people()
        import bpdb

        bpdb.set_trace()
