# totoro

# Application Details
- Environment Management using `pyenv` and `poetry`
- Precommit hooks using `precommit` and code autoformatting using `black`
- Python 3.7 and Django 2.2 web application
- 12 Factor environment variables using Django Configuration
- API using Django REST Framework
- API documentation interface using OpenAPI 2 and Swagger
- Model View Controller Service architecture paradigm
- Service layer for storing the Business logic
- Caching using Redis
- Test cases using Pytest and Unittest Mock
- Exception Management through Sentry
- Containerization using Docker
- Please check the `Makefile` for more detailed commands


# Setup
- Run the command `make create-env-vars-from-template` to copy the env vars from `.env.template`
- Use the command `make docker-totoro-server` or `docker-detached-totoro-server` to run the server


# Roadmap
- Setup Python environment - *(SHA: e64dbf1bba7dc32d7a4473f46bc58380b473d83b)*
    - Python 3
    - Poetry
    - Precommit hooks
    - AutoPEP8 formatting
- Django 2.2 LTS setup - *(SHA: 7a01b066309d2e5b790d1dfd1fcb744d421a335a)*
    - Django Extensions
    - Django Configuration for environment variables management
    - Django REST Framework
    - Pytest and Django Pytest (Dev Environment)
    - Django Debug toolbar (Dev Environment)
    - Django YASG for Swagger Documentation
- Movies barebones API - *(SHA: 4632ba44e2b27b3feb73596297efb3dc0a1df321)*
- Caching API response - *(SHA: 6c708c57cdf9a0a24de097a37378760ccca11264)*
- Facade Pattern: API client over Ghibli API - *(SHA: 6958462601566cad91ff3374639e1d35f426d660)*
- Plug in external API response inside Movies API - *(SHA: 59a4c0852e5168f6e0feb2a298ea141cac1383c5)*
- Refactor Services - *(SHA: 79bbd7b30339ba967c57ac69e84f221f913aacc9)*
- Application Exceptions - *(SHA: 79bbd7b30339ba967c57ac69e84f221f913aacc9)*
- Test Suite - *(SHA: 982c1eeb827fb1938bab519d89a7dcb557578c1c)*
- Exception Management Using Sentry - *(SHA: f45e5c7719dc337e9a7e4c2f76e7fee337f4e9c6)*
- Dockerization - *(SHA: 8b9c13f5d89fa0979c16e1276be8e0574a606165)*
- Documentation

# Note:
- **Currently, since there the external data set is very small, there is no pagination implemented on  the application level**
- **Pagination in not available in the External API provided in the requirements which leads to downloading all the data and then merging the results in memory**


---

# Development Environment

## Simple
- Poetry is used for environment management
- Using Precommit hooks to run checks before issuing a commit
- Using Black for code autoformatting. [PEP8 guidelines are a subset of Black](https://www.mattlayman.com/blog/2018/python-code-black/)
- Copy the `.poetry.env.template` to `.poetry.env` for using environment variables
- Load the environment variables using `source .poetry.env`
- Check out the `Makefile` for the list of commands

## Docker
- `.env` is used for loading the environment variables in the Docker container
- Use the command `make docker-totoro-server` or `docker-detached-totoro-server` to run the server


# API documentation

## Notes
- The API successful response data is present using the following structure
```
{
    api_data: <result-data>,
    timestamp: <utc timestamp>
}
```
- The timestamp can used to confirm that the API response is cached for 1 minute as the timestamp value remains the same for API calls done after the response is cached.

## API endpoints
- `http://localhost:8000/movies/` will return a list of all the movies
- `http://localhost:8000/movies/2baf70d1-42bb-4437-b551-e5fed5a87abe/` will return details of a particular movie

## OpenAPI interface
- The homepage `localhost:8000` provides the Swagger interface
- `localhost:8000/redoc/` provides the Redoc interface


---

# Next Steps
- Implementing pagination
- Write Serializer for representing the data
- Adding retries and backoff mechanisms when the external API requests are failing
- API throttling to prevent DDoS attacks using DRF throttle classes
- Enable CORS
- More structured logging
- More detailed test cases for the controller layer
- Implement type checks using `mypy` for making the codebase more robust
- Integrate a persistent datastore (Postgres) is required
- Class Base Services for consistent interfacing and extendibility
