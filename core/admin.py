from django.contrib import admin

from core.models import UserProfile, Exercise, UserRecommendation, Equipment, Category, BodySection, Muscle, Pushpull

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Exercise)
admin.site.register(UserRecommendation)
admin.site.register(Equipment)
admin.site.register(Category)
admin.site.register(BodySection)
admin.site.register(Muscle)
admin.site.register(Pushpull)