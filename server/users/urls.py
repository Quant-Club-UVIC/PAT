from django.urls import path

from server.users.views import RegisterView
from server.users.views.logout_view import LogoutView
from server.users.views.token_view import AccessAndRefreshTokenView, NewAccessTokenObtainView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', AccessAndRefreshTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', NewAccessTokenObtainView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]