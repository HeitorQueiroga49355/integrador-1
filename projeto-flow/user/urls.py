from django.urls import path
from . import views

urlpatterns = [
  path('', views.index_view, name='index'),
  path('login/', views.LoginView.as_view(), name='login'),
  path('logout/', views.LogoutView.as_view(), name='logout'),
  path('register/', views.RegisterView.as_view(), name='register'),

  path('dashboard/', views.dashboard_router, name='dashboard'),
]
