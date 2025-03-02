from django.urls import path
from .views import (
    fetch_pagespeed_results,
    get_past_searches,
    google_maps_search,
    google_custom_search,
    google_my_business_search,
    website_status
)

urlpatterns = [
    path('pagespeed/', fetch_pagespeed_results, name='pagespeed_results'),
    path('past-searches/', get_past_searches, name='past_searches'),
    path('maps-search/', google_maps_search, name='maps_search'),
    path('search/', google_custom_search, name='custom_search'),
    path('business-search/', google_my_business_search, name='business_search'),
    path('website-status/', website_status, name='website_status'),
]
