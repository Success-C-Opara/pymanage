from django.shortcuts import render

# Create your views here.

def home (request):

    return render (request , 'loginapp/home.html')
    


def service(request):
    return render (request, 'loginapp/services.html')