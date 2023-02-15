from django.contrib import admin

from users.models import Location, User

# ----------------------------------------------------------------------------------------------------------------------
# Register models
admin.site.register(Location)
admin.site.register(User)
