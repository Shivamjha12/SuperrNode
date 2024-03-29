from django.urls import path, include
from .views import *
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('linkclick/<str:id>', LinkClick.as_view()), 
    path('linklistclick/<str:id>', LinkGroupClick.as_view()),
]