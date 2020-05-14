import logging

from external_services.api_clients.ghibli_api import GhibliAPIClient
from movies.exceptions import (
    DataMappingError,
    MovieDoesNotExist,
    MultipleMoviesExist,
)

logger = logging.getLogger(__name__)


# application facing services


def generate_list_movies_with_people():
    movies_data = _fetch_all_movies()
    people_data = _fetch_all_people()

    response_data = _merge_movies_data_with_people_data(
        movies_data, people_data
    )

    return response_data


def generate_movie_data_with_people(movie_uuid):
    movie_data = _fetch_movie_data(movie_uuid)
    people_data = _fetch_all_people()

    merged_data = _merge_movies_data_with_people_data(movie_data, people_data)

    if len(merged_data) != 1:
        raise DataMappingError("Movies and People Data Mapping Error!")

    return merged_data[0]


# "private" helpers


def _fetch_all_movies():
    client = GhibliAPIClient()
    movies_fields = {"fields": "id,title,director,producer,release_date,url"}
    movies_data = client.get_movies(**movies_fields)
    return movies_data


def _fetch_all_people():
    client = GhibliAPIClient()
    people_fields = {"fields": "id,name,films,url"}
    people_data = client.get_people(**people_fields)
    return people_data


def _fetch_movie_data(movie_uuid):
    all_movies_data = _fetch_all_movies()
    movie_data = [
        movie_data
        for movie_data in all_movies_data
        if movie_data["id"] == movie_uuid
    ]

    if not movie_data:
        raise MovieDoesNotExist(
            f"Movie ID {movie_uuid} not present in external API!"
        )

    if len(movie_data) > 1:
        raise MultipleMoviesExist(
            f"External API returned more than one movies for UUID {movie_uuid}!"
        )

    return movie_data


def _merge_movies_data_with_people_data(movies_data, people_data):
    response_data = dict()

    if not movies_data:
        return response_data

    movies_data_by_url_dict = {
        current_movie["url"]: current_movie for current_movie in movies_data
    }

    all_movie_urls = list(movies_data_by_url_dict.keys())

    """
    - iterate over the people
    - if the movie url is present in all movies, attach the people in a new dict across the movie
    - at the end of the loop, merge the OG movies dict and the movie_people dict
    """

    movie_people_mapping = dict()

    for person in people_data:

        person_movie_urls = person["films"]

        for movie_url in person_movie_urls:

            if movie_url not in all_movie_urls:
                continue

            movie_people = movie_people_mapping.get(movie_url, [])
            movie_people.append(person)
            movie_people_mapping[movie_url] = movie_people

    # movies with no people have an empty array against the people key
    for movie_url, movie_info in movies_data_by_url_dict.items():
        movie_people = movie_people_mapping.get(movie_url, [])
        movie_info["people"] = movie_people
        movies_data_by_url_dict[movie_url] = movie_info

    response_data = list(movies_data_by_url_dict.values())

    return response_data
