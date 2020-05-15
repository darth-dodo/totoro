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
    """
    Service used to fetch all the movies and people data

    - interacts with the external movies API
    - interacts with the external people API
    - merge the data

    :return response_data list: Response Data
    """
    movies_data = _fetch_all_movies()
    people_data = _fetch_all_people()

    response_data = _merge_movies_data_with_people_data(
        movies_data, people_data
    )

    return response_data


def generate_movie_data_with_people(movie_uuid):
    """
    Service used to generate the data for a single movie or raise DataMapping Error

    - Fetch Movie data or raise Exception
    - Merge the Movie data with People data
    - Return the Response

    :param movie_uuid str: External Service Movie UUID
    :return dict: Response Data
    """
    movie_data = _fetch_movie_data(movie_uuid)
    people_data = _fetch_all_people()

    merged_data = _merge_movies_data_with_people_data(movie_data, people_data)

    if len(merged_data) != 1:
        raise DataMappingError("Movies and People Data Mapping Error!")

    return merged_data[0]


# "private" helpers


def _fetch_all_movies():
    """
    Helper function to interact with External API client and ask for selective result fields
    :return: Movies data as returned by the external client
    """
    client = GhibliAPIClient()
    movies_fields = {"fields": "id,title,director,producer,release_date,url"}
    movies_data = client.get_movies(**movies_fields)
    return movies_data


def _fetch_all_people():
    """
    Helper function to interact with External API client and ask for selective result fields
    :return: People data as returned by the external client
    """
    client = GhibliAPIClient()
    people_fields = {"fields": "id,name,films,url"}
    people_data = client.get_people(**people_fields)
    return people_data


def _fetch_movie_data(movie_uuid):
    """
    Helper function to interact with External API client and ask for a particular movie
    - Raise `MovieDoesNotExist` in case the movie is not present in the external provider response
    - Raise `MultipleMoviesExist` in case the result set from external client as duplicate values across a single UUID

    :return: Movie data as returned by the external client
    """

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
    """
    Helper function to merge responses of people and movies data

    :param movies_data dict: Response data from helper function
    :param people_data dict: Response data from helper function
    :return response_data: Movies and People merged data
    """
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
