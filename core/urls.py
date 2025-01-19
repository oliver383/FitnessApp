from django.urls import path, include
from django.views.generic import TemplateView

from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile', views.profile, name='profile'),
    path('help', views.help_page, name='help'),
    path('update_recommendations', views.update_recommendations_view, name='update_recommendations'),
]