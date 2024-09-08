from django.urls import path
from users import views


urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("register/", views.UserRegistrationAPIView.as_view(), name="register"),
]