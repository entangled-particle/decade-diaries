"""
WSGI config for decadediaries project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Ensure the project root is on PYTHONPATH when running in Vercel.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'decadediaries.settings')

application = get_wsgi_application()

# Vercel's Python runtime commonly looks for `app`.
app = application
