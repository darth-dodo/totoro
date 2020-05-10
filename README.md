# totoro

# Feature List
- Python 3 Django Application with DRF
- Ghibli API client for making external API requests
- Response caching with TTL of 1 minute
- Test Cases

# Roadmap
- Setup Python environment
    - Python 3
    - Poetry
    - Precommit hooks
    - AutoPEP8 formatting
- Django 2.2 LTS setup
    - Django Extensions
    - Django Configuration for environment variables management
    - Django REST Framework
    - Pytest and Django Pytest (Dev Environment)
    - Django Debug toolbar (Dev Environment)
    - Django YASG for Swagger Documentation
- Movies barebones API
- Caching API response
- Facade API client over Ghibli API
- Plug in external API response inside Movies API
- Structured Logging
- Exception Management Using Sentry


# Development Environment
- Poetry is used for environment management
- Using Precommit hooks to run checks before issuing a commit
- Using Black for code autoformatting. [PEP8 guidelines are a subset of Black](https://www.mattlayman.com/blog/2018/python-code-black/)
