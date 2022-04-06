from django.urls import path, include
from medicine_api.admin import admin_site
from django.http import HttpResponse, HttpResponseRedirect

urlpatterns = [
    path('maintenance/', admin_site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('medicine_api.urls')),
]

def handler404(request, exception):
    """
    A simple 404 handler to redirect the user to the main homepage.
    """
    return HttpResponseRedirect('https://medicineforukraine.org')