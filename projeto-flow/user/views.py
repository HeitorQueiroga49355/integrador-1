from django.shortcuts import render

# Create your views here.

def login(request):
  return render(request, './login/index.html')

def register(request):
    return render(request, './register/index.html')