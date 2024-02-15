from django.urls import path, include
from .views import *
from accounts import views 
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('register', register.as_view()),
    path('login', login.as_view()),
    path('user/<str:JWTUser>', userView.as_view()),
    path('logout', logout.as_view()),
    path('resetpassword/<slug:uidb64>/<slug:token>/', views.resetPassword,name="resetpassword"),
    path('forgotpassword', forgotPassword.as_view(),name="forgetpassword"),
    path('reset/done/', views.password_reset_done_page, name='password_reset_done'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    
]