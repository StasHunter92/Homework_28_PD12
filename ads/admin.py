from django.contrib import admin

from ads.models import Ad, Category

# ----------------------------------------------------------------------------------------------------------------------
# Register models
admin.site.register(Ad)
admin.site.register(Category)
