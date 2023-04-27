import os
from .common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True

    INTERNAL_IPS = ['127.0.0.1']

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ('pytest_django',)
    MIDDLEWARE = Common.MIDDLEWARE
    TEST_RUNNER = 'callingcards.PytestTestRunner.PytestTestRunner'
    # settings for pytest
    # create a pytest.ini file in your project root directory and add the following content
    # [pytest]
    # addopts = --cov=callingcards --cov-report=html

    # Mail
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # Database
    # https://docs.djangoproject.com/en/4.1/ref/settings/#databases

    DATABASES = {
        'default': {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR + "/test.sqlite",
        }
    }

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/
    # http://django-storages.readthedocs.org/en/latest/index.html
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
    }
