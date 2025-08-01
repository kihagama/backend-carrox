import os
import sys
sys.path.append('/opt/render/project/src')  # Add src/ to Python path
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')  # Use src.api.settings
application = get_wsgi_application()