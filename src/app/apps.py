from django.apps import AppConfig

class AppConfigName(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'  # ✅ MUST match your import path!
