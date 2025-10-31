from django.urls import path
from . import views


urlpatterns = [
    path('/properties/', views.property_list, 'property_list'),
]