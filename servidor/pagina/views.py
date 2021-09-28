from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'login.html')

def inicio(request):
    return render(request, 'index.html')