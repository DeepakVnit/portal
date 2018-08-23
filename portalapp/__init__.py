from django.apps import AppConfig

class AutheticationAppConfig(AppConfig):
    name = "portalapp"
    label = "portalapp"
    verbose_name = "Authentication"

    def ready(self):
        import signals

default_app_config = "portalapp.AutheticationAppConfig"