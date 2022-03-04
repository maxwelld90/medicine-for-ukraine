from django.urls import path
from api_app.countries import views as country_views

app_name = 'api_app'

urlpatterns = [
    path('countries/', country_views.CountryListing.as_view()),
]