import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

print("Creating migrations for exams app...")
call_command('makemigrations', 'exams', interactive=False, verbosity=2)
print("\n✓ Exams app migrations created successfully!")
