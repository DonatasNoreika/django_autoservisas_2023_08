from django.apps import AppConfig


class AutoserviceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autoservice'

    def get_model(self, model_name, require_ready=True):
        from .signals import create_profile, save_profile


