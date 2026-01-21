from django.urls import path
from . import views

urlpatterns = [
  path('login/', views.login, name='login'),
  path('register/', views.register, name='register'),

  path('list/profile/', views.ProfileListView.as_view(), name='profile-list'),
] 