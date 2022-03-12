from django.urls import path
from api_app.countries import views as country_views
from api_app.items import views as item_views
from api_app.save import views as save_views
from api_app.status import views as status_views

app_name = 'api_app'

urlpatterns = [
    path('status/', status_views.ServerStatus.as_view()),
    path('languages/', country_views.LanguageCodeListing.as_view()),
    path('countries/', country_views.CountryListing.as_view()),
    path('countries/address/<str:country_code>', country_views.CountryAddress.as_view()),
    path('items/<str:df_str>/<str:country_code>', item_views.ItemsListForCountry.as_view()),
    path('links/<str:df_str>/<str:country_code>/<int:item_index>', item_views.LinksForItem.as_view()),
    path('save/', save_views.SaveRequest.as_view())
]