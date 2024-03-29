from django.urls import path, include
from .views import *
from Link import views 
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('get/<str:id>', LinkGetView.as_view()), # for to get a specific link object by passing uuid
    path('get/user/<str:username>', UserLinkView.as_view()), # get links of a user by passing username
    path('operations', LinkCreateEditDeleteView.as_view()),# for performing operations like create/edit/delete on link object with required arguments
    path('linklist/<str:username>', UserLinklistListView.as_view()), # get all LinkList of user by pasing username
    path('linklist/view/<str:id>', LinklistView.as_view()), # for to get a specific LinkList object by passing link_group_id
    path('linklist', LinklistCreateEditDeleteView.as_view()),
    path('linklist/add/link', LinklistAddLinkView.as_view()),
    path('linklist/remove/link', LinklistRemoveLinkView.as_view())
]