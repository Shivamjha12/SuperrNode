from django.urls import path, include
from .views import *
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('get/<str:username>', GetUserProfileView.as_view()),
    path('operations', CreateEditDeleteProfileView.as_view()),
    
]