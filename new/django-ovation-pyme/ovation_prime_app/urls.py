from django.urls import path, include

from . import views
urlpatterns = [
    path('api/v1/conductance_interpolated/', views.get_ovation_prime_conductance_interpolated),
    path('api/v1/conductance/', views.get_ovation_prime_conductance),
    path('api/v1/weighted_flux/', views.get_weighted_flux),
    path('api/v1/weighted_flux_interpolated/', views.get_weighted_flux_interpolated),
    path('api/v1/seasonal_flux/', views.get_seasonal_flux),
]

