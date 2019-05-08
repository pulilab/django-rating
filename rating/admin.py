from django.contrib import admin
from .models import ObjectRating


class ObjectRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type']


admin.site.register(ObjectRating, ObjectRatingAdmin)
