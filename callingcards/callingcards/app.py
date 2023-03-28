from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'callingcards'

    def ready(self):
        import callingcards.db_signals  # noqa
