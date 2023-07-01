from django.urls import path, include


urlpatterns = [
    path('accounts/', include('api.v1.accounts.urls')),
    path('ads/', include('api.v1.ads.urls')),
    path('main/', include('api.v1.main.urls')),
    path('companies/', include('api.v1.companies.urls')),
    path('orders/', include('api.v1.orders.urls')),
]
