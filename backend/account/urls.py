from django.urls import path 
from .views import (
    LoginView, AccessTokenView,
    LogoutView
)

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('token/access', AccessTokenView.as_view(), name='access-token'),
]