from django.shortcuts import render

def hello_world(request):
    return render(request, 'marketplace/hello_world.html', {})
