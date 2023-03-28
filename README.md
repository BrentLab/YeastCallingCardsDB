# yeast_cc_db

[![Tests](https://github.com/BrentLab/YeastCallingCardsDB/actions/workflows/build-and-test.yaml/badge.svg)](https://github.com/BrentLab/YeastCallingCardsDB/actions/workflows/build-and-test.yaml)
[![Coverage](https://img.shields.io/codecov/c/github/BrentLab/YeastCallingCardsDB?label=Coverage&logo=codecov)](https://codecov.io/gh/BrentLab/YeastCallingCardsDB)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

A database of Scerevisiae calling cards data. Check out the project's [documentation](http://cmatkhan.github.io/yeast_cc_db/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```
# Notes for later

I removed the `nose` test runner entirely. I did this by adding django-pytest, 
changing the local config to this:

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ('pytest_django',)
    TEST_RUNNER = 'callingcards.PytestTestRunner.PytestTestRunner'
    # settings for pytest
    # create a pytest.ini file in your project root directory and add the following content
    # [pytest]
    # addopts = --cov=callingcards --cov-report=html

[and adding the script per these instructions](https://pytest-django.readthedocs.io/en/latest/faq.html#how-can-i-use-manage-py-test-with-pytest-django)

note the pytest.ini in this package of course.

I then rmeoved all the nose imports from the test scripts and replaced them with 
assert statements for pytest and removed nose from the dependencies

# some additional deps

django-extensions added

add to config/common `INSTALLED_APPS` 'django_extensions

which makes this work easily:

```bash
poetry run python manage.py shell_plus --ipython
```

and can get a jupyter interface working, too