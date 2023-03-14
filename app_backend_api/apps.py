from django.apps import AppConfig

class AppBackendApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_backend_api'

    def ready(self):
        import app_backend_api.signals

