import csv
import os

import django
from django.apps import apps

from Homework_28_PD12.settings import BASE_DIR

CAT_PATH = os.path.join(BASE_DIR, 'ads', 'data', 'category.csv')
LOC_PATH = os.path.join(BASE_DIR, 'users', 'data', 'location.csv')
US_PATH = os.path.join(BASE_DIR, 'users', 'data', 'user.csv')
ADS_PATH = os.path.join(BASE_DIR, 'ads', 'data', 'ad.csv')

# ----------------------------------------------------------------------------------------------------------------------
# Setup env settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Homework_28_PD12.settings')
django.setup()

# ----------------------------------------------------------------------------------------------------------------------
# Add models
Category = apps.get_model('ads', 'Category')
Location = apps.get_model('users', 'Location')
User = apps.get_model('users', 'User')
Ad = apps.get_model('ads', 'Ad')

# ----------------------------------------------------------------------------------------------------------------------
# Write data from file to database
with open(CAT_PATH, encoding="utf-8") as f:
    data = csv.DictReader(f)

    for row in data:
        Category.objects.create(name=row.get('name'))

# ----------------------------------------------------------------------------------------------------------------------
# Write data from file to database
with open(LOC_PATH, encoding="utf-8") as f:
    data = csv.DictReader(f)

    for row in data:
        location = {"name": row.get('name').split(",")[0].strip(),
                    "lat": row.get('lat'),
                    "lng": row.get('lng')
                    }
        Location.objects.create(**location)

        location = {"name": row.get('name').split(",")[1].strip(),
                    "lat": row.get('lat'),
                    "lng": row.get('lng')
                    }
        Location.objects.create(**location)

# ----------------------------------------------------------------------------------------------------------------------
# Write data from file to database
with open(US_PATH, encoding="utf-8") as f:
    data = csv.DictReader(f)

    for row in data:
        data = {"first_name": row.get('first_name'),
                "last_name": row.get('last_name'),
                "username": row.get('username'),
                "password": row.get('password'),
                "role": row.get('role'),
                "age": row.get('age'),
                # "locations_id": row.get('location_id'),
                }
        User.objects.create(**data)

# ----------------------------------------------------------------------------------------------------------------------
# Write data from file to database
with open(ADS_PATH, encoding="utf-8") as f:
    data = csv.DictReader(f)

    for row in data:
        is_published = True if row.get('is_published') == "TRUE" else False
        data = {"name": row.get('name'),
                "author_id": row.get('author_id'),
                "price": row.get('price'),
                "description": row.get('description'),
                "is_published": is_published,
                "image": row.get('image'),
                "category_id": row.get('category_id'),
                }

        Ad.objects.create(**data)

# ----------------------------------------------------------------------------------------------------------------------
# Success message
print("Success")
