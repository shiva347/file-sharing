from django.urls import path
from . import views

urlpatterns = [
  path('register/', views.UserRegisterAPIView.as_view()),
  path("get_profile/<int:pk>/", views.GetUserProfileAPIView.as_view()),
  path("login/", views.UserLogIn.as_view()),
]