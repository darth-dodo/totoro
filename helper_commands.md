## Django Extensions
- `python manage.py runserver_plus`: Power Runserver
- `python manage.py runserver_plus --print-sql`: Power Runserver with SQL queries
- `python manage.py shell_plus --ipython`: Power Shell using ipython
- `python manage.py shell_plus --bpython`: Power Shell using bpython

## Pytest
- `pytest -v`: Run the test suite based on the settings defined in `pytest.ini`
- --x: Pytest to stop after the first test fail
- --nf: "new tests" first.
- --ff: "fail tests" first.
- --lf: only the "last fail"

## Caching
- Caching is done using Redis
- Redis database can be opened using `redis-cli -n 1`
- The keys can be viewed using `keys *`
- Use the command `FLUSHALL` to remove all the keys
