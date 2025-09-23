from django.urls import path

from .views import (RegisterView, AccessAndRefreshTokenView, NewAccessTokenObtainView, LogoutView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', AccessAndRefreshTokenView.as_view(), name='login'),
    path('token/refresh/', NewAccessTokenObtainView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]