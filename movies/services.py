import logging

from external_services.api_clients.ghibli_api import GhibliAPIClient

logger = logging.getLogger(__name__)


def fetch_all_movies():
    client = GhibliAPIClient()
    movies_fields = {"fields": "id,title,director,producer,release_date,url"}
    movies_data = client.get_movies(**movies_fields)
    return movies_data


def fetch_all_people():
    client = GhibliAPIClient()
    people_fields = {"fields": "id,name,films,url"}
    people_data = client.get_people(**people_fields)
    return people_data


def generate_list_of_films_with_people(filter_movies_uuid=[]):
    movies_data = fetch_all_movies()
    people_data = fetch_all_people()

    if not isinstance(filter_movies_uuid, list):
        filter_movies_uuid = [filter_movies_uuid]

    if filter_movies_uuid:
        movies_data_by_url_dict = {
            current_movie["url"]: current_movie for current_movie in movies_data if current_movie["id"] in filter_movies_uuid
        }
    else:
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
                logger.info("Person movie is not present in all movies")
                continue

            movie_people = movie_people_mapping.get(movie_url, [])
            movie_people.append(person)
            movie_people_mapping[movie_url] = movie_people

    # movies with no people have an empty array against the people key
    for movie_url, movie_info in movies_data_by_url_dict.items():
        movie_people = movie_people_mapping.get(movie_url, [])
        movie_info["people"] = movie_people
        movies_data_by_url_dict[movie_url] = movie_info

    return list(movies_data_by_url_dict.values())
