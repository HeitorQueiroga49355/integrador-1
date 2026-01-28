from django.urls import path
from . import views

urlpatterns = [
  path('', views.LoginView.as_view(), name='login'),
  path('login/', views.LoginView.as_view(), name='login'),
  path('logout/', views.LogoutView.as_view(), name='logout'),
  path('register/', views.RegisterView.as_view(), name='register'),
]
