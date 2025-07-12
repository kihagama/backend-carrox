import os
from django.core.wsgi import get_wsgi_application

# ✅ IMPORTANT: use the full dotted path relative to your project root
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

application = get_wsgi_application()
