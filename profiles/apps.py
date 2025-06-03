from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'
    
    def ready(self):
        # Register the custom user model
        from django.contrib import auth
        auth.get_user_model()
