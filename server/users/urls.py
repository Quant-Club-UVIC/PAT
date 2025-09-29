from django.urls import path

from users.views.logout_view import LogoutView
from users.views.register_view import RegisterView
from users.views.login_view import LoginView, NewAccessTokenObtainView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', NewAccessTokenObtainView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]