import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
print("Creating migrations for authentication app...")
call_command('makemigrations', 'authentication', interactive=False, verbosity=2)
print("\n✓ Authentication migrations created!")
