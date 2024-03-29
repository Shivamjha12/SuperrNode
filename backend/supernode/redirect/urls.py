from django.urls import path, include
from .views import *
from Link import views 
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('<str:username>/<str:UniqueLinkKeyword>', LinkRedirectView.as_view())
]