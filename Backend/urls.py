from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # App URLs
    path('api/users/', include('users.urls')),
    path('api/vehicles/', include('vehicles.urls')),
    path('api/drivers/', include('drivers.urls')),
    path('api/routes/', include('routes.urls')),
    path('api/trips/', include('trips.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/maintenance/', include('maintanence.urls')),
    path('api/fuel/', include('fuel.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/dispatcher/',include('dispatcher.urls')),
    path('api/accountant/',include('accountant.urls')),
    path('api/billing/',include('billing.urls')),
    path('api/customer/',include('customers.urls'))
]
