import json
from django.urls import path, include
from medicine_api.admin import admin_site
from api.error_handlers import handler404, handler500

urlpatterns = [
    path('maintenance/', admin_site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('medicine_api.urls')),
]

handler404 = handler404
handler500 = handler500