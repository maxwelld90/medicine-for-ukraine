from django.apps import AppConfig


class ApiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "Medicine for Ukraine"
    name = 'api_app'