from django.urls import path 
from .views import (
    LoginView, AccessTokenView,
    LogoutView, SignedTokenView,
)

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('token/access', AccessTokenView.as_view(), name='access-token'),
    path('token/signed-token', SignedTokenView.as_view(), name='signed-token'),
]