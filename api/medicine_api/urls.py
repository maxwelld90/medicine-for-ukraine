from django.urls import path
from django.conf import settings
# from medicine_api.countries import views as country_views
# from medicine_api.items import views as item_views
# from medicine_api.save import views as save_views
# from medicine_api.status import views as status_views

from medicine_api.handlers.countries import views as country_views
from medicine_api.handlers.languages import views as language_views
from medicine_api.handlers.recipients import views as recipient_views
from medicine_api.handlers.items import views as item_views
from medicine_api.handlers.save import views as save_views

app_name = 'medicine_api'

urlpatterns = [
    path('countries/', country_views.CountryListing.as_view()),
    path('languages/', language_views.LanguageListing.as_view()),
    path('recipients/', recipient_views.RecipientListing.as_view()),
    path('recipients/address/<uuid:recipient_id>/', recipient_views.WarehouseAddress.as_view()),
    path('items/<uuid:recipient_id>/', item_views.ItemsForRecipient.as_view()),
    path('links/<uuid:recipient_id>/<int:row_number>/', item_views.LinksForRecipientItem.as_view()),
    path('save/', save_views.SaveRequest.as_view()),
]

# When running the development server (and with DEBUG=True), serve media files (at /uploads/).
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)