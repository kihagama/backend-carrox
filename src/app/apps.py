from django.apps import AppConfig

class AppConfigName(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.app'  # ✅ MUST match your import path!
