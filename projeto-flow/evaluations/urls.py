from django.urls import path
from . import views

app_name = 'evaluations'

urlpatterns = [
    path('evaluation/<int:submission_id>/', views.evaluation_create, name='evaluation_create'),
]