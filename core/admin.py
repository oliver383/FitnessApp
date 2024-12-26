from django.contrib import admin

from core.models import UserProfile, Exercise, UserRecommendation

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Exercise)
admin.site.register(UserRecommendation)