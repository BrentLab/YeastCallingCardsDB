# yeast_cc_db

[![Build Status](https://travis-ci.org/cmatkhan/yeast_cc_db.svg?branch=master)](https://travis-ci.org/cmatkhan/yeast_cc_db)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

A database of Scerevisiae calling cards data. Check out the project's [documentation](http://cmatkhan.github.io/yeast_cc_db/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)

# Initialize the project

Start the dev server for local development:

```bash
docker-compose up
```

Create a superuser to login to the admin:

```bash
docker-compose run --rm web ./manage.py createsuperuser
```
