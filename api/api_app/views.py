from django.http import HttpResponse

def landing_view(request):
    return HttpResponse('<h1>API Server</h1>')