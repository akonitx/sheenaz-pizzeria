from django.apps import AppConfig


class MenuConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "menu"

    def ready(self):
        from menu.signals import remove_session, add_session
        from django.contrib.auth import user_logged_in, user_logged_out
        from django.contrib.auth.models import User

        user_logged_in.connect(add_session, sender=User)
        user_logged_out.connect(remove_session, sender=User)
