from pyexpat import model
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import Profile

# Create your views here.

def login(request):
  return render(request, './login/index.html')

def register(request):
    return render(request, './register/index.html')

class ProfileListView(ListView):
  model = Profile
  queryset = Profile.objects.all()
  template_name = 'user/user_list.html'