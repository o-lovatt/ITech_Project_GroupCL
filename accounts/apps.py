from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from .models import create_default_admin, create_default_guest
        create_default_admin()
        create_default_guest()

# from django.apps import AppConfig


# class AccountsConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    # name = 'accounts'
