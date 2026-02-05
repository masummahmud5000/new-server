from django.urls import path
from .views import register, login, profile
from rest_framework_simplejwt.views import TokenRefreshView
# //////////////////////////
urlpatterns = [
    path('register/', register.as_view()),
    path('login/', login.as_view()),
    path('profile/', profile.as_view()),
    path('refresh/', TokenRefreshView.as_view())
]

