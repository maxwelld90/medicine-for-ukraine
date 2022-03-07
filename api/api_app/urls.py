from django.urls import path
from api_app.countries import views as country_views
from api_app.items import views as item_views

app_name = 'api_app'

urlpatterns = [
    path('languages/', country_views.LanguageCodeListing.as_view()),
    path('countries/', country_views.CountryListing.as_view()),
    path('countries/address/<str:country_code>', country_views.CountryAddress.as_view()),
    path('items/<str:df_str>/<str:country_code>', item_views.ItemsListForCountry.as_view()),
    path('links/<str:df_str>/<str:country_code>/<int:item_index>', item_views.LinksForItem.as_view()),
]