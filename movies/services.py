from external_services.api_clients.ghibli_api import GhibliAPIClient


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


def generate_list_of_films_with_people():
    movies_data = fetch_all_movies()
    people_data = fetch_all_people()

    movies_data_by_url_dict = {
        current_movie["url"]: current_movie for current_movie in movies_data}

    all_movies_urls = set(movies_data_by_url_dict.keys())

    for person in people_data:
        person_movies_set = set(person["films"])
        print(all_movies_urls)
        print(person_movies_set)

        if not person_movies_set.intersection(all_movies_urls):
            print("This person is not present in any of the movies")
            continue

        print("Intersection found!")
        print(person_movies_set.intersection(all_movies_urls))

        for current_movie in person_movies_set:
            current_movie_details = movies_data_by_url_dict.get(current_movie)
            current_movie_people = current_movie_details.get("people", [])
            current_movie_people.append(person)

            current_movie_details["people"] = current_movie_people
            movies_data_by_url_dict[current_movie] = current_movie_details

    # convert the movies from key value to list
    movies_data = list(movies_data_by_url_dict.values())

    return movies_data
